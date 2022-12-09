from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Pertanyaan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=256)
    konten = models.TextField()
    snippet = models.TextField(default=None, blank=True, null=True)
    waktu_upload = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('forum-question-detail', kwargs={'pk': self.pk})

class Jawaban(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pertanyaan_asal = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    konten = models.TextField()
    snippet = models.TextField(default=None, blank=True, null=True)
    waktu_upload = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('forum-question-detail', kwargs={'pk': self.pk})

class Komentar(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pertanyaan_asal = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    konten = models.TextField()
    waktu_upload = models.DateTimeField(default=timezone.now)