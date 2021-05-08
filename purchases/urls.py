from django.urls import path, include
from rest_framework import routers
from .views import PurchaseViewSet

router = routers.DefaultRouter()
router.register('', PurchaseViewSet)

urlpatterns = [
    path('', include(router.urls))
]