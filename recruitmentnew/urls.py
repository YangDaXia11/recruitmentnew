"""recruitmentnew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.utils.translation import gettext as _

urlpatterns = [
    path('', include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('interview.urls')),
    path('', include('interview.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('', include('jobs.urls')),
        path('__debug__/', include(debug_toolbar.urls)),
        path('grappelli/', include('grappelli.urls')),
        path('admin/', admin.site.urls),
        path('', include('interview.urls')),
        path('accounts/', include('registration.backends.simple.urls')),  # django的registra包的固定写法
    ]

# 调整 adminsite 基本信息
# admin.site.site_title= 站点标题
# admin.site.site_header= 站点头
# admin.site.index_title= 首页标题
admin.site.site_header = _('招聘网站系统')  # 设置后台的标题
# admin.site.index_title = _('应聘者信息')
# admin.site.site_title = _('应聘者')
