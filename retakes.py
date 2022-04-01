import csv
from sql import add_retake

def retakes_to_db():
    with open('retakes.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for i in csv_file:
            print(i)

retakes_to_db()