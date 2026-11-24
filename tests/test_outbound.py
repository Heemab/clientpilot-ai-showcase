import socket
import time
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import urlsplit

from src import outbound


def address(ip):
    return (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (ip, 443))


def reply(status, headers=(), chunks=()):
    connection = MagicMock()
    response = connection.getresponse.return_value.__enter__.return_value
    response.status = status
    response.reason = "Test response"
    response.getheaders.return_value = headers
    response.getheader.side_effect = lambda name, default=None: dict(headers).get(name, default)
    response.read1.side_effect = chunks
    return connection


class OutboundTests(TestCase):
    def test_rejects_non_public_and_invalid_destinations_without_connecting(self):
        for url in (
            "http://127.0.0.1/",
            "http://10.0.0.1/",
            "http://169.254.1.1/",
            "http://168.63.129.16/",
            "http://100.64.0.1/",
            "http://224.0.0.1/",
            "http://[::1]/",
            "http://[fc00::1]/",
            "http://[fe80::1]/",
            "http://[::ffff:127.0.0.1]/",
            "http://intranet.local/",
            "file:///sample",
            "https://user@example.org/",
            "https://example.org:8443/",
        ):
            with self.subTest(url=url), patch.object(outbound, "_connection") as connect:
                with self.assertRaises(outbound.OutboundFetchError):
                    outbound.fetch_public_url(url)
                connect.assert_not_called()

    def test_mixed_dns_answers_are_rejected(self):
        with patch.object(
            outbound.socket, "getaddrinfo",
            return_value=[address("93.184.216.34"), address("10.0.0.1")],
        ), patch.object(outbound, "_connection") as connect:
            with self.assertRaises(outbound.OutboundFetchError):
                outbound.fetch_public_url("https://public.example.org/")
            connect.assert_not_called()

    def test_socket_uses_only_the_vetted_address(self):
        target = urlsplit("http://public.example.org/")
        record = address("93.184.216.34")
        deadline = time.monotonic() + 5
        with patch.object(outbound.socket, "socket") as socket_factory, patch.object(
            outbound.socket, "getaddrinfo"
        ) as resolver:
            connection = outbound._connection(target, target.hostname, 80, [record], deadline)
            connection.connect()
            socket_factory.return_value.connect.assert_called_once_with(record[4])
            resolver.assert_not_called()
            connection.close()

    def test_redirect_is_validated_before_the_next_socket(self):
        for location in ("https://127.0.0.1/", "http://public.example.org/"):
            with self.subTest(location=location), patch.object(
                outbound.socket, "getaddrinfo", return_value=[address("93.184.216.34")]
            ), patch.object(outbound, "_connection", return_value=reply(
                302, [("Location", location)]
            )) as connect:
                with self.assertRaises(outbound.OutboundFetchError):
                    outbound.fetch_public_url("https://public.example.org/")
                connect.assert_called_once()

    def test_public_redirect_retains_tls_and_response(self):
        with patch.object(
            outbound.socket, "getaddrinfo", return_value=[address("93.184.216.34")]
        ) as dns, patch.object(outbound, "_connection", side_effect=[
            reply(301, [("Location", "https://other.example.org/final")]),
            reply(200, [("Content-Type", "text/html; charset=utf-8")], [b"sample", b""]),
        ]):
            response = outbound.fetch_public_url("http://public.example.org/")
        self.assertEqual(response.url, "https://other.example.org/final")
        self.assertEqual(response.text, "sample")
        self.assertEqual([call.args[0] for call in dns.call_args_list], [
            "public.example.org.", "other.example.org."
        ])
        self.assertTrue(outbound.TLS_CONTEXT.check_hostname)

    def test_redirect_limit_and_body_limit(self):
        with patch.object(
            outbound.socket, "getaddrinfo", return_value=[address("93.184.216.34")]
        ), patch.object(
            outbound, "_connection", return_value=reply(302, [("Location", "/next")])
        ) as connect:
            with self.assertRaisesRegex(outbound.OutboundFetchError, "redirect limit"):
                outbound.fetch_public_url("https://public.example.org/")
            self.assertEqual(connect.call_count, outbound.MAX_REDIRECTS + 1)

        with patch.object(
            outbound.socket, "getaddrinfo", return_value=[address("93.184.216.34")]
        ), patch.object(outbound, "_connection", return_value=reply(
            200, chunks=[b"x" * (outbound.MAX_BODY + 1)]
        )):
            with self.assertRaisesRegex(outbound.OutboundFetchError, "too large"):
                outbound.fetch_public_url("https://public.example.org/")
