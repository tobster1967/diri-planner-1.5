from django.urls import path
from django.views.generic import RedirectView
from core.views.application_list_view import ApplicationListView

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='core:application_list', permanent=False), name='home'),
    path('application/', ApplicationListView.as_view(), name='application_list'),
]