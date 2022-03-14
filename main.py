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



def matrixOfList(list, numRow):
    column = -1
    matrix = []
    for i in range(len(list)):
        if i % numRow == 0:
            column += 1
            matrix.append([])
        matrix[column].append(list[i])
    return matrix

def choose_faculty(id,reg=False):    
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_facultylist(),2) + ([['Отмена']]))
    sql.chg_position(id, 7 if reg else 8)
    msg = "Выберете ваш факультет"
    bot.send_msg(id, msg, keyboard.get_keyboard())

def choose_course(id,fac,reg=False):
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_courselist(fac),3) + ([['Отмена']]))
    sql.chg_position(id, 9 if reg else 10)
    msg = "Выберете курс"
    bot.send_msg(id, msg, keyboard.get_keyboard())
    

def choose_group(id,reg=False):
    keyboard = VkBot.create_keyboard(matrixOfList(sql.get_grouplist1(sql.get_faculty_user(id),sql.get_course(id)),2) + ([['Отмена']]))
    sql.chg_position(id, 1 if reg else 4)
    msg = "Выберите группу"
    bot.send_msg(id, msg, keyboard.get_keyboard())

        
def choose_subgroup(id,reg=False):
    keyboard = VkBot.create_keyboard([['1','2']] + ([] if reg else [['Отмена']]))
    sql.chg_position(id, 2 if reg else 5)
    bot.send_msg(id, "Выберите подгруппу", keyboard.get_keyboard())

def main_menu(id):
    keyboard = VkBot.create_keyboard([['Расписание']]+ ([['Пересдачи']] if sql.get_faculty_user(id) == 'Математический' else []) +[['Изменить группу','Изменить подгруппу']])
    sql.chg_position(id,3)
    bot.send_msg(id, "Вы в главном меню", keyboard.get_keyboard())

def choose_day(id):
    keyboard = VkBot.create_keyboard([["На сегодня","На завтра"]] + matrixOfList(sql.get_dayslist(id),3) + [["Отмена"]])
    sql.chg_position(id,6)
    bot.send_msg(id,"Выберите на какой день вам нужно расписание", keyboard.get_keyboard())

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
            choose_subgroup(id,reg=True)
        if text == 'ОТМЕНА':
            choose_course(id, sql.get_faculty_user, True)
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
            bot.send_msg(id,getrasp.get_retakes(id))
            main_menu(id)
        elif text == "Изменить группу":
            choose_faculty(id)
        elif text == "Изменить подгруппу":
            choose_subgroup(id)
        else:
            bot.send_msg(id,"Что-то пошло не так. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            main_menu(id)

    elif number_position == 4:
        text = text.replace('-','').replace(' ','').upper()
        if text in group_list:
            sql.set_group(id, text)
            bot.send_msg(id, f"Была выбрана группа {text}")
            logging.info(f"{id} choose group {text}")
            main_menu(id)
        elif text == 'ОТМЕНА':
            choose_course(id, sql.get_faculty_user, True)
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
                bot.send_msg(id,getrasp.get_text_rasp(id,timework.getNextDay()))
            elif text == "На сегодня":
                bot.send_msg(id,getrasp.get_text_rasp(id,timework.getToday()))
            else:
                bot.send_msg(id,getrasp.get_text_rasp(id,dayWeeks.index(text)))
            main_menu(id)
        elif text == "Отмена":
            main_menu(id)
        else:
            bot.send_msg(id, f"Вы выбрали неверный день. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_day(id)

    elif number_position in [7, 8]:
        if text in sql.get_facultylist():
            bot.send_msg(id, f"Был выбран факультет {text}")
            logging.info(f"{id} choose fac {text}")
            sql.set_faculty(id,text)
            choose_course(id, text, True if number_position == 7 else False)
        elif text == "Отмена" and number_position == 8:
            main_menu(id)
        else:
            bot.send_msg(id, f"Вы выбрали неверный факультет. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_faculty(id, True if number_position == 7 else False)
    
    elif number_position in [9, 10]:
        if text in sql.get_courselist(sql.get_faculty_user(id)):
            bot.send_msg(id, f"Был выбран курс {text}")
            logging.info(f"{id} choose course {text}")
            sql.set_course(id, text)
            choose_group(id, True if number_position == 9 else False )
        elif text == "Отмена":
            choose_faculty(id, True if number_position == 9 else False )
        else:
            bot.send_msg(id, f"Вы выбрали неверный курс. Попробуйте ещё раз")
            logging.error(f"{id} write wrong message")
            choose_course(id, True if number_position == 9 else False )

    
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
                    
                    
