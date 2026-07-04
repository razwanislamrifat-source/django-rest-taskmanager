from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        # Group by status
        status_counts = queryset.values('status').annotate(count=Count('id'))
        status_summary = {item['status']: item['count'] for item in status_counts}
        # Group by priority
        priority_counts = queryset.values('priority').annotate(count=Count('id'))
        priority_summary = {item['priority']: item['count'] for item in priority_counts}
        return Response({
            'by_status': status_summary,
            'by_priority': priority_summary,
        }, status=status.HTTP_200_OK)

