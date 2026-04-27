from rest_framework import generics, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Facility
from .serializers import FacilitySerializer


@method_decorator(cache_page(60 * 5), name='list')  # Cache 5 minutes
class FacilityListView(generics.ListCreateAPIView):
    queryset = Facility.objects.filter(is_deleted=False)
    serializer_class = FacilitySerializer
    permission_classes = [permissions.AllowAny]  # Public read access


class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.filter(is_deleted=False)
    serializer_class = FacilitySerializer
    permission_classes = [permissions.AllowAny]  # Public read access

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

