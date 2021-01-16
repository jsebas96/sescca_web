from django.db import models

# Create your models here.
class AutoEvaluation(models.Model):
    time_range = models.PositiveSmallIntegerField(verbose_name='Rango de Tiempo para autoevaluación')
    activate = models.BooleanField(verbose_name="activo", default=False)

    class Meta:
        verbose_name = 'tiempo'
        verbose_name_plural = 'tiempos'

    def __str__(self):
        return str(self.time_range) + ' Minutos'