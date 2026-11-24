from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.audits.models import Audit
from apps.leads.models import Lead, LeadTask
from apps.organizations.models import Organization
from apps.outreach.models import Outreach
from apps.proposals.models import Proposal


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="showcase@example.invalid",
    SECURE_SSL_REDIRECT=False,
    CSRF_COOKIE_SECURE=False,
    SESSION_COOKIE_SECURE=False,
    STATIC_ROOT=None,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class ShowcaseWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model().objects
        org = Organization.objects.create(name="Example Team", slug="example-team")
        other_org = Organization.objects.create(name="Other Team", slug="other-team")
        cls.owner = users.create_user(username="example", organization=org)
        cls.other = users.create_user(username="other", organization=other_org)
        cls.lead = Lead.objects.create(
            organization=org, company_name="Example Studio",
            email="lead@example.invalid", website="https://example.invalid",
        )

    def token_for(self, user):
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(user)
        self.assertEqual(browser.get(reverse("discovery:index")).status_code, 200)
        return browser, browser.cookies["csrftoken"].value

    def assert_action_permissions(self, route, args, endpoint_data=None):
        url = reverse(route, args=args)
        owner, token = self.token_for(self.owner)
        peer, peer_token = self.token_for(self.other)
        self.assertEqual(Client().post(url).status_code, 302)
        self.assertEqual(owner.get(url).status_code, 405)
        self.assertEqual(owner.post(url).status_code, 403)
        self.assertEqual(peer.post(url, {"csrfmiddlewaretoken": peer_token}).status_code, 404)
        response = owner.post(url, {"csrfmiddlewaretoken": token, **(endpoint_data or {})})
        self.assertEqual(response.status_code, 302)
        return owner

    def test_authenticated_post_workflow_and_tenant_isolation(self):
        html = "<html><head><title>Sample</title></head><body><h1>Sample</h1></body></html>"
        response = SimpleNamespace(
            url=self.lead.website, text=html, headers={}, content=html.encode(), status_code=200
        )
        with patch("apps.audits.services.utils.fetch_public_url", return_value=response), patch(
            "apps.audits.services.ssl.fetch_public_url", return_value=response
        ):
            self.assert_action_permissions("audits:run", [self.lead.pk])
        audit = Audit.objects.get(lead=self.lead)
        self.assertEqual(audit.page_title, "Sample")
        owner = self.assert_action_permissions("proposals:generate_proposal", [audit.pk])
        proposal = Proposal.objects.get(lead=self.lead)
        pdf = owner.get(reverse("proposals:proposal_pdf", args=[proposal.pk]))
        self.assertEqual(pdf.status_code, 200)
        self.assertTrue(pdf.content.startswith(b"%PDF"))

        self.assert_action_permissions("outreach:generate_outreach", [proposal.pk])
        outreach = Outreach.objects.get(proposal=proposal)
        self.assert_action_permissions("outreach:outreach_status", [outreach.pk, "sent"])
        self.assert_action_permissions("outreach:send_email", [outreach.pk])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.lead.email])

    def test_discovery_and_import_use_post_and_synthetic_results(self):
        owner, token = self.token_for(self.owner)
        discovery = reverse("discovery:index")
        with patch("apps.discovery.views.DiscoveryService.search", return_value=[]) as search:
            self.assertEqual(owner.get(discovery, {"query": "Dental"}).status_code, 200)
            search.assert_not_called()
            self.assertEqual(owner.post(discovery, {"query": "Dental"}).status_code, 403)
            result = owner.post(discovery, {"query": "Dental", "csrfmiddlewaretoken": token})
            self.assertContains(result, "Bright Dental Clinic")
            search.assert_called_once()
        imported = owner.post(reverse("discovery:import_all"), {"csrfmiddlewaretoken": token})
        self.assertEqual(imported.status_code, 302)
        self.assertTrue(Lead.objects.filter(
            organization=self.owner.organization, company_name="Bright Dental Clinic"
        ).exists())

    @override_settings(SERPAPI_API_KEY="")
    def test_discovery_skips_external_request_without_key(self):
        owner, token = self.token_for(self.owner)
        with patch("apps.discovery.services.google_maps_service.GoogleSearch") as external:
            result = owner.post(reverse("discovery:index"), {
                "query": "Dental", "csrfmiddlewaretoken": token,
            })
            self.assertContains(result, "fictional results")
            external.assert_not_called()

    def test_logout_requires_post_and_csrf(self):
        browser, token = self.token_for(self.owner)
        url = reverse("accounts:logout")
        self.assertEqual(browser.get(url).status_code, 405)
        self.assertEqual(browser.post(url).status_code, 403)
        self.assertEqual(browser.post(url, {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertEqual(browser.get(reverse("dashboard:index")).status_code, 302)

    def test_demo_seed_is_scoped_and_repeatable(self):
        for _ in range(2):
            call_command("seed_demo", username=self.owner.username, stdout=StringIO())
        leads = Lead.objects.filter(company_name="Sample Orchard Studio")
        self.assertEqual(leads.count(), 1)
        self.assertEqual(leads.get().organization, self.owner.organization)
        self.assertEqual(LeadTask.objects.filter(lead=leads.get()).count(), 1)
