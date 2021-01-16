from django.db import models

# Create your models here.
class InterfaceView(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre Vista')
    active = models.BooleanField(verbose_name='Vista Activa', default=False)

    class Meta:
        verbose_name = 'vista'
        verbose_name_plural = 'vistas'

    def __str__(self):
        return self.name