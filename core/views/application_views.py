from neapolitan.views import CRUDView
from core.models import Application


class ApplicationCRUDView(CRUDView):
    """
    Neapolitan CRUD views for Application model.
    Provides list, detail, create, update, and delete views.
    """
    model = Application
    fields = ['name', 'description', 'parent', 'slug', 'attributes', 'organisations']
    filterset_fields = ['name', 'parent']
    
    # Customize the list view
    list_display = ['name', 'parent', 'slug', 'created_at']
    
    # Order by tree path to maintain hierarchical structure
    queryset = Application.objects.all().order_by('_path')
    
    # Support UUID primary keys
    path_converter = 'uuid'
    lookup_field = 'pk'