import csv
import sys

with open(sys.argv[1], 'rt', encoding='UTF-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
