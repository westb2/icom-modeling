#-----------------------------------------------------------------------------
#running different configuraitons of tilted V
#-----------------------------------------------------------------------------

from parflow import Run
import os


model = Run("icom", __file__)

model.FileVersion = 4

model.Process.Topology.P = 12
model.Process.Topology.Q = 15
model.Process.Topology.R = 1


PROJECT_PATH = os.getcwd()
FORCING_DIRECTORY = (PROJECT_PATH+"/forcing/WY2003_forcing")
model.dist(FORCING_DIRECTORY+"/icom_ELM_p_et.00000.pfb")
