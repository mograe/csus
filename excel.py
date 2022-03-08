from csv import excel
from openpyxl import *
from sql import add_lesson

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
    symb = next_alpha(columnNumber)
    digital = 15
    print(symb+str(digital))
    while sheet[symb+str(digital)].value != None:
        group = sheet[symb+str(digital)].value
        print(group)
        digital += 1
        while digital < endOfTable:
            week = 0
            subgroup = 0
            if sheet[columnNumber+str(digital)].value != None:
                number = sheet[columnNumber+str(digital)].value
            if sheet[columnDays+str(digital)].value != None:
                day = str(sheet[columnDays+str(digital)].value).lower()
            for n, i in enumerate([symb,next_alpha(symb)]):
                if(sheet[i+str(digital)].value != None):
                    cell1 = str(sheet[i+str(digital)].value)
                    if(cell1.startswith("1Н.") or cell1.startswith("2Н.")):
                        week = int(cell1.strip()[0])
                        name = cell1.strip()[3:].strip()
                    else:
                        name = cell1.strip()
                    teacherAndClassroom = str(sheet[i+str(digital+1)].value)
                    if(isMerge(sheet[i+str(digital)],sheet)):
                        add_lesson(name, teacherAndClassroom, number, group, day, week, subgroup)
                        break
                    subgroup = n+1
                    add_lesson(name, teacherAndClassroom, number, group, day, week, subgroup)
            if(sheet[symb+str(digital)].value != None or sheet[next_alpha(symb)+str(digital)].value):
                digital+=1
            digital += 1      
        symb = next_alpha(next_alpha(symb))
        digital = 15

if __name__ == '__main__':
    wb = load_workbook(filename="math.xlsx")
    for sheet in wb:
        print(sheet.title)
        excel_to_db(sheet)