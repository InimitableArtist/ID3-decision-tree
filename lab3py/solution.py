from data_reader import read_data, get_goals, get_attribute_values
from tree import Node
import math
import sys


class ID3:

    def __init__(self):
        self.filename = sys.argv[1]
        self.data = read_data(self.filename)
        self.header = self.data[0]
        self.realData = self.data[1]
        self.goals = get_goals(self.data[1])

        self.vrijednostiZnacajki = get_attribute_values(self.header, self.realData)

    #D - skup oznacenih primjera, X - skup svih znacajki, y - oznaka klase
    def fit(self, D, X, y):
        pass

    def predict(self, D):
        print('predict nigga hours....')

    
    def dataset_entropy(self):
        n = len(self.realData)
        dataFlatten = [item for sublist in self.realData for item in sublist]
        H = 0
        for goal in self.goals:
            H += - (dataFlatten.count(goal)/n) * math.log2(dataFlatten.count(goal)/n)
        
        return H

    def info_gain(self, data, znacajka, cilj):
        cijelaEntropija = self.dataset_entropy()

    def entropy(self, znacajka):
        H = 0
        for goal in self.goals:
            brojac = 0
            n = 0
            for line in self.realData:
                if znacajka in line:
                    n += 1
                    if goal in line:
                        brojac += 1
            if brojac == 0:
                H = 0
                return H
            else:
                H += -(brojac/n) * math.log2(brojac/n)
        return H




        

    def info_gain(self, attributeName, goals):

        entropija = self.dataset_entropy(data, goals)
            
            
def main():
    #filename = r'lab3_files[8]\datasets\volleyball.csv'
    
    a = ID3()
    datasetEntropija = a.dataset_entropy()
    #print(datasetEntropija)

    while True:
        entropija_vrijeme_suncano = a.entropy(input())

        print(entropija_vrijeme_suncano)

    
if __name__ == '__main__':
    main()