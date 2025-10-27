"""
Test home URL redirect.
"""

from django.test import Client, TestCase


class HomeRedirectTest(TestCase):
    """Test home URL redirect."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_home_redirects_to_application_list(self):
        """Test that root URL redirects to application list."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith("/application/"))
