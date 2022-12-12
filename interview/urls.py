from interview import views
from django.urls import path, include

urlpatterns = [
    path('', include('jobs.urls')),
]