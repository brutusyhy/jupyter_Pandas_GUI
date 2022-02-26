## jupyter_Pandas_GUI
[Introduction](#introduction) | [Current Features](#current-features) | 
[Wishlist](#wishlist) | [Usage](#usage) | [Installation](#installation) | 
[Change Log](#change-log) | [Issues or comments](#issues-or-comments) | 
[License](#this-software-is-distributed-under-the-gnu-v3-license)
#### Introduction:

GUI tools to help the user construct Pandas and Python expressions such as a 
to create things such as new calculated columns, plots or fits. The tools are 
meant to run in an interactive Jupyter notebook.  **Currently, they only work 
in the classic Jupyter notebook and not Jupyter lab.** All tools are based on 
Jupyter widgets.

These tools are meant to help the user learn how to construct the commands. 
They are intended for new or occasional users of Pandas. However, 
sophisticated users may find them useful for doing simple one-off tasks where 
the ability to choose python objects from menus can reduce errors.

[![Binder](https://mybinder.org/badge_logo.svg)
](https://mybinder.org/v2/gh/JupyterPhysSciLab/jupyter_Pandas_GUI.git/HEAD?urlpath=/tree/Demonstration%20of%20jupyter_Pandas_GUI.ipynb)
Try the demonstration notebooks.

#### Current Features:

The user can pass the GUI tools a list of Pandas 
DataFrames to work with. If nothing is passed, the GUI will look for 
Pandas DataFrames in the interactive session. The whole GUI and the Jupyter 
cell that created it is deleted when done. This leaves only the code that was 
generated by the GUI and the results of running the generated code.

The generated code contains sparse comments meant to help new users 
understand the code.

*Currently defined GUIs:*

* `new_pandas_column_GUI()`: A GUI with four steps to lead the user through 
  formulating an expression for a new column.

  <img src = "DataSets/new_col_GUI.png" style="width:90%;"/>
* `plot_pandas_GUI()`: A GUI with four steps to lead the user through plotting 
  Pandas data as a scatter or line plot using plotly.

  <img src = "DataSets/plot_GUI.png" style="width:90%;"/>
* `fit_pandas_GUI()`: A GUI with six steps to lead the user through fitting 
  Pandas data to a line, polynomial, exponential, Gaussian or sine function.

  <img src = "DataSets/GUI_fitexp_1.png" style="width:90%;"/>

#### Wishlist:

  * GUIs for plots beyond scatter/line plots.
  
#### Usage:
If the `jupyter_Pandas_GUI` is installed in your Jupyter/Python environment 
start by importing it:
```
from pandas_GUI import *
```
When you want to use a particular GUI issue the appropriate command. Currently:
```
new_pandas_column_GUI()
```
or
```
plot_pandas_GUI()
```
See the docstrings for information about passing dataframes that are not at the
root of the interactive namespace or presenting the user with alternative names
for the dataframes. There is also an option to make columns containing text 
available. By default they are ignored.


#### Installation:

Installation using pip into a virtual environment is recommended.

*Production*

1. If not installed, install pipenv:`$ pip3 install --user pipenv`. You may
need to add `~/.local/bin` to your `PATH` to make `pipenv`
available in your command shell. More discussion: 
[The Hitchhiker's Guide to Python](https://docs.python-guide.org/dev/virtualenvs/).
1. Navigate to the directory where this package will be installed.
1. Start a shell in the environment `$ pipenv shell`.
1. Install using pip.
    1. `$ pip install jupyter-Pandas-GUI`. This will install 
       Jupyter into the same virtual
    environment if you do not already have it on your machine. If Jupyter is already
    installed the virtual environment will use the existing installation. This takes
    a long time on a Raspberry Pi. It will not run on a 3B+ without at least 1 GB of
    swap. See: [Build Jupyter on a Pi](https://www.uwosh.edu/facstaff/gutow/computer-and-programming-how-tos/installing-jupyter-on-raspberrian).
    1. Still within the environment shell test this by starting jupyter
`$ jupyter notebook`. Jupyter should launch in your browser.
        1. Open a new notebook using the default (Python 3) kernel.
        1. In the first cell import the pandas_GUI module:
            `from pandas_GUI import *`
        1. To try:
           1. Create some Pandas DataFrames in the notebook.
           1. Use the command `new_pandas_column_GUI()` to start the GUI.
           1. It will search for the DataFrames you created.
           1. Follow the steps to create a new column in one of your
              DataFrames.
        
1. _Optional_ You can make this environment available to an alternate Jupyter install as a special kernel when you are the user.
    1. Make sure you are running in your virtual environment `$ pipenv shell` in the directory for  virtual
    environment will do that.
    1. Issue the command to add this as a kernel to your personal space: 
    `$ python -m ipykernel install --user --name=<name-you-want-for-kernel>`.
    1. More information is available in the Jupyter/Ipython documentation. A simple tutorial from Nikolai Jankiev
    (_Parametric Thoughts_) can be found [here](https://janakiev.com/til/jupyter-virtual-envs/). 
    
*Development*

Simply replace `$ pip install jupyter-Pandas-GUI` with `$ pip 
install -e ../jupyter_Pandas_GUI` in the _Production_
instructions.

#### Change Log
* 0.5.2 
  * Widget states autosaved when a new plot is made.
  * Began making use of [JPSLUtils](https://github.com/JupyterPhysSciLab/JPSLUtils).  
* 0.5.1
  * Possible to use pandas dataframes in namespaces other than the
    user global namespace.
  * Readme updates.
* 0.5.0 Initial beta release.

#### Issues or comments

[JupyterPhysSciLab/jupyter_Pandas_GUI/issues](https://github.com/JupyterPhysSciLab/jupyter_Pandas_GUI/issues)

##### [This software is distributed under the GNU V3 license](https://gnu.org/licenses)
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Copyright - Jonathan Gutow, 2021, 2022.