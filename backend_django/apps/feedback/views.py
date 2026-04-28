from rest_framework import generics, permissions, filters
from .models import Feedback
from .serializers import FeedbackSerializer
from apps.users.permissions import IsAnyAdmin, IsSuperAdmin


class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.AllowAny]  # Fixed: Allow anonymous feedback submission
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment', 'category', 'user__username']
    ordering_fields = ['created_at', 'rating']

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsSuperAdmin]

