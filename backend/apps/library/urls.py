from django.urls import path

from .views import ImportJobDetailView, ImportJobListView, PlaylistDetailView, PlaylistListView, ResourceDetailView, ResourceListView, ResourceSummaryCreateView

urlpatterns = [
    path("playlists/", PlaylistListView.as_view(), name="playlist-list"),
    path("playlists/<int:pk>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("resources/", ResourceListView.as_view(), name="resource-list"),
    path("resources/<int:pk>/", ResourceDetailView.as_view(), name="resource-detail"),
    path("resources/<int:pk>/summary/", ResourceSummaryCreateView.as_view(), name="resource-summary-create"),
    path("imports/", ImportJobListView.as_view(), name="import-job-list"),
    path("imports/<int:pk>/", ImportJobDetailView.as_view(), name="import-job-detail"),
]
