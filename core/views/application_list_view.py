from django.views.generic import ListView
from core.models import Application


class ApplicationListView(ListView):
    """
    Plain vanilla list view for Application model
    """
    model = Application
    template_name = 'core/application_list.html'
    context_object_name = 'applications'
    ordering = ['name']