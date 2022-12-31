#-----------------------------------------------------------------------------
#running different configuraitons of tilted V
#-----------------------------------------------------------------------------

from parflow import Run
import shutil
import os
import json


PROJECT_PATH = os.getcwd() + "/../.."
# with open("../../config.json") as file:
#     config = json.load(file)
#     PROJECT_PATH = config["project_path"]

FB_FILE = "Shangguan_200m_FBZ.pfb"
MANN_PFB = "icom_mannings_rv50_4_7_10_dec_mann.pfb"
INITIAL_PRESSURE_FILE = "G1_Multi_EF_ShgFBz_200m_kz01_rv50_dec_mann_25inc.out.press.08760.pfb"
DOMAIN_DIRECTORY = f"{PROJECT_PATH}/domain" #"/glade/p/univ/ucsm0002/ICOM_danielle/icom-modeling/domain"
FORCING_DIRECTORY = "/glade/scratch/tijerina/Subsurface_Paper/ICOM_Danielle/WY2003"
#FORCING_DIRECTORY = f"{PROJECT_PATH}/forcing/WY2003_forcing"

istep = 0
clmstep = istep + 1

model = Run("icom", __file__)

#-----------------------------------------------------------------------------

model.FileVersion = 4

model.Process.Topology.P = 24
model.Process.Topology.Q = 27
model.Process.Topology.R = 1




 
files=os.listdir(DOMAIN_DIRECTORY)
 
# iterating over all the files in
# the source directory
for fname in files:
     
    # copying the files to the
    # destination directory
    shutil.copy(os.path.join(DOMAIN_DIRECTORY,fname), ".")

#---------------------------------------------------------
# Copy necessary files
#---------------------------------------------------------
#Slope files
# copytree(DOMAIN_DIRECTORY, sys.argv[1])
# copy(f"{DOMAIN_DIRECTORY}/icom_rm_coast_slopex3.pfb", ".")
# copy(f"{DOMAIN_DIRECTORY}/icom_rm_coast_slopey3.pfb", ".")

# #Solid file
# copy(f"{DOMAIN_DIRECTORY}/icom_mask_final_rm_coastcells3.pfsol", ".")
# copy(f"{DOMAIN_DIRECTORY}/GLHYMPS_1.0_Multi_Efold_new.pfb", ".")
# #copy({DOMAIN_DIRECTORY}/icom_rm_coast_PME3.pfb, ".")


# copy(f"{DOMAIN_DIRECTORY}/{INITIAL_PRESSURE_FILE}", ".")
# #spatial Mannings

# copy(f"{DOMAIN_DIRECTORY}/{MANN_PFB}", ".")

# #Flow barrier file

# copy(f"{DOMAIN_DIRECTORY}/{FB_FILE}", ".")

#---------------------------------------------------------
# Computational Grid
#---------------------------------------------------------
model.ComputationalGrid.Lower.X = 0.0
model.ComputationalGrid.Lower.Y = 0.0
model.ComputationalGrid.Lower.Z = 0.0

model.ComputationalGrid.NX = 416
model.ComputationalGrid.NY = 480
model.ComputationalGrid.NZ = 10

model.ComputationalGrid.DX =	1000.0
model.ComputationalGrid.DY =  1000.0
model.ComputationalGrid.DZ =	200.00

#---------------------------------------------------------
# The Names of the GeomInputs
#---------------------------------------------------------
model.GeomInput.Names                  = "domaininput indi_input"

model.GeomInput.domaininput.GeomName   = "domain"

model.GeomInput.domaininput.InputType  = "SolidFile"
model.GeomInput.domaininput.GeomNames  = "domain"
model.GeomInput.domaininput.FileName   = "icom_mask_final_rm_coastcells3.pfsol"

model.Geom.domain.Patches             = "land ocean top bottom"

#--------------------------------------------
# variable dz assignments
#------------------------------------------
model.Solver.Nonlinear.VariableDz =  True

model.dzScale.GeomNames =           "domain"
model.dzScale.Type =                "nzList"

model.dzScale.nzListNumber =        10

model.Cell._0.dzScale.Value =         1
model.Cell._1.dzScale.Value =         0.5
model.Cell._2.dzScale.Value =         0.25
model.Cell._3.dzScale.Value =         0.125
model.Cell._4.dzScale.Value =         0.05
model.Cell._5.dzScale.Value =         0.025
model.Cell._6.dzScale.Value =         0.005
model.Cell._7.dzScale.Value =         0.003
model.Cell._8.dzScale.Value =         0.0015
model.Cell._9.dzScale.Value =         0.0005


#------------------------------------------------------------------------------
# Flow Barrier between the 1-km layer and 100-m layer
#--------------------------------------------------------------

model.Solver.Nonlinear.FlowBarrierZ = True
model.FBz.Type = "PFBFile"
model.Geom.domain.FBz.FileName = FB_FILE
model.dist(FB_FILE)

#-----------------------------------------------------------------------------
# Indicator Geometry Input
#-----------------------------------------------------------------------------

model.GeomInput.indi_input.InputType =   "IndicatorField"
model.GeomInput.indi_input.GeomNames =   "s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8 b1 b2"
# model.GeomInput.indi_input.GeomNames =   "s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 b1 b2"
model.Geom.indi_input.FileName =           "GLHYMPS_1.0_Multi_Efold_new.pfb"

model.GeomInput.s1.Value =    1
model.GeomInput.s2.Value =    2
model.GeomInput.s3.Value =    3
model.GeomInput.s4.Value =    4
model.GeomInput.s5.Value =    5
model.GeomInput.s6.Value =    6
model.GeomInput.s7.Value =    7
model.GeomInput.s8.Value =    8
model.GeomInput.s9.Value =    9
model.GeomInput.s10.Value =   10
model.GeomInput.s11.Value =   11
model.GeomInput.s12.Value =   12
model.GeomInput.s13.Value =   13

model.GeomInput.g1.Value =    21
model.GeomInput.g2.Value =    22
model.GeomInput.g3.Value =    23
model.GeomInput.g4.Value =    24
model.GeomInput.g5.Value =    25
model.GeomInput.g6.Value =    26
model.GeomInput.g7.Value =    27
model.GeomInput.g8.Value =    28

model.GeomInput.b1.Value =    19
model.GeomInput.b2.Value =    20

#-----------------------------------------------------------------------------
# Perm (values in m/hr)
#-----------------------------------------------------------------------------

model.Geom.Perm.Names =                "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8 b1 b2"

# model.Geom.Perm.Names =                "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 b1 b2"

# Values in m/hour

model.Geom.domain.Perm.Type =            "Constant"
model.Geom.domain.Perm.Value =            0.02

model.Geom.s1.Perm.Type =                "Constant"
model.Geom.s1.Perm.Value =                0.269022595

model.Geom.s2.Perm.Type =                "Constant"
model.Geom.s2.Perm.Value =                0.043630356

model.Geom.s3.Perm.Type =                "Constant"
model.Geom.s3.Perm.Value =                0.015841225

model.Geom.s4.Perm.Type =                "Constant"
model.Geom.s4.Perm.Value =                0.007582087

model.Geom.s5.Perm.Type =                "Constant"
model.Geom.s5.Perm.Value =                0.01818816

model.Geom.s6.Perm.Type =                "Constant"
model.Geom.s6.Perm.Value =                0.005009435

model.Geom.s7.Perm.Type =                "Constant"
model.Geom.s7.Perm.Value =                 0.005492736

model.Geom.s8.Perm.Type =           "Constant"
model.Geom.s8.Perm.Value =           0.004675077

model.Geom.s9.Perm.Type =           "Constant"
model.Geom.s9.Perm.Value =           0.003386794

model.Geom.s10.Perm.Type =           "Constant"
model.Geom.s10.Perm.Value =           0.004783973

model.Geom.s11.Perm.Type =           "Constant"
model.Geom.s11.Perm.Value =           0.003979136

model.Geom.s12.Perm.Type =           "Constant"
model.Geom.s12.Perm.Value =           0.006162952

model.Geom.s13.Perm.Type =           "Constant"
model.Geom.s13.Perm.Value =           0.005009435

model.Geom.b1.Perm.Type =           "Constant"
model.Geom.b1.Perm.Value =           0.005

model.Geom.b2.Perm.Type =           "Constant"
model.Geom.b2.Perm.Value =           0.01

model.Geom.g1.Perm.Type =           "Constant"
model.Geom.g1.Perm.Value =           0.02

model.Geom.g2.Perm.Type =           "Constant"
model.Geom.g2.Perm.Value =           0.03

model.Geom.g3.Perm.Type =           "Constant"
model.Geom.g3.Perm.Value =           0.04

model.Geom.g4.Perm.Type =           "Constant"
model.Geom.g4.Perm.Value =           0.05

model.Geom.g5.Perm.Type =           "Constant"
model.Geom.g5.Perm.Value =           0.06

model.Geom.g6.Perm.Type =           "Constant"
model.Geom.g6.Perm.Value =           0.08

model.Geom.g7.Perm.Type =           "Constant"
model.Geom.g7.Perm.Value =           0.1

model.Geom.g8.Perm.Type =           "Constant"
model.Geom.g8.Perm.Value =           0.2
#
model.Perm.TensorType = 'TensorByGeom'
model.Geom.Perm.TensorByGeom.Names = 'domain b1 b2 g1 g2 g4 g5 g6 g7'

model.Geom.domain.Perm.TensorValX = 1.0
model.Geom.domain.Perm.TensorValY = 1.0
model.Geom.domain.Perm.TensorValZ = 1.0

model.Geom.b1.Perm.TensorValX = 1.0
model.Geom.b1.Perm.TensorValY = 1.0
model.Geom.b1.Perm.TensorValZ = 0.1

model.Geom.b2.Perm.TensorValX = 1.0
model.Geom.b2.Perm.TensorValY = 1.0
model.Geom.b2.Perm.TensorValZ = 0.1

model.Geom.g1.Perm.TensorValX = 1.0
model.Geom.g1.Perm.TensorValY = 1.0
model.Geom.g1.Perm.TensorValZ = 0.1

model.Geom.g2.Perm.TensorValX = 1.0
model.Geom.g2.Perm.TensorValY = 1.0
model.Geom.g2.Perm.TensorValZ = 0.1

model.Geom.g4.Perm.TensorValX = 1.0
model.Geom.g4.Perm.TensorValY = 1.0
model.Geom.g4.Perm.TensorValZ = 0.1

model.Geom.g5.Perm.TensorValX = 1.0
model.Geom.g5.Perm.TensorValY = 1.0
model.Geom.g5.Perm.TensorValZ = 0.1

model.Geom.g6.Perm.TensorValX = 1.0
model.Geom.g6.Perm.TensorValY = 1.0
model.Geom.g6.Perm.TensorValZ = 0.1

model.Geom.g7.Perm.TensorValX = 1.0
model.Geom.g7.Perm.TensorValY = 1.0
model.Geom.g7.Perm.TensorValZ = 0.1

#-----------------------------------------------------------------------------
# Specific Storage
#-----------------------------------------------------------------------------

model.SpecificStorage.Type =               "Constant"
model.SpecificStorage.GeomNames =          "domain"
model.Geom.domain.SpecificStorage.Value =   0.0001

#-----------------------------------------------------------------------------
# Phases
#-----------------------------------------------------------------------------

model.Phase.Names ="water"

model.Phase.water.Density.Type	=        "Constant"
model.Phase.water.Density.Value =	        1.0

model.Phase.water.Viscosity.Type	=      "Constant"
model.Phase.water.Viscosity.Value =	      1.0

#-----------------------------------------------------------------------------
# Contaminants
#-----------------------------------------------------------------------------

model.Contaminants.Names	=		""

#-----------------------------------------------------------------------------
# Retardation
#-----------------------------------------------------------------------------

model.Geom.Retardation.GeomNames =          ""

#-----------------------------------------------------------------------------
# Gravity
#-----------------------------------------------------------------------------

model.Gravity	=			1.0

#-----------------------------------------------------------------------------
# Setup timing info
#-----------------------------------------------------------------------------

#
model.TimingInfo.BaseUnit =        1
model.TimingInfo.StartCount =      istep
model.TimingInfo.StartTime =       istep
model.TimingInfo.StopTime =        8760
model.TimingInfo.DumpInterval =    1.0
model.TimeStep.Type =             "Constant"
model.TimeStep.Value =             1

#model.TimeStep.Type ="Growth"
#model.TimeStep.InitialStep 1
#model.TimeStep.GrowthFactor 1.2
#model.TimeStep.MaxStep 100
#model.TimeStep.MinStep 1

#-----------------------------------------------------------------------------
# Porosity
#-----------------------------------------------------------------------------
model.Geom.Porosity.GeomNames =         'domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8'

model.Geom.domain.Porosity.Type =        "Constant"
model.Geom.domain.Porosity.Value =        0.33

model.Geom.s1.Porosity.Type =   "Constant"
model.Geom.s1.Porosity.Value =   0.375

model.Geom.s2.Porosity.Type =   "Constant"
model.Geom.s2.Porosity.Value =   0.39

model.Geom.s3.Porosity.Type =   "Constant"
model.Geom.s3.Porosity.Value =   0.387

model.Geom.s4.Porosity.Type =   "Constant"
model.Geom.s4.Porosity.Value =   0.439

model.Geom.s5.Porosity.Type =   "Constant"
model.Geom.s5.Porosity.Value =   0.489

model.Geom.s6.Porosity.Type =   "Constant"
model.Geom.s6.Porosity.Value =   0.399

model.Geom.s7.Porosity.Type =   "Constant"
model.Geom.s7.Porosity.Value =   0.384

model.Geom.s8.Porosity.Type =           "Constant"
model.Geom.s8.Porosity.Value =           0.482

model.Geom.s9.Porosity.Type =           "Constant"
model.Geom.s9.Porosity.Value =           0.442

model.Geom.s10.Porosity.Type =           "Constant"
model.Geom.s10.Porosity.Value =           0.385

model.Geom.s11.Porosity.Type =           "Constant"
model.Geom.s11.Porosity.Value =           0.481

model.Geom.s12.Porosity.Type =           "Constant"
model.Geom.s12.Porosity.Value =           0.459

model.Geom.s13.Porosity.Type =           "Constant"
model.Geom.s13.Porosity.Value =           0.399

model.Geom.g1.Porosity.Type =           "Constant"
model.Geom.g1.Porosity.Value =           0.33

model.Geom.g2.Porosity.Type =           "Constant"
model.Geom.g2.Porosity.Value =           0.33

model.Geom.g3.Porosity.Type =           "Constant"
model.Geom.g3.Porosity.Value =           0.33

model.Geom.g4.Porosity.Type =           "Constant"
model.Geom.g4.Porosity.Value =           0.33

model.Geom.g5.Porosity.Type =           "Constant"
model.Geom.g5.Porosity.Value =           0.33

model.Geom.g6.Porosity.Type =           "Constant"
model.Geom.g6.Porosity.Value =           0.33

model.Geom.g7.Porosity.Type = 'Constant'
model.Geom.g7.Porosity.Value = 0.33

model.Geom.g8.Porosity.Type = 'Constant'
model.Geom.g8.Porosity.Value = 0.33

#-----------------------------------------------------------------------------
# Domain
#-----------------------------------------------------------------------------

model.Domain.GeomName = "domain"

#-----------------------------------------------------------------------------
# Relative Permeability
#-----------------------------------------------------------------------------
model.Phase.RelPerm.Type =              "VanGenuchten"
model.Phase.RelPerm.GeomNames =     "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13"
#model.Phase.RelPerm.GeomNames      "domain s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13"
#model.Phase.RelPerm.GeomNames      "domain"

model.Geom.domain.RelPerm.Alpha =    1.0
model.Geom.domain.RelPerm.N =        3.0
model.Geom.domain.RelPerm.NumSamplePoints =   20000
model.Geom.domain.RelPerm.MinPressureHead =   -300
model.Geom.domain.RelPerm.InterpolationMethod =  "Linear"


model.Geom.s1.RelPerm.Alpha =        3.548
#model.Geom.s1.RelPerm.Alpha =        2.5
model.Geom.s1.RelPerm.N =            4.162
model.Geom.s1.RelPerm.NumSamplePoints =   20000
model.Geom.s1.RelPerm.MinPressureHead =   -300
model.Geom.s1.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s2.RelPerm.Alpha =        3.467
model.Geom.s2.RelPerm.N =            2.738
model.Geom.s2.RelPerm.NumSamplePoints =   20000
model.Geom.s2.RelPerm.MinPressureHead =   -300
model.Geom.s2.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s3.RelPerm.Alpha =        2.692
model.Geom.s3.RelPerm.N =            2.445
model.Geom.s3.RelPerm.NumSamplePoints =   20000
model.Geom.s3.RelPerm.MinPressureHead =   -300
model.Geom.s3.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s4.RelPerm.Alpha =        0.501
model.Geom.s4.RelPerm.N =            2.659
model.Geom.s4.RelPerm.NumSamplePoints =   20000
model.Geom.s4.RelPerm.MinPressureHead =   -300
model.Geom.s4.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s5.RelPerm.Alpha =        0.661
model.Geom.s5.RelPerm.N =            2.659
model.Geom.s5.RelPerm.NumSamplePoints =   20000
model.Geom.s5.RelPerm.MinPressureHead =   -300
model.Geom.s5.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s6.RelPerm.Alpha =        1.122
model.Geom.s6.RelPerm.N =            2.479
model.Geom.s6.RelPerm.NumSamplePoints =   20000
model.Geom.s6.RelPerm.MinPressureHead =   -300
model.Geom.s6.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s7.RelPerm.Alpha =        2.089
model.Geom.s7.RelPerm.N =            2.318
model.Geom.s7.RelPerm.NumSamplePoints =   20000
model.Geom.s7.RelPerm.MinPressureHead =   -300
model.Geom.s7.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s8.RelPerm.Alpha =        0.832
model.Geom.s8.RelPerm.N =            2.514
model.Geom.s8.RelPerm.NumSamplePoints =   20000
model.Geom.s8.RelPerm.MinPressureHead =   -300
model.Geom.s8.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s9.RelPerm.Alpha =        1.585
model.Geom.s9.RelPerm.N =            2.413
model.Geom.s9.RelPerm.NumSamplePoints =   20000
model.Geom.s9.RelPerm.MinPressureHead =   -300
model.Geom.s9.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s10.RelPerm.Alpha =        3.311
#model.Geom.s10.RelPerm.Alpha =        2.
model.Geom.s10.RelPerm.N =            2.202
model.Geom.s10.RelPerm.NumSamplePoints =   20000
model.Geom.s10.RelPerm.MinPressureHead =   -300
model.Geom.s10.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s11.RelPerm.Alpha =        1.622
model.Geom.s11.RelPerm.N =            2.318
model.Geom.s11.RelPerm.NumSamplePoints =   20000
model.Geom.s11.RelPerm.MinPressureHead =   -300
model.Geom.s11.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s12.RelPerm.Alpha =        1.514
model.Geom.s12.RelPerm.N =            2.259
model.Geom.s12.RelPerm.NumSamplePoints =   20000
model.Geom.s12.RelPerm.MinPressureHead =   -300
model.Geom.s12.RelPerm.InterpolationMethod =  "Linear"

model.Geom.s13.RelPerm.Alpha =        1.122
model.Geom.s13.RelPerm.N =            2.479
model.Geom.s13.RelPerm.NumSamplePoints =   20000
model.Geom.s13.RelPerm.MinPressureHead =   -300
model.Geom.s13.RelPerm.InterpolationMethod =  "Linear"

#---------------------------------------------------------
# Saturation
#---------------------------------------------------------
model.Phase.Saturation.Type =             "VanGenuchten"
model.Phase.Saturation.GeomNames =         "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13"
#model.Phase.Saturation.GeomNames =         "domain s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13"
#model.Phase.Saturation.GeomNames =         "domain"
#
# @RMM added very low Sres to help with dry / large evap

model.Geom.domain.Saturation.Alpha =        1.0
model.Geom.domain.Saturation.N =            3.0
model.Geom.domain.Saturation.SRes =         0.001
model.Geom.domain.Saturation.SSat =         1.0
#
model.Geom.s1.Saturation.Alpha =        3.548
model.Geom.s1.Saturation.N =            4.162
model.Geom.s1.Saturation.SRes =         0.0001
model.Geom.s1.Saturation.SSat =         1.0

model.Geom.s2.Saturation.Alpha =        3.467
#model.Geom.s2.Saturation.Alpha =        2.5
model.Geom.s2.Saturation.N =            2.738
model.Geom.s2.Saturation.SRes =         0.0001
#model.Geom.s2.Saturation.SRes         0.1
model.Geom.s2.Saturation.SSat =         1.0

model.Geom.s3.Saturation.Alpha =        2.692
model.Geom.s3.Saturation.N =            2.445
model.Geom.s3.Saturation.SRes =         0.0001
model.Geom.s3.Saturation.SSat =         1.0

model.Geom.s4.Saturation.Alpha =        0.501
model.Geom.s4.Saturation.N =            2.659
model.Geom.s4.Saturation.SRes =         0.1
model.Geom.s4.Saturation.SSat =         1.0

model.Geom.s5.Saturation.Alpha =        0.661
model.Geom.s5.Saturation.N =            2.659
model.Geom.s5.Saturation.SRes =         0.0001
model.Geom.s5.Saturation.SSat =         1.0

model.Geom.s6.Saturation.Alpha =        1.122
model.Geom.s6.Saturation.N =            2.479
model.Geom.s6.Saturation.SRes =         0.0001
model.Geom.s6.Saturation.SSat =         1.0

model.Geom.s7.Saturation.Alpha =        2.089
model.Geom.s7.Saturation.N =            2.318
model.Geom.s7.Saturation.SRes =         0.0001
model.Geom.s7.Saturation.SSat =         1.0

model.Geom.s8.Saturation.Alpha =        0.832
model.Geom.s8.Saturation.N =            2.514
model.Geom.s8.Saturation.SRes =         0.0001
model.Geom.s8.Saturation.SSat =         1.0

model.Geom.s9.Saturation.Alpha =        1.585
model.Geom.s9.Saturation.N =            2.413
model.Geom.s9.Saturation.SRes =         0.0001
model.Geom.s9.Saturation.SSat =         1.0

model.Geom.s10.Saturation.Alpha =        3.311
model.Geom.s10.Saturation.N =            2.202
model.Geom.s10.Saturation.SRes =         0.0001
model.Geom.s10.Saturation.SSat =         1.0

model.Geom.s11.Saturation.Alpha =        1.622
model.Geom.s11.Saturation.N =            2.318
model.Geom.s11.Saturation.SRes =         0.0001
model.Geom.s11.Saturation.SSat =         1.0

model.Geom.s12.Saturation.Alpha =        1.514
model.Geom.s12.Saturation.N =            2.259
model.Geom.s12.Saturation.SRes =         0.0001
model.Geom.s12.Saturation.SSat =         1.0

model.Geom.s13.Saturation.Alpha =        1.122
model.Geom.s13.Saturation.N =            2.479
model.Geom.s13.Saturation.SRes =         0.0001
model.Geom.s13.Saturation.SSat =         1.0

#-----------------------------------------------------------------------------
# Wells
#-----------------------------------------------------------------------------
model.Wells.Names =                          ""

#-----------------------------------------------------------------------------
# Time Cycles
#-----------------------------------------------------------------------------
model.Cycle.Names ="constant rainrec"
#model.Cycle.Names ="constant"

model.Cycle.constant.Names =             "alltime"
model.Cycle.constant.alltime.Length =     1
model.Cycle.constant.Repeat =            -1

# rainfall and recession time periods are defined here
# rain for 1 hour, recession for 2 hours
model.Cycle.rainrec.Names =                "rain rec"
model.Cycle.rainrec.rain.Length =          1
model.Cycle.rainrec.rec.Length =           5000000
model.Cycle.rainrec.Repeat =               -1


#-----------------------------------------------------------------------------
# Boundary Conditions: Pressure
#-----------------------------------------------------------------------------
model.BCPressure.PatchNames =                  "land ocean top bottom"

# zero head boundaries for ocean, sink and lake boundaries

model.Patch.ocean.BCPressure.Type =      "DirEquilRefPatch"

model.Patch.ocean.BCPressure.Cycle =     "constant"
model.Patch.ocean.BCPressure.RefGeom =       "domain"
model.Patch.ocean.BCPressure.RefPatch =    "top"
model.Patch.ocean.BCPressure.alltime.Value =  0

#no flow boundaries for the land borders and the bottom
model.Patch.land.BCPressure.Type	=	      "FluxConst"
model.Patch.land.BCPressure.Cycle =		      "constant"
model.Patch.land.BCPressure.alltime.Value =	      0.0

model.Patch.bottom.BCPressure.Type	=	      "FluxConst"
model.Patch.bottom.BCPressure.Cycle =		      "constant"
model.Patch.bottom.BCPressure.alltime.Value =	      0.0


## overland flow boundary condition with rainfall then nothing
model.Patch.top.BCPressure.Type	=	      "OverlandKinematic"
model.Patch.top.BCPressure.Cycle = "constant"
model.Patch.top.BCPressure.alltime.Value = 0.0

# PmE flux
model.Solver.EvapTransFile = False
#model.Solver.EvapTransFileTransient = True

#model.Solver.EvapTrans.FileName icom_rm_coast_PME3.pfb
#model.Solver.EvapTrans.FileName = f"{FORCING_DIRECTORY}/icom_ELM_p_et"

#---------------------------------------------------------
# Topo slopes
#---------------------------------------------------------

model.TopoSlopesX.Type = "PFBFile"
model.TopoSlopesX.GeomNames = "domain"
model.TopoSlopesX.FileName = "icom_rm_coast_slopex3.pfb"

model.TopoSlopesY.Type = "PFBFile"
model.TopoSlopesY.GeomNames = "domain"
model.TopoSlopesY.FileName = "icom_rm_coast_slopey3.pfb"

#---------------------------------------------------------
# Initial conditions: water pressure
#---------------------------------------------------------

# set water table to be at the bottom of the domain, the top layer is initially dry
model.ICPressure.Type =                                  "HydroStaticPatch"
model.ICPressure.GeomNames   =                           "domain"
#model.Geom.domain.ICPressure.Value =                     1191

model.Geom.domain.ICPressure.RefGeom  =                  "domain"
model.Geom.domain.ICPressure.RefPatch  =                 "bottom"

#set INITIAL_PRESSURE_FILE                                             "icom_rmcoast_init_press_200m.pfb"
model.ICPressure.Type =                                  "PFBFile"
model.Geom.domain.ICPressure.FileName	=		              INITIAL_PRESSURE_FILE

#---------------------------------------------------------
# Mannings coefficient
#---------------------------------------------------------

#model.Mannings.Type =""Constant""
#model.Mannings.GeomNames "domain"
#model.Mannings.Geom.domain.Value = 2.e-6
#model.Mannings.Geom.domain.Value = 0.0000024

model.Mannings.GeomNames = "domain"
model.Mannings.Type = "PFBFile"
model.Mannings.FileName = MANN_PFB

#---------------------------------------------------------
##  Distribute inputs
#---------------------------------------------------------

model.ComputationalGrid.NZ =1
model.dist( "icom_rm_coast_slopex3.pfb")
model.dist( "icom_rm_coast_slopey3.pfb")
model.dist( MANN_PFB)

model.ComputationalGrid.NZ =10
model.dist( "GLHYMPS_1.0_Multi_Efold_new.pfb")
#model.dist( icom_rm_coast_PME3.pfb)
#model.dist( icom_ELM_p_et.pfb)
model.dist( INITIAL_PRESSURE_FILE)

#-----------------------------------------------------------------------------
# Phase sources:
#-----------------------------------------------------------------------------

model.PhaseSources.water.Type =                        "Constant"
model.PhaseSources.water.GeomNames =                   "domain"
model.PhaseSources.water.Geom.domain.Value =            0.0

#-----------------------------------------------------------------------------
# Exact solution specification for error calculations
#-----------------------------------------------------------------------------

model.KnownSolution  =                                  "NoKnownSolution"

#-----------------------------------------------------------------------------------------
# Set LSM parameters
#-----------------------------------------------------------------------------------------

model.Solver.LSM                   = 'CLM'
model.Solver.CLM.CLMFileDir        = "clm_output/"
model.Solver.CLM.Print1dOut        = False
model.Solver.CLM.CLMDumpInterval   = 1

model.Solver.CLM.MetForcing        = '3D'
model.Solver.CLM.MetFileName       = 'NLDAS'
model.Solver.CLM.MetFilePath       = FORCING_DIRECTORY 
model.Solver.CLM.MetFileNT         = 24
model.Solver.CLM.IstepStart        = clmstep

model.Solver.CLM.EvapBeta          = 'Linear'
model.Solver.CLM.VegWaterStress    = 'Saturation'
model.Solver.CLM.ResSat            = 0.2
model.Solver.CLM.WiltingPoint      = 0.2
model.Solver.CLM.FieldCapacity     = 1.00
model.Solver.CLM.IrrigationType    = 'none'

model.Solver.CLM.RootZoneNZ        = 4
model.Solver.CLM.SoiLayer          = 4
model.Solver.CLM.ReuseCount        = 1
model.Solver.CLM.WriteLogs         = False
model.Solver.CLM.WriteLastRST      = False
model.Solver.CLM.DailyRST          = True
model.Solver.CLM.SingleFile        = True
model.Solver.WriteCLMBinary        = False
#-----------------------------------------------------------------------------
# Set solver parameters
#-----------------------------------------------------------------------------
model.Solver.TerrainFollowingGrid  =                    True

model.Solver =                                          "Richards"
model.Solver.MaxIter =                                  2500000
model.Solver.Nonlinear.MaxIter    =                     300
model.Solver.Nonlinear.ResidualTol   =                  1e-5


model.Solver.Drop =                                     1E-20
model.Solver.AbsTol =                                    1E-10
model.Solver.MaxConvergenceFailures =                       7

model.Solver.Nonlinear.EtaChoice =                       "EtaConstant"
model.Solver.Nonlinear.EtaValue =                        1e-3
model.Solver.Nonlinear.UseJacobian =                     True

model.Solver.Nonlinear.DerivativeEpsilon =               1e-16
model.Solver.Nonlinear.StepTol =				 		             1e-25
#model.Solver.Nonlinear.Globalization =                   LineSearch
model.Solver.Linear.KrylovDimension =                    300
model.Solver.Linear.MaxRestarts =                         5


model.Solver.Linear.Preconditioner =                      "PFMG"
#model.Solver.Linear.Preconditioner.PCMatrixType         FullJacobian
model.Solver.Linear.Preconditioner.PCMatrixType =         "PFSymmetric"


model.Solver.PrintSubsurfData =                     True
model.Solver.PrintSaturation =                      True
model.Solver.PrintPressure =                        True
model.Solver.PrintSlopes =                          True
model.Solver.PrintMannings =                        True
model.Solver.PrintCLM =                             True
#model.Solver.PrintSpecificStorage                   True
#model.Solver.PrintMask                              True
#model.Solver.PrintPorosity                          True
#model.Solver.PrintSlopes                            True

#-----------------------------------------------------------------------------
# Add spin up flag
#-----------------------------------------------------------------------------
#the spinup flag will sweep all the ponding water on the surface, this may speed up the Spinup
#but will affect water balance

#model.Solver.Spinup                                 True

#-----------------------------------------------------------------------------
# Run and Unload the ParFlow output files
#-----------------------------------------------------------------------------

#puts $runname

#pfrun $runname
#pfundist $runname
#
# pfwritedb $runname

model.write()
