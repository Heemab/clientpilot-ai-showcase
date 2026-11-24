"""Bounded HTTP fetching for prospect URLs in the web app and engine."""

from contextlib import closing
import http.client
import ipaddress
import re
import socket
import ssl
import time
from urllib.parse import quote, urljoin, urlsplit

import requests


MAX_BODY = 2 * 1024 * 1024
MAX_REDIRECTS = 4
REDIRECT_CODES = {301, 302, 303, 307, 308}
PORTS = {"http": 80, "https": 443}
PLATFORM_ADDRESSES = {ipaddress.ip_address("168.63.129.16")}
SPECIAL_IPV6 = tuple(
    ipaddress.ip_network(network)
    for network in ("64:ff9b::/96", "64:ff9b:1::/48", "2002::/16", "2001::/32")
)
TLS_CONTEXT = ssl.create_default_context()


class OutboundFetchError(requests.exceptions.RequestException):
    """A prospect URL was rejected or could not be fetched."""


def _parse(url):
    if not url or len(url) > 4096 or re.search(r"[\x00-\x20\x7f\\]", url):
        raise OutboundFetchError("Invalid website URL.")
    try:
        target = urlsplit(url)
        host = target.hostname
        port = PORTS.get(target.scheme)
        if (
            not host
            or not port
            or target.port not in (None, port)
            or target.username is not None
            or "@" in target.netloc
            or "%" in host
        ):
            raise OutboundFetchError("Only public HTTP and HTTPS URLs on standard ports are supported.")
        host = host.rstrip(".").encode("idna").decode("ascii")
    except (ValueError, UnicodeError):
        raise OutboundFetchError("Invalid website hostname.") from None
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if "." not in host or not all(
            re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label, re.I)
            for label in host.split(".")
        ) or host.endswith((".localhost", ".local", ".internal", ".home.arpa")):
            raise OutboundFetchError("A public website hostname is required.") from None
    return target, host, port


def _public_address(address):
    ip = ipaddress.ip_address(address)
    if not ip.is_global or ip.is_multicast or ip.is_reserved or ip in PLATFORM_ADDRESSES:
        return False
    return ip.version != 6 or (
        not ip.ipv4_mapped and not any(ip in network for network in SPECIAL_IPV6)
    )


def _resolve(host, port):
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        # An absolute DNS name avoids applying a machine's local search domains.
        records = socket.getaddrinfo(host + ".", port, type=socket.SOCK_STREAM)
    else:
        if literal.version == 4:
            records = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (host, port))]
        else:
            records = [(socket.AF_INET6, socket.SOCK_STREAM, 0, "", (host, port, 0, 0))]
    if not records or any(not _public_address(record[4][0]) for record in records):
        raise OutboundFetchError("Website resolves to a destination outside the public Internet.")
    return records


def _remaining(deadline):
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise OutboundFetchError("Website request timed out.")
    return seconds


def _connection(target, host, port, records, deadline):
    if target.scheme == "https":
        connection = http.client.HTTPSConnection(
            host, port, timeout=_remaining(deadline), context=TLS_CONTEXT
        )
    else:
        connection = http.client.HTTPConnection(host, port, timeout=_remaining(deadline))

    def connect(_destination, _timeout, _source_address=None):
        # Connect to the inspected sockaddr. HTTP Host and TLS verification keep
        # using the original hostname. No proxy or second DNS lookup is involved.
        for family, kind, proto, _, address in records:
            sock = socket.socket(family, kind, proto)
            try:
                sock.settimeout(_remaining(deadline))
                sock.connect(address)
                return sock
            except TimeoutError:
                sock.close()
                _remaining(deadline)
            except OutboundFetchError:
                sock.close()
                raise
            except OSError:
                sock.close()
        raise OutboundFetchError("Could not connect to the public website.")

    connection._create_connection = connect
    return connection


def _read_body(response, sock, deadline):
    encoding = response.getheader("Content-Encoding", "identity").lower().strip()
    if encoding != "identity":
        raise OutboundFetchError("Website returned an unsupported content encoding.")
    length = response.getheader("Content-Length")
    if length and length.isdecimal() and int(length) > MAX_BODY:
        raise OutboundFetchError("Website response is too large.")
    body = bytearray()
    while len(body) <= MAX_BODY:
        sock.settimeout(_remaining(deadline))
        chunk = response.read1(min(65536, MAX_BODY + 1 - len(body)))
        if not chunk:
            return bytes(body)
        body.extend(chunk)
    raise OutboundFetchError("Website response is too large.")


def fetch_public_url(url, *, timeout=10, headers=None):
    """Fetch HTTP(S) with pinned public DNS, per-hop checks, and bounded reads."""
    deadline = time.monotonic() + timeout
    headers = {
        "User-Agent": (headers or {}).get("User-Agent", "ClientPilot-Website-Assessment"),
        "Accept-Encoding": "identity",
    }
    try:
        for hop in range(MAX_REDIRECTS + 1):
            target, host, port = _parse(url)
            path = quote(target.path or "/", safe="/%:@!$&'()*+,;=-._~")
            if target.query:
                path += "?" + quote(target.query, safe="/?%:@!$&'()*+,;=-._~")
            with closing(_connection(target, host, port, _resolve(host, port), deadline)) as connection:
                connection.request("GET", path, headers=headers)
                sock = connection.sock
                with connection.getresponse() as response:
                    location = response.getheader("Location")
                    if response.status in REDIRECT_CODES and location:
                        if hop == MAX_REDIRECTS:
                            raise OutboundFetchError("Website exceeded the redirect limit.")
                        if re.search(r"[\x00-\x20\x7f\\]", location):
                            raise OutboundFetchError("Invalid redirect location.")
                        url = urljoin(url, location)
                        redirect, _, _ = _parse(url)
                        if target.scheme == "https" and redirect.scheme != "https":
                            raise OutboundFetchError("HTTPS websites cannot redirect to HTTP.")
                        continue
                    result = requests.Response()
                    result.url = url
                    result.status_code = response.status
                    result.reason = response.reason
                    result.headers.update(response.getheaders())
                    result.encoding = requests.utils.get_encoding_from_headers(result.headers)
                    result._content = _read_body(response, sock, deadline)
                    return result
    except OutboundFetchError:
        raise
    except (OSError, http.client.HTTPException, ValueError):
        raise OutboundFetchError("Website request failed.") from None
