from cluster import Cluster
import math
import sys
from copy import deepcopy


def eucledian(x, y):
    sum = 0.0
    for index in range(0, len(x)-2):
        sum += (x[index] - y[index]) ** 2
    return math.sqrt(sum)


class DBSCAN():
    data = set()
    mu = 0
    epsilon = 0
    noise = None
    clusters = []
    data_length = 0
    count = 0

    def __init__(self,data,mu,epsilon):
        self.data = data
        self.mu = mu
        self.epsilon = epsilon
        self.noise = Cluster("noise")
        self.clusters = []
        self.data_length = len(self.data)

    def classify(self):
        cluster_name = 0
        for point in self.data:
            # check if point is already visited
            if point[3] is 1:
                continue

            self.count += 1
            self.progress()
            point[3] = 1
            neighbourhood = self.find_points_in_range(point)

            if len(neighbourhood) >= self.mu:
                cluster = Cluster(cluster_name)
                self.expand_cluster(cluster,neighbourhood)
                self.clusters.append(cluster)
                cluster_name += 1
                self.remove_assignd_points(cluster)
            else:
                point[3] = 0
        return self.clusters

    def find_points_in_range(self,current_point):
        point_in_range = []
        for point in self.data:
            if point[4] == 0:
                if eucledian(current_point,point) <= self.epsilon:
                    point_in_range.append(point)
        return point_in_range

    def expand_cluster(self,cluster,neighbours):
        for point in neighbours:
            # if point is not already visited
            if point[3] is 0:
                self.count += 1
                self.progress()

                point[3] = 1
                neighbourhood = self.find_points_in_range(point)
                if len(neighbourhood) >= self.mu:
                    for p in neighbourhood:
                        if p not in neighbours:
                            neighbours.append(p)
            cluster.addPoint(point)

    def remove_assignd_points(self,cluster):
        for point in cluster.points:
            i = self.data.index(point)
            self.data[i][4]=1

    def progress(self):
        x = self.count
        y = self.data_length
        progress = float(x) / float(y)
        msg = "\r{0}%  {1} of {2} , clusters : {3}".format(round((progress * 100),2),x, y,len(self.clusters))

        sys.stdout.write(msg)
        sys.stdout.flush()

