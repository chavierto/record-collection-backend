from rest_framework import serializers
from .models import Artist, Album, Song


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    albums = serializers.HyperlinkedRelatedField(
        view_name='album_detail',
        many=True,
        read_only=True
    )
    artist_url = serializers.ModelSerializer.serializer_url_field(
        view_name='artist_detail'
    )

    class Meta:
        model = Artist
        fields = ('artist', 'notes', 'photo_url', 'albums', 'artist_url')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    artist = serializers.HyperlinkedRelatedField(
        view_name='artist_detail', read_only=True,
    )
    artist_string = serializers.CharField(source='artist.artist')
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'
    )
    songs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='song_detail'
    )

    class Meta:
        model = Album
        fields = ('id', 'title', 'artist', 'artist_string', 'artist_id', 'release_date',
                  'acquired_date', 'genre', 'label', 'notes', 'photo_url', 'songs')


class SongSerializer(serializers.HyperlinkedModelSerializer):
    artist = serializers.HyperlinkedRelatedField(
        view_name='artist_detail', read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'
    )
    album = serializers.HyperlinkedRelatedField(
        view_name='album_detail', read_only=True)

    class Meta:
        model = Song
        fields = ('id', 'track', 'title', 'artist',
                  'artist_id', 'album', 'song_url')
