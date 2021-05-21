from .models import Store
from .serializers import StoreSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    authentication_classes = (TokenAuthentication,)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        if not user.is_superuser and not user.is_staff:
            queryset = Store.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

