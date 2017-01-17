from naiveBayes import NaiveBayes
from dbscan.dbScan import DBScan
from myCsvParser import myCsvParser
from decisionTree.decisionTree import decisionTree
from imageclustering import Image_clustering

import csv
import math


class Train_data:
    data = None
    dataLabels = []
    labelColumn = None

    def __init__(self,path=None,data=None,labelColumn=[]):
        self.labelColumn = labelColumn
        p = myCsvParser()
        if path:
            self.data = p.getData(path)
        elif data:
            self.data = data
        for row in self.data:
            self.dataLabels.append(row[labelColumn])
            # row.pop(labelColumn)

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

def create_dataset(path, ignoreColumn=[],hasHeader = False,removeHeader = False):
    p = myCsvParser()
    data = p.getData(path)
    tempHeader = data[0] if hasHeader and not removeHeader else None

    if hasHeader:
        data.pop(0)
    for row in data:
        for item in ignoreColumn:
            row.pop(item)

    import random
    random.shuffle(data)
    length = len(data)
    train_length = int(round(length * 0.6))
    test_length = length - train_length
    train_data = data[:train_length]
    test_data = data[test_length:]

    if hasHeader and not removeHeader:
        train_data.insert(0,tempHeader)

    return (train_data , test_data)

def naiveBayes(training , test):
    label_column = 0
    ignore_list = []

    data = create_dataset("mushrooms.csv",ignoreColumn=[],hasHeader=True)

    print("Start labeling Training Data")
    naiveBayes = NaiveBayes(data=data[0], labelColumn=label_column, ignoreColumns=ignore_list)
    # naiveBayes.label_int();
    print("Start training")
    naiveBayes.print_enable = True
    naiveBayes.train()

    print("Start labeling Test Data")
    print (data[1])
    t = Train_data(data=data[1],labelColumn=0)
    # t.label_int()

    print("start classifying")
    return naiveBayes.predict(t.data), t

def accuracy(prediction,train_data):
    print len(prediction)
    print len(train_data.dataLabels)
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
        accuracy(nb[0],nb[1])

    elif data == 2:
        db = DBScan("dbscan.csv",1.5)
        db.clustering(min_points=3)

        for value in db.clusters:
            print (" Cluster: %d" % value.name)
            for item in value.points:
                print(item)
            print("")

    elif data == 3:
        # p = myCsvParser()
        # dataset = p.getData("mushroom.csv")
        # for row in dataset:
        #     row.pop(0)

        dataset = create_dataset("mushrooms.csv",ignoreColumn=[],hasHeader=True)

        # dt = decisionTree(dataset=dataset[0],
        #                   class_column= 0,
        #                   hasHeader=True)

        dt = decisionTree(dataset=dataset[0],
                          class_column=0,
                          hasHeader=True)


        dt.create_tree()
        print("-------------------")
        train = Train_data(data=dataset[1],labelColumn=0)

        result = dt.start_classification(dataset[1])
        print( "training labels")
        print train.dataLabels
        print result
        accuracy(result,train)

    else:
        Image_clustering().get_image()
        print("wrong number")