from django.urls import path, include
from rest_framework import routers
from .views import InventoryViewSet

router = routers.DefaultRouter()
router.register('', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]