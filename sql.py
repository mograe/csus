
import sqlite3
from timework import dayWeeks, isEvenWeek
from datetime import datetime

def table_to_lists(table):
    list = []
    for row in table:
       list.append(row[0])
    return list

def add_lesson(name, tar, number, group, day, week, subgroup):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO lessons (name, tar, number, lesson_group, day, week, subgroup)" 
        + f"VALUES ('{name}','{tar}',{number},'{group}','{day}',{week},{subgroup})")
    db.commit()

def add_retake(date, teacher, lesson, group, time, cabinet):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO retakes (date, teacher, lesson, lesson_group, time, cabinet)" 
        + f"VALUES ('{date}','{teacher}','{lesson}','{group}','{time}','{cabinet}')")
    db.commit()

def get_grouplist():
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute("SELECT DISTINCT lesson_group from lessons")
    return table_to_lists(sql_cur.fetchall())

def add_sub(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
    db.commit()


def take_position(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT pos FROM users WHERE user_id = '{user_id}'")
    pos = sql_cur.fetchall()
    if pos == []:
        return 0
    else:
        return pos[0][0]

def chg_position(user_id,pos):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE users SET pos = '{pos}' WHERE user_id = '{user_id}'")
    db.commit()


def set_group(user_id, group):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE users SET lesson_group = '{group}' WHERE user_id = '{user_id}'")
    db.commit()

def get_group(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT lesson_group from users WHERE user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]
    

def set_subgroup(user_id, subgroup):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE users SET subgroup = '{subgroup}' WHERE user_id = '{user_id}'")
    db.commit()

def get_subgroup(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT subgroup from users WHERE user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]

def get_rasp(user_id, day):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    day_str = dayWeeks[day]
    sql_cur.execute(f"SELECT number, name, tar from lessons WHERE lesson_group = '{get_group(user_id)}'" +
     f"AND day = '{day_str}' AND (week = 0 OR week = {int(isEvenWeek(day_str))+1})" +
     f"AND (subgroup = 0 OR subgroup = {get_subgroup(user_id)}) ORDER BY number")
    return sql_cur.fetchall()

def get_retakes(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT * from retakes WHERE lesson_group = '{get_group(user_id)}'")
    table = sql_cur.fetchall()
    res = []
    for i in table:
        dt_obj = datetime.strptime(i[1],'%Y-%m-%d %H:%M:%S')
        if(datetime.now() < dt_obj):
            res.append(i)
    return res
    


def get_dayslist(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT DISTINCT day from lessons WHERE lesson_group = '{get_group(user_id)}'")
    return table_to_lists(sql_cur.fetchall())

def add_lesson_group(fac,course,group):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO lesson_groups (lesson_group, faculty, course)" 
        + f"VALUES ('{group}','{fac}', '{course}')")
    db.commit()

def get_facultylist():
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute("SELECT DISTINCT faculty from lesson_groups")
    return table_to_lists(sql_cur.fetchall())

def get_courselist(fac):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT DISTINCT course from lesson_groups WHERE faculty = '{fac}'")
    return table_to_lists(sql_cur.fetchall())

def get_faculty_user(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT faculty from users WHERE user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]

def set_faculty(user_id, faculty):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE users SET faculty = '{faculty}' WHERE user_id = '{user_id}'")
    db.commit()

def get_course(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT course from users WHERE user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]

def set_course(user_id, course):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE users SET course = '{course}' WHERE user_id = '{user_id}'")
    db.commit()

def get_grouplist1(faculty, course):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT DISTINCT lesson_group from lesson_groups WHERE faculty = '{faculty}' AND course = '{course}'")
    return table_to_lists(sql_cur.fetchall())
