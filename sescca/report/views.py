from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from school.models import Student
from .models import Conduct, DailyData, WeeklyData
from django.http.response import HttpResponse
from openpyxl import Workbook

# Create your views here.
class IndividualReport(DetailView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        student = Student.objects.get(id=pk)
        context['conduct_list'] = Conduct.objects.filter(student=student)
        context['daily_score_list'] = DailyData.objects.filter(student=student)
        context['weekly_score_list'] = WeeklyData.objects.filter(student=student)
        return context

class GenerateReport(TemplateView):
    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=1)
        group = student.group_set.all()

        wb = Workbook()
        ws = wb.active
        ws['B1'] = 'REPORTE DE ESTUDIANTE'
        ws['B3'] = 'NOMBRES'
        ws['C3'] = 'APELLIDOS'
        ws['D3'] = 'SEDE'
        ws['E3'] = 'JORNADA'
        ws['F3'] = 'CURSO'
        ws['G3'] = 'GRUPO'
        cont = 4
        ws.cell(row=cont, column=2).value = student.name
        ws.cell(row=cont, column=3).value = student.last_name
        ws.cell(row=cont, column=4).value = student.campus.name
        ws.cell(row=cont, column=5).value = student.worktime.name
        ws.cell(row=cont, column=6).value = str(student.section.grade) + student.section.letter
        if group:
            ws.cell(row=cont, column=7).value = group[0]
        else:
            ws.cell(row=cont, column=7).value = 'No asignado'

        nombre_archivo = student.name + '_Report.xlsx'

        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename={0}".format(nombre_archivo)

        response["Content-Disposition"] = contenido

        wb.save(response)

        return response

