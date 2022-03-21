import schedule
import sql
import time
from main import send_rasp

def send_timetable():
    list_users = sql.get_sub_list()
    for i in list_users:
        send_rasp(id)

schedule.every().day.at("18:00").do(send_timetable)

while True:
    schedule.run_pending()
    time.sleep(1)