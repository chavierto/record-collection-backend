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
    album_count = serializers.IntegerField(source='albums.count', read_only=True)

    def validate_artist(self, value):
        qs = Artist.objects.filter(artist__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'An artist with this name already exists.'
            )
        return value

    class Meta:
        model = Artist
        fields = ('id', 'artist', 'notes', 'photo_url', 'albums', 'artist_url', 'album_count')


class SongInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'track', 'title', 'song_url')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    artist = serializers.HyperlinkedRelatedField(
        view_name='artist_detail', read_only=True,
    )
    artist_string = serializers.CharField(source='artist.artist', read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist'
    )
    songs = SongInlineSerializer(many=True, read_only=True)

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
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        source='album'
    )

    class Meta:
        model = Song
        fields = ('id', 'track', 'title', 'artist',
                  'artist_id', 'album', 'album_id', 'song_url')
