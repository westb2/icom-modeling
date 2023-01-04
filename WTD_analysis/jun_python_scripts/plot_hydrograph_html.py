#%%
import os
import plotly as py
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
#%%
"""
csv_files = ['results_usgs1.csv',
			 'USGS_GLHYMPS.csv', 'USGS_GLHYMPS_FBz.csv',
			 'USGS_bedrock.csv', 'USGS_bedrock_soil10.csv', 'USGS_bedrock_kz01.csv', 'USGS_bedrock_FBz.csv',
			 'CONUS1_stretch.csv', 'CONUS1_stretch_FBz.csv',
			 'USGS.csv',
			 'GLHYMPS_2.0.csv',
			 'K9.csv', 'K7.csv', 'K1.csv',
			 'GLHYMPS_USGS.csv', 'GLHYMPS_USGS_bedrock.csv',
			 'USGS_bedrock_final_slope.csv', 'CONUS1_stretch_final_slope.csv']
"""

csv_files = ['icom_USGS.csv', 'icom_USGS_bedrock.csv', 'icom_GLHYMPS_1_Efold.csv',
			 'icom_analytical_K_1.csv', 'icom_analytical_K_7.csv',
			 'icom_USGS_FBz.csv','icom_K_7_FBz.csv']

csv_files = ['csvs/'+x for x in csv_files]

"""
sce_names = ['Current slope',
			 'USGS_GLHYMPS', 'USGS_GLHYMPS_FBz',
			 'USGS_bedrock', 'USGS_bedrock_soil10', 'USGS_bedrock_kz01', 'USGS_bedrock_FBz',
			 'CONUS1_stretch', 'CONUS1_stretch_FBz',
			 'USGS',
			 'GLHYMPS_2.0',
			 'K9', 'K7', 'K1',
			 'GLHYMPS_USGS', 'GLHYMPS_USGS_bedrock',
			 'USGS_bedrock_final_slope', 'CONUS1_stretch_final_slope']
"""

sce_names = ['USGS', 'USGS_bedrock', 'CONUS1_stretch', 'K1', 'K7','USGS_FBz','K7_FBz']

pd_list = []
for fi in csv_files:
	tmp_pd = pd.read_csv(fi)
	tmp_pd['date'] = pd.to_datetime(tmp_pd['date'])
	pd_list.append(tmp_pd)

sel_ids = pd_list[1].id.unique().tolist()
sorterIndex = dict(zip(sel_ids, range(len(sel_ids))))

pd0 = pd_list[0]
pd0 = pd0.loc[pd0.id.isin(sel_ids)]

color_groups = [
   "#FFFFFF", "#0000FF", "#FF0000",
    "#00FF00", "#000033", "#FF00B6",
    "#005300", "#FFD300", "#009FFF",
   "#9A4D42", "#00FFBE", "#783FC1",
   "#1F9698", "#FFACFD", "#B1CC71",
   "#F1085C", "#FE8F42", "#DD00FF",
   "#201A01", "#720055", "#21E625",
   "#030679"
]

color_groups = [x.lower() for x in color_groups]

fig_idx = {x:ii for ii, x in enumerate(pd_list[1].id.unique().tolist())}

fig = make_subplots(rows=6,cols=2,
					subplot_titles=(pd_list[1].site_name.unique().tolist()))

groups1 = pd0.groupby('id')

for ii,(name,group) in enumerate(groups1):
	jj = fig_idx[name]
	if ii==0:
		fig.add_trace(
			go.Scatter(x=group.date, y=group.value/3600.,
			line=go.scatter.Line(color=color_groups[1]),name='observation',textfont=dict(
								size=18),legendgroup='group1'),
			row=1+jj//2, col=1+jj%2,
		)
	
		fig.add_trace(
			go.Scatter(x=group.date,y=group.sim_value/3600.,
			line=go.scatter.Line(color=color_groups[2]),name=sce_names[0],textfont=dict(
								size=18),legendgroup='group2'),
			row=1+jj//2, col=1+jj%2,
		)
	else:
		fig.add_trace(
			go.Scatter(x=group.date, y=group.value/3600.,
			line=go.scatter.Line(color=color_groups[1]),legendgroup='group1',showlegend=False),
			row=1+jj//2, col=1+jj%2,
		)
	
		fig.add_trace(
			go.Scatter(x=group.date,y=group.sim_value/3600.,
			line=go.scatter.Line(color=color_groups[2]),legendgroup='group2',showlegend=False),
			row=1+jj//2, col=1+jj%2,
		)

legend_groups = ['group'+str(x) for x in range(3, len(pd_list)+3)]

#selected_result_names = ['soil10','USGS','USGS_Kz01','USGS_bedrock','CONUS1_stretch']

for jj,selected_result in enumerate(pd_list[1:]):
	groups = selected_result.groupby('site_name')
	for name, group in groups:
		ii = [i for i,x in enumerate(pd_list[1].site_name.unique().tolist()) \
						if x.lower() == name.lower()][0]
		if ii==0:
			fig.add_trace(
				go.Scatter(x=group.date,y=group.sim_value/3600.,
				line=go.scatter.Line(color=color_groups[jj+4]),
							name=sce_names[jj+1],
							textfont=dict(size=18),legendgroup=legend_groups[jj]),
				row=1+ii//2, col=1+ii%2,
			)
		else:
			fig.add_trace(
				go.Scatter(x=group.date,y=group.sim_value/3600.,
				line=go.scatter.Line(color=color_groups[jj+4]),
									legendgroup=legend_groups[jj],
									showlegend=False),
				row=1+ii//2, col=1+ii%2,
			)

fig.update_yaxes(title_text="Daily flow (cms)")
fig.update_layout(
    template='plotly_white'
)

#fig.show()
py.offline.plot(fig,filename='icom_hydrographs_11162020.html')







# %%
