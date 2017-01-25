from myCsvParser import myCsvParser


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