"""
Tests for Organisation model.
"""

from django.test import TestCase

from core.models import Organisation


class OrganisationModelTest(TestCase):
    """Test suite for Organisation model."""

    fixtures = ["test_data.json"]

    def setUp(self):
        """Set up test data."""
        self.parent_org = Organisation.objects.get(slug="company-a")
        self.child_org = Organisation.objects.get(slug="subsidiary-1")

    def test_organisation_creation(self):
        """Test creating an organisation."""
        org = Organisation.objects.create(name="Test Org", slug="test-org", code="TO", description="Test description")
        self.assertEqual(org.name, "Test Org")
        self.assertEqual(org.code, "TO")

    def test_organisation_str_representation(self):
        """Test string representation of organisation."""
        self.assertEqual(str(self.parent_org), "Company A")

    def test_organisation_hierarchy(self):
        """Test hierarchical relationships."""
        self.assertIsNone(self.parent_org.parent)
        self.assertEqual(self.child_org.parent, self.parent_org)

    def test_organisation_contact_fields(self):
        """Test contact information fields."""
        self.assertEqual(self.parent_org.email, "contact@company-a.example")
        self.assertEqual(self.parent_org.phone, "+1-555-0001")
        self.assertEqual(self.parent_org.website, "https://company-a.example")

    def test_organisation_is_active_default(self):
        """Test default value for is_active."""
        org = Organisation.objects.create(name="Active Test", slug="active-test", code="AT")
        self.assertTrue(org.is_active)
