
import csv

def readcsv(filename):
    matrix = []
    with open(filename, newline='') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            matrix.append(row)
    return matrix

