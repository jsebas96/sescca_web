import threading
from school.models import Student
from core.models import InterfaceView
from evaluation.models import Disruption
salida = False

def disruption():
    global salida
    print("Interrupt")
    view = InterfaceView.objects.get(name="Vista Individual")
    if view.section:
        section = view.section
        students = Student.objects.filter(section=section)
        for student in students:
            if student.disruption is True:
                if student.ip_board:
                    response = os.popen(f"ping -c 2 {student.ip_board}").read()
                    if "2 received" in response:
                        url = "http://" + student.ip_board
                        r = requests.get(url, params={'minus':'true'})
                        print(r.status_code)
                        student.score = student.score - 1
                        student.accum_score = student.accum_score - 1
                        student.disruption = False
                        student.save()

                    else:
                        print("No hay conexión")
    salida = True
    print(salida)

def run():
    global salida
    print("Start")
    disrupt = Disruption.objects.get(id=1)
    if disrupt.active is True:
        clock = threading.Timer(10, disruption)
        clock.start()
        while disrupt.activate is True:
            disrupt = Disruption.objects.get(id=1)
            if salida is True:
                salida = False
                print("break")
                break
        clock.cancel()
        print("Cancel Timer")
        run()