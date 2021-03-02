from django.urls import path
from .views import IndividualReport, GenerateReport

urlpatterns = [
    path('student/<int:pk>/', IndividualReport.as_view(), name='ind_report'),
    path('generate/<int:pk>/', GenerateReport.as_view(), name='report'),
]