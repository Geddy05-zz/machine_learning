from naiveBayes import NaiveBayes
from dbscan.dbScan import DBScan
from myCsvParser import myCsvParser
from decisionTree.decisionTree import decisionTree
from imageclustering import Image_clustering
from dbscan.dbscannew import DBSCAN
from testdb import dbscan
import csv
import math

import random
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

py.sign_in('GeddySchellevis', 'VCYb9ulpyXeKtimPbOJD')

import numpy as np


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

    data = create_dataset("mushrooms.csv",ignoreColumn=[],hasHeader=True,removeHeader=True)

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

def read_data(path, label_column = None, ignore_columns = [] ):
    p = myCsvParser()
    data = p.getData(path,ignore_items=ignore_columns,is_set = True)
    dataset= set()
    import random
    #
    # random.shuffle(data)
    # self.data = self.data[:10000]
    return data


def plotClusters(clusters):
    traces = []
    for cluster in clusters:
        trace1 = go.Scatter3d(
            x=[row[0] for row in cluster.points],
            y=[row[1] for row in cluster.points],
            z=[row[2] for row in cluster.points],
            mode='markers',
            marker=dict(
                size=4,
                line=dict(
                    color=random_color(),
                    width=0.2
                ),
                opacity=0.8
            )
        )
        traces.append(trace1)

    # x2, y2, z2 = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
    # trace2 = go.Scatter3d(
    #     x=x2,
    #     y=y2,
    #     z=z2,
    #     mode='markers',
    #     marker=dict(
    #         color='rgb(127, 127, 127)',
    #         size=12,
    #         symbol='circle',
    #         line=dict(
    #             color='rgb(204, 204, 204)',
    #             width=1
    #         ),
    #         opacity=0.9
    #     )
    # )
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = go.Figure(data=traces, layout=layout)
    plot(fig)


def random_color():
    return 'rgba({0}, {1}, {2}, 0.14)'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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
        # db = DBScan("stars.csv",max_distance=0.08,min_points=100,ignoreColumns=[7,6,5,4,3])
        # # print db.data[1]
        # db.plot([])
        # db.clustering()
        # print ("")
        # print ("")
        #


        data = read_data("stars.csv" , ignore_columns =[7,6,5,4,3])

        db = DBSCAN(data=data,mu=10,epsilon=0.08)

        # db = DBSCAN(data=data,mu=80,epsilon=0.05)
        clusters = db.classify()
        plotClusters(clusters)
        # for value in db.clusters:
        #     print (" Cluster: %d" % value.name)
        #     for item in value.points:
        #         print(item)
        #     print("")
        #
        # print(clusters)

    elif data == 3:
        # p = myCsvParser()
        # dataset = p.getData("mushroom.csv")
        # for row in dataset:2
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