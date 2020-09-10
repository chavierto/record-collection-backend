from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    photo_url = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='albums')
    release_year = models.DateField(blank=True)
    acquired_date = models.DateField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=100, blank=True)
    # songs = models.ForeignKey(
    #     Song, on_delete=models.CASCADE, related_name='songs')
    notes = models.TextField(blank=True)
    photo_url = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100, default='Song title')
    track = models.CharField(max_length=100, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='songs')
    song_url = models.TextField(blank=True)

    class Meta:
        unique_together = ['album', 'track']
        ordering = ['track']

    def __str__(self):
        return f'{self.track} - {self.title}'
