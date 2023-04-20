"""
URL configuration for cisco project.

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
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('devices/', views.device_list, name='device_list'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('', views.network_list, name='network_list'),
    path('network/<int:pk>/', views.network_detail, name='network_detail'),
    path('devices/add/', views.device_add, name='device_add'),
    path('network/add/', views.NetworkCreateView.as_view(), name='network_create'),
    path('network/<int:pk>/connection/create/', views.connection_create, name='connection_create'),
    path('connection/create/step2/<int:pk1>/<int:pk2>/', views.connection_create2, name='connection_create2'),
    path('<int:pk>/device/<int:pk2>/delete/', views.device_delete, name='device_delete'),
    path('network/<int:pk>/connection/<int:id>/delete/', views.connection_delete, name='connection_delete'),
]
