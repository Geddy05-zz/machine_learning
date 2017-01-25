import csv

class myCsvParser:
    data = None

    def getData(self,filePath, ignore_items = None, is_set = False):
        f = open(filePath)
        self.data = csv.reader(f)
        if is_set:
            return self.parseCsvSet(ignore_items = ignore_items)
        return self.parseCsv()

    def parseCsv(self):
        parsed_data = []
        for row in self.data:
            row_array = []

            for item in row:
                value = self.is_int(item)
                row_array.append(value)
            parsed_data.append(row_array)
        return parsed_data

    def parseCsvSet(self,ignore_items):
        parsed_data = []
        for row in self.data:
            row_array = []
            count = 0
            for item in row:
                if count not in ignore_items:
                    value = self.is_int(item)
                    row_array.append(value)
                count += 1
            row_array.append(0)
            row_array.append(0)

            parsed_data.append(row_array)
        return parsed_data[:20000]

    def is_int(self,item):
        try:
            return int(item)
        except:
            try:
                return float(item)
            except:
                return item