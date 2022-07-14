from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import AutoEvaluation, Disruption
from .forms import AutoEvaluationForm

from school.models import Student
from report.models import Conduct, DailyData, WeeklyData
# Create your views here.

import requests
import os
import datetime

def activate_view(request):
    if request.user.is_authenticated:
        id = 1
        value = request.GET.get('val', None)
        if id:
            time = get_object_or_404(AutoEvaluation, id=id)
            if value == 'true':
                time.activate = True
            else: 
                time.activate = False
            time.save()
    else:
        raise Http404("User is not authenticated")
    return render(request, 'evaluation/autoevaluation_form.html')

@method_decorator(login_required, name='dispatch')
class AutoEvaluationView(UpdateView):
    form_class = AutoEvaluationForm
    template_name = 'evaluation/autoevaluation_form.html'
    success_url = reverse_lazy('student_list')

    def get_object(self):
        time, created = AutoEvaluation.objects.get_or_create(id=1)
        return time

def restart_board(request):
    json_response = {'recount':'False'}
    if request.user.is_authenticated:
        id = request.GET.get('idb', None)
        if id:
            student = get_object_or_404(Student, id_board=id)
            response = os.popen(f"ping -c 2 {student.ip_board}").read()
            if "2 received" in response:
                #print(student.ip_board)
                _ = requests.get("http://"+str(student.ip_board), params={'recount':'true'})
                json_response['recount'] = True
            else:
                print("No hay conexión")
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def activate_view(request):
    if request.user.is_authenticated:
        id = 1
        value = request.GET.get('val', None)
        if id:
            time = get_object_or_404(AutoEvaluation, id=id)
            if value == 'true':
                time.activate = True
            else: 
                time.activate = False
            time.save()
    else:
        raise Http404("User is not authenticated")
    return render(request, 'evaluation/autoevaluation_form.html')

def activate_disruption(request):
    json_response = {'updated':'False'}
    if request.user.is_authenticated:
        id = 1
        value = request.GET.get('val', None)
        if id:
            disrupt = get_object_or_404(Disruption, id=id)
            if value == 'true':
                disrupt.active = True
            else: 
                disrupt.active = False
            disrupt.save()
            json_response['updated'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def plus_score(request):
    json_response = {'sent':'False'}
    if request.user.is_authenticated:
        id = request.GET.get('cs', None)
        if id:
            student = get_object_or_404(Student, id=id)
            response = os.popen(f"ping -c 2 {student.ip_board}").read()
            if "2 received" in response:
                #print(student.ip_board)
                _ = requests.get("http://"+str(student.ip_board), params={'plus':'true'})
                student.score = student.score + 1
                student.accum_score = student.accum_score + 1
                student.save()
                json_response['sent'] = True
                date = datetime.datetime.now()
                try:
                    daily_data = DailyData.objects.get(student=student, created__day=date.day, created__month=date.month, created__year=date.year)
                    daily_data.daily_score = student.score
                    daily_data.save()
                except Exception:
                    daily_data = DailyData.objects.create(student=student, daily_score=student.score)
            else:
                print("No hay conexión")
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def minus_score(request):
    json_response = {'sent':'False'}
    if request.user.is_authenticated:
        id = request.GET.get('cs', None)
        if id:
            student = get_object_or_404(Student, id=id)
            response = os.popen(f"ping -c 2 {student.ip_board}").read()
            if "2 received" in response:
                _ = requests.get("http://"+str(student.ip_board), params={'minus':'true'})
                student.score = student.score - 1
                student.accum_score = student.accum_score - 1
                student.save()
                json_response['sent'] = True
                date = datetime.datetime.now()
                try:
                    daily_data = DailyData.objects.get(student=student, created__day=date.day, created__month=date.month, created__year=date.year)
                    daily_data.daily_score = student.score
                    daily_data.save()
                except Exception:
                    daily_data = DailyData.objects.create(student=student, daily_score=student.score)
            else:
                print("No hay conexión")
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def receive_score_from_board(request):
    json_response = {'received':'False'}
    id = int(request.POST.get('id', None))
    state = int(request.POST.get('state', None))
    if id:
        student = get_object_or_404(Student, id=id)
        if (state == 1) & (student.disruption == False):
            student.score = student.score + 1
            student.accum_score = student.accum_score + 1
        elif (state == 1) & (student.disruption == True):
            student.score = student.score - 1
            student.accum_score = student.accum_score - 1
            Conduct.objects.create(student=student, conduct='Levantarse')
            student.disruption = False
        elif (state == 0) & (student.disruption) == True:
            student.score = student.score - 1
            student.accum_score = student.accum_score - 1
            Conduct.objects.create(student=student, conduct='Levantarse')
            student.disruption = False
        elif (state) == 0 & (student.disruption) == False:
            student.score = student.score + 1
            student.accum_score = student.accum_score + 1
        student.save()
        json_response['received'] = True
        date = datetime.datetime.now()
        try:
            daily_data = DailyData.objects.get(student=student, created__day=date.day, created__month=date.month, created__year=date.year)
            daily_data.daily_score = student.score
            daily_data.save()
        except Exception:
            daily_data = DailyData.objects.create(student=student, daily_score=student.score)
    return JsonResponse(json_response)