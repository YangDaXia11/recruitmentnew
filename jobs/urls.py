from django.urls import path, re_path
from jobs import views
urlpatterns = [
    path('joblist/', views.joblist, name='joblist'),
    re_path(r'^job/(?P<job_id>\d+)/$', views.detail, name='jobdetail'),

    # 设置首页自动跳转到职位列表
    re_path(r'^$', views.joblist, name='name'),
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),

]