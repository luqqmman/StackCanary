from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Pertanyaan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=256)
    konten = models.TextField()
    snippet = models.TextField()
    waktu_upload = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.judul

class Jawaban(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pertanyaan_asal = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    konten = models.TextField()
    snippet = models.TextField()
    waktu_upload = models.DateTimeField(default=timezone.now)

class Komentar(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pertanyaan_asal = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    konten = models.TextField()
    waktu_upload = models.DateTimeField(default=timezone.now)