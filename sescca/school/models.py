from django.db import models
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


# Create your models here.
class Campus(models.Model):
    name = models.CharField(max_length=20, verbose_name='Sede')
    mean_score = models.DecimalField(verbose_name='Promedio', max_digits=5, decimal_places=2, default=000.00)

    class Meta:
        verbose_name = 'sede'
        verbose_name_plural = 'sedes'

    def __str__(self):
        return self.name

class Worktime(models.Model):
    name = models.CharField(max_length=20, verbose_name='Jornada')
    mean_score = models.DecimalField(verbose_name='Promedio', max_digits=5, decimal_places=2, default=000.00)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, verbose_name='Sede')

    class Meta:
        verbose_name = 'jornada'
        verbose_name_plural = 'jornadas'

    def __str__(self):
        return self.name

class Section(models.Model):
    grade = models.PositiveSmallIntegerField(verbose_name='grado')
    letter = models.CharField(max_length=1, verbose_name='sección')
    mean_score = models.DecimalField(verbose_name='Promedio', max_digits=5, decimal_places=2, default=000.00)
    worktime = models.ForeignKey(Worktime, on_delete=models.CASCADE, verbose_name='Jornada')

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

    def __str__(self):
        return str(self.grade) + self.letter

class Student(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombres')
    last_name = models.CharField(max_length=200, verbose_name='Apellidos')
    id_board = models.PositiveIntegerField(verbose_name='ID Tarjeta', default=0)
    ip_board = models.GenericIPAddressField(verbose_name='IP Tarjeta', blank=True, null=True)
    score = models.PositiveSmallIntegerField(verbose_name='Puntaje', default=0, validators=[MaxValueValidator(100),])
    accum_score = models.PositiveSmallIntegerField(verbose_name='Acumulado Semanal', default=0, validators=[MaxValueValidator(500),])
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    worktime = models.ForeignKey(Worktime, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'
        ordering = ['last_name',]

    def __str__(self):
        return self.name + ' ' + self.last_name
@receiver(pre_save, sender=Student)
def leave_group_section_exchange(sender, instance, **kwargs):
    try:
        old_instance = Student.objects.get(pk=instance.pk)
    except Student.DoesNotExist:
        old_instance = None
    if old_instance !=None:
        if instance.section != old_instance.section:
            groups = instance.group_set.all()
            if groups:
                for group in groups:
                    group.students.remove(instance)

class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre del grupo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    mean_score = models.DecimalField(verbose_name='Promedio', max_digits=5, decimal_places=2, default=000.00)
    students = models.ManyToManyField(Student)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    worktime = models.ForeignKey(Worktime, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'
        ordering = ['-created',]

    def __str__(self):
        return self.name