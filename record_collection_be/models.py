from django.db import models
from django.db.models import F
from django.db.models.functions import Lower


class Artist(models.Model):
    artist = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('artist'), F('user_id'),
                name='artist_name_user_case_insensitive_unique'
            )
        ]

    def __str__(self):
        return self.artist


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(
        Artist, on_delete=models.PROTECT, related_name='albums')
    release_date = models.DateField(blank=True, null=True)
    acquired_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100, default='Song title')
    track = models.CharField(max_length=100, blank=True, null=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='songs')
    song_url = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['track']

    def __str__(self):
        return f'{self.track} - {self.title}'
