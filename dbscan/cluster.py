class Cluster:
    points = []
    name = None

    def __init__(self,name):
        self.name = name

    def addPoint(self,point):
        self.points.append(point)

    def clearPoints(self):
        self.points = []

