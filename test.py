import csv

# open white.csv
white = open('white.csv', 'r')

# read the file
white_reader = csv.reader(white)

for line in white_reader:
    print(line)
