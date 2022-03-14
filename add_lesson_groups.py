from sql import add_lesson_group, get_grouplist

list_groups = get_grouplist()

for i in list_groups:
    if len(i) == 5:
        add_lesson_group('Математический', i[2], i)
    elif len(i) == 8:
        add_lesson_group('Математический', i[2:6], i)