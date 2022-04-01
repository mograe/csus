from datetime import date, timedelta, datetime

dayWeeks = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота','воскресенье']
dayWeeks_ind = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу','воскресенье']
time_lessons = ['8:00 - 9:30','9:40 - 11:10','11:20 - 12:50','13:15 - 14:45','15:00 - 16:30','16:40 - 18:10','18:20 - 19:50','19:55 - 21:25']

def isNextWeek(day):
    return not day in dayWeeks[getToday():]

def days_left(data):
    return (datetime.strptime(data,'%Y-%m-%d %H:%M:%S').date() - date.today()).days

def isEvenWeek(day):
    date1 = date.today()
    if isNextWeek(day):
        return not date1.isocalendar()[1] % 2 == 0
    return date1.isocalendar()[1] % 2 == 0

def getToday():
    return date.today().weekday()

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

def getNextDay():
    date1 = date.today()
    date1 += timedelta(1)
    return date1.weekday()

def add_begin_zero(number):
    if number // 10 == 0:
        return '0' + str(number)
    return str(number)

def next_weekday(weekday):
    d = date.today()
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)
