from myCsvParser import myCsvParser
import math


class NaiveBayes:
    print_enable = True
    data = None
    labelColumn = None
    ignoreColumns = []
    rowLength = 0
    labelList = {}
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

    def label_int(self):
        count_row = 0
        for row in self.data:
            count_collum = 0
            for item in row:
                if count_collum is self.labelColumn :
                    count_collum +=1
                    continue
                if item < 1:
                    self.data[count_row][count_collum] = "White"
                else:
                    self.data[count_row][count_collum] = "Inked"
                count_collum += 1
            count_row += 1

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
        column_key = 0
        for f in temprow:
            if count == self.labelColumn:
                count += 1
                continue
            if count in self.ignoreColumns:
                count += 1
                continue
            if type(f) is str:
                self.stringColumns.append(column_key)
            else:
                self.numberColumns.append(column_key)
            count += 1
            column_key += 1

        for key, value in self.labelList.iteritems():
            n = float(value)
            self.probLabel[key] = (float(n/float(len(self.data))))

        self.calculate_with_numbers()
        for key, value in self.labelList.iteritems():
            for i in self.stringColumns:
                self.calculate_with_label(i, class_name=key)
        print ("finished Training")

    # continues variables
    def calculate_with_numbers(self):
        for i in self.numberColumns:
            if i != self.labelColumn:
                totaal = {}
                for key, value in self.labelList.iteritems():
                    totaal[key] = 0
                    for row in self.data:
                        if key == row[self.labelColumn]:
                            totaal[row[self.labelColumn]] = (totaal[row[self.labelColumn]] + row[i])
                    self.mean[key][i] = totaal[key]/value

        for key, value in self.labelList.iteritems():
            for i in self.numberColumns:
                if i != self.labelColumn:
                    sse = 0
                    for row in self.data:
                        if row[self.labelColumn] == key:
                            sse += pow(row[i] - self.mean[key][i], 2)
                    self.standaardDeviatie[key][i] = math.sqrt(sse / (value - 1))

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

    def predict(self, items):
        results = []
        for item in items:
            prediction = []
            for key,value in self.labelList.iteritems():
                probabilty = self.probLabel[key]
                for i in range(0,len(item)-1):

                    # if value is a label
                    if type(item[i]) is str:
                        if item[i] in self.countData[key][i] :
                            probabilty += math.log(float(self.countData[key][i][item[i]]) /value)
                    else:
                        tempItem = item[i]
                        train_column_number = i if i < self.labelColumn else i + 1

                        if(train_column_number > len(self.mean[key])):
                            continue

                        mean = self.mean[key][train_column_number]
                        standaardDev = self.standaardDeviatie[key][train_column_number]
                        pro_density = self.pdf(mean,standaardDev,tempItem)
                        if pro_density > 0:
                            probabilty += math.log(self.pdf(mean,standaardDev,tempItem))
                prediction.append((probabilty, key))
            if self.print_enable: print (prediction)
            results.append(max(prediction)[1])
        return results

    # re-write it my self
    def pdf(self,mean, ssd, x):
        """Probability Density Function computing P(x|y)
        input is the mean, sample standard deviation for all the items in y,
        and x."""
        try:
            ePart = math.pow(math.e, -(x - mean) ** 2 / (2 * ssd ** 2))
            return (1.0 / (math.sqrt(2 * math.pi) * ssd)) * ePart
        except:
            return 0.0