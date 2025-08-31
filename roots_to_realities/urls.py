"""
URL configuration for roots_to_realities project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from villages.views import VillageViewSet, AIStoryViewSet
from marketplace.views import EntrepreneurViewSet, ProductViewSet, OrderViewSet
from training.views import TrainingModuleViewSet, UserTrainingProgressViewSet
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# API Router
router = DefaultRouter()
router.register(r'villages', VillageViewSet)
router.register(r'ai-stories', AIStoryViewSet)
router.register(r'entrepreneurs', EntrepreneurViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'training-modules', TrainingModuleViewSet)
router.register(r'training-progress', UserTrainingProgressViewSet, basename='training-progress')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('api/auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
