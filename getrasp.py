from os import fsdecode
import sql
from timework import dayWeeks_ind, next_weekday, add_begin_zero, time_lessons

def auditory_and_teacher(str):
    list = str.split(',')
    list[0] = list[0].title()
    list[-1] = list[-1].replace(" АУД. ",'')
    return list

def get_text_rasp(id, day):
    rasp = sql.get_rasp(id,day)
    day_lessons = next_weekday(day)
    if rasp == []:
        return f"Пар на {dayWeeks_ind[day]} нет! Отдыхайте ☺️"
    text_rasp = f"Расписание на {dayWeeks_ind[day]} {day_lessons.day}.{add_begin_zero(day_lessons.month)}:\n\n"
    for lesson in sql.get_rasp(id,day):
        aud_and_t = auditory_and_teacher(lesson[2])
        text_rasp += f"Пара {lesson[0]} ({time_lessons[lesson[0]-1]}):\n {lesson[1].title()}\n Преподаватель: {aud_and_t[0]}\n Аудитория: {aud_and_t[-1]} \n\n"
    return text_rasp[:-2]


