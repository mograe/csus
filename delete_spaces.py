import sqlite3

def set_group(id, group):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"UPDATE lessons SET lesson_group = '{group}' WHERE id = '{id}'")
    db.commit()

def get_group(id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT lesson_group from lessons WHERE id = '{id}'")
    return sql_cur.fetchall()[0][0]

if __name__ == '__main__':
    for i in range(72,767):
        set_group(i,get_group(i).replace(' ',''))



