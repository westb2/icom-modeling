from parflow.tools.io import read_array_pfb
import pandas as pd
import numpy as np
import plotly.graph_objects as go


file = "../runs/abs_path_test/test_run.out.press.00050.pfb"

data = pd.DataFrame(read_array_pfb(file)[0])
data = np.clip(data, a_max=None, a_min=0)


colorscale = [[0, 'white'], [1, 'mediumturquoise']]
fig = go.Figure(
    data = go.Contour(
        z = data,
        colorbar=dict(
            title='Pressure'
        ),
        colorscale=colorscale,
        contours_coloring="heatmap"
    )
)
fig.show()

