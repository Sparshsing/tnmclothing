from django.urls import path, include
from rest_framework import routers
from .views import InvoiceListView, InvoiceDetailView, generate_invoices

urlpatterns = [
    path('', InvoiceListView.as_view()),
    path('<int:pk>/', InvoiceDetailView.as_view()),
    path('generate_invoices/', generate_invoices)
]