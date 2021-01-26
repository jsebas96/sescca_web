import threading, time, requests, random, os
from evaluation.models import AutoEvaluation
from school.models import Student
payload = {'data':'alert'}

def timer_interrupt():
    print("Interrupt")
    students = Student.objects.all()
    for student in students:
        if student.ip_board:
            response = os.popen(f"ping -c 4 {student.ip_board}").read()
            if "4 received" in response:
                url = "http://" + student.ip_board
                r = requests.get(url, params=payload)
                print(r.status_code)
            else:
                print("No hay conexión")
    run()

def run():
    print("Start")
    timer = AutoEvaluation.objects.get(id=1)
    if timer.activate is True:
        timer_b = timer.time_range * 60 + timer.time_range * 30
        timer_a = 45
        last_time = timer.time_range
        clock = threading.Timer(random.randint(timer_a, timer_b), timer_interrupt)
        clock.start()
        while timer.activate is True:
            time.sleep(0.5)
            timer = AutoEvaluation.objects.get(id=1)
            if timer.time_range != last_time:
                print("break")
                break
        clock.cancel()
        run()
    else:
        pass
        time.sleep(1)
        run()
