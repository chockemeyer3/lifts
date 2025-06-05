# workouts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LiftEntryViewSet

router = DefaultRouter()
router.register(r'lifts', LiftEntryViewSet, basename='lifts')

urlpatterns = [
    path('', include(router.urls)),
]
