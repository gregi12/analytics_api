"""
URL configuration for analytics_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from auth_and_tracking.views import signup, basic_info, top_pages, langauges, entry_pages, browsers, delete
from .tasks import test_token

from django.urls import path, re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path('signup/', signup , name='signup'),
    re_path('site_info/', test_token , name='site_info'),
    re_path('basic_info/', basic_info , name='basic_info'),
    re_path('top_pages/', top_pages , name='top_pages'),
    re_path('languages/', langauges , name='languages'),
    re_path('entry_pages/', entry_pages , name='entry_pages'),
    re_path('browsers/', browsers , name='browsers'),
    re_path('delete_account/', delete , name='delete_account'),
    #re_path('active_users/', ActiveUsersView.as_view() , name='active_users'),

]