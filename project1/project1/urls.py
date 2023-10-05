"""project1 URL Configuration

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
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path ('home', views.home,name='home page'),
    path ('signin', views.signin,name='signin page'),
    path ('signup', views.signup,name='signup page'),
    # path('private_dashboard', views.private_dashboard, name='private_dashboard'),
    path('logout', views.logout, name='logout page'),

    path ('chart', views.chart,name='chart page'),
    path('api/generate-auto-data/', views.generate_auto_data, name='generate_auto_data'),
    path('generate_auto_data/', views.generate_auto_data, name='generate_auto_data'),
    path('api/generate_and_insert_data/', views.generate_and_insert_data, name='generate_and_insert_data'),
    path('private_dashboard/user_tabledata&<str:table_name>/', views.private_dashboard, name='private_dashboard'),

    # re_path(r'^private_dashboard/(?P<unique_table_name>[\w\d_]+)/$', generate_and_insert_data),


    # path('fetch_temperature_data/', views.fetch_temperature_data, name='fetch_temperature_data'),
    
]

