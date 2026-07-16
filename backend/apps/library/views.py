from django.db.models import Count, Q
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImportJob, Playlist, Resource, ResourceSummary
from .serializers import ImportJobSerializer, PlaylistSerializer, ResourceSerializer
from .tasks import generate_resource_summary


class PlaylistListView(ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user).annotate(resource_count=Count("playlist_resources"))


class PlaylistDetailView(RetrieveAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user).annotate(resource_count=Count("playlist_resources"))


class ResourceListView(ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = Resource.objects.filter(owner=self.request.user).prefetch_related("playlist_memberships__playlist").select_related("summary")
        query = self.request.query_params.get("q", "").strip()
        playlist_id = self.request.query_params.get("playlist")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if playlist_id:
            queryset = queryset.filter(playlist_memberships__playlist_id=playlist_id)
        return queryset.distinct()


class ResourceDetailView(RetrieveAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        return Resource.objects.filter(owner=self.request.user).prefetch_related("playlist_memberships__playlist").select_related("summary")


class ImportJobListView(ListAPIView):
    serializer_class = ImportJobSerializer

    def get_queryset(self):
        return ImportJob.objects.filter(owner=self.request.user)


class ImportJobDetailView(RetrieveAPIView):
    serializer_class = ImportJobSerializer

    def get_queryset(self):
        return ImportJob.objects.filter(owner=self.request.user)


class ResourceSummaryCreateView(APIView):
    def post(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk, owner=request.user)
        except Resource.DoesNotExist:
            return Response({"code": "not_found", "detail": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        summary, _ = ResourceSummary.objects.update_or_create(
            resource=resource,
            defaults={"status": ResourceSummary.Status.QUEUED, "content": "", "model": "", "error_detail": ""},
        )
        generate_resource_summary.delay(summary.pk)
        return Response({"id": summary.pk, "status": summary.status}, status=status.HTTP_202_ACCEPTED)
