"""
Tests for Attribute model.
"""

from django.test import TestCase

from core.models import Attribute


class AttributeModelTest(TestCase):
    """Test suite for Attribute model."""

    fixtures = ["test_data.json"]

    def setUp(self):
        """Set up test data."""
        self.parent_attr = Attribute.objects.get(slug="category-a")
        self.child_attr = Attribute.objects.get(slug="tag-1")

    def test_attribute_creation(self):
        """Test creating an attribute."""
        attr = Attribute.objects.create(name="Test Attr", slug="test-attr", value="test", data_type="string")
        self.assertEqual(attr.name, "Test Attr")
        self.assertEqual(attr.data_type, "string")

    def test_attribute_str_representation(self):
        """Test string representation of attribute."""
        self.assertEqual(str(self.parent_attr), "Category A")

    def test_attribute_hierarchy(self):
        """Test hierarchical relationships."""
        self.assertIsNone(self.parent_attr.parent)
        self.assertEqual(self.child_attr.parent, self.parent_attr)

    def test_attribute_data_types(self):
        """Test different data types."""
        self.assertEqual(self.parent_attr.data_type, "boolean")
        self.assertEqual(self.parent_attr.value, "true")

    def test_attribute_is_active_default(self):
        """Test default value for is_active."""
        attr = Attribute.objects.create(name="Active Test", slug="active-test", value="test", data_type="string")
        self.assertTrue(attr.is_active)
