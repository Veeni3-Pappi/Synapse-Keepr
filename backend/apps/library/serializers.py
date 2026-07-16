from rest_framework import serializers

from .models import ImportJob, Playlist, Resource


class PlaylistSerializer(serializers.ModelSerializer):
    resource_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "name", "description", "thumbnail_url", "imported_at", "resource_count"]


class ResourceSerializer(serializers.ModelSerializer):
    playlists = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ["id", "title", "description", "url", "thumbnail_url", "published_at", "duration_seconds", "playlists"]

    def get_playlists(self, resource):
        return [membership.playlist.name for membership in resource.playlist_memberships.all()]


class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = ["id", "status", "playlists_discovered", "resources_imported", "error_detail", "created_at", "started_at", "completed_at"]
