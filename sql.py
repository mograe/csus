import sqlite3
from timework import dayWeeks, isEvenWeek

def table_to_lists(table):
    list = []
    for row in table:
       list.append(row[0])
    return list

def add_lesson(name, tar, number, group, day, week, subgroup):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    print('work')
    sql_cur.execute(f"INSERT INTO lessons (name, tar, number, lesson_group, day, week, subgroup)" 
        + f"VALUES ('{name}','{tar}',{number},'{group}','{day}',{week},{subgroup})")
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

def get_dayslist(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT DISTINCT day from lessons WHERE lesson_group = '{get_group(user_id)}'")
    return table_to_lists(sql_cur.fetchall())