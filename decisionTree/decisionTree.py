from math import log
import operator
from node import Node,Leaf
from copy import deepcopy

class decisionTree:
    dataset = []
    header = []
    class_column = 0
    class_header_name =""

    entropyDict = {}
    entropyPerLabel = {}
    rootTree = None

    def __init__(self,dataset,class_column, hasHeader = True):
        self.dataset = dataset
        self.class_column = class_column
        if hasHeader:
            self.header = dataset[0]
            self.class_header_name = dataset[0][class_column]

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

    def expand_tree(self, node,chooses):
        for choos in chooses:
            print (choos)
            subset = self.create_subset(node.subset,node.name,choos)
            information_gain = self.information_gain(subset, subset[0].index(self.class_header_name))
            highest = max(information_gain.iteritems(), key=operator.itemgetter(1))

            index = subset[0].index(self.class_header_name)

            if highest[1] == 0.0:
                node_name = subset[1][index]
                leaf = Leaf(node_name)
                print("leaf")
                print(node.name)
                print (leaf.name)
                print(" == ")
                node.add_child(leaf)
            else:
                child_node = Node(highest[0] )
                child_node.subset = deepcopy(subset)
                print(child_node.name)
                node.add_child(child_node)
                new_chooses = self.get_unique_values(subset, label=highest[0])
                self.expand_tree(child_node,chooses=new_chooses)

            # node.add_child(Node())
        # note_one = Node("one")
        # note_two = Node("two")
        # root_node.add_child(note_one)
        # root_node.add_child(note_two)
        # print(root_node)

    def create_tree(self):
        information_gain = self.information_gain(self.dataset,self.class_column)
        highest = max(information_gain.iteritems(),key=operator.itemgetter(1))
        self.rootTree = Node(highest[0])
        self.rootTree.subset = deepcopy( self.dataset)
        chooses = self.get_unique_values(self.dataset,label=highest[0])
        print(self.rootTree.name)
        self.expand_tree(self.rootTree,chooses=chooses)


        # #TODO: extend tree
        # for choos in chooses:
        #     self.create_subset(self.dataset,highest[0],choos)
        #
        # print (self.dataset)

    def get_unique_values(self,dataset,label):
        header = dataset[0]
        index = header.index(label)
        unique_value = []
        for row in dataset:
            if row != header:
                if row[index] not in unique_value:
                    unique_value.append(row[index])
        return unique_value

    def create_subset(self,dataset,columnName,label):
        temp_set = deepcopy(dataset)
        subset = []
        header = temp_set[0]
        index = header.index(columnName)
        for row in temp_set:
            if row[index] == label:
                row.pop(index)
                subset.append(row)
            elif row[index] == columnName:
                row.pop(index)
                subset.append(row)
        return subset
