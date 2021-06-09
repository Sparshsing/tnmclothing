from django.urls import path, include
from rest_framework import routers
from .views import InvoiceViewSet

router = routers.DefaultRouter()
router.register('', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls))
]