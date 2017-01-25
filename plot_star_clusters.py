import random
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

class plot_star_clusters:
    def __init__(self):
        py.sign_in('GeddySchellevis', 'VCYb9ulpyXeKtimPbOJD')

    def plot_clusters(self,clusters):
        traces = []
        for cluster in clusters:
            trace1 = go.Scatter3d(
                x=[row[0] for row in cluster.points],
                y=[row[1] for row in cluster.points],
                z=[row[2] for row in cluster.points],
                mode='markers',
                marker=dict(
                    size=4,
                    line=dict(
                        color=random_color(),
                        width=0.2
                    ),
                    opacity=0.8
                )
            )
            traces.append(trace1)
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=traces, layout=layout)
        plot(fig)

def random_color():
    return 'rgba({0}, {1}, {2}, 0.14)'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
