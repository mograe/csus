from os import fsdecode
from re import sub
import string
import sql
from timework import dayWeeks_ind, next_weekday, add_begin_zero, time_lessons, days_left, plural_days

def auditory_and_teacher(str):
    list = str.split(',')
    list[0] = list[0].title()
    list[-1] = list[-1].replace(" АУД. ",'')
    return list

def first_word(str):
    return str.split(' ')[0]

def add_zero(n):
    strn = str(n)
    while len(strn) < 3:
        strn = '0' + strn
    return strn

def get_text_rasp(id, day):
    rasp = sql.get_rasp(id,day)
    day_lessons = next_weekday(day)
    if rasp == []:
        return f"Пар на {dayWeeks_ind[day]} нет! Отдыхайте ☺️"
    text_rasp = f"Расписание на {dayWeeks_ind[day]} {day_lessons.day}.{add_begin_zero(day_lessons.month)} для группы {sql.get_group(id)}:\n\n"
    for lesson in sql.get_rasp(id,day):
        aud_and_t = auditory_and_teacher(lesson[2])
        text_rasp += f"Пара {lesson[0]} ({time_lessons[lesson[0]-1]}):\n {lesson[1].capitalize()}\n Преподаватель: {aud_and_t[0]}\n Аудитория: {aud_and_t[-1]} \n\n"
    return text_rasp[:-2]

def get_text_rasp_for_group(group, day):
    rasp = sql.get_rasp_by_group(group,day)
    day_lessons = next_weekday(day)
    if rasp == []:
        return f"Пар на {dayWeeks_ind[day]} нет! Отдыхайте ☺️"
    text_rasp = f"Расписание на {dayWeeks_ind[day]} {day_lessons.day}.{add_begin_zero(day_lessons.month)} для группы {group}:\n\n"
    for lesson in sql.get_rasp_by_group(group,day):
        aud_and_t = auditory_and_teacher(lesson[2])
        subgroup = lesson[3]
        subgroup_str = f"подгруппа {subgroup}"
        text_rasp += f"Пара {lesson[0]} ({time_lessons[lesson[0]-1]}) {subgroup_str if subgroup != 0 else ''} :\n {lesson[1].capitalize()}\n Преподаватель: {aud_and_t[0]}\n Аудитория: {aud_and_t[-1]} \n\n"
    return text_rasp[:-2]

def get_retakes(id):
    retakes = sql.get_retakes(id)
    if retakes == []:
        return "Для Вашей группы пересдач пока не назначено"
    text_rasp = f"Пересдачи для группы {sql.get_group(id)} \n\n"
    for r in retakes:
        text_rasp += f"({r[0]}) Пересдача на {first_word(r[1])} ({r[5][:-3]}):\n {r[3]}\n Преподаватель: {r[2]}\n Аудитория: {add_zero(r[6])}\n осталось {plural_days(days_left(r[1]))} \n\n"
    return text_rasp[:-2]

def get_retakes_by_id(id):
    r = sql.get_retake_by_id(id)
    text_rasp = f"({r[0]}) Пересдача на {first_word(r[1])} ({r[5][:-3]}):\n {r[3]}\n Преподаватель: {r[2]}\n Аудитория: {add_zero(r[6])}\n осталось {plural_days(days_left(r[1]))} \n\n"
    return text_rasp
     


