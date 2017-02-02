from myCsvParser import myCsvParser
import math
from operator import itemgetter
import copy

class NaiveBayes:
    print_enable = True
    data = None
    labelColumn = None
    ignoreColumns = []
    rowLength = 0
    labelslist = {}
    mean = {}
    standaardDeviatie = {}
    probLabel = {}
    countData = {}
    stringColumns = []
    numberColumns = []

    def __init__(self,path=None, data = None ,labelColumn= 0, ignoreColumns = []):
        self.labelColumn = labelColumn
        if path is not None:
            p = myCsvParser()
            self.data = p.getData(path)
            self.labelColumn = labelColumn
            for row in self.data:
                for item in ignoreColumns:
                    row.pop(item)
        if data is not None:
            self.data = data

    def train(self):
        for row in self.data:
            self.rowLength = len(row)
            labelname = row[self.labelColumn]

            # prepare dicts
            if labelname in self.labelslist:
                self.labelslist[labelname] += 1.0
            else:
                self.labelslist[labelname] = 1.0
                self.standaardDeviatie[labelname] = {}
                self.mean[labelname] = {}
                self.countData[labelname] = {}

        count = 0
        for f in self.data[0]:
            #check if it is a discrete or continuous variable
            if type(f) is str:
                self.stringColumns.append(count)
            else:
                self.numberColumns.append(count)
            count += 1

        self.calculate_with_label()
        # self.calculate_with_numbers()

    # # continues variables
    # def calculate_with_numbers(self):
    #     for i in self.numberColumns:
    #         if i != self.labelColumn:
    #             totaal = {}
    #             for key, value in self.labelslist.iteritems():
    #                 totaal[key] = 0
    #                 for row in self.data:
    #                     if key == row[self.labelColumn]:
    #                         totaal[row[self.labelColumn]] = (totaal[row[self.labelColumn]] + row[i])
    #                 self.mean[key][i] = totaal[key]/value
    #
    #     for key, value in self.labelslist.iteritems():
    #         for i in self.numberColumns:
    #             if i != self.labelColumn:
    #                 sse = 0
    #                 for row in self.data:
    #                     if row[self.labelColumn] == key:
    #                         sse += pow(row[i] - self.mean[key][i], 2)
    #                 self.standaardDeviatie[key][i] = math.sqrt(sse / (value - 1))

        self.print_dict(title='Mean', dictt=self.mean)

        self.print_dict(title='ssd', dictt=self.standaardDeviatie)

    # labels
    def calculate_with_label(self):
        for columnNumber in self.stringColumns:
            for row in self.data:
                value = row[columnNumber]
                class_row = row[self.labelColumn]
                if columnNumber not in self.countData[class_row]:
                    self.countData[class_row][columnNumber] = {}

                #count nr. of occurrence in data set
                if value in self.countData[class_row][columnNumber]:
                    self.countData[class_row][columnNumber][value] += 1.0
                else:
                    self.countData[class_row][columnNumber][value] = 1.0

    def predict(self, items):
        results = []
        for item in items:
            prediction = []
            for key,value in self.labelslist.items():
                probabilty = math.log2(value/len(self.data))
                for i in range(0,len(item)-1):

                    if type(item[i]) is str and i is not self.labelColumn:
                        if item[i] in self.countData[key][i]:
                            probabilty += math.log2(float(self.countData[key][i][item[i]]) / value)
                        else:
                            probabilty += math.log2( float(1) / value+1)

                    # continues variables
                    # else:
                    #     tempItem = item[i]
                    #     train_column_number = i if i < self.labelColumn else i + 1
                    #
                    #     if train_column_number > len(self.mean[key]):
                    #         continue
                    #
                    #     mean = self.mean[key][train_column_number]
                    #     standaardDev = self.standaardDeviatie[key][train_column_number]
                    #     pro_density = self.pdf(mean,standaardDev,tempItem)
                    #     if pro_density > 0:
                    #         probabilty += math.log(pro_density)
                prediction.append((probabilty, key))
            prediction.sort(key=itemgetter(0))
            if self.print_enable: print (prediction)
            results.append(prediction[len(prediction)-1][1])

        return results

    # def baysianRatio(self,item,className ,column):
    #     r = 0
    #     if column < (len(item) -1):
    #         r = self.baysianRatio(item,className,(column +1))
    #
    #     if item[column] in self.countData[className][column]:
    #         r2 = math.log2(float(self.countData[className][column][item[column]]) /
    #                       self.countData[className][self.labelColumn][className])
    #
    #     else:
    #         r2 = math.log2(float(1) / self.countData[className][self.labelColumn][className]+1)
    #     return r+r2

    def pdf(self,mean, ssd, x):
        """Probability Density Function computing P(x|y)
        input is the mean, sample standard deviation for all the items in y,
        and x."""
        try:
            ePart = math.pow(math.e, -(x - mean) ** 2 / (2 * ssd ** 2))
            return (1.0 / (math.sqrt(2 * math.pi) * ssd)) * ePart
        except:
            return 0.0

    def print_dict(self, title="", dictt=None):
        if self.print_enable:
            print("------------ " + title + " ------------")
            for key, value in dictt.items():
                for k, v in value.items():
                    print(key, k, v)
            print("------------------------------")
            print('')