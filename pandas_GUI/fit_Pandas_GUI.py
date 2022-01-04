import numpy as np


def fit_pandas_GUI(dfs_info=None, show_text_col = False, **kwargs):
    """
    If passed no parameters this will look for all the dataframes in the user
    namespace and make them available for plotting. Once a
    dataframe is chosen only the numerical columns from that dataframe will
    be available for inclusion in the plotting expression.

    This GUI produces code to use the lmfit package to fit data and the plotly
    interactive plotting package to display the results.

    If you wish to allow only certain dataframes or have them show up as
    user friendly names in the menus provide that information in the first
    paramater dfs_info.

    To allow inclusion of text columns pass True for show_text_col.

    :param show_text_col: bool (default = False). When True columns containing
    text will be shown.
    :param dfs_info: List of Lists of strings [[globalname, userfriendly]
    ],..]
        :globalname: string name of the object in the user global name space.
        :userfriendly: string name to display for user selection.
    :keyword figname: string used to override default python name for figure.
    :return:
    """
    from ipywidgets import Layout, Box, HBox, VBox, GridBox, Tab, \
        Accordion, Dropdown, Label, Text, Button, Checkbox, FloatText, \
        RadioButtons, BoundedIntText
    from ipywidgets import HTML as richLabel
    from ipywidgets import HTMLMath as texLabel
    from IPython.display import display, HTML
    from IPython.display import Javascript as JS
    from IPython import get_ipython
    from .utils import new_cell_immediately_below,\
        select_cell_immediately_below, move_cursor_in_current_cell, \
        insert_text_into_next_cell, insert_text_at_beginning_of_current_cell, \
        insert_newline_at_end_of_current_cell, select_containing_cell, \
        delete_selected_cell, iconselector, notice_group
    import JPSLUtils
    from lmfit import models

    if dfs_info == None:
        from .utils import find_pandas_dataframe_names
        from IPython import get_ipython
        global_dict = get_ipython().user_ns
        dfs_info = []
        for k in find_pandas_dataframe_names():
            dfs_info.append([global_dict[k],k,k])
    friendly_to_globalname = {k[2]:k[1] for k in dfs_info}
    friendly_to_object = {k[2]:k[0] for k in dfs_info}

    figname = kwargs.pop('figname',None)
    from .utils import find_figure_names
    figlst = find_figure_names()
    if figname in figlst:
        raise UserWarning (str(figname) + ' already exists. Choose a '
                                          'different name for the figure.')
    if figname == None:
        figname = 'Figure_'+str(len(figlst)+1)
    fitmodels = ['LinearModel','PolynomialModel','ExponentialModel',
                 'GaussianModel']
    fitmodeleqns = {
    'LinearModel':r'$fit = \color{red}{a}x+\color{red}{b}$, where a = slope,' \
                  r' b = intercept',
    'PolynomialModel': r'$fit = \sum_{n=0}^{\le7}{\color{red}{c_n}x^n}$',
    'ExponentialModel': r'$fit = \color{red}{A} \exp \left( \frac{-x} ' \
                        r'{\color{red}{\tau}}\right)$, where A = amplitude,' \
                        r'$ \tau$ = decay',
    'GaussianModel': r'$fit = \frac{\color{red}{A}}{\color{red}{\sigma} ' \
                     r'\sqrt{2 \pi}} \exp \left( \frac{-(x-\color{red}' \
                     r'{\mu})^2}{2 \color{red}{\sigma}^2} \right)$, where ' \
                     r'A = amplitude, $\sigma$ = sigma, $\mu$ = center'
    }
    #### Define GUI Elements ####
    # Those followed by a * are required.
    display(HTML(
        "<h3 id ='pandasfitGUI' style='text-align:center;'>Pandas Fit "
        "Composer</h3> <div style='text-align:center;'>"
        "<span style='color:green;'>Steps with a * are required.</span> The "
        "code that will generate the fit is being "
        "built in the cell immediately below.</div><div "
        "style='text-align:center;'>This composer uses a subset of "
        "<a href ='https://lmfit.github.io/lmfit-py/'> the lmfit package</a>"
        " and <a href ='https://plotly.com/python/line-and-scatter/#'> "
        "the plotly scatter plot</a> capabilities.</div>"))

    longdesc = {'description_width':'initial'}

    # Notices for the Final Check Tab.
    makeplot_notices = notice_group(['Need data to fit',
                                     'Need a fit model',
                                     'Axes must have labels.'],
                                    'Notices:','','red')
    makeplot_notices.set_active([0,1,2])

    # 1. Pick and variables to fit and fit model
    #   a. Select Y vs. X (DataFrame, X and Y, which must be from single
    #       frame.
    # Notices for the Pick Trace(s) tab.
    notice_list = [
        'Data set (DataFrame) required.',
        'X- and Y-values required.',
    ]
    trace_notices = notice_group(notice_list, 'Notices:','','red')
    trace_notices.set_active([0,1])
    step1instr = richLabel(value = '<ol><li>Select a DataFrame (Data '
                                   'set);</li>'
                                   '<li>Select the column containing the X '
                                   'values;</li>'
                                   '<li>Select the column containing the Y '
                                   'values (what is being fit);</li>'
                                   '<li>Provide a name for the trace if you do'
                                   ' not like the default. This text will be '
                                   'used for the legend;</li></ol>'
                           )
    step1instracc = Accordion(children = [step1instr])
    step1instracc.set_title(0,'Instructions')
    step1instracc.selected_index = None

    # DataFrame selection
    tempopts = []
    tempopts.append('Choose data set.')
    for k in dfs_info:
        tempopts.append(k[2])
    whichframe = Dropdown(options=tempopts,
                                description='DataFrame: ',)

    def update_columns(change):
        if change['new'] == 'Choose data set.':
            Xcoord.disabled = True
            Ycoord.disabled = True
            add_trace_but.disabled = True
            add_trace_but.button_style = ''
            trace_notices.activate_notice(0)
            trace_notices.activate_notice(1)
            trace_notices.activate_notice(2)
            add_trace_notices.value = trace_notices.notice_html()
            return
        df = friendly_to_object[change['new']]
        tempcols = df.columns.values
        tempopt = ['Choose column for coordinate.']
        for k in tempcols:
            if show_text_col:
                tempopt.append(k)
            else:
                if df[k].dtype != 'O':
                    tempopt.append(k)
        Xcoord.options = tempopt
        Xcoord.value = tempopt[0]
        Ycoord.options = tempopt
        Ycoord.value = tempopt[0]
        Xcoord.disabled = False
        Ycoord.disabled = False
        trace_notices.activate_notice(1)
        trace_notices.deactivate_notice(0)
        add_trace_notices.value =trace_notices.notice_html()
        pass
    whichframe.observe(update_columns, names='value')

    # Data selection
    Xcoord = Dropdown(options=['Choose X-coordinate.'],
                           description='X: ',
                           disabled = True)
    Ycoord = Dropdown(options=['Choose Y-coordinate.'],
                           description='Y: ',
                           disabled = True)
    def trace_name_update(change):
        if change['new'] != 'Choose column for coordinate.':
            trace_name.value = Ycoord.value
        if Xcoord.value != 'Choose column for coordinate.' and Ycoord.value \
                != 'Choose column for coordinate.':
            yerrtype.disabled = False
            trace_name.disabled = False
            trace_notices.deactivate_notice(1)
            add_trace_notices.value = trace_notices.notice_html()
        else:
            yerrtype.disabled = True
            trace_name.disabled = True
            trace_notices.activate_notice(1)
            add_trace_notices.value = trace_notices.notice_html()
        pass

    Ycoord.observe(trace_name_update,names='value')

    # Trace name
    trace_name = Text(placeholder = 'Trace name for legend',
                      description = 'Trace name: ',
                      disabled = True)

    trace_notices.set_active([0,1])
    add_trace_notices = richLabel(value = trace_notices.notice_html())
    step1tracebox = VBox([whichframe,Xcoord,Ycoord,trace_name])
    step1actionbox = VBox([add_trace_notices])
    step1hbox = HBox([step1tracebox,step1actionbox])
    step1 = VBox([step1instracc, step1hbox])

    # 2. Set data uncertainty
    step2instr = richLabel(value = 'If you know the uncertainty in your data '
                                   'values (Y-values)you should '
                                   'specify it, as the uncertainty impacts '
                                   'the final uncertainty in the fit '
                                   'parameters. '
                                   'If you do not know the uncertainty of '
                                   'your data leave the "Error Type" as '
                                   '"none". In this case all the data values '
                                   'will be equally weighted during the fit. '
                                   'Alternatives are: a constant uncertainty '
                                   'that is the same for every data point; a '
                                   'percentage of each value; data (a '
                                   'column) specifying the uncertainty for '
                                   'every data point.')

    yerrtype = Dropdown(options = ['none','percent','constant','data'],
                        description = 'Error Type: ',
                        disabled = True)

    def error_settings_OK():
        check = True
        if (yerrtype.value == 'data') and (yerrdata.value == 'Choose error '
                                                        'column.'):
            check = False
        return check

    def yerr_change(change):
        df = friendly_to_object[whichframe.value]
        if change['new'] == 'percent' or change['new'] == 'constant':
            yerrvalue.disabled = False
            yerrdata.disabled = True
        if change['new'] == 'data':
            yerrvalue.disabled = True
            tempopts = ['Choose error column.']
            tempcols = df.columns.values
            for k in tempcols:
                if df[k].dtype != 'O':
                    tempopts.append(k)
            yerrdata.options=tempopts
            yerrdata.disabled = False
        if change['new'] == 'none':
            yerrvalue.disabled = True
            yerrdata.disabled = True
        add_trace_notices.value = trace_notices.notice_html()
        pass

    yerrtype.observe(yerr_change, names = 'value')

    yerrvalue = FloatText(description = '% or constant: ', disabled = True,
                          style=longdesc, value=1.0)
    yerrdata = Dropdown(options = ['Choose error column.'],
                        description = 'Error values: ',
                        disabled = True)

    def errdata_change(change):
        if error_settings_OK():
            #trace_notices.deactivate_notice(2)
            pass
        else:
            #trace_notices.activate_notice(2)
            pass
        add_trace_notices.value = trace_notices.notice_html()
        pass

    yerrdata.observe(errdata_change, names = 'value')
    yerrrow1 = HBox([yerrtype,yerrvalue])
    yerror = VBox([yerrrow1,yerrdata])
    step2instracc = Accordion(children=[step2instr])
    step2instracc.selected_index = None
    step2 = VBox([step2instr,yerror])

    # 3. Set fit parameters
    step3instr = richLabel(value = '<ol><li>Choose the fit type ('
                                   'functional form). Red symbols are the '
                                   'fit parameters.</li>'
                                   '<li>You may use the default settings for '
                                   'the '
                                   'initial guesses and parameter ranges or '
                                   'you may set them.</li>'
                                   '<li>To fix a value at the '
                                   'initial guess select the "fix" checkbox. '
                                   'You must provide an initial guess if you '
                                   'fix a parameter.</li></ol>')
    step3instracc = Accordion(children = [step3instr])
    step3instracc.set_title(0,'Instructions')
    step3instracc.selected_index = None
    # TODO: get selected fit model and update parameters list.
    modeldrop = Dropdown(options=fitmodels)
    modeleqn = texLabel(value = fitmodeleqns[modeldrop.value])
    def getcurrmodel_param(modelname, params_set):
        '''
        Using the model name return ipywidgets for setting the fit 
        parameters and constraints, populated with the default values.
        :param string modelname: The string name for the lmfit model.
        :param VBox params_set: The VBox containing the HBoxes for parameter
            guesses and constraints.
        :return VBox: params_set with fields reset and those available visible.
        '''
        currmodel = getattr(models,modelname)()
        currmodel_param = []
        for i in range(0,6):
            labeltext = ''
            fix = False
            value = None
            min = -np.inf
            max = np.inf
            expr = None  # Not used, maybe for arbitrary functions.
            if i < len(currmodel.param_names):
                labeltext = currmodel.param_names[i]
                hints = currmodel.param_hints.get(labeltext,None)
                if isinstance(hints,dict):
                    fix = not(hints.get('vary',True))
                    value = hints.get('value',None)
                    min = hints.get('min',-np.inf)
                    max = hints.get('max',np.inf)
                    expr = hints.get('expr',None)
                params_set.children[i].layout.display=''
            else:
                labeltext = str(i)
                params_set.children[i].layout.display='none'
        params_set.children[i].children[0].value = labeltext
        params_set.children[i].children[1].children[0].value = fix
        params_set.children[i].children[1].children[1].value = value
        params_set.children[i].children[1].children[2].value = min
        params_set.children[i].children[1].children[3].value = max
        pass

    def make_param_set():
        '''
        Creates at VBox with 7 parameters each having fields in an HBox:
        1. fixcheck (checkbox for fixing the value)
        2. valuefield (floatText for setting the value)
        3. minfield (floatText for setting the minimum allowed value)
        4. maxfield (floatText for setting the maximum allowed value)
        By default the all VBox components have their `layout.display=none`.
        :return: VBox
        '''
        currmodel_param=[]
        for i in range (0,6):
            fixcheck = Checkbox(value=False,
                                description='Fix (hold)',
                                disabled=False,
                                style=longdesc)
            valuefield = FloatText(value=None,
                                   description='Value: ',
                                   disabled=False,
                                   style=longdesc)
            minfield = FloatText(value=None,
                                 description='Min: ',
                                 disabled=False,
                                 style=longdesc)
            maxfield = FloatText(value=None,
                                 description='Max: ',
                                 disabled=False,
                                 style=longdesc)
            parambox = HBox([Label(str(i)),HBox([fixcheck,valuefield,minfield,
                                    maxfield])])
            parambox.layout.display = 'none'
            currmodel_param.append(parambox)
        params_set = VBox(currmodel_param)
        return params_set

    def modeldrop_change(change):
        modeleqn.value=fitmodeleqns[modeldrop.value]
        getcurrmodel_param(modeldrop.value,params_set)
        pass
    modeldrop.observe(modeldrop_change, names = 'value')
    params_set = make_param_set()

    step3 = VBox([step3instracc,HBox([modeldrop,modeleqn]),params_set])

    # 4.Title, Axes, Format ...
    step4instr = richLabel(value = 'You must set the axes labels to something '
                           'appropriate. For example if the X - values '
                           'represent time in seconds "Time (s)" is a good '
                           'choice. Likewise, choose an appropriate label '
                                   'for the Y - axis.')
    plot_title = Text(value = figname,
                       description = 'Plot title: ',
                      layout = Layout(width='80%'))
    X_label = Text(placeholder = 'Provide an X-axis label (usually has units)',
                   description = 'X-axis label: ',
                   style = longdesc,
                   layout=Layout(width='45%'))
    Y_label = Text(placeholder = 'Provide a Y-axis label (usually has units)',
                   description = 'Y-axis label: ',
                   style = longdesc,
                   layout=Layout(width='45%'))
    def mirror_axes_change(change):
        if change['new']:
            mirror_ticks.disabled= False
        else:
            mirror_ticks.disabled= True
            mirror_ticks.value = False
        pass

    mirror_axes = Checkbox(value = False,
                           description = 'Display Mirror Axes',
                           style = longdesc)
    mirror_axes.observe(mirror_axes_change, names = 'value')
    mirror_ticks = Checkbox(value = False,
                            description = 'Mirror Tick Marks',
                            disabled = True)
    plot_template = Dropdown(options=['none','simple_white', 'ggplot2',
                                    'seaborn',
                                 'plotly', 'plotly_white', 'plotly_dark',
                                 'presentation', 'xgridoff''ygridoff',
                                 'gridon'],
                        value='simple_white',
                        description = 'Plot Styling: ',
                        style = longdesc)
    step4hbox1 = HBox([X_label, Y_label])
    step4hbox2 = HBox([mirror_axes,mirror_ticks, plot_template])
    step4 = VBox([step4instr, plot_title, step4hbox1, step4hbox2])

    # 5. Final Check*
    step5instr = richLabel(value = 'Things to check before clicking "Do '
                                   'Fit": <ul>'
                                   '<li>Fix any problems listed in '
                                   '"Notices".</li>'
                                   '<li>Check for any unpaired parentheses, '
                                   'brackets or braces (usually highlighted '
                                   'in red).</li>'
                                   '<li>Check that all single and double '
                                   'quotes are paired.</li>'
                                   '<li>If you did any manual editing '
                                   'double-check for typos.</li>')
    step5noticebox = richLabel(value = makeplot_notices.notice_html())
    def dofit_click(change):
        select_cell_immediately_below()
        dfname = friendly_to_globalname[whichframe.value]
        text = 'scat = go.Scatter(x = '+dfname+'[\'' \
               +Xcoord.value+'\'],'
        text += ' y = ' +dfname+'[\''+Ycoord.value+ \
                                          '\'],\\n'
        text += '        mode = \''+modedrop.value+'\', name = \'' \
                                               +trace_name.value+'\','
        # in here add other formatting items using ifs.
        if yerrtype.value != 'none':
            text +='\\n        '
            if yerrtype.value == 'data':
                text += 'error_y_type=\'data\', ' \
                        'error_y_array='+dfname
                text += '[\''+yerrdata.value+'\'],'
            else:
                text += 'error_y_type=\''+yerrtype.value+'\', error_y_value='
                text += str(yerrvalue.value)+','
        text += ')\\n'
        text += figname + '.add_trace(scat)\\n'
        text += figname + '.update_xaxes(title= \''+X_label.value+'\''
        def get_mirror_text():
            if mirror_axes.value:
                mirror_text = ', mirror = True)'
                if mirror_ticks.value:
                    mirror_text = ', mirror= \'ticks\')'
            else:
                mirror_text = ')'
            return mirror_text
        text += get_mirror_text()
        insert_newline_at_end_of_current_cell(text)
        text = figname + '.update_yaxes(title= \''+Y_label.value+'\''
        text += get_mirror_text()
        insert_newline_at_end_of_current_cell(text)
        if plot_title.value !='' or plot_template.value != 'simple_white':
            text = figname+'.update_layout(title = \''+plot_title.value+'\', '
            text += 'template = \''+ plot_template.value +'\')'
            insert_newline_at_end_of_current_cell(text)
        text = figname +'.show()'
        insert_newline_at_end_of_current_cell(text)
        text = '# Force save widget states so that graph will still be'
        insert_newline_at_end_of_current_cell(text)
        text = '# available when notebook next opened in trusted state.'
        insert_newline_at_end_of_current_cell(text)
        jscode = 'Jupyter.actions.call(\\"widgets:save-with-widgets\\");'
        text = 'JPSLUtils.OTJS(\''+jscode+'\')'
        insert_newline_at_end_of_current_cell(text)
        # run the cell to build the plot
        JPSLUtils.OTJS('Jupyter.notebook.get_selected_cell().execute()')
        # remove the GUI cell
        select_containing_cell('pandasfitGUI')
        delete_selected_cell()
        from time import sleep
        pass
    dofitbut = Button(description = 'Do Fit', disabled = True)
    dofitbut.on_click(dofit_click)
    step5vbox = VBox([dofitbut,step5noticebox])
    step5 = HBox([step5instr,step5vbox])


    steps = Tab([step1, step2, step3, step4, step5])
    steps.set_title(0,'1. Pick Data*')
    steps.set_title(1,'2. Data Uncertainty*')
    steps.set_title(2,'3. Set up Model*')
    steps.set_title(3,'4. Axes Format*')
    steps.set_title(4, '5. Final Check*')
    def tab_changed(change):
        if change['new'] ==4:
            if X_label.value == '' or Y_label.value == '':
                makeplot_notices.activate_notice(2)
                dofitbut.disabled = True
                dofitbut.button_style = ''
            else:
                makeplot_notices.deactivate_notice(2)
            if Xcoord.value == 'Choose X-coordinate.' or \
                    Ycoord.value == 'Choose X-coordinate.':
                makeplot_notices.activate_notice(0)
                dofitbut.disabled = True
                dofitbut.button_style = ''
            else:
                makeplot_notices.deactivate_notice(0)
            if modeldrop.value == '':
                makeplot_notices.activate_notice(1)
                dofitbut.disabled = True
                dofitbut.button_style = ''
            else:
                makeplot_notices.deactivate_notice(1)
            step5noticebox.value = makeplot_notices.notice_html()
        if len(makeplot_notices.get_active()) == 0:
            dofitbut.disabled = False
            dofitbut.button_style = 'success'
        pass

    steps.observe(tab_changed, names = 'selected_index')
    display(steps)
    select_containing_cell('pandasfitGUI')
    new_cell_immediately_below()
    text = 'from plotly import graph_objects as go\\n'
    text += 'import lmfit as lmfit\\n'
    text += str(figname) + ' = go.FigureWidget(' \
                          'layout_template=\\"simple_white\\")'
    insert_text_into_next_cell(text)
    pass