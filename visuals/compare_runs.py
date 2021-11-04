from parflow.tools.io import read_array_pfb
import pandas as pd
import plotly.graph_objects as go


my_file = "../runs/fixed_params2/icom.out.press.00047.pfb"
juns_file = "../runs/tcl_run/ELM_re1.out.press.00047.pfb"

my_data = pd.DataFrame(read_array_pfb(my_file)[5])
juns_data = pd.DataFrame(read_array_pfb(juns_file)[5])
diff = my_data-juns_data


colorscale = [[0, 'white'], [1, 'black']]
fig = go.Figure(
    data = go.Contour(
        z = diff,
        colorbar=dict(
            title='Pressure'
        ),
        colorscale=colorscale,
        contours_coloring="heatmap"
    )
)
fig.show()