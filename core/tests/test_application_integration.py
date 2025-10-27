"""
Integration tests for Application CRUD workflow.
"""
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Application, Attribute, Organisation


class ApplicationIntegrationTest(TestCase):
    """Integration tests for Application CRUD workflow."""
    
    fixtures = ['test_data.json']
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow for an application."""
        # 1. LIST: View all applications
        response = self.client.get(reverse('application-list'))
        self.assertEqual(response.status_code, 200)
        initial_count = Application.objects.count()
        
        # 2. CREATE: Create a new application
        create_data = {
            'name': 'Integration Test App',
            'description': 'Created during integration test',
            'slug': 'integration-test-app',
        }
        response = self.client.post(reverse('application-create'), create_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.count(), initial_count + 1)
        
        # Get the created application
        app = Application.objects.get(slug='integration-test-app')
        
        # 3. DETAIL: View the created application
        url = reverse('application-detail', kwargs={'pk': app.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test App')
        
        # 4. UPDATE: Update the application
        url = reverse('application-update', kwargs={'pk': app.pk})
        update_data = {
            'name': 'Updated Integration Test App',
            'description': 'Updated during integration test',
            'slug': 'integration-test-app',
        }
        response = self.client.post(url, update_data)
        self.assertEqual(response.status_code, 302)
        app.refresh_from_db()
        self.assertEqual(app.name, 'Updated Integration Test App')
        
        # 5. DELETE: Delete the application
        url = reverse('application-delete', kwargs={'pk': app.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.count(), initial_count)
        self.assertFalse(Application.objects.filter(pk=app.pk).exists())
    
    def test_create_with_relationships(self):
        """Test creating an application with attributes and organisations."""
        attr = Attribute.objects.get(slug='tag-1')
        org = Organisation.objects.get(slug='subsidiary-1')
        
        data = {
            'name': 'App with Relations',
            'description': 'Has attributes and organisations',
            'slug': 'app-with-relations',
            'attributes': [str(attr.pk)],
            'organisations': [str(org.pk)],
        }
        response = self.client.post(reverse('application-create'), data)
        self.assertEqual(response.status_code, 302)
        
        # Verify relationships
        app = Application.objects.get(slug='app-with-relations')
        self.assertEqual(app.attributes.count(), 1)
        self.assertEqual(app.organisations.count(), 1)
    
    def test_hierarchy_in_list_view(self):
        """Test that parent-child relationships are visible in list."""
        response = self.client.get(reverse('application-list'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        
        # Parent should appear
        self.assertIn('App A', content)
        # Children should appear
        self.assertIn('App B', content)
        self.assertIn('App C', content)