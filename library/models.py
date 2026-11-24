from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    subtitle = models.FileField(upload_to='subtitles/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(blank=True, null=True)
    last_position = models.FloatField(default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.title


class WatchLog(models.Model):
    date = models.DateField(unique=True)
    seconds = models.FloatField(default=0)

    def __str__(self):
        return f"{self.date} — {int(self.seconds // 60)} dəq"