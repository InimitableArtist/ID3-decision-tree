import csv

def read_data(filename):
    data = dict()
    with open(filename) as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        lineCount = 0
        for row in csvReader:
            if lineCount == 0:
                header = row
                lineCount +=1
                for i in range(len(header)):
                    data[header[i]] = []
            else:
                for i in range(len(header)):
                    data[header[i]].append(row[i])
                

    return data

def read_test_data(filename):
    data = list()
    with open(filename) as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        lineCount = 0
        for row in csvReader:
            row = row[:-1]
            if lineCount == 0:
                header = row
                lineCount += 1
            else:
                current = {}
                for i in range(len(header)):
                    current[header[i]] = row[i]
                data.append(current) 
    return data
            

def get_goals(data):
    goals = set(data[list(data.keys())[-1]])
    return goals

def get_attribute_values(data):
    attributeValues = {}
    attributeNames = list(data.keys())
    for i in attributeNames:
        attributeValues[i] = set(data[i])

    return attributeValues
