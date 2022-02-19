from datetime import date, timedelta

dayWeeks = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота','воскресенье']
dayWeeks_ind = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу','воскресенье']

def isNextWeek(day):
    return not day in dayWeeks[getToday():]

def isEvenWeek(day):
    date1 = date.today()
    if isNextWeek(day):
        return not date1.isocalendar()[1] % 2 == 0
    return date1.isocalendar()[1] % 2 == 0

def getToday():
    return date.today().weekday()

def getNextDay():
    date1 = date.today()
    date1 += timedelta(1)
    return date1.weekday()