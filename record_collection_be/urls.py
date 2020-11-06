from django.urls import path
from . import views
from django.conf.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

urlpatterns = [

    path('', views.AlbumList.as_view()),
    path('artists', views.ArtistList.as_view(), name='artist_list'),
    path('artists/<int:pk>', views.ArtistDetail.as_view(), name='artist_detail'),
    path('albums', views.AlbumList.as_view(), name='album_list'),
    path('albums/<int:pk>', views.AlbumDetail.as_view(), name='album_detail'),
    path('songs', views.SongList.as_view(), name='song_list'),
    path('songs/<int:pk>', views.SongDetail.as_view(), name='song_detail')
]
