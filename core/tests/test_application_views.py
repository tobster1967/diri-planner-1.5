"""
Tests for Application views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Application
import uuid


class ApplicationViewTest(TestCase):
    """Test suite for Application views."""
    
    fixtures = ['test_data.json']
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.parent_app = Application.objects.get(slug='app-a')
        self.child_app = Application.objects.get(slug='app-b')
    
    def test_application_list_view(self):
        """Test application list view."""
        response = self.client.get(reverse('application-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'App A')
        self.assertContains(response, 'App B')
        self.assertContains(response, 'App C')
    
    def test_application_list_view_ordering(self):
        """Test applications are ordered by tree path."""
        response = self.client.get(reverse('application-list'))
        self.assertEqual(response.status_code, 200)
        # Get the applications from context
        apps = list(response.context['object_list'])
        # Parent should come before children
        self.assertEqual(apps[0].slug, 'app-a')
    
    def test_application_detail_view(self):
        """Test application detail view."""
        url = reverse('application-detail', kwargs={'pk': self.parent_app.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'App A')
        self.assertContains(response, 'Primary application')
        self.assertContains(response, 'app-a')  # slug
    
    def test_application_detail_view_shows_hierarchy(self):
        """Test detail view shows hierarchy information."""
        url = reverse('application-detail', kwargs={'pk': self.child_app.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Should show level
        self.assertContains(response, 'Level')
        # Should show parent
        self.assertContains(response, 'App A')
    
    def test_application_create_view_get(self):
        """Test GET request to create view."""
        response = self.client.get(reverse('application-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Application')
    
    def test_application_create_view_post(self):
        """Test POST request to create view."""
        data = {
            'name': 'New App',
            'description': 'New application description',
            'slug': 'new-app',
        }
        response = self.client.post(reverse('application-create'), data)
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        # Verify application was created
        self.assertTrue(Application.objects.filter(slug='new-app').exists())
    
    def test_application_update_view_get(self):
        """Test GET request to update view."""
        url = reverse('application-update', kwargs={'pk': self.parent_app.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Application')
        self.assertContains(response, 'App A')
    
    def test_application_update_view_post(self):
        """Test POST request to update view."""
        url = reverse('application-update', kwargs={'pk': self.parent_app.pk})
        data = {
            'name': 'Updated App A',
            'description': 'Updated description',
            'slug': 'app-a',
        }
        response = self.client.post(url, data)
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        # Verify application was updated
        self.parent_app.refresh_from_db()
        self.assertEqual(self.parent_app.name, 'Updated App A')
    
    def test_application_delete_view_get(self):
        """Test GET request to delete view (confirmation page)."""
        url = reverse('application-delete', kwargs={'pk': self.parent_app.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete Application')
        self.assertContains(response, 'App A')
    
    def test_application_delete_view_post(self):
        """Test POST request to delete view."""
        # Create a test app that we can safely delete
        test_app = Application.objects.create(
            name='To Delete',
            slug='to-delete',
            description='Will be deleted'
        )
        app_id = test_app.pk
        
        url = reverse('application-delete', kwargs={'pk': app_id})
        response = self.client.post(url)
        # Should redirect after successful deletion
        self.assertEqual(response.status_code, 302)
        # Verify application was deleted
        self.assertFalse(Application.objects.filter(pk=app_id).exists())
    
    def test_application_404_for_invalid_uuid(self):
        """Test 404 response for non-existent application."""
        fake_uuid = uuid.uuid4()
        url = reverse('application-detail', kwargs={'pk': fake_uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)