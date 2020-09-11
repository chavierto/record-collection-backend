from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField(blank=True, null=True)
    acquired_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    # songs = models.ForeignKey(
    #     Song, on_delete=models.CASCADE, related_name='songs')
    notes = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100, default='Song title')
    track = models.CharField(max_length=100, blank=True, null=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='songs')
    song_url = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['album', 'track']
        ordering = ['track']

    def __str__(self):
        return f'{self.track} - {self.title}'
