from csv import excel
from openpyxl import *
from sql import add_lesson, add_retake

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65)

def prev_alpha(s):
    if(ord(s.upper())-1 - 65 < 0 ):
        return 'Z'
    return chr((ord(s.upper())-1 - 65) % 26 + 65)

def isMerge(c, sheet):
    for mergedCell in sheet.merged_cells.ranges:
        if (c.coordinate in mergedCell):
            return True
    return False



#sheet = wb['МП 101,102, 103']


def excel_to_db(sheet):
    symb = 'A'
    digital = 15
    while sheet[symb+str(digital)].value == None:
        symb = next_alpha(symb)

    columnNumber = prev_alpha(symb)
    columnDays = prev_alpha(columnNumber)
    

    digital = 15
    while not str(sheet[columnDays+str(digital)].value).startswith("Декан"):
        digital += 1

    endOfTable = digital-3
    digital = 15
    print(symb+str(digital))
    while sheet[symb+str(digital)].value != None or isMerge(sheet[symb+str(digital)],sheet):
        symb = next_alpha(symb)
    max_symp = symb
    print(max_symp)
    symb = next_alpha(columnNumber)
    while sheet[symb+str(digital)].value != None:
        group = sheet[symb+str(digital)].value.replace(' ','')
        print(group)
        digital += 1
        while digital < endOfTable:
            week = 0
            subgroup = 0
            ns = 1
            if sheet[columnNumber+str(digital)].value != None:
                number = sheet[columnNumber+str(digital)].value
            if sheet[columnDays+str(digital)].value != None:
                day = str(sheet[columnDays+str(digital)].value).lower()
            list = [symb,next_alpha(symb)] if max_symp > 'H' else [symb]
            for n, i in enumerate(list):
                if(sheet[i+str(digital)].value != None and not str(sheet[i+str(digital)].value).startswith('+') and 
                not sheet[i+str(digital)].value in ['ДЕНЬ', 'САМОСТОЯТЕЛЬНЫХ', 'ЗАНЯТИЙ']):
                    cell1 = str(sheet[i+str(digital)].value)
                    print(cell1)
                    if(cell1.startswith("1Н.") or cell1.startswith("2Н.")):
                        week = int(cell1.strip()[0])
                        name = cell1.strip()[3:].strip()
                    else:
                        name = cell1.strip()
                    ns = 1
                    while sheet[i+str(digital+ns)].border.bottom.style == None and sheet[i+str(digital+ns+1)].value != None:
                        name += ' ' + str(sheet[i+str(digital+ns)].value)
                        ns += 1
                    teacherAndClassroom = str(sheet[i+str(digital+ns)].value)
                    ns += 1
                    if(isMerge(sheet[i+str(digital)],sheet) or max_symp <= 'H' ):
                        print(name, teacherAndClassroom, number, group, day, week, subgroup)
                        add_lesson(name, teacherAndClassroom, number, group, day, week, subgroup)
                        break
                    subgroup = n+1
                    add_lesson(name, teacherAndClassroom, number, group, day, week, subgroup)
            # if(sheet[symb+str(digital)].value != None or sheet[next_alpha(symb)+str(digital)].value):
            #     digital += 1
            digital += ns

            # while (sheet[symb+str(digital)].value == None and digital < endOfTable):
            #    print(symb+str(digital)) 
            #    digital += 1      
        symb = next_alpha(next_alpha(symb) if max_symp > 'H' else symb)
        digital = 15

def excel_retake_to_db(sheet):
    digital = 1
    while sheet['A'+str(digital)].value != None:
        print(sheet['A'+str(digital)].value)
        date = sheet['A'+str(digital)].value
        teacher = sheet['B'+str(digital)].value
        lesson = sheet['C'+str(digital)].value
        groups = sheet['D'+str(digital)].value.split(', ')
        begin_time = sheet['E'+str(digital)].value
        cabinet = sheet['F'+str(digital)].value
        for g in groups:
            add_retake(date,teacher,lesson,g.replace('-',''),begin_time,cabinet)
        digital += 1


def start_timetable():
    wb = load_workbook(filename="math.xlsx")
    for sheet in wb:
        print(sheet.title)
        excel_to_db(sheet)

def start_retake():
    wb = load_workbook(filename='retake.xlsx')
    for sheet in wb:
        excel_retake_to_db(sheet)

start_timetable()


