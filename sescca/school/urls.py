from django.urls import path
from .views import StudentFormView, StudentUpdateView, StudentListView, StudentListView2, StudentDeleteView, CampusSelected, WorktimeSelected, SectionSelected, GroupFormView, GroupUpdateView, GroupListView, GroupDeleteView

urlpatterns = [
    path('newstudent/', StudentFormView.as_view(), name='student'),
    path('students/update/<int:pk>', StudentUpdateView.as_view(), name='update_student'),
    path('students/delete/<int:pk>', StudentDeleteView.as_view(), name='delete_student'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/info/', StudentListView2.as_view(), name='student_list2'),
    path('campus/', CampusSelected, name='campus'),
    path('worktime/', WorktimeSelected, name='worktime'),
    path('section/', SectionSelected, name='section'),
    path('groups/add/', GroupFormView.as_view(), name='create_group'),
    path('groups/update/<int:pk>/', GroupUpdateView.as_view(), name='update_group'),
    path('groups/delete/<int:pk>/', GroupDeleteView.as_view(), name='delete_group'),
    path('groups/', GroupListView.as_view(), name='groups'),
]