from django.db import models
from school.models import Section
# Create your models here.
class InterfaceView(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre Vista')
    active = models.BooleanField(verbose_name='Vista Activa', default=False)
    section = models.OneToOneField(Section, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'vista'
        verbose_name_plural = 'vistas'

    def __str__(self):
        return self.name