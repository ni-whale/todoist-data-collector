import plotly.graph_objs as go

class Charts:
    def __init__(self):
        ...

    def test(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 2, 3, 5]

        # create a trace for the scatter plot
        trace = go.Scatter(x=x, y=y, mode='markers')

        # create a figure and add the trace to it
        fig = go.Figure(data=[trace])

        # show the figure
        fig.show()
