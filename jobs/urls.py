from django.urls import path,re_path
from jobs import views
urlpatterns = [
    path('joblist/', views.joblist, name='joblist'),
    re_path(r'^job/(?P<job_id>\d+)/$', views.detail, name='jobdetail')

]