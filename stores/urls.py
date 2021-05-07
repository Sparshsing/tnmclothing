from django.urls import path, include
from rest_framework import routers
from .views import StoreViewSet

router = routers.DefaultRouter()
router.register('', StoreViewSet)

urlpatterns = [
    path('', include(router.urls))
]