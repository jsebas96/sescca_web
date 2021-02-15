from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import InterfaceView
from school.models import Campus, Section

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

class BoardView(ListView):
    model = InterfaceView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = context['interfaceview_list'].get(name='Vista individual').section
        view_id = context['interfaceview_list'].get(name='Vista individual').id
        context['section'] = section
        context['view_id'] = view_id
        return context

class BoardUpdateView(UpdateView):
    model = InterfaceView
    fields = ['section',]
    template_name = "core/interfaceview_update_form.html"

    def get_success_url(self):
        return reverse_lazy('board') + '?updated'

    def post(self, request, *args, **kwargs):
        view_section = request.POST.get('section')
        views = InterfaceView.objects.all()
        section = Section.objects.get(id=view_section)
        for view in views:
            view.section = section
            view.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campusses'] = Campus.objects.all()
        return context

def change_view(request):
    if request.user.is_authenticated:
        json_response = {'change':'False'}
        id = request.GET.get('vw', None)
        view = InterfaceView.objects.get(id=id)
        views = InterfaceView.objects.all().exclude(id=id)
        if view.active == False:
            view.active = True
            view.save()
            for view_aux in views:
                view_aux.active = False
                view_aux.save()
        else:
            view.active = False
            view.save()
            for view_aux in views:
                view_aux.active = False
                view_aux.save()
        json_response['change'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)