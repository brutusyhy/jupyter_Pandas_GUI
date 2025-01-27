# Development Notes

[General](#general-notes) | [Make Docs](#constructing-the-documentation) | 
[Build PyPi Package](#building-pypi-package) |
## General Notes
1. Thoughts on GUI for loading data. Could use ipyfilechooser to select 
   local files. A dropdown for html vs csv to filter and select the reader. 
   A checkbox for the index (label) column or not in file. The html loader 
   creates an array of dataframes, one for each table. These should be 
   broken up or the user asked which ones to load.
2. Consider making array of code strings for each trace in plot GUI, 
   allowing the user to then delete them from a list and have the plot code 
   updated.
3. Consider showing error band, when error bars reach high density.

## Constructing the Documentation

1. Make sure pdoc is installed and updated in the virtual environment `pip 
   install -U pdoc`.
2. The main README combined with Development Notes is used as first page.
   * During development you may point to images and so on in the local
    directory structure. However, they will have to be changed to absolute 
     (full url) paths before pushing to the main repository. The root is 
     `https://jupyterphysscilab.github.io/jupyter_Pandas_GUI/DataSets` for 
     images.
   * DO NOT change absolute (full url) paths.
3. Make edits to the file `Pandas_GUI_Doc_Home.html`.
4. At the root level run pdoc `pdoc --logo Pandas_GUI_Icon.svg --logo-link 
https://jupyterphysscilab.github.io/jupyter_Pandas_GUI/ --footer-text 
   "jupyter_Pandas_GUI vX.X.X" -html -o docs pandas_GUI` where `X.X.X` is the 
   version number.
5. Edit the created `index.html` so that the refresh points to 
   `Pandas_GUI_Doc_Home.html`.

### Tasks for Documentation

## Building PyPi package

1. Make sure to update the version number in setup.py first.
1. Install updated  setuptools and twine in the virtual environment:
   ```
   pipenv shell
   pip install -U setuptools wheel twine
   ```
1. Build the distribution `python -m setup sdist bdist_wheel`.
1. Test it on `test.pypi.org`.
    1. Upload it (you will need an account on test.pypi.org):
       `python -m twine upload --repository testpypi dist/*`.
    1. Create a new virtual environment and test install into it:
        ```
        exit # to get out of the current environment
        cd <somewhere>
        mkdir <new virtual environment>
        cd <new directory>
        pipenv shell #creates the new environment and enters it.
        pip install -i https://test.pypi.org/..... # copy actual link from the
                                                   # repository on test.pypi.
        ```
       There are often install issues because sometimes only older versions of
       some of the required packages are available on test.pypi.org. If this
       is the only problem change the version to end in `rc0` for release
       candidate and try it on the regular pypi.org as described below for
       releasing on PyPi.
    1. After install test by running a jupyter notebook in the virtual 
       environment.

### Releasing on PyPi

Proceed only if testing of the build is successful.

1. Double check the version number in setup.py.
1. Rebuild the release: `python -m setup sdist bdist_wheel`.
1. Upload it: `python -m twine upload dist/*`
1. Make sure it works by installing it in a clean virtual environment. This
   is the same as on test.pypi.org except without `-i https://test.pypy...`. If
   it does not work, pull the release.
