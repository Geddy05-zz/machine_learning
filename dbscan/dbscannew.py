from cluster import Cluster
import math
import sys
import math
from operator import add

VISITED = 3
ASSIGNED = 4

# def eucledian(current, y):
#     sum = 0.0
#     for index in range(0, len(current)):
#         sum += (current[index] - y[index]) ** 2
#     return math.sqrt(sum)

def eucledian(x,y):
    return math.sqrt(reduce(add,map(lambda z: (z[0] - z[1])**2 , zip(x, y))))

class DBSCAN():
    data = set()
    mu = 0
    epsilon = 0
    clusters = []
    data_length = 0
    count = 0

    def __init__(self,data,mu,epsilon):
        self.data = data
        self.mu = mu
        self.epsilon = epsilon
        self.clusters = []
        self.data_length = len(self.data)

    def classify(self):
        cluster_name = 0
        for i in range(len(self.data)):
            # check if point is already visited
            if self.data[i][VISITED] is 1:
                continue

            self.count += 1
            self.progress(False)
            self.data[i][VISITED] = 1
            neighbourhood = self.find_points_in_range(self.data[i])

            if len(neighbourhood) >= self.mu:
                cluster = Cluster(cluster_name)
                self.expand_cluster(cluster,neighbourhood)
                self.clusters.append(cluster)
                cluster_name += 1
                self.remove_assignd_points(cluster)
            else:
                self.data[i][VISITED] = 0
        return self.clusters

    def find_points_in_range(self,current_point):
        return filter(
            lambda x: eucledian(current_point[:-2],x[:-2]) <= self.epsilon if x[ASSIGNED] == 0 else False,
            self.data
        )

    def expand_cluster(self,cluster,neighbours):
        for point in neighbours:
            # if point is not already visited
            if point[VISITED] is 0:
                self.count += 1
                self.progress(True)

                point[VISITED] = 1
                neighbourhood = self.find_points_in_range(point)
                if len(neighbourhood) >= self.mu:
                    for p in neighbourhood:
                        if p not in neighbours:
                            neighbours.append(p)
            cluster.addPoint(point)

    def remove_assignd_points(self,cluster):
        for point in cluster.points:
            i = self.data.index(point)
            self.data[i][ASSIGNED]=1

    def progress(self,is_expanding):
        x = self.count
        y = self.data_length
        progress = float(x) / float(y)
        msg = "\r{0}%  {1} of {2} , clusters : {3}  is expand_cluster {4}"\
            .format(round((progress * 100),2),
                    x,
                    y,
                    len(self.clusters),is_expanding)

        sys.stdout.write(msg)
        sys.stdout.flush()

