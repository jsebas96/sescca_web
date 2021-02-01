from django.contrib import admin
from .models import Student, Campus, Worktime, Section, Group

# Register your models here.
def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['last_name', 'name', 'id_board', 'ip_board', 'score',]
    list_filter = (('campus', custom_titled_filter('Sede')), ('worktime', custom_titled_filter('Jornada')), ('section', custom_titled_filter('Curso')))
    readonly_fields = ["accum_score", "disruption",]

class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ['name', 'created', 'mean_score']
    readonly_fields = ["created",]

class CampusAdmin(admin.ModelAdmin):
    model = Campus
    list_display = ['name', 'mean_score']

class WorktimeAdmin(admin.ModelAdmin):
    model = Worktime
    list_display = ['name', 'campus','mean_score']

class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ['grade', 'letter', 'worktime','mean_score']

admin.site.register(Student, StudentAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Worktime, WorktimeAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Group, GroupAdmin)