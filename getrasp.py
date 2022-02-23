from os import fsdecode
import sql
from timework import dayWeeks_ind, next_weekday, add_begin_zero

def get_text_rasp(id, day):
    rasp = sql.get_rasp(id,day)
    day_lessons = next_weekday(day)
    if rasp == []:
        return f"Пар на {dayWeeks_ind[day]} нет! Отдыхайте ☺️"
    text_rasp = f"Расписание на {dayWeeks_ind[day]} {day_lessons.day}.{add_begin_zero(day_lessons.month)}:\n\n"
    for lesson in sql.get_rasp(id,day):
        text_rasp += f"Пара {lesson[0]}: {lesson[1]}\n {lesson[2]}\n\n"
    return text_rasp[:-2]


