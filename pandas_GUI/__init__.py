name = "pandas_GUI"
"""
This code utilizes Jupyter widgets to provide python expression composer GUIs:
* to generate code to add a new column to an existing Pandas DataFrame;
* to generate code to plot existing Pandas data using Plotly;
* to generate code to fit Pandas data using lmfit and plot the results using
Plotly.
"""

import os

# locate directory for this package to use for loading ancillary files.
# absolute path to directory containing this file.
mydir = os.path.dirname(__file__)

# load any supporting files

# import the GUI tools
from pandas_GUI.new_pandas_column_GUI import new_pandas_column_GUI
from pandas_GUI.plot_Pandas_GUI import plot_pandas_GUI
from pandas_GUI.fit_Pandas_GUI import fit_pandas_GUI
import JPSLUtils

# clean up namespace
del os
del mydir