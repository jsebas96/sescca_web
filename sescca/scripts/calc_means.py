import threading
from school.models import Student, Campus, Worktime, Section, Group

def calculate():
    students = Student.objects.all()
    campusses = Campus.objects.all()
    worktimes = Worktime.objects.all()
    sections = Section.objects.all()
    groups = Group.objects.all()
    if campusses:
        for campus in campusses:
            mean = 0
            students_in = 0
            for student in students:
                if campus == student.campus:
                    students_in += 1
                    mean = mean + student.score
            if students_in != 0:
                campus.mean_score = mean / students_in
            campus.save()
    if worktimes:
        for worktime in worktimes:
            mean = 0
            students_in = 0
            for student in students:
                if worktime == student.worktime:
                    students_in += 1
                    mean = mean + student.score
            if students_in != 0:
                worktime.mean_score = mean / students_in
            worktime.save()
    if sections:
        for section in sections:
            mean = 0
            students_in = 0
            for student in students:
                if section == student.section:
                    students_in += 1
                    mean = mean + student.score
            if students_in != 0:
                section.mean_score = mean / students_in
            section.save()
    if groups:
        for group in groups:
            mean = 0
            for student in group.students.all():
                mean = mean + student.score
            if len(group.students.all()) != 0:
                group.mean_score = mean / len(group.students.all())
            group.save()
    run()
def run():
    clock = threading.Timer(10, calculate)
    clock.start()
