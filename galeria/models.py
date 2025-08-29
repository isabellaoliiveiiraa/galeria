from django.db import models
from django.utils import timezone

class Foto(models.Model):
    STATUS_CHOICES = [
        ('PUBLICADO', 'Publicado'),
        ('RASCUNHO', 'Rascunho'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_foto = models.DateField(default=timezone.now)
    local = models.CharField(max_length=150, blank=True)
    imagem = models.ImageField(upload_to='fotos/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RASCUNHO')
    estrela = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_foto']

    def __str__(self):
        return self.titulo