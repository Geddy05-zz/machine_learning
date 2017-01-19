from myCsvParser import myCsvParser
from cluster import Cluster
import math
import time, sys

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

py.sign_in('GeddySchellevis', 'VCYb9ulpyXeKtimPbOJD')

import numpy as np


def eucledian(x, y):
    sum = [(a - b) ** 2 for a, b in zip(x, y)]
    return math.sqrt(sum)


class DBScan:
    data = None
    labelColumn = None
    max_distance = 0.0
    visited = []
    noise = []
    clusters = []
    data_length = []
    points_assigned = []
    count = 0;

    def update_progress(self, length, value):
        progress = float(value) / float(length)
        length = 50  # modify this to change the length
        block = int(round(length * progress))
        msg = "\r{0}: [{1}] {2}% , visites: {3} noise: {4} amount of clusters: {5}".format("DBSCAN",
                                                                                           "#" * block + "-" * (
                                                                                           length - block),
                                                                                           round(progress * 100, 4),
                                                                                           value, len(self.noise),
                                                                                           len(self.clusters))
        if progress >= 1: msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()

    def __init__(self, path, max_distance, min_points, labelColumn=None, ignoreColumns=[]):
        self.max_distance = max_distance
        self.min_points = min_points
        self.count = 0
        self.points_assigned = []
        p = myCsvParser()
        self.data = p.getData(path)
        import random
        #
        # random.shuffle(data)
        # self.data = self.data[:10000]
        for row in self.data:
            if labelColumn:
                row.pop(labelColumn)
            for item in ignoreColumns:
                row.pop(item)

    def clustering(self):
        cluster_name = 0
        cluster = Cluster(cluster_name)
        self.data_length = len(self.data) - 1
        print self.data_length

        while self.count < self.data_length:
            point = self.data[self.count]
            self.count += 1
            if point in self.visited:
                continue

            self.update_progress(self.data_length, len(self.visited))
            self.visited.append(point)
            neighbourhood = self.find_points_in_range(point)
            if len(neighbourhood) < self.min_points:
                self.noise.append(point)
            else:
                cluster.addPoint(point)
                self.clusters.append(self.cluster_expansion(neighbourhood, cluster))
                print(cluster_name)
                cluster_name += 1
                cluster = Cluster(cluster_name)
                cluster.clearPoints()

    def removePoints(self, cluster):
        for point in cluster.points:
            # i = self.data.index(point)
            self.points_assigned.append(point)

    def cluster_expansion(self, neighbourhood, cluster):
        for point in neighbourhood:
            if point not in self.visited or point in self.noise:
                self.update_progress(self.data_length, len(self.visited))

                self.visited.append(point)
                temp_neighbours = self.find_points_in_range(point)
                if temp_neighbours >= self.min_points:
                    for p in temp_neighbours:
                        if p not in neighbourhood and p not in self.points_assigned:
                            neighbourhood.append(p)
            if point not in self.points_assigned:
                cluster.addPoint(point)
        return cluster

    def find_points_in_range(self, current_point):
        points_in_range = []
        count = 0
        while count < self.data_length - 1:
            point = self.data[count]
            count += 1

            if point in self.points_assigned:
                continue
            if eucledian(current_point, point) <= self.max_distance:
                points_in_range.append(point)
        return points_in_range

    def randrange(self, n, vmin, vmax):
        '''
        Helper function to make an array of random numbers having shape (n, )
        with each number distributed Uniform(vmin, vmax).
        '''
        return (vmax - vmin) * np.random.rand(n) + vmin

    def plot(self, data):

        x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        trace1 = go.Scatter3d(
            x=[row[0] for row in self.data],
            y=[row[1] for row in self.data],
            z=[row[2] for row in self.data],
            mode='markers',
            marker=dict(
                size=2,
                line=dict(
                    color='rgba(217, 217, 217, 0.14)',
                    width=0.2
                ),
                opacity=0.8
            )
        )

        # x2, y2, z2 = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        # trace2 = go.Scatter3d(
        #     x=x2,
        #     y=y2,
        #     z=z2,
        #     mode='markers',
        #     marker=dict(
        #         color='rgb(127, 127, 127)',
        #         size=12,
        #         symbol='circle',
        #         line=dict(
        #             color='rgb(204, 204, 204)',
        #             width=1
        #         ),
        #         opacity=0.9
        #     )
        # )
        data = [trace1]
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
