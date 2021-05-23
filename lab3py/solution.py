from data_reader import read_data, get_goals, get_attribute_values, read_test_data
import math
from pprint import pprint
import sys

class ID3:

    def __init__(self, dubina = None):
        self.dubina = dubina
        if self.dubina != None:
            self.dubina = int(dubina)
        
        self.filename = sys.argv[1]
        self.filenameTrain = sys.argv[2]
        self.data = read_data(self.filename)
        self.testData = read_test_data(self.filenameTrain)
        self.testGoals = list(read_data(self.filenameTrain).values())[-1]
        self.goals = get_goals(self.data)
        self.goalName = list(self.data.keys())[-1]
        self.vrijednostiZnacajki = get_attribute_values(self.data)
        znacajke = list(self.data.keys())[:-1]
        stablo = self.fit(self.data, self.data, znacajke, self.goalName)
        branches = list(self.get_branches(stablo))
        self.print_branches(branches)
        self.predicted = self.test(self.testData, stablo)
        self.matrica_zabune()

        
    def uniq(self, lista):
        new = []
        ponavljanja = []
        for i in lista:
            if i not in new:
                new.append(i)
        for n in sorted(new):
            ponavljanja.append(lista.count(n))
        return [new, ponavljanja]
        
        
    def max_index(self, lista):
        _max = max(lista)
        _maxIndex = lista.index(_max)
        return _maxIndex

    def fit(self, data, originalData, znacajke, imeCilja, parentNode = None, depth = 0):

        if len(self.uniq((data[imeCilja]))[0]) <= 1:
            return list(set(data[imeCilja]))[0]
            
        elif len(data) == 0:
            return self.uniq(originalData[imeCilja])[self.max_index(self.uniq(originalData[imeCilja])[1])]

        elif len(znacajke) == 0:
            return parentNode

        else:
            b = sorted(self.uniq(originalData[imeCilja])[0])
            parentNode = b[self.max_index(self.uniq(data[imeCilja])[1])]
            
            itemValues = [self.info_gain(data, znacajka) for znacajka in znacajke]

            pom = {}
            for k in range(len(itemValues)):
                print('IG(%s)=%.4f' % (znacajke[k], itemValues[k]), end = ' ')
                pom[znacajke[k]] = itemValues[k]

            
            print()
            zn = sorted(pom.items(), key = lambda x: (-x[1], x[0]))

            maxZnacajka = zn[0][0]

            stablo = {maxZnacajka : {}}

            znacajke = [i for i in znacajke if i != maxZnacajka]

            for j in self.uniq(data[maxZnacajka])[0]:
                subData = self.get_sub_tree(data, maxZnacajka, j)

                
                subTree = self.fit(subData, originalData, znacajke, self.goalName, parentNode, depth + 1)
                stablo[maxZnacajka][j] = subTree

            if depth == self.dubina:
                return parentNode

            return stablo

    def get_sub_tree(self, data, node, v):

        indeksi = []
        nData = {}
        for key, vals in data.items():
            if (key == node):
                for i in range(len(vals)):
                    if (vals[i] == v):
                        indeksi.append(i)
        
        for znacajka in data.keys():
            if (znacajka != node):
                nData[znacajka] = []

        for key, vals in data.items():
            if (key != node):
                for i in range(len(vals)):
                    if i in indeksi:
                        nData[key].append(vals[i])

        return nData

    def find_default(self, lista):
        brojac = 0
        lista = sorted(lista)
        element = lista[0]

        for i in lista:
            fr = lista.count(i)
            if (fr > brojac):
                brojac = fr
                element = i
        
        
        return element

    def predict(self, testData, stablo):
        for key in list(testData.keys()):
            if key in list(stablo.keys()):
                try:
                    result = stablo[key][testData[key]]
                except Exception as e:
                    default = self.find_default(self.data[self.goalName])

                    return default

                result = stablo[key][testData[key]]

                if isinstance(result, dict):
                    return self.predict(testData, result)
                else:
                    return result

    def test(self, allTestData, stablo):
        predicted = [self.predict(testData, stablo) for testData in allTestData]

        print('[PREDICTIONS]: ', end = '')
        correct = 0
    
        for i in range(len(predicted)):
            print(predicted[i], end = ' ')
            if predicted[i] == self.testGoals[i]:
                correct += 1

        print()
        print('[ACCURACY]: ', end = '')
        n = len(self.testGoals)
        print('{:.5f}'.format(round(correct / n, 5)))
        return predicted

    def matrica_zabune(self):


        matrica = {}
        for goal in self.goals:
            matrica[goal] = {}
            for g in self.goals:
                matrica[goal][g] = 0

        
        for i in range(len(self.testGoals)):
            stvarKlasa = self.testGoals[i]
            predKlasa = self.predicted[i]
            matrica[stvarKlasa][predKlasa] += 1

        print('[CONFUSION_MATRIX]: ')

        stvarneKlase = sorted(list(matrica.keys()))
        for klasa in stvarneKlase:
            redak = sorted(list(matrica[klasa].keys()))
            for g in redak:
                print(matrica[klasa][g], end = ' ')
            print()
    
    def dataset_entropy(self, data):
        n = len(list(data.values())[0])
        dataGoals = list(data.values())[-1]
        H = 0
        for goal in self.goals:   
            H += - (dataGoals.count(goal)/n) * math.log2(dataGoals.count(goal)/n)
        
        return H

    def info_gain(self, data, znacajka):
        
        n = len(list(data.values())[0])
        cijelaEntropija = self.dataset_entropy(data)
        vrijednostiZnacajke = self.vrijednostiZnacajki[znacajka]

        wEntropija = 0
        col = data[znacajka]
        for vrijednost in vrijednostiZnacajke:
            trenutna = 0
            wEntropija += -(col.count(vrijednost)/n * self.entropy(data, vrijednost, znacajka))

        infoGain = cijelaEntropija + wEntropija
        return infoGain

    def entropy(self, data, vrijednostZnacajke, znacajka):
        H = 0
        sveVrijednosti = data[znacajka]
        for goal in self.goals:
            brojac = 0
            n = 0
            for i in range(len(sveVrijednosti)):
                if vrijednostZnacajke == sveVrijednosti[i]:
                    n += 1
                    goalName = list(data.keys())[-1]
                    trenutniGoal = data[goalName][i]
                    if goal == trenutniGoal:
                        brojac += 1
            if brojac == 0:
                H = 0
                return H
            else:
                H += -(brojac/n) * math.log2(brojac/n)
        
        return H

    def get_branches(self, stablo, l = []):
        for a, b in stablo.items():
            yield from ([l+[a, b]] if not isinstance(b, dict) else self.get_branches(b, l+[a]))

    def print_branches(self, branches):
        print('[BRANCHES]:')
        for branch in branches:
            index = 1
            for i in range(len(branch)):
                if branch[i] in self.data.keys():
                    print(str(index) + ':', end = '')
                    print(branch[i] + '=', end = '')
                    index += 1
                else:
                    print(branch[i], end = ' ')
            print()
     
def main():
    
    if len(sys.argv) == 4:
        a = ID3(sys.argv[3])
    else:
        a = ID3()

if __name__ == '__main__':
    main()