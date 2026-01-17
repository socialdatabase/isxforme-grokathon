from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GrokathonViewSet

# Create a router and register the ViewSet
router = DefaultRouter()
router.register(r'grokathon', GrokathonViewSet, basename='grokathon')

urlpatterns = [
    path('', include(router.urls)),
]
