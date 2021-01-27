import threading, time, requests, random, os
from evaluation.models import AutoEvaluation
from school.models import Student
from core.models import InterfaceView
payload = {'data':'alert'}
salida = False

def timer_interrupt():
    global salida
    print("Interrupt")
    view = InterfaceView.objects.get(name="Vista individual")
    if view.section:
        section = view.section
        students = Student.objects.filter(section=section)
        for student in students:
            if student.ip_board:
                response = os.popen(f"ping -c 4 {student.ip_board}").read()
                if "4 received" in response:
                    url = "http://" + student.ip_board
                    r = requests.get(url, params=payload)
                    print(r.status_code)
                else:
                    print("No hay conexión")
    salida = True
    print(salida)

def run():
    global salida
    print("Start")
    timer = AutoEvaluation.objects.get(id=1)
    if timer.activate is True:
        timer_b = timer.time_range * 60 + timer.time_range * 30
        timer_a = 45
        last_time = timer.time_range
        interval = random.randint(timer_a, timer_b)
        print(interval)
        clock = threading.Timer(interval, timer_interrupt)
        clock.start()
        while timer.activate is True:
            # print("Loop")
            # time.sleep(0.5)
            timer = AutoEvaluation.objects.get(id=1)
            if timer.time_range != last_time:
                print("break")
                break
            if salida is True:
                salida = False
                print("break")
                break
        clock.cancel()
        print("Cancel Timer")
        run()
    else:
        pass
        time.sleep(1)
        run()
