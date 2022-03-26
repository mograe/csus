import schedule
import sql
import time
from main import send_rasp
from vkbot import VkBot
from config import vk_token as vt
import getrasp
import timework

def send_rasp(id):
    bot = VkBot(vt)
    bot.send_msg(id,getrasp.get_text_rasp(id,timework.getNextDay()))

def send_timetable():
    list_users = sql.get_sub_list()
    print('hello')
    for i in list_users:
        if(sql.get_rasp(i,timework.getNextDay()) != []):
            send_rasp(i)

schedule.every().day.at("18:00").do(send_timetable)

while True:
    schedule.run_pending()
    time.sleep(1)