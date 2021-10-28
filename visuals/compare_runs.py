from parflow.tools.io import read_array_pfb
import matplotlib.pyplot as plot
import matplotlib.cm as cm
import pandas as pd


my_file = "../runs/abs_path_test/test_run.out.press.00050.pfb"
juns_file = "../runs/jun_run/ELM_re1.out.press.00050.pfb"

my_data = pd.DataFrame(read_array_pfb(my_file)[0])
juns_data = pd.DataFrame(read_array_pfb(juns_file)[0])
print(my_data-juns_data)