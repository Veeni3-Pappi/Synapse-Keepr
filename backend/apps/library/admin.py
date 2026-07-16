from django.contrib import admin

from .models import ImportJob, IntegrationConnection, Playlist, PlaylistResource, Resource

admin.site.register((ImportJob, IntegrationConnection, Playlist, PlaylistResource, Resource))
