from django.urls import path
from .views import AutoEvaluationView, activate_view, restart_board, plus_score, minus_score

urlpatterns = [
    path('', AutoEvaluationView.as_view(), name='evaluation'),
    path('activate/', activate_view, name='activate'),
    path('plus/', plus_score, name='plus_score'),
    path('minus/', minus_score, name='minus_score'),
    path('restartboard/', restart_board, name='restart_board'),
]