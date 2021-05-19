import csv

def read_data(filename):
    with open(filename) as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        lineCount = 0
        lines = []
        for row in csvReader:
            if lineCount == 0:
                header = row
                lineCount +=1
            else:
                lines.append(row)

    return [header, lines]

def get_goals(lines):
    goals = set([line[-1] for line in lines])
    return goals


