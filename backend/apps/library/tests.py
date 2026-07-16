from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from .models import ImportJob, IntegrationConnection, Playlist, PlaylistResource, Provider, Resource, ResourceSummary


class LibraryApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="alex", password="secret")
        self.other_user = get_user_model().objects.create_user(username="sam", password="secret")
        self.connection = IntegrationConnection.objects.create(
            owner=self.user, provider=Provider.YOUTUBE, provider_account_id="youtube-channel-1"
        )
        self.playlist = Playlist.objects.create(owner=self.user, connection=self.connection, external_id="playlist-1", name="Django")
        self.resource = Resource.objects.create(
            owner=self.user,
            provider=Provider.YOUTUBE,
            external_id="video-1",
            title="Django REST Framework tutorial",
            description="Build a useful API.",
            url="https://youtube.com/watch?v=video-1",
        )
        PlaylistResource.objects.create(playlist=self.playlist, resource=self.resource, position=1)
        Resource.objects.create(
            owner=self.other_user,
            provider=Provider.YOUTUBE,
            external_id="private-video",
            title="Someone else's video",
            url="https://youtube.com/watch?v=private-video",
        )
        self.client.force_login(self.user)

    def test_playlist_list_is_scoped_to_authenticated_owner(self):
        response = self.client.get(reverse("playlist-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Django")
        self.assertEqual(response.json()[0]["resource_count"], 1)

    def test_resource_search_and_playlist_filter(self):
        response = self.client.get(reverse("resource-list"), {"q": "framework", "playlist": self.playlist.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["playlists"], ["Django"])

    def test_unauthenticated_requests_are_rejected(self):
        self.client.logout()

        response = self.client.get(reverse("resource-list"))

        self.assertEqual(response.status_code, 403)

    def test_import_jobs_are_scoped_to_authenticated_owner(self):
        ImportJob.objects.create(owner=self.user, connection=self.connection, status=ImportJob.Status.RUNNING, playlists_discovered=3)
        other_connection = IntegrationConnection.objects.create(
            owner=self.other_user, provider=Provider.YOUTUBE, provider_account_id="youtube-channel-2"
        )
        ImportJob.objects.create(owner=self.other_user, connection=other_connection, status=ImportJob.Status.COMPLETED)

        response = self.client.get(reverse("import-job-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["status"], "running")
        self.assertEqual(response.json()[0]["playlists_discovered"], 3)

    @patch("apps.library.views.generate_resource_summary.delay")
    def test_summary_request_is_queued_for_owned_resource(self, delay):
        response = self.client.post(reverse("resource-summary-create", args=[self.resource.pk]))

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["status"], "queued")
        summary = ResourceSummary.objects.get(resource=self.resource)
        delay.assert_called_once_with(summary.pk)
