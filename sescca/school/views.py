from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from  django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView
from django import forms

from .forms import StudentForm, GroupForm
from .models import Student, Campus, Worktime, Section, Group

# Create your views here.
def CampusSelected(request):
    json_response = {'created':False}
    if request.user.is_authenticated:
        campus_id = request.GET.get("cam", None)
        campus = Campus.objects.get(id=campus_id)
        worktimes = Worktime.objects.filter(campus=campus)
        json_response['worktimes'] = []

        for worktime in worktimes:
            json_response['worktimes'].append({'name':worktime.name, 'value':worktime.id})

        json_response['created'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def WorktimeSelected(request):
    json_response = {'created':False}
    if request.user.is_authenticated:
        worktime_id = request.GET.get("wt", None)
        worktime = Worktime.objects.get(id=worktime_id)
        sections = Section.objects.filter(worktime=worktime)
        json_response['sections'] = []

        for section in sections:
            json_response['sections'].append({'grade':section.grade, 'letter':section.letter,'value':section.id})

        json_response['created'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def SectionSelected(request):
    json_response = {'created':False}
    if request.user.is_authenticated:
        section_id = request.GET.get("st", None)
        section = Section.objects.get(id=section_id)
        students = Student.objects.filter(section=section)
        json_response['students'] = []

        for student in students:
            if not student.group_set.all():
                json_response['students'].append({'name':student.name, 'last_name':student.last_name,'value':student.id})
            
        json_response['created'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response) 

@method_decorator(login_required, name='dispatch')
class StudentFormView(FormView):
    form_class = StudentForm
    template_name = 'school/student_form.html'
    
    def get_success_url(self):
        return reverse_lazy('student_list') + '?created'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        id_board = request.POST.get('id_board')

        id_campus = request.POST.get('campus')
        campus = Campus.objects.get(id=id_campus)
        id_worktime = request.POST.get('worktime')
        worktime = Worktime.objects.get(id=id_worktime)
        id_section = request.POST.get('section')
        section = Section.objects.get(id=id_section)
        
        if form.is_valid():
            Student.objects.create(name=name, last_name=last_name, id_board=id_board, campus=campus, worktime=worktime, section=section)            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campusses'] = Campus.objects.all()
        return context

def StudentListView(request):
    template_name ='school/student_list.html'
    context = {}
    context['campusses'] = Campus.objects.all()

    if request.user.is_authenticated:
        id_campus = request.GET.get('cam', None)
        id_worktime = request.GET.get('wt', None)
        id_section = request.GET.get('st', None)
        id_group = request.GET.get('gp', None)
        students = Student.objects.all()
        if id_campus:
            campus = Campus.objects.get(id=id_campus)
            students = students.filter(campus=campus)
            context['campus_object'] = campus
            context['campus_name'] = campus.name
            context['worktimes'] = Worktime.objects.filter(campus=campus)
        if id_worktime:
            worktime = Worktime.objects.get(id=id_worktime)
            students = students.filter(worktime=worktime)
            context['worktime_object'] = worktime
            context['worktime_name'] = worktime.name
            context['sections'] = Section.objects.filter(worktime=worktime)
        if id_section:
            section = Section.objects.get(id=id_section)
            students = students.filter(section=section)
            context['section_info'] = section
            context['groups'] = Group.objects.filter(section=section)
        if id_group:
            group = Group.objects.get(id=id_group)
            students = students.filter(group=group)
            context['group_object'] = group
        context['student_list'] = students
        
    else:
        raise Http404("User is not authenticated")
    return render(request, template_name, context)

def StudentListView2(request):
    template_name = 'school/student_list2.html'
    context = {}
    context['campusses'] = Campus.objects.all()

    if request.user.is_authenticated:
        id_campus = request.GET.get('cam', None)
        id_worktime = request.GET.get('wt', None)
        id_section = request.GET.get('st', None)
        id_group = request.GET.get('gp', None)
        students = Student.objects.all()
        if id_campus:
            campus = Campus.objects.get(id=id_campus)
            students = students.filter(campus=campus)
            context['campus_name'] = campus.name
            context['worktimes'] = Worktime.objects.filter(campus=campus)
        if id_worktime:
            worktime = Worktime.objects.get(id=id_worktime)
            students = students.filter(worktime=worktime)
            context['worktime_name'] = worktime.name
            context['sections'] = Section.objects.filter(worktime=worktime)
        if id_section:
            section = Section.objects.get(id=id_section)
            students = students.filter(section=section)
            context['section_info'] = section
            context['groups'] = Group.objects.filter(section=section)
        if id_group:
            group = Group.objects.get(id=id_group)
            students = students.filter(group=group)
            context['group_object'] = group
        context['student_list'] = students
        
    else:
        raise Http404("User is not authenticated")
    return render(request, template_name, context)

@method_decorator(login_required, name='dispatch')
class StudentUpdateView(UpdateView):
    form_class = StudentForm
    template_name = 'school/student_update_form.html'
    
    def get_success_url(self):
        return reverse_lazy('student_list2') + '?updated'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        student = Student.objects.get(id=pk)
        return student       

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        student = Student.objects.get(id=pk)
        context['campusses'] = Campus.objects.all()
        context['worktimes'] = Worktime.objects.filter(campus=student.campus)
        context['sections'] = Section.objects.filter(worktime=student.worktime)
        return context

@method_decorator(login_required, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student

    def get_success_url(self):
        return reverse_lazy('student_list')

@method_decorator(login_required, name='dispatch')
class GroupFormView(FormView):
    form_class = GroupForm
    template_name = 'school/group_form.html'
    
    def get_success_url(self):
        return reverse_lazy('groups') + '?created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campusses'] = Campus.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        name = request.POST.get('name')
        id_campus = request.POST.get('campus')
        campus = Campus.objects.get(id=id_campus)
        id_worktime = request.POST.get('worktime')
        worktime = Worktime.objects.get(id=id_worktime)
        id_section = request.POST.get('section')
        section = Section.objects.get(id=id_section)
        student_id_list = request.POST.getlist('student_list')

        if form.is_valid():          
            mean = 0
            group = Group.objects.create(name=name, mean_score=mean, campus=campus, worktime=worktime, section=section)
            if len(student_id_list) > 0:
                for student_id in student_id_list:
                    student = Student.objects.get(id=student_id)
                    group.students.add(student)
                    mean = mean + student.score
                mean = mean/len(group.students.all())
                group.mean_score = mean
            group.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class GroupListView(ListView):
    model = Group
    template_name = 'school/group_list.html'

class GroupUpdateView(UpdateView):
    form_class = GroupForm
    template_name = 'school/group_update.html'
    
    def get_success_url(self):
        return reverse_lazy('groups') + '?updated'

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        student_list_delete = request.POST.getlist('student_list_delete')
        student_list_add = request.POST.getlist('student_list_add')
        group = Group.objects.get(id=pk)
        for student_id in student_list_delete:
            student = Student.objects.get(id=student_id)
            group.students.remove(student)
        for student_id in student_list_add:
            student = Student.objects.get(id=student_id)
            group.students.add(student)
            group.save()
        self.object = self.get_object()
        return super(GroupUpdateView, self).post(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        group = Group.objects.get(id=pk)
        return group

    def get_form(self, form_class=None):
        form = super(GroupUpdateView, self).get_form()
        form.fields['name'].widget = forms.TextInput(attrs={'class':'form-control mb-3 font-weight-bold', 'placeholder':'Nombre del grupo'})
        return form 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get(self.pk_url_kwarg)
        group = Group.objects.get(id=pk)

        students = Student.objects.filter(section=group.section).exclude(group=group)

        for student in students:
            groups = student.group_set.all()
            if groups:
                students = students.exclude(id=student.id)
            print(students)
        
        context['students_add'] = students
        context['students'] = group.students.all()
        return context

class GroupDeleteView(DeleteView):
    model = Group
    
    def get_success_url(self):
        return reverse_lazy('groups') + '?deleted'