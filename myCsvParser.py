import csv

class myCsvParser:
    data = None

    def getData(self,filePath, ignore_items = None):
        f = open(filePath)
        self.data = csv.reader(f)
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

    def is_int(self,item):
        try:
            return int(item)
        except:
            try:
                return float(item)
            except:
                return item