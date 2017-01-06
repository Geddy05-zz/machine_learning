from math import log

class decisionTree:

    entropyDict = {}
    totaalRecords = 0.0

    def prepare_entropy(self,dataset,column):
        first = True
        for row in dataset:

            if first:
                first = False
                continue

            self.totaalRecords += 1.0
            if row[column] not in self.entropyDict:
                label = row[column]
                count = 0.0
                for row in dataset:
                    if row[column] == label:
                        count += 1.0
                self.entropyDict[label] = count

        self.calculate_entropy(self.entropyDict,self.totaalRecords)

    def calculate_entropy(self,dataset, totaal_items):
        entropy = 0.0
        for key in dataset:
            fergment = self.entropyDict[key]/totaal_items
            entropy -= (fergment * log(fergment,2))

        return entropy

