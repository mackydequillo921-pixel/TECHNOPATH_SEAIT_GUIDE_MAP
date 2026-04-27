from rest_framework import generics, permissions
from .models import Facility
from .serializers import FacilitySerializer


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

