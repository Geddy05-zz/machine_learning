from math import log
import operator
from node import Node

class decisionTree:
    dataset = []
    header = []
    class_column = 0

    entropyDict = {}
    entropyPerLabel = {}
    rootTree = None

    def __init__(self,dataset,class_column, hasHeader = True):
        self.dataset = dataset
        self.class_column = class_column
        if hasHeader:
            self.header = dataset[0]

    def entropy(self,dataset,column,perLabel = False, hasHeader=True):
        first = hasHeader
        self.entropyDict[column]={}
        totaalRecords = 0.0
        for row in dataset:

            if first:
                first = False
                continue

            totaalRecords += 1.0
            if row[column] not in self.entropyDict:
                label = row[column]
                count = 0.0
                for row in dataset:
                    if row[column] == label:
                        count += 1.0
                self.entropyDict[column][label] = count

        return self.calculate_entropy(self.entropyDict,column = column , totaal_items=totaalRecords, perLabel= perLabel)

    def calculate_entropy(self, dataset, column, totaal_items, perLabel = False):
        entropy = 0.0
        self.entropyPerLabel[column] = {}

        for key in dataset[column]:
            fergment = self.entropyDict[column][key]/totaal_items
            entropy -= (fergment * log(fergment,2))

        return entropy


    def information_gain(self, dataset, classColumn):
        entropy_classes = self.entropy(dataset=dataset,column= classColumn)
        temprow = dataset[0]

        temp_entropy = {}

        for i in range(0,len(temprow)-1):
            entropy_S = entropy_classes
            values_in_column = {}
            first = True
            for row in dataset:
                if first:
                    first = False
                    continue
                label = row[i]
                if label not in values_in_column:
                    values_in_column[label] = 1
                else:
                    values_in_column[label] +=1

            for item in values_in_column:
                tempdata = [ val for val in dataset if val[i] == item ]
                fragment = float(len(tempdata)) / float(len(dataset)-1)
                entropy = self.entropy(dataset=tempdata, column=classColumn, perLabel=True, hasHeader=False)
                entropy_S -= fragment*entropy

            temp_entropy[temprow[i]]= entropy_S
        return temp_entropy

    def get_all_values(self,name):
        index = self.header.index(name)
        values = []
        for row in self.dataset:
            if row[index] not in values:
                values.append(row[index])
        values.pop(0)
        return (values)

    def create_subset(self, dataset):



    def create_tree(self):
        information_gain = self.information_gain(self.dataset,self.class_column)
        highest = max(information_gain.iteritems(),key=operator.itemgetter(1))
        self.rootTree = Node(highest[0])
        print(self.get_all_values(highest[0]))
        print (self.dataset)


