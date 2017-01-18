from myCsvParser import myCsvParser
from cluster import Cluster
import math
import time, sys

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot


py.sign_in('GeddySchellevis', 'VCYb9ulpyXeKtimPbOJD')

import numpy as np

class DBScan:
    data = None
    labelColumn = None
    max_distance = 0.0
    visited = []
    noise = []
    clusters = []

    def update_progress(self, length,value):
        progress = float(value)/float(length)
        length = 50  # modify this to change the length
        block = int(round(length * progress))
        msg = "\r{0}: [{1}] {2}%".format("DBSCAN", "#" * block + "-" * (length - block), round(progress * 100, 4))
        if progress >= 1: msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()

    def __init__(self,path,max_distance,labelColumn= None,ignoreColumns=[]):
        self.max_distance =max_distance
        p = myCsvParser()
        self.data = p.getData(path)

        for row in self.data:
            if labelColumn:
                row.pop(labelColumn)
            for item in ignoreColumns:
                    row.pop(item)

    def clustering(self,min_points):
        cluster_name = 0
        total_data = len(self.data)
        cluster = Cluster(cluster_name)
        for point in self.data:
            if point not in self.visited:
                self.update_progress(total_data, len(self.visited))
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
            # self.update_progress(len(self.data),len(self.visited))
            # if point not in self.visited:
            self.visited.append(point)
            for p in self.find_points_in_range(point):
                if p not in neighbourhood:
                    neighbourhood.append(p)
            cluster.addPoint(point)
        return cluster

    def find_points_in_range(self,current_point):
        points_in_range = []
        for point in self.data:
            self.update_progress(len(self.data), len(self.visited))
            if point not in self.visited:
                if self.eucledian(current_point,point) < self.max_distance:
                    points_in_range.append(point)
        return points_in_range

    def eucledian(self , x , y):
        sum = 0.0;
        for index in range(0,len(x)):
            sum += (x[index] - y[index]) **2
        print math.sqrt(sum)
        return math.sqrt(sum)

    def randrange(self,n, vmin, vmax):
        '''
        Helper function to make an array of random numbers having shape (n, )
        with each number distributed Uniform(vmin, vmax).
        '''
        return (vmax - vmin) * np.random.rand(n) + vmin

    def plot(self,data):

        x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        trace1 = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=12,
                line=dict(
                    color='rgba(217, 217, 217, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )

        x2, y2, z2 = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        trace2 = go.Scatter3d(
            x=x2,
            y=y2,
            z=z2,
            mode='markers',
            marker=dict(
                color='rgb(127, 127, 127)',
                size=12,
                symbol='circle',
                line=dict(
                    color='rgb(204, 204, 204)',
                    width=1
                ),
                opacity=0.9
            )
        )
        data = [trace1, trace2]
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        plot(fig)
