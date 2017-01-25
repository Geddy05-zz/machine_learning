class Cluster:
    points = []
    name = None

    def __init__(self,name):
        self.name = name
        self.points = []

    def addPoint(self,point):
        self.points.append(point)

    def clearPoints(self):
        self.points = []

