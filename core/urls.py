from django.urls import path
from django.views.generic import RedirectView
from core.views.application_views import ApplicationCRUDView

urlpatterns = [
    path('', RedirectView.as_view(url='/application/', permanent=False), name='home'),
] + ApplicationCRUDView.get_urls()