import schedule
import sql
import time
from main import send_rasp, go_to_mm
from vkbot import VkBot
from config import vk_token as vt
import getrasp
import timework
import json
from random_anime_picture import random_pic

def send_rasp(id):
    bot = VkBot(vt)
    bot.send_msg(id,getrasp.get_text_rasp(id,timework.getNextDay()))
    go_to_mm(id)

def send_rasp_for_group(id, group):
    bot = VkBot(vt)
    bot.send_msg(id,getrasp.get_text_rasp_for_group(group,timework.getNextDay()))
    go_to_mm(id)

def send_retake(id, id_retake):
    bot = VkBot(vt)
    bot.send_msg(id,getrasp.get_retakes_by_id(id_retake))
    go_to_mm(id)

def send_timetable():
    list_users = sql.get_all_users()
    for user in list_users:
        id = user[0]
        list_groups = json.loads(user[2])
        if(user[1] == 1):
            if(sql.get_rasp(id,timework.getNextDay()) != []):
                send_rasp(id)
        if(list_groups != []):
            for g in list_groups:
                if(getrasp.get_text_rasp_for_group(g,timework.getNextDay()) != []):
                    send_rasp_for_group(id,g)

def send_retakes():
    list_users = sql.get_all_users_retakes()
    for user in list_users:
        id = user[0]
        list_retakes = json.loads(user[1])
        if list_retakes != []:
            for r in list_retakes:
                send_retake(id,r)
                if timework.days_left(sql.get_retake_by_id(r)[1]) <= 1:
                    sql.unsub_retakes_list_user(id,r)

schedule.every().day.at("18:00").do(send_timetable)
schedule.every().day.at("20:00").do(send_retakes)

while True:
    schedule.run_pending()
    time.sleep(1)