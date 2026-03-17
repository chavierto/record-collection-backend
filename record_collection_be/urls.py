from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlbumList.as_view()),
    path('artists', views.ArtistList.as_view(), name='artist_list'),
    path('artists/<int:pk>', views.ArtistDetail.as_view(), name='artist_detail'),
    path('albums', views.AlbumList.as_view(), name='album_list'),
    path('albums/<int:pk>', views.AlbumDetail.as_view(), name='album_detail'),
    path('songs', views.SongList.as_view(), name='song_list'),
    path('songs/<int:pk>', views.SongDetail.as_view(), name='song_detail'),
    path('discogs/search', views.DiscogsSearch.as_view(), name='discogs_search'),
    path('discogs/release/<int:release_id>', views.DiscogsRelease.as_view(), name='discogs_release'),
    path('discogs/master/<int:master_id>', views.DiscogsMaster.as_view(), name='discogs_master'),
    path('discogs/image', views.DiscogsImage.as_view(), name='discogs_image'),
]
