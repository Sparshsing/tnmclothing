from django.urls import path, include
from rest_framework import routers
from .views import InvoiceViewSet, invoice_pdf_view

router = routers.DefaultRouter()
router.register('', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pdf/<int:id>/', invoice_pdf_view)
]