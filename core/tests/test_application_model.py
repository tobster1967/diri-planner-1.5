"""
Tests for Application model.
"""
from django.test import TestCase
from core.models import Application


class ApplicationModelTest(TestCase):
    """Test suite for Application model."""
    
    fixtures = ['test_data.json']
    
    def setUp(self):
        """Set up test data."""
        self.parent_app = Application.objects.get(slug='app-a')
        self.child_app = Application.objects.get(slug='app-b')
    
    def test_application_creation(self):
        """Test creating an application."""
        app = Application.objects.create(
            name='Test App',
            description='Test description',
            slug='test-app'
        )
        self.assertEqual(app.name, 'Test App')
        self.assertEqual(app.slug, 'test-app')
        self.assertIsNone(app.parent)
    
    def test_application_str_representation(self):
        """Test string representation of application."""
        self.assertEqual(str(self.parent_app), 'App A')
    
    def test_application_hierarchy(self):
        """Test hierarchical relationships."""
        self.assertIsNone(self.parent_app.parent)
        self.assertEqual(self.child_app.parent, self.parent_app)
        self.assertEqual(self.parent_app._depth, 0)
        self.assertEqual(self.child_app._depth, 1)
    
    def test_application_level_property(self):
        """Test level property returns correct depth."""
        self.assertEqual(self.parent_app.level, 0)
        self.assertEqual(self.child_app.level, 1)
    
    def test_application_slug_unique(self):
        """Test slug uniqueness."""
        with self.assertRaises(Exception):
            Application.objects.create(
                name='Duplicate',
                slug='app-a'  # Already exists
            )
    
    def test_application_with_attributes(self):
        """Test application with attributes."""
        app = Application.objects.get(slug='app-b')
        self.assertEqual(app.attributes.count(), 2)
        attribute_names = set(attr.name for attr in app.attributes.all())
        self.assertEqual(attribute_names, {'Tag 1', 'Tag 2'})
    
    def test_application_with_organisations(self):
        """Test application with organisations."""
        app = Application.objects.get(slug='app-b')
        self.assertEqual(app.organisations.count(), 2)
        org_names = set(org.name for org in app.organisations.all())
        self.assertEqual(org_names, {'Subsidiary 1', 'Subsidiary 2'})
    
    def test_application_tree_path(self):
        """Test tree path generation."""
        self.assertEqual(self.parent_app._path, '000')
        self.assertTrue(self.child_app._path.startswith('000.'))