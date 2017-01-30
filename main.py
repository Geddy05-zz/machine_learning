from naiveBayes.naiveBayes import NaiveBayes
from dataReader import dataReader
from train_data import Train_data
from plot_star_clusters import plot_star_clusters

from dbscan.dbScan import DBScan
from decisionTree.decisionTree import decisionTree
from imageclustering import Image_clustering
from dbscan.dbscannew import DBSCAN
import csv

def naive_bayes():
    label_column = 0
    ignore_list = []

    data = dataReader.create_dataset("datasets/mushrooms.csv",ignoreColumn=[],hasHeader=True,removeHeader=True)

    naiveBayes = NaiveBayes(data=data[0], labelColumn=label_column, ignoreColumns=ignore_list)
    naiveBayes.print_enable = True
    naiveBayes.train()

    t = Train_data(data=data[1],labelColumn=0)

    return naiveBayes.predict(t.data), t

def accuracy(prediction,train_data):
    print(train_data.dataLabels)
    correct = 0.0
    for i in range(0,len(prediction)-1):
        if train_data.dataLabels[i] == prediction[i]:
            correct += 1
    print(correct)
    print(len(prediction))
    print (correct / (len(prediction)-1))

def write_to_csv(result):
    # first write column headers
    csvWriter = csv.writer(open("test_out.csv", 'w'), delimiter=',', quotechar=' ',
                           quoting=csv.QUOTE_NONE)
    csvWriter.writerow(["ImageId","Label"])

    count = 1
    for data in result:
        csvWriter.writerow([count , data])
        count += 11

if __name__ == "__main__":

    print( "Select a algorithm")
    print ("1: Naive Bayes")
    print ("2: DBScan")
    print ("3: DecisionTree")
    print ("4: image clustering (Work in Progress)")

    data = 1

    if data == 1:
        nb = naive_bayes()
        predict = nb[0]
        print(predict)

        accuracy(nb[0],nb[1])

    elif data == 2:

        data = dataReader.read_data("datasets/stars.csv" , ignore_columns =[7,6,5,4,3])

        db = DBSCAN(data=data,mu=10,epsilon=0.05)

        clusters = db.classify()

        pl = plot_star_clusters()
        pl.plot_clusters(clusters)

        with open("Output.txt", "w") as text_file:
            for value in db.clusters:
                text_file.write("\n\nCluster Name: {}".format(value.name))
                for item in value.points:
                    text_file.write("\n\t%s" % item)

    elif data == 3:
        dataset = dataReader.create_dataset("datasets/mushrooms.csv",ignoreColumn=[],hasHeader=True)

        dt = decisionTree(dataset=dataset[0],
                          class_column=0,
                          hasHeader=True)

        dt.create_tree()
        train = Train_data(data=dataset[1],labelColumn=0)
        result = dt.start_classification(dataset[1])
        print(result)
        accuracy(result,train)

    else:
        Image_clustering().get_image()
        print("wrong number")