from myCsvParser import myCsvParser
from cluster import Cluster
import math

class DBScan:
    data = None
    labelColumn = None
    max_distance = 0
    visited = []
    noise = []
    clusters = []

    def __init__(self,path,max_distance,labelColumn= None):
        self.max_distance =max_distance
        p = myCsvParser()
        self.data = p.getData(path)
        for row in self.data:
            if labelColumn:
                self.dataLabels.append(row[labelColumn])
                row.pop(labelColumn)

    def clustering(self,min_points):
        cluster_name = 0
        cluster = Cluster(cluster_name)
        for point in self.data:
            if point not in self.visited:
                self.visited.append(point)
                neighbourhood = self.find_points_in_range(point)
                if len(neighbourhood) < min_points:
                    self.noise.append(point)
                else:
                    cluster.addPoint(point)
                    self.clusters.append(self.cluster_expansion(neighbourhood,cluster))
                    cluster_name += 1
                    cluster = Cluster(cluster_name)
                    cluster.clearPoints()

    def cluster_expansion(self,neighbourhood,cluster):
        for point in neighbourhood:
            if point not in self.visited:
                self.visited.append(point)
                for p in self.find_points_in_range(point):
                    if p not in neighbourhood:
                        neighbourhood.append(p)
                cluster.addPoint(point)
        return cluster

    def find_points_in_range(self,current_point):
        points_in_range = []
        for point in self.data:
            if point not in self.visited:
                if self.eucledian(current_point,point) < self.max_distance:
                    points_in_range.append(point)
        return points_in_range

    def eucledian(self , x , y):
        sum = 0.0;
        for index in range(0,len(x)):
            sum += (x[index] - y[index]) **2
        return math.sqrt(sum)