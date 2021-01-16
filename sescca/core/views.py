from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import ListView
from .models import InterfaceView

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

class BoardView(ListView):
    model = InterfaceView

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