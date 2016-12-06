from myCsvParser import myCsvParser
import math


class NaiveBayes:
    print_enable = True
    data = None
    labelColumn = None
    rowLength = 0
    labelList = {}
    mean = {}
    standaardDeviatie = {}
    probLabel = {}
    countData = {}
    stringColumns = []
    numberColumns = []

    def __init__(self,path=None, labelColumn=0):
        p = myCsvParser()
        self.data = p.getData(path)
        self.labelColumn = labelColumn

    def train(self):
        temprow = None
        for row in self.data:
            if not temprow:
                temprow = row
            self.rowLength = len(row)
            labelname = row[self.labelColumn]
            if self.labelList.has_key(labelname):
                self.labelList[labelname] += 1
            else:
                self.labelList[labelname] = 1
                self.standaardDeviatie[labelname] = {}
                self.mean[labelname] = {}
                self.countData[labelname] = {}
        count = 0
        for f in temprow:
            if count == self.labelColumn:
                continue
            if type(f) is str:
                self.stringColumns.append(count)
            else:
                self.numberColumns.append(count)
            count += 1

        for key, value in self.labelList.iteritems():
            n = float(value)
            self.probLabel[key] = (float(n/float(len(self.data))))
        self.calculate_with_numbers()

    def calculations(self):
        # TODO: write decision algorithm for pro numbers and labels
        return None

    # continues variables
    def calculate_with_numbers(self):
        for i in range(0, self.rowLength):
            if i != self.labelColumn and i in self.numberColumns:
                totaal = {}
                for key, value in self.labelList.iteritems():
                    totaal[key] = 0
                    for row in self.data:
                        if key == row[self.labelColumn]:
                            totaal[row[self.labelColumn]] = (totaal[row[self.labelColumn]] + row[i])
                    self.mean[key][i] = totaal[key]/value

        for key, value in self.labelList.iteritems():
            for i in range(0, self.rowLength):
                if i != self.labelColumn and i in self.numberColumns:
                    sse = 0
                    for row in self.data:
                        if row[self.labelColumn] == key:
                            sse += pow(row[i] - self.mean[key][i], 2)
                    self.standaardDeviatie[key][i] = math.sqrt(sse / (value - 1))
                elif i in self.stringColumns:
                    self.calculate_with_label(i, class_name= key)

        self.print_dict(title='Mean', dictt=self.mean)

        self.print_dict(title='ssd', dictt=self.standaardDeviatie)

    # labels
    def calculate_with_label(self, columnNumber, class_name= ''):
        self.countData[class_name][columnNumber] = {}
        for row in self.data:
            value = row[columnNumber]
            class_row = row[self.labelColumn]
            if class_row != class_name:
                continue

            if value in self.countData[class_name][columnNumber]:
                self.countData[class_name][columnNumber][value] += 1
            else:
                self.countData[class_name][columnNumber][value] = 1

    def print_dict(self, title="", dictt=None):
        if self.print_enable:
            print "------------ " + title + " ------------"
            for key, value in dictt.iteritems():
                for k, v in value.iteritems():
                    print key, k, v
            print "------------------------------"
            print ''

    def predict(self, item):
        prediction = []
        for key,value in self.labelList.iteritems():
            probabilty = self.probLabel[key]
            for i in range(0,len(item)):

                # if value is a label
                if type(item[i]) is str:
                    probabilty += math.log(float(self.countData[key][i][item[i]]) /value)
                else:
                    mean = self.mean[key][i]
                    standaardDev = self.standaardDeviatie[key][i]
                    tempItem = item[i]
                    probabilty += math.log(self.pdf(mean,standaardDev,tempItem))
            prediction.append((probabilty, key))
        return max(prediction)[1]

    # re-write it my self
    def pdf(self,mean, ssd, x):
        """Probability Density Function computing P(x|y)
        input is the mean, sample standard deviation for all the items in y,
        and x."""
        ePart = math.pow(math.e, -(x - mean) ** 2 / (2 * ssd ** 2))
        return (1.0 / (math.sqrt(2 * math.pi) * ssd)) * ePart