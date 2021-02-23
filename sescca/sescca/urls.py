"""sescca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('board/', core_views.BoardView.as_view(), name='board'),
    path('board/change/', core_views.change_view, name='change_view'),
    path('board/update/<int:pk>/', core_views.BoardUpdateView.as_view(), name='update_view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('school/', include('school.urls')),
    path('report/', include('report.urls')),
]
