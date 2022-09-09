#! /usr/bin/env python3
# vim: set syntax=none nospell expandtab ts=4 sw=4:
# ###################################### #
# Author: geoffm.companionway@gmail.com  #
# ###################################### #

# see gtools for def list_files()

# ### IMPORTS ### #
import os
from datetime import datetime
from docopt import docopt
import re
# export PYTHONPATH=$PYTHONPATH:/home/geoffm/dev/python/gmodules
# from dbug import dbug
import matplotlib.pyplot as plt  # noqa:
import pandas as pd  # noqa:
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy.signal import savgol_filter
from gtools3 import dbug, kv_cols, printit, shadowed, do_edit, funcname, gselect
# from rtools import rkv_cols, rprint, rselect, rtable


# ### GLOBALS ### #
dtime = datetime.now().strftime("%Y%m%d-%H%M")


# ### FUNCTIONS ### #
# ###################
def handleOPTS(args):
    # ###############
    # dbug(args)
    if args['-E']:
        do_edit(__file__)
        return
    if args['-d']:
        dbug("Debugging has been turned on")
    if args['-t']:
        import doctest
        doctest.testmod(verbose=True, report=False, raise_on_error=False, exclude_empty=False)
        return
    if args["-P"]:
        plot_file(args["<filename>"])


def get_dtime_format(s_date):
    """
    WIP
    """
    if isinstance(s_date, float):
        s_date = int(s_date)
    if isinstance(s_date, int):
        s_date = str(s_date)
    # in case it is still numpy int or whatever...
    add_this = ""
    if str(s_date).endswith(","):
        add_this = ","
        s_date = s_date.strip(",")
    s_date = str(s_date)
    # dbug(s_date)
    # dbug(type(s_date))
    date_patterns = ["%Y%m%d", "%d-%m-%Y", "%Y-%m-%d", "%Y%m%d-%H%M", "%Y-%m-%d %H:%M", "%Y%m%d-%H:%M", "%Y-%m-%d %H:%M:%S"]
    for pattern in date_patterns:
        try:
            # dbug(f"Trying pattern: {pattern} against s_date: {s_date}")
            # return datetime.datetime.strptime(s_date, pattern).date()
            r =  datetime.strptime(s_date, pattern).date()
            return pattern + add_this
        except:
            # dbug(f"pattern: {pattern}\nFAILed against\ns_date: {s_date}")
            pass
    # if we got here something went wrong...
    dbug(f"Date: [{s_date}] is not in expected format. Searched date_patterns: {date_patterns}")
    return None


def dfread_file(filename, colnames_l=[], title=""):
    """
    WIP 
    20220429 
    first written for a file that starts with the first line commented as a header
    this assumes that the first line is not a csv header ... I need to fix this
    return: a new_df
    """
    DAT_FILE = filename
    f = open(DAT_FILE)
    firstline = f.readline()
    if firstline.startswith("#"):
        fline = firstline.lstrip("# ")
    else:
        fline = firstline
        df = pd.read_csv(filename)
        f.close()
        return df
    f.close()
    from gtools3 import purify_file
    lines = purify_file(filename)
    lines = [line + '\n' for line in lines]
    tmp_file = "/tmp/mytmp.dat"
    myfile = open(tmp_file, 'w')
    myfile.writelines(lines)
    myfile.close()
    DAT_FILE = tmp_file
    # dbug(lines, 'ask')
    if ":" in fline:
        fline = fline.replace(":", " ")
        names = fline.split()
        title = names[0]
        # ylabel = names[1]
        # xlabel = names[2]
        names = names[2:]  # skip title name
    else:
        if title == "":
            title = os.path.basename(DAT_FILE)
        # ylabel = "index"
        # xlabel = "dtime"
        names = fline.split()
        # names.insert(0,"index")
    if "," in names[0]:
        names = names[0].split(",")
        # dbug(names)
    """--== SEP LINE ==--"""
    if DAT_FILE.endswith("csv"):
        df = pd.read_csv(DAT_FILE, thousands=',', comment="#", header=0, names=names, on_bad_lines='warn', engine='python', infer_datetime_format=True)
    if DAT_FILE.endswith("dat"):
        df = pd.read_csv(
            DAT_FILE,
            sep=r"\s+",
            thousands=",",
            comment="#",
            header=None,
            names=names,
            on_bad_lines='warn',
            engine="python",
            parse_dates=True,
            infer_datetime_format=True,
        )
    df.dropna(how="all", axis="columns")
    # dbug(df.head())
    # first_entry = str(int(df.iloc[0][0]))
    # dbug(df.head())
    # dbug(df.info())
    """--== SEP LINE ==--"""
    if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
        # dbug()
        first_date_entry = str(df.iloc[0][0])
    else:    
        # df is currently indexed and colnames[0] is probably 'Date' or similar
        # ok , 'date' might be in multiple cols, we are going to assume use of the first one with 'date' string in it
        # this complexity is kind of for future use
        # we could probably just assume the first colname is the date/time column
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if len(date_cols) < 1:
            # just go ahead and assume the first column is a dtime column with a name that doesn't have 'date' in it like 'dtime'
            first_date_entry = str(df.iloc[0][0])
        else:
            # dbug(list(df.columns))
            first_date_colname = date_cols[0]
            # dbug(first_date_colname)
            first_date_entry = df.loc[df.index[0], first_date_colname] 
        # dbug(first_date_entry)
        # dbug(date_cols[0])
    # dbug(first_date_entry, 'ask')
    """--== SEP LINE ==--"""
    # dbug(first_date_entry)
    dtformat = get_dtime_format(first_date_entry)
    # dbug(dtformat)
    df.iloc[:, 0] = pd.to_datetime(pd.Series(df.iloc[:, 0]), format=dtformat, errors='coerce')
    if len(colnames_l) != 0:
        # dbug(colnames_l)
        df.columns = colnames_l
    # consider: df.set_index(['Date'], inplae=True) 
    # dbug(df)
    new_df = df.set_index(df.columns[0])
    # Now, you may need this to "see" if the first column (now index) is Datetime
    # if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
    #     xlabel = "Date"
    # dbug(new_df)
    return new_df
    # ### EOB def dfread_file(filename, colnames_l=[], title=""): ### #


# ######################
def plot_file(filename, mavgs=False, max=False, shadow=False, savefile="", title="", choose=True, window_size=0, colnames_l=[]):
    # ##################
    """
    WIP
    filename should be a valid csv file 
    or 
    a [gwm].dat file where first line is a commented colon separated column list and the rest is space delimited
    need info!
    examines firstline for title and labels as a comment
    # TODO: add title=string_title
    TODO: add label=list or string (test needed) parsed for column names
    savefile should be the full path for a graph img file if you want one saved
    NOTE: this expects a df with the first column (dates/times) as the index
    """
    # TODO: 20210923 change this next section to: df = dfread_file(filename)
    # dbug(funcname())
    if isinstance(filename, str):
        df = dfread_file(filename, colnames_l=colnames_l, title=title)
    else:
        # maybe this is already a pandas dataframe so accept it as the df to plot
        # TODO: change the name of this to plotit - somehow make it do subplots...
        # dbug(type(filename))
        df = filename
    # dbug(df)
    cols = df.columns
    ans = "y"
    choices_l = []
    choices_l = df.columns.to_list()
    if type(df.index) == pd.core.indexes.datetimes.DatetimeIndex:
        xlabel = df.index
        ylabel = cols[0]
        # ax = df.plot(kind="line", xlabel=xlabel, y=choices, color=colors, figsize=(15, 5))
        #choices = cols
        # dbug(choices)
    else:
        ylabel = cols[1]
        # ax = df.plot(kind="line", x=xlabel, y=choices, color=colors, figsize=(15, 5))
        #choices = cols[1:]
        # dbug(choices)
    # note: if the df was/is a Series instead of a DataFrame you could do this
    """--== SEP LINE ==--"""
    selections = []
    selections_l = []
    while ans == "y" and choose:
        title = "Selections: " + str(selections_l)
        selection = gselect(choices_l, width=140, title=title, prompt="Add the desired column or q)uit: ", center=True)
        # dbug(selection)
        if selection in ("q", "Q", ""):
            ans = "n"
            break
        selections_l.append(selection)
        # dbug(selections_l)
    """--== SEP LINE ==--"""
    selections = selections_l  # need to correct all this TODO
    if selections == []:
        dbug('ask')
        return
    # dbug('ask')
    if not choose:
        # selections = cols[1:]
        selections = cols
    # dbug(cols)
    # dbug(selections)
    if window_size > 1:
        # smooths data - you must have more than 10+ lines of data...
        # dbug(cols[0])
        try:
            df = df.apply(lambda x: savgol_filter(x, window_size, 1) if x.name != cols[0] else x)
        except Exception as e:
            dbug(f"Smoothing failed... Error: {e}")
    colors = ["red", "blue", "green", "lightblue", "cyan", "yellow"]
    if len(selections) == 0:
        return
    if max:
        maxes = df.max()
    if mavgs:
        # dbug(f"selections: {selections}")
        df["50ma"] = df[selections[0]].rolling(window=50, min_periods=0).mean()
        df["200ma"] = df[selections[0]].rolling(window=200, min_periods=0).mean()
        selections.append("50ma")
        selections.append("200ma")
        df.dropna(inplace=True)
        last_50ma = round(df["50ma"].iloc[-1], 2)
        last_200ma = round(df["200ma"].iloc[-1])
    ax = df.plot(kind="line", xlabel=xlabel, y=selections, color=colors, figsize=(15, 5))
    ax.ticklabel_format(axis='y', style='plain')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Date")
    # plt.format_xdata = mdates.DateFormatter('%Y-%m XX')  # does nothing
    plt.style.use('seaborn')
    plt.tight_layout()
    if savefile != "":
        # NOTE!!!! this has to be called BEFORE plt.show !!!! NOTE #
        plt.savefig(f"{savefile}")
    # dbug("start plt.show()")
    plt.show()
    # dbug("end plt.show()")
    if max:
        if max:
            # dbug(selections)
            maxes = df.max()
            # dbug(maxes)
            # dbug(maxes[selections[0]])
        return {"max": maxes[selections[0]], "last_50ma": last_50ma, "last_200ma": last_200ma}
    return df
    # ### EOB def plot_file(filename):


def mmap_io(filename):
    """
    uses mmap to read a file
    """
    import mmap
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            text = mmap_obj.read()
            lines = text.splitlines()
            lines = [x.decode('utf8') for x in lines]
            return lines


# #################
# ### Main Code ###
# #################
def main(args):
    # #############
    """
    Usage:
        myprog [-hdtE]
        myprog -P <filename>

    Options:
        -h --help    show this help
        -d           debug
        -t           test
        -E           edit this file
        -P           plot file
    """
    handleOPTS(args)
    # lines = mmap_io("/etc/passwd")
    # dbug(lines)
    # for line in lines:
    #     print(line)


if __name__ == '__main__':
    args = docopt(main.__doc__, version=" 0.9")
    main(args)
