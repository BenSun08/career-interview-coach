from django.core.exceptions import DisallowedHost
from django.test import RequestFactory, SimpleTestCase


class LoopbackHostSettingsTests(SimpleTestCase):
    def test_ipv4_and_ipv6_loopback_hosts_are_allowed(self) -> None:
        factory = RequestFactory()

        for host in ("127.0.0.1:8000", "[::1]:8000"):
            with self.subTest(host=host):
                request = factory.get("/", HTTP_HOST=host)
                self.assertEqual(request.get_host(), host)

    def test_non_loopback_host_is_rejected(self) -> None:
        request = RequestFactory().get("/", HTTP_HOST="example.com")

        with self.assertRaises(DisallowedHost):
            request.get_host()
