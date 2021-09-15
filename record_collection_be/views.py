# The following came in with the inital setup:
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Song, Album

# Create your views here.


# def artist_list(request):
#     artists = Artist.objects.all()
#     return render(request, 'record_collection_be/artist_list.html', {'artists': artists})


class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects
    serializer_class = AlbumSerializer


class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

def create_new_record(request):
    if request.method == 'POST':
        artist_name = request.POST['artist_name']
        artist = Artist.objects.create(artist=artist_name)
        album = Album.objects.create(artist, )
        return HttpResponse(album)