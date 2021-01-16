from django import forms
from .models import Student, Group

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("name", "last_name", "id_board", "campus", "worktime", "section")

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombres'}),
            'last_name':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Apellidos'}),
            'id_board':forms.NumberInput(attrs={'class':'form-control mb-3'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)