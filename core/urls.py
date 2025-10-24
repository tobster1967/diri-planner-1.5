from django.urls import path
from core.views.application_list_view import ApplicationListView

app_name = 'core'

urlpatterns = [
    path('application/', ApplicationListView.as_view(), name='application_list'),
]