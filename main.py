from naiveBayes import NaiveBayes
from dbscan.dbScan import DBScan
from myCsvParser import myCsvParser
from decisionTree.decisionTree import decisionTree
from fractions import Fraction

import csv
import math


class Train_data:
    data = None
    dataLabels = []
    labelColumn = None

    def __init__(self,path,labelColumn):
        self.labelColumn = labelColumn
        p = myCsvParser()
        self.data = p.getData(path)
        for row in self.data:
            self.dataLabels.append(row[labelColumn])
            row.pop(labelColumn)

    def label_int(self):
        count_row = 0
        for row in self.data:
            count_collum = 0
            for item in row:
                if item < 1:
                    self.data[count_row][count_collum] = "White"
                else:
                    self.data[count_row][count_collum] = "Inked"
                count_collum += 1
            count_row += 1

def naiveBayes(training , test):
    label_column = 4
    ignore_list = [0]

    print("Start labeling Training Data")
    naiveBayes = NaiveBayes(training, labelColumn=label_column, ignoreColumns=ignore_list)
    # naiveBayes.label_int();
    print("Start training")
    naiveBayes.print_enable = True
    naiveBayes.train()

    print("Start labeling Test Data")
    t = Train_data(test,4)
    # t.label_int()

    print("start classifying")
    return naiveBayes.predict(t.data), t

def accuracy(prediction,train_data):
    print(prediction)

    correct = 0.0
    for i in range(0,len(prediction)):
        if train_data.dataLabels[i] == prediction[i]:
            correct += 1

    print (correct / len(prediction))

def write_to_csv(result):
    # first write column headers
    csvWriter = csv.writer(open("test_out.csv", 'w'), delimiter=',', quotechar=' ',
                           quoting=csv.QUOTE_NONE)
    csvWriter.writerow(["ImageId","Label"])

    count = 1
    for data in result:
        csvWriter.writerow([count , data])
        count += 1

                       # now data, assuming each column has the same # of values
    # for key, value in result.iteritems():
        # csvWriter.writerow([key,value])

if __name__ == "__main__":

    print( "Select a algorithm")
    print ("1: Naive Bayes")
    print ("2: DBScan")
    print ("3: DecisionTree")

    data = input("Enter a number: ")

    if data == 1:
        nb = naiveBayes("iris.csv","train_iris.csv",)
        predict = nb[0]
        print(predict)

        # write_to_csv(predict)
        # accuracy(nb[0],nb[1])

    elif data == 2:
        db = DBScan("dbscan.csv",100)
        db.clustering(min_points=0)

        for value in db.clusters:
            print (" Cluster: %d" % value.name)
            for item in value.points:
                print(item)
            print("")

    elif data == 3:
        p = myCsvParser()
        dataset = p.getData("sunny.csv")
        for row in dataset:
            row.pop(0)

        dt = decisionTree(dataset=dataset,
                          class_column= 4,
                          hasHeader=True)

        print(dt.information_gain(dataset, 4))
        dt.create_tree()
        dt.create_subset(None)

        # print(dt.prepare_entropy(dataset,4))

        print(0.940 - ((8.0/14.0)*  0.811) - ((6.0/14.0) * 1.0))
    else:
        print("wrong number")