import logging
import threading
import sql
from vk_api import longpoll
from vk_api.longpoll import VkLongPoll, VkEventType
from vkbot import VkBot
from config import vk_token as vt
import getrasp
import timework
from timework import dayWeeks
import requests
import json
from random_anime_picture import random_pic

def get_list_retakes_id(table):
    ids = []
    for row in table:
        ids.append(str(row[0]))
    return ids

def matrixOfList(list, numRow):
    column = -1
    matrix = []
    for i in range(len(list)):
        if i % numRow == 0:
            column += 1
            matrix.append([])
        matrix[column].append(list[i])
    return matrix

def send_rasp(id):
    bot = VkBot(vt)
    bot.send_msg(id,getrasp.get_text_rasp(id,timework.getNextDay()))

def go_to_mm(id):
    bot = VkBot(vt)
    keyboard = VkBot.create_keyboard([['Расписание']]+ ([['Пересдачи', 'Рассылка']] if sql.get_faculty_user(id) == 'Математический' else (['Рассылка'])) + [['Изменить группу'] + (['Изменить подгруппу'] if sql.group_is_have_subgroup(id) else [])])
    sql.chg_position(id,3)
    bot.send_msg(id, "Вы в главном меню", keyboard.get_keyboard())
 

def choose_faculty(id,reg=False, sub = False):    
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_facultylist(),2) + ([] if reg else [['Отмена']]))
    if reg:
        sql.chg_position(id, 7)
    elif sub:
        sql.chg_position(id, 11)
    else:
        sql.chg_position(id, 8)
    msg = "Выберете ваш факультет"
    bot.send_msg(id, msg, keyboard.get_keyboard())

def choose_course(id,fac,reg=False, sub = False):
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_courselist(fac),3) + ([['Отмена']]))
    if reg:
        sql.chg_position(id, 9)
    elif sub:
        sql.chg_position(id, 12)
    else:
        sql.chg_position(id, 10)    
    msg = "Выберете курс"
    bot.send_msg(id, msg, keyboard.get_keyboard())
    

def choose_group(id,reg=False, sub = False):
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_grouplist1(sql.get_faculty_user(id),sql.get_course(id)),2) + ([['Отмена']]))
    if sub:
        sql.chg_position(id, 13)
    else:
        sql.chg_position(id, 1 if reg else 4)
    msg = "Выберите группу"
    bot.send_msg(id, msg, keyboard.get_keyboard())

        
def choose_subgroup(id,reg=False):
    keyboard = VkBot.create_keyboard([['1','2']] + ([] if reg else [['Отмена']]))
    sql.chg_position(id, 2 if reg else 5)
    bot.send_msg(id, "Выберите подгруппу", keyboard.get_keyboard())

def main_menu(id):
    keyboard = VkBot.create_keyboard([['Расписание']]+ ([['Пересдачи','Рассылка']] if sql.get_faculty_user(id) == 'Математический' else (['Рассылка'])) + [['Изменить группу'] + (['Изменить подгруппу'] if sql.group_is_have_subgroup(id) else [])])
    sql.chg_position(id,3)
    bot.send_msg(id, "Вы в главном меню", keyboard.get_keyboard())

def choose_day(id):
    keyboard = VkBot.create_keyboard([["На сегодня","На завтра"]] + matrixOfList(sql.get_dayslist(id),3) + [["Отмена"]])
    sql.chg_position(id,6)
    bot.send_msg(id,"Выберите на какой день вам нужно расписание", keyboard.get_keyboard())


def subscribe(id):
    sql.sub_user(id)
    bot.send_msg(id, f"Вы подписались на рассылку для группы {sql.get_group(id)}")
    main_menu(id)

def unsubscribe(id):
    sql.unsub_user(id)
    bot.send_msg(id, f"Вы отписались на рассылку для группы {sql.get_group(id)}")
    main_menu(id)

def send_menu(id):
    keyboard = VkBot.create_keyboard([(['Подписаться на рассылку для вашей группы'] if not sql.get_sub_user(id) else ['Отписаться от рассылки для вашей группы']),['Подписаться на другую группу','Удалить группу из списка подписок'],['Отписаться от пересдачи'], ['Отмена']])
    sql.chg_position(id, 14)
    list = json.loads(sql.get_sub_user_list(id))
    msg = f"Вы {'не ' if not sql.get_sub_user(id) else ''}подписаны на рассылки для вашей группы и подгруппы\n"
    if list == []:
        msg += "Вы не подписаны ни на одну другую группу"
    else:
        msg += "Список группы, на которые вы подписаны:\n"
        for i in list:
            msg += '-' + i + '\n'
    msg += '\n'
    list = json.loads(sql.get_retakes_user_list(id))
    if list == []:
        msg += "Вы не подписаны ни на одну пересдачу"
    else:
        msg += "Список пересдач, на которые вы подписаны:\n"
        for i in list:
            msg += getrasp.get_retakes_by_id(int(i))
    bot.send_msg(id,msg[:-2], keyboard.get_keyboard())

def del_group(id):
    keyboard = VkBot.create_keyboard(matrixOfList(json.loads(sql.get_sub_user_list(id)),3) + [['Отмена']])
    sql.chg_position(id, 15)
    bot.send_msg(id,"Выберите от какой группы Вы хотите отписаться", keyboard.get_keyboard())

def sub_retakes(id):
    keyboard = VkBot.create_keyboard(matrixOfList(get_list_retakes_id(sql.get_retakes(id)),3) + [['Отмена']])
    sql.chg_position(id, 16)
    bot.send_msg(id,"Выберите на какую пересдачу вы бы хотели подписаться", keyboard.get_keyboard())

def del_retakes(id):
    keyboard = VkBot.create_keyboard(matrixOfList(json.loads(sql.get_retakes_user_list(id)),3) + [['Отмена']])
    sql.chg_position(id,17)
    bot.send_msg(id,"Выберите от какой пересдачи вы бы хотели отписаться", keyboard.get_keyboard())


def processing_message(id, text):
    number_position = sql.take_position(id)
    logging.info(f"{id} in {number_position} position")

    if number_position == 0: #Приветствие
        bot.send_msg(id, 'Привет. Это бот "Расписание ЧелГУ". Пожалуйста, пройдите регистрацию.')
        choose_faculty(id,reg=True)
        sql.add_sub(id)
    
    elif number_position == 1:
        text = text.replace('-','').replace(' ','').upper()
        if text in group_list:
            sql.set_group(id, text)
            bot.send_msg(id, f"Была выбрана группа {text}")
            logging.info(f"{id} choose group {text}")
            if sql.group_is_have_subgroup(id):
                choose_subgroup(id,reg=True)
            else:
                sql.set_subgroup(id,0)
                main_menu(id)
        elif text == 'ОТМЕНА':
            choose_course(id, sql.get_faculty_user(id), True)
        else:
            bot.send_msg(id, f"Вы выбрали неверную группу. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_group(id,reg=True)
    
    elif number_position == 2:
        if text in ['1','2']:
            sql.set_subgroup(id, text)
            bot.send_msg(id, f"Была выбрана подгруппа {text}")
            logging.info(f"{id} choose subgroup {text}")
            main_menu(id)
        else:
            print(text)
            bot.send_msg(id, f"Вы выбрали неверную подгруппу. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_subgroup(id,reg=True)

    elif number_position == 3:
        if text == "Расписание":
            choose_day(id)
        elif text == "Пересдачи":
            bot.send_msg_with_pic(id,getrasp.get_retakes(id),random_pic())
            sub_retakes(id)
        elif text == "Изменить группу":
            choose_faculty(id)
        elif text == "Изменить подгруппу":
            choose_subgroup(id)
        elif text == 'Рассылка':
            send_menu(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            main_menu(id)

    elif number_position in [4,13]:
        text = text.replace('-','').replace(' ','')
        if text in group_list:
            if number_position == 13:
                if not text in json.loads(sql.get_sub_user_list(id)):
                    sql.add_sub_user(id,text)
                    bot.send_msg(id, f"Была выбрана группа {text}")
                else:
                    bot.send_msg(id, f"Вы подписаны уже на эту группу")
            else:
                sql.set_group(id, text)
            logging.info(f"{id} choose group {text}")
            main_menu(id)
        elif text == 'Отмена':
            choose_course(id, sql.get_faculty_user(id))
        else:
            bot.send_msg(id, f"Вы выбрали неверную группу. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_group(id)
    
    elif number_position == 5:
        if text in ['1','2']:
            sql.set_subgroup(id, text)
            bot.send_msg(id, f"Была выбрана подгруппа {text}")
            logging.info(f"{id} choose subgroup {text}")
            main_menu(id)
        elif text == 'Отмена':
            main_menu(id)
        else:
            print(text)
            bot.send_msg(id, f"Вы выбрали неверную подгруппу. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_subgroup(id)

    elif number_position == 6:
        if text in ["На завтра","На сегодня"] + sql.get_dayslist(id):
            logging.info(f"{id} choose day {text}")
            if text == "На завтра":
                print(timework.getNextDay())
                bot.send_msg_with_pic(id,getrasp.get_text_rasp(id,timework.getNextDay()),random_pic())
            elif text == "На сегодня":
                bot.send_msg_with_pic(id,getrasp.get_text_rasp(id,timework.getToday()),random_pic())
            else:
                bot.send_msg_with_pic(id,getrasp.get_text_rasp(id,dayWeeks.index(text)),random_pic())
            main_menu(id)
        elif text == "Отмена":
            main_menu(id)
        else:
            bot.send_msg(id, f"Вы выбрали неверный день. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_day(id)

    elif number_position in [7, 8, 11]:
        if text in sql.get_facultylist():
            bot.send_msg(id, f"Был выбран факультет {text}")
            logging.info(f"{id} choose fac {text}")
            sql.set_faculty(id,text)
            choose_course(id, text, True if number_position == 7 else False, True if number_position == 11 else False)
        elif text == "Отмена" and number_position == 8:
            main_menu(id)
        else:
            bot.send_msg(id, f"Вы выбрали неверный факультет. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_faculty(id, True if number_position == 7 else False, True if number_position == 11 else False)
    
    elif number_position in [9, 10, 12]:
        if text in sql.get_courselist(sql.get_faculty_user(id)):
            bot.send_msg(id, f"Был выбран курс {text}")
            logging.info(f"{id} choose course {text}")
            sql.set_course(id, text)
            choose_group(id, True if number_position == 9 else False, True if number_position == 12 else False)
        elif text == "Отмена":
            choose_faculty(id, True if number_position == 9 else False, True if number_position == 12 else False)
        else:
            bot.send_msg(id, f"Вы выбрали неверный курс. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_course(id, True if number_position == 9 else False, True if number_position == 12 else False)

    elif number_position == 14:
        if text == 'Подписаться на рассылку для вашей группы':
            subscribe(id)
        elif text == 'Отписаться от рассылки для вашей группы':
            unsubscribe(id)
        elif text == 'Подписаться на другую группу':
            if len(json.loads(sql.get_sub_user_list(id))) >= 9:
                bot.send_msg(id, "Слишком много групп в ваших подписках. Пожалуйста отпишитесь от какой-то группы, чтобы подписаться на новую")
                send_menu(id)
            else:
                choose_faculty(id, False, True)
        elif text == 'Удалить группу из списка подписок':
            del_group(id)
        elif text == 'Отписаться от пересдачи':
            del_retakes(id)
        elif text == 'Отмена':
            main_menu(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            send_menu(id)

    elif number_position == 15:
        if text in json.loads(sql.get_sub_user_list(id)):
            sql.unsub_list_user(id,text)
            main_menu(id)
        elif text == 'Отмена':
            send_menu(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            del_group(id)

    elif number_position == 16:
        if text in get_list_retakes_id(sql.get_retakes(id)):
            if not text in sql.get_retakes_user_list(id):
                sql.add_retakes_user(id,text)
            else:
                bot.send_msg(id,"Вы уже подписаны на эту пересдачу")
            main_menu(id)
        elif text == 'Отмена':
            main_menu(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            sub_retakes(id)

    elif number_position == 17:
        if text in json.loads(sql.get_retakes_user_list(id)):
            sql.unsub_retakes_list_user(id,text)
            main_menu(id)
        elif text == 'Отмена':
            main_menu(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            del_retakes(id)

if __name__ == '__main__': 
    logging.info("Bot is starting")
    while True:
        session = requests.Session()
        bot = VkBot(vt)
        longpoll = VkLongPoll(bot.vk_session)
        group_list = sql.get_grouplist()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                threading.Thread(target=processing_message, args=(event.user_id, event.text)).start()
                    
                    
