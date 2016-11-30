from myCsvParser import myCsvParser
import math


class NaiveBayes:
    data = None
    labelColumn = None
    rowLength = 0
    labelList = {}
    mean = {}
    standaardDeviatie = {}
    probLabel= {}

    def __init__(self,path=None, labelColumn=0):
        p = myCsvParser()
        self.data = p.getData(path)
        self.labelColumn = labelColumn

    def calculations(self):
        for row in self.data:
            self.rowLength = len(row)
            labelname = row[self.labelColumn]
            if self.labelList.has_key(labelname):
                self.labelList[labelname] += 1
            else:
                self.labelList[labelname] = 1
                self.standaardDeviatie[labelname] = {}
                self.mean[labelname] = {}

        for key, value in self.labelList.iteritems():
            n = float(value)
            self.probLabel[key] = (float(n/float(len(self.data))))
        self.calculate_with_numbers()

    def calculate_with_numbers(self):
        for i in range(0, self.rowLength):
            if i != self.labelColumn:
                totaal = {}
                for key, value in self.labelList.iteritems():
                    totaal[key] = 0
                    for row in self.data:
                        if key == row[self.labelColumn]:
                            totaal[row[self.labelColumn]] = (totaal[row[self.labelColumn]] + row[i])
                    self.mean[key][i] = totaal[key]/value

        for key, value in self.labelList.iteritems():
            for i in range(0, self.rowLength):
                if i != self.labelColumn:
                    sse = 0
                    for row in self.data:
                        if row[self.labelColumn] == key:
                            sse += pow(row[i] - self.mean[key][i], 2)
                    self.standaardDeviatie[key][i] = math.sqrt(sse / (value - 1))
        print(self.mean)
        print(self.standaardDeviatie)

    def predict(self,item):
        prediction = []
        for key,value in self.standaardDeviatie.iteritems():
            sqrt2pi = math.sqrt(2 * math.pi)
            probabilty = 0.5
            for k,v in value.iteritems():
                mean = self.mean[key][k]
                tempItem = item[k]
                part = math.pow(math.e, -(tempItem - mean) ** 2 / (2 * v ** 2))
                probabilty *= (1.0 / (sqrt2pi * v)) * part
            prediction.append((probabilty,key))
        return max(prediction)[1]