from naiveBayes import NaiveBayes
from dbScan import DBScan
from myCsvParser import myCsvParser
import math
class Train_data:
    data = None
    dataLabels = []

    def __init__(self,path,labelColumn):
        p = myCsvParser()
        self.data = p.getData(path)
        for row in self.data:
            self.dataLabels.append(row[labelColumn])
            row.pop(labelColumn)

def naiveBayes(training , test):
    naiveBayes = NaiveBayes(training, 4, [0])
    # naiveBayes.print_enable = True
    naiveBayes.train()

    t = Train_data(test,4)

    return naiveBayes.predict(t.data), t


def accuracy(prediction,train_data):
    print(prediction)

    correct = 0.0
    for i in range(0,len(prediction)):
        if train_data.dataLabels[i] == prediction[i]:
            correct += 1

    print (correct / len(prediction))

if __name__ == "__main__":

    print( "Select a algorithm")
    print ("1: Naive Bayes")
    print ("2: DBScan")

    data = input("Enter a number: ")

    if data == 1:
        nb = naiveBayes("Iris.csv","train_iris.csv")
        accuracy(nb[0],nb[1])
    elif data == 2:
        db = DBScan("dbscan.csv",2)
        db.clustering(3)
        print(db.clusters)
    else:
        print("wrong number")