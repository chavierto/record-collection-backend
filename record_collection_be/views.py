from django.db.models import ProtectedError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Song, Album


class ArtistList(generics.ListCreateAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        return Artist.objects.filter(user_id=self.request.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user_id)


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        return Artist.objects.filter(user_id=self.request.user_id)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'This artist has albums. Remove their albums before deleting.'},
                status=status.HTTP_409_CONFLICT
            )


class AlbumList(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user_id)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user_id)


class SongList(generics.ListCreateAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(album__user_id=self.request.user_id)


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(album__user_id=self.request.user_id)
