from rest_framework import serializers

from .models import ImportJob, Playlist, Resource, ResourceSummary


class PlaylistSerializer(serializers.ModelSerializer):
    resource_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "name", "description", "thumbnail_url", "imported_at", "resource_count"]


class ResourceSerializer(serializers.ModelSerializer):
    playlists = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ["id", "title", "description", "url", "thumbnail_url", "published_at", "duration_seconds", "playlists", "summary"]

    def get_playlists(self, resource):
        return [membership.playlist.name for membership in resource.playlist_memberships.all()]

    def get_summary(self, resource):
        try:
            summary = resource.summary
        except ResourceSummary.DoesNotExist:
            return None
        return {"status": summary.status, "content": summary.content, "model": summary.model}


class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = ["id", "status", "playlists_discovered", "resources_imported", "error_detail", "created_at", "started_at", "completed_at"]
