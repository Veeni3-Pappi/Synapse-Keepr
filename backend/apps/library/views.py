from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import ImportJob, Playlist, Resource
from .serializers import ImportJobSerializer, PlaylistSerializer, ResourceSerializer


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
        queryset = Resource.objects.filter(owner=self.request.user).prefetch_related("playlist_memberships__playlist")
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
        return Resource.objects.filter(owner=self.request.user).prefetch_related("playlist_memberships__playlist")


class ImportJobListView(ListAPIView):
    serializer_class = ImportJobSerializer

    def get_queryset(self):
        return ImportJob.objects.filter(owner=self.request.user)


class ImportJobDetailView(RetrieveAPIView):
    serializer_class = ImportJobSerializer

    def get_queryset(self):
        return ImportJob.objects.filter(owner=self.request.user)
