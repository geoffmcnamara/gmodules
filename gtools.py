#!/usr/bin/env python3
# vim: set syntax=none nospell:
# #####################
# Script name: gtools.py
# Created by: geoff.mcnamara@gmail.com
# Created on: 2018
# Purpose: this is a quick-n-dirty set of tools that might be useful
# ... much room for improvment and lots of danger points - not recommended for anything you care about  # noqa:
# ... use this file in anyway and all your data could be at risk ;)
# ... lots of debugging code still remains and legacy code that should be removed  # noqa:
# ... this file is constantly changing so nothing should depend on it ;)
# ... depends on python3!
# LICENSE = MIT
# WARNING: Use at your own risk! 
#          Side effects include but not limited: severe nosebleeds and complete loss of data. 
#          This file is subject to frequent change!
# Please contact me anytime. I willingly accept compliments and I tolerate complaints (most of the time).
# Requires: docopt, dbug.py, gftools.py, and others
# #####################################
# To see an overview: 
# python3 -m pydoc gtools3
# note: because dbug is pulled in with import you can call it drectly from this module as well, also funcname
# to have access:
# in bash --- export PYTHONPATH="${PYTHONPATH}:/home/geoffm/dev/python/gmodules"
# or
# import sys
# sys.path.append("/home/geoffm/dev/python/gmodules")
# #####################################

# ### IMPORTS ### #
import os
import sys
import shutil
import glob
# import platform
import re
# import readline
import subprocess
# import glob
from datetime import datetime  # , date
from math import ceil, floor
# import matplotlib.dates as mdates
# ### imports ######  #
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import sys
from urllib.request import urlopen
# import columnize
# try:
#     from Xdbug import dbug, funcname, lineno, ddbug
# except Exception as Error:
#     print(f"SPECIAL DEBUG: Error: {Error}")
#     """--== SEP_LINE ==--"""
import inspect
from inspect import (getframeinfo, currentframe, getouterframes, getfile)

# from colorama import init, Fore, Style
# from docopt import docopt
import time
try:
    import gio
except:
    pass
import requests
import time
import threading
from inspect import currentframe  # needed for f() [WIP]
import configparser
import itertools


# ### GLOBALS ### #
# console = Console()
dtime = datetime.now().strftime("%Y%m%d-%H%M")
SCRIPT = os.path.basename(__file__)
styles_d = {'normal': '0', 'bold': '1', 'bright': 1, 'dim': '2', 'italic': '3', 'underline': '4', 'blink': '5', 'fast_blink': '6', 'reverse': '7', 'crossed_out': '9'}
fg_colors_d = {'black': ";30", 
        'red': ";31", 
        'green': ";32",  # I don't like "their" green, should "my" green (;38) instead or even better is rgb(0,215,0)
        # 'green': ";38", 
        'yellow': ';33', 
        'blue': ';34', 
        'magenta': ';35', 
        'cyan': ';36', 
        'white': ';37', 
        'normal': '38', 
        'bold normal': ';39'}
#fg_colors_d = {'black': "30", 
#        'red': "31", 
#        'green': "32",  #  I don't like "their" green, should "my" green (;38) instead or even better is rgb(0,215,0)
#        # 'green': "38", 
#        'yellow': '33', 
#        'blue': '34', 
#        'magenta': '35', 
#        'cyan': '36', 
#        'white': '37', 
#        'normal': '38', 
#        'bold normal': '39'}
#
# bg_colors_d = {'black': ";40", 
        #         'red': ";41", 
        # 'green': ";42", 
        # 'yellow': ";43", 
        # "blue": ";44", 
        # 'magenta': ";45", 
        # "cyan": ";46", 
        # 'white': ";47", 
        # 'normal': ';48', 
        # 'normal1': ';49'}
bg_colors_d = {'black': "40", 
        'red': "41", 
        'green': "42", 
        'yellow': "43", 
        "blue": "44", 
        'magenta': "45", 
        "cyan": "46", 
        'white': "47", 
        'normal': '48', 
        'normal1': '49'}
# add 40 to make bright|bold
# RESET = "\x1b[0m"
# PRFX = "\x1b["
# log_fmt = '%(asctime)s:%(levelname)s:%(message)s'
# log_file = "/home/geoffm/" + "gtools3" + ".log"
# logging.basicConfig(format=log_fmt, filename=log_file, encoding="utf-8", level=logging.INFO)
# for the record: level can be (in increasing severity): DEBUG, INFO, WARNING, ERROR


# init(autoreset=True)  # don't have to RESET after a color print
# RED = Style.BRIGHT + Fore.RED
# DIM_RED = Style.DIM + Fore.RED
# GREEN = Style.BRIGHT + Fore.GREEN
# DIM_GREEN = Style.DIM + Fore.GREEN
# BLUE = Style.BRIGHT + Fore.BLUE
# DIM_BLUE = Style.DIM + Fore.BLUE
# BLACK = Style.BRIGHT + Fore.BLACK
# GRAY = Style.BRIGHT + Fore.LIGHTBLACK_EX
# CYAN = Style.BRIGHT + Fore.CYAN
# DIM_CYAN = Style.DIM + Fore.CYAN
# MAGENTA = Style.BRIGHT + Fore.MAGENTA
# DIM_MAGENTA = Style.DIM + Fore.MAGENTA
# YELLOW = Style.BRIGHT + Fore.YELLOW
# DIM_YELLOW = Style.DIM + Fore.YELLOW
# RESET = Style.RESET_ALL


# ############### #
# ### CLASSES ### #
# ############### #

# ############
class Spinner:
    # ########
    """
    purpose: prints a spinner in place
    input: msg="": str style='bar': ellipsis, pipe, box, arrow, clock, bar, balloons, moon, dot, braille, pulse
        prog: bool
        color: str
        txt_color: str
    requires:
        import sys
        import threading
        import itertools
    return: none
    use:
        with Spinner("Working...", style='bar')
            long_proc()
    """
    def __init__(self, message="", *args, delay=0.2, style="pipe", prog=False, **kwargs):
        """--== debugging ==--"""
        # dbug(f"class: Spinner {funcname()} style: {style} args: {args} kwargs: {kwargs}")
        # dbug(args)
        # dbug(kwargs)
        """--== config ==--"""
        # color = kvarg_val("color", kwargs, dflt="")
        self.color = color = kvarg_val(["color"], kwargs, dflt="")
        # self.colors = kvarg_val("colors", kwargs, dflt=[color])
        # if isinstance(color, list):
        self.colors = kvarg_val(["colors", "color"], kwargs, dflt=[self.color])
        if isinstance(self.color, list):
            self.colors = self.color
        else:
            self.COLOR = sub_color(self.color)
        # self.COLOR = sub_color(color)
        txt_color = kvarg_val(["txt_color", 'txt_clr'], kwargs, dflt="")
        self.TXT_COLOR = sub_color(txt_color)
        time_color = kvarg_val(["time_color", 'time_clr', 'elapsed_clr', 'elapsed_time_clr', 'elapsed_color', 'elapse_color', 'elapse_clr'], kwargs, dflt=txt_color)
        self.time_color = time_color
        # dbug(time_color)
        self.TIME_COLOR = sub_color(time_color)
        self.centered = bool_val(['center', 'centered'], args, kwargs, dflt=False)
        self.RESET = sub_color('reset')
        self.start_time = time.time()
        # self.elapsed_time = 0
        self.etime = bool_val(["etime", "show_elapsed", 'elpased_time', 'elapsed', 'time'], args, kwargs, dflt=False)
        # dbug(self.etime)
        self.style = style = kvarg_val(["style", 'type'], kwargs, dflt=style)
        # dbug(self.style)
        self.prog = bool_val("prog", args, kwargs, dflt=prog)
        self.style_len = kvarg_val(["length", "width"], kwargs, dflt=4)
        """--== set default ==--"""
        spinner_chrs = ['.', '.', '.', '.']  # the default will be ellipsis
        self.prog = True  # the default
        """--== SEP_LINE ==--"""
        if style in ('ellipsis', 'elipsis', 'elipses', 'ellipses'):  # for the spelling challenged like me
            spinner_chrs = ['.', '.', '.', '.']
            # spinner_chrs = ['.' * self.style_len]
            self.style_len = len(spinner_chrs)
            self.prog = True
            # dbug(f"Style: {self.style} prog: {self.prog} style_len: {self.style_len} color: {self.color} time_color: {self.time_color}")
        if style == "pipe":
            spinner_chrs = ['/', '-', '\\', '|']
            self.prog = False
        if style == "arrow":
            # spinner_chrs = ['⬍', '⬈', '⮕', '⬊', '⬍', '⬋', '⬅', '⬉']
            spinner_chrs = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
            self.prog = False
        if style == 'clock':
            spinner_chrs = ['🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢' '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦']
            self.style_len = len(spinner_chrs)
            self.prog = False
        if style == 'moon':
            spinner_chrs = ['🌑', '🌘', '🌗', '🌖', '🌕', '🌔', '🌓', '🌒']
            self.prog = False
        if style == 'vbar':
            spinner_chrs = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂', '▁', ' ']
            self.style_len = len(spinner_chrs)
        if style == 'bar':
            spinner_chrs = ['█', '█', '█', '█', '█']
            self.prog = True
            self.style_len = 20
        if style == 'braille':
            spinner_chrs = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
            self.prog = False
        if style == 'dot':
            spinner_chrs = ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈']
            self.prog = False
        if style == 'box':
            spinner_chrs = ['◰', '◳', '◲', '◱']
            self.prog = False
        if style == 'balloons':
            spinner_chrs = ['.', 'o', 'O', '@', '*']
            self.prog = False
        if style == 'pulse':
            spinner_chrs = ['.', 'o', 'O', 'o']
            self.prog = False
        if style == 'batball':
            spinner_chrs = ['q', 'p', 'b']
            self.prog = False
        # self.style_len = len(spinner_chrs)
        self.chr_cnt = 1
        self.clr_cnt = 0
        self.spinner = itertools.cycle(spinner_chrs)
        self.delay = kvarg_val("delay", kwargs, dflt=delay)
        self.busy = False
        self.spinner_visible = False
        if self.centered:
            spinner_len = 1
            if self.prog:
                spinner_len = len(spinner_chrs)
            shift = -(spinner_len)
            message = printit(message, 'centered', prnt=False, rtrn_type="str", color=txt_color, shift=shift)
        sys.stdout.write(message)
    """--== SEP_LINE ==--"""
    def write_next(self):
        # write the next chr in spinner_chrs
        with self._screen_lock:
            if not self.spinner_visible:
                if len(self.colors) > 1:
                    color = self.colors[self.clr_cnt]
                    self.COLOR = sub_color(color)
                    # dbug(f"color: {color} chr_cnt: {self.clr_cnt} repr(self.COLOR): {repr(self.COLOR)}") 
                    self.clr_cnt += 1
                    if self.clr_cnt > len(self.colors) - 1:
                        self.clr_cnt = 0
                spinner_chr = self.COLOR + str(next(self.spinner)) + self.RESET
                if self.style == 'clock':
                    if self.chr_cnt >= self.style_len:
                        self.chr_cnt = 0
                    else:
                        self.chr_cnt += 1
                if self.style == 'clock':
                    if nclen(spinner_chr) > 1:
                        # I have absolutely no idea why this is needed but it is. Believe me I beat this to death - it causes a 'blink'
                        # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                        sys.stdout.write('  ')
                    else:
                        # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                        sys.stdout.write(spinner_chr)
                else:
                    # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                    sys.stdout.write(spinner_chr)
                # sys.stdout.write(spinner_chr)
                self.spinner_visible = True
                sys.stdout.flush()
                """--== SEP_LINE ==--"""
    def spin_backover(self, cleanup=False):
        with self._screen_lock:
            # _self_lock is the thread
            if self.spinner_visible:
                if not self.prog:
                    # backover chr if not prog (progressive)
                    # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len}")
                    sys.stdout.write('\b')
                else:
                    # if progressive then ...
                    # clr_cnt = self.chr_cnt % len(self.colors)
                    # self.COLOR = self.colors[clr_cnt]
                    # dbug(self.COLOR)
                    # dbug(f"prog: {self.prog} chr_cnt: {self.chr_cnt} style_len: {self.style_len}")
                    self.chr_cnt += 1
                    if self.chr_cnt > self.style_len:
                        # if we hit the len of style_len... print elapsed time... then...
                        if self.etime:
                            elapsed_time = round(time.time() - self.start_time, 2)
                            elapsed_time = f"{elapsed_time:>6}"  # if we go over 999 seconds we will be in trouble with the length
                            # dbug(elapsed_time)
                            sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                            # time.sleep(self.delay)
                            sys.stdout.write("\b" * (len(str(elapsed_time)) + 1))
                            # sys.stdout.write(self.RESET)
                            sys.stdout.flush()
                        while self.chr_cnt > 1:
                            # while chr_cnt is more than 1... back over
                            self.chr_cnt -= 1
                            sys.stdout.write("\b")
                            sys.stdout.write(" ")
                            sys.stdout.write("\b")
                            time.sleep(self.delay)
                            sys.stdout.flush()
                        sys.stdout.write(" ")
                        sys.stdout.write("\b")
                        sys.stdout.flush()
                        time.sleep(self.delay)
                        # self.chr_cnt = 0
                if self.style in ('clock', 'moon'):
                    sys.stdout.write('\b')
                # if self.chr_cnt > self.style_len:
                #     #dbug("how did we get here")  # not sure if this section is needed
                #     if self.etime:
                #         elapsed_time = round(time.time() - self.start_time, 2)
                #         sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                sys.stdout.write('\x1b[?25l')  # Hide cursor
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')              # overwrite spinner with blank
                    sys.stdout.write('\r')             # move to next line
                    sys.stdout.write("\x1b[?25h")      # Restore cursor
                sys.stdout.flush()
                """--== SEP_LINE ==--"""
    def spin_proc(self):
        while self.busy:
            self.write_next()
            if self.etime and not self.prog:
                elapsed_time = round(time.time() - self.start_time, 2)
                elapsed_time = f"{elapsed_time:>6}"  # this is to assure proper back over length - if we go over 999 seconds we are in trouble with the length
                sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                # dbug(len(elapsed_time))
                # time.sleep(self.delay)
                sys.stdout.write("\b" * (len(elapsed_time) + 1))
            time.sleep(self.delay)
            self.spin_backover()
            """--== SEP_LINE ==--"""
    def __enter__(self):
        try:
            if sys.stdout.isatty():
                self._screen_lock = threading.Lock()
                self.busy = True
                self.thread = threading.Thread(target=self.spin_proc)
                self.thread.start()
        except Exception as e:
            pass
        """--== SEP_LINE ==--"""
    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.busy = False
        if sys.stdout.isatty():
            # self.busy = False
            # end_time = time.time()
            # self.elapsed_time = (end_time - self.start_time)
            # sys.stdout.write(f"({self.elapsed_time})")
            self.spin_backover(cleanup=True)
            sys.stdout.write('\r')
            sys.stdout.flush()
            print()  # ??? tries to force the cursor to the next line
        else:
            sys.stdout.write("\x1b[?25h")     # Restore cursor
            sys.stdout.write('\r')
            sys.stdout.flush()
            print()  # ??? tries to force the cursor to the next line
    # ### class Spinner: ### #


# #########################
class Transcript:
    # #####################
    """
    Transcript - direct print output to a file, in addition to terminal. It appends the file target
    Usage:
        import transcript
        transcript.start('logfile.log')
        print("inside file")
        transcript.stop()
        print("outside file")
    Requires:
        import sys
        class Transcript
        def transcript_start
        def transcript_stop
    This should be moved to gtools.py
    """
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a")
    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)
    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass
    # ### class Transcript: ### #


# #############################
def transcript_start(filename, *args, **kwargs):
    # ##########################
    """
    Start class Transcript(object=filename),
    appending print output to given filename
    """
    prnt = bool_val(["prnt", 'printit', 'show'], args, kwargs, dflt=False)
    centered_b = bool_val(['centered'], args, kwargs, dflt=False)
    if prnt:
        printit(f"Starting transcript out to {filename}", centered=centered_b)
    sys.stdout = Transcript(filename)


# ########################
def transcript_stop(*args, **kwargs):
    # ###################
    """
    Stop class Transcript() and return print functionality to normal
    """
    prnt = bool_val(["prnt", 'printit', 'show'], args, kwargs, dflt=False)
    centered_b = bool_val(['centered'], args, kwargs, dflt=False)
    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal
    if prnt:
        printit("Stopping transcript out", centered=centered_b)


def transcript_demo():
    file = "./gtools3-transcript-demo.out"
    if file_exists(file):
        printit(f"Removing existing file: {file}", 'centered')
        os.remove(file)
    printit(f"We are now going to write all output to file: {file}", 'centered')
    transcript_start(file, 'prnt', 'centered')
    printit("This output will also be found in file: {file}", 'boxed', 'centered')
    transcript_stop('prnt', 'centered')
    printit(f"Here are the contents of file: {file}", 'centered')
    contents = cat_file(file)
    printit(contents)



# #######################################
class ThreadWithReturn(threading.Thread):
    # ###################################
    """
    requires: 
        import threading
    usage:
        run_cmd_threaded(cmd)
        which does this ...
        dbug("Just getting started...")
        cmd = "/home/geoffm/ofrd.sh"
        t1 = ThreadWithReturn(target=run_cmd, args=(cmd,))
        t1.start()
        dbug("Done")
        result = t1.join()
        dbug(result)
    """
    def __init__(self, *init_args, **init_kwargs):
        threading.Thread.__init__(self, *init_args, **init_kwargs)
        self._return = None
    def run(self):
        self._return = self._target(*self._args, **self._kwargs)
    def join(self):
        threading.Thread.join(self)
        return self._return


# #############
class DoMenu:
    # #########
    """
    deprecated for gselect
    NOTE: to test this: echo 1 | python3 -m doctest -v ./gtools.py
    Use:
    Make sure you have the functions called for:
      do_item1() do_item2() do_item3() do_item4() etc
    Note: this is a dictionary ... hence do_select({title: function})
    # >>> main_menu = DoMenu("Main")
    # >>> main_menu.add_selection({"item1":cls})
    # >>> main_menu.do_select()  # doctest: +ELLIPSIS
    # ============================================================
    #                             Main
    # ============================================================
    #                            1 item1...
    # ...
    """
    # #####################
    def __init__(self, name):
        self.name = name
        # dbug(f"args:{self.args}")
        self.selections = {}
        self.choices = {}
        self.length = 60
        self.cls = False
        self.center = True

    def add_selection(self, selection):
        """
        selection needs to be a dictionary element ie:
          {"get this done":do_it} where do_it is actually a function name
        """
        # dbug(f"selection:{selection}")
        if not isinstance(selection, dict):
            dbug("Selection: " + selection + "must be a dictionary")
        self.selections.update(selection)
    """--== SEP_LINE ==--"""
    def do_select(self):
        if self.cls:
            cls()
        cnt = 0
        # dbug(f"self.itms:{self.itms}")
        # dbug(f"self.selections:{self.selections}")
        mmax = max(self.selections)
        mmax_len = len(mmax)
        side_len = mmax_len / 2
        position = int((self.length + 2) / 2 - side_len)
        # dbug(f"mmax:{mmax} mmax_len:{mmax_len} side_len:{side_len} position:{position}")  # noqa:
        do_title_three_line(self.name, self.length)
        # do_line("=",self.length)
        # do_title(self.name,"+",self.length)
        # do_line("=",self.length)
        #
        self.add_selection({"Quit [Qq] or blank": exit})
        for k, v in self.selections.items():
            cnt += 1
            print(f"{cnt:{position}} {k}")
            # print("{:position}} {}".format(cnt, k))
            # dbug(f"k:{k} v:{v}")
            self.choices.update({str(cnt): v})
        doline("=", self.length)
        # prompt = input(f"Please make your selection [q=quit or 1-{cnt}]: ")
        prompt = input("Please make your selection [q=quit or 1-{}]: ".format(cnt))
        ans = input(centered(prompt, self.length))
        doline("=", self.length)
        # dbug(f"Selected: {ans} Action: {self.choices[ans]}")
        # dbug(f"self.choices:{self.choices}")
        if ans in ("q", "Q", ""):
            sys.exit()
        ret = self.choices[ans]()
        # dbug(f"returning ret: {ret}")
        return ret
    # EOB class DoMenu:


# ### FUNCTIONS ### #

# ################
def funcname(n=0):
    # ############
    """
    purpose: returns current function name - primarily used for debugging
    """
    return sys._getframe(n + 1).f_code.co_name


# ###########
def lineno():
    # #######
    """
    purpose: returns current line number - primarily used for debugging
    """
    cf = currentframe()
    return str(cf.f_back.f_lineno)


# ##############################################
def ddbug(msg="", *args, ask=False, exit=False):
    # ##########################################
    """
    purpose: this is for use by dbug only... as dbug can't call itself
    """
    # dbug = DBUG if DBUG else 1
    # my_centered = True if 'center' in args else False
    # my_centered = True if 'centered' in args else centered
    ask = True if 'ask' in args else False
    exit = True if 'exit' in args else False
    # cf = currentframe()
    filename = str(inspect.getfile(currentframe().f_back))
    filename = os.path.basename(filename)
    fname = str(getframeinfo(currentframe().f_back).function)
    fname = os.path.basename(fname)
    lineno = str(inspect.currentframe().f_back.f_lineno)
    # msg = "DEBUG: [" + {fname} + ":" + {lineno} + "] " + {msg}
    # if file:
    #     msg = "DEBUG: [" + filename + ";" + fname + "(..):" + lineno + "] " + msg
    # else:
    #     msg = "DEBUG: [ " + str(fname) + "():" + str(lineno) + " ] " + str(msg)
    msg = f"*** DDBUG ***: [{filename}; {fname} (..): {lineno} ] {msg}"
    # from gtools3 import printit  # imported here to avoid circular referece
    try:
        print(msg)
    except Exception as e:
        print(f"print({msg}) failed Error: {e}")
        print(msg)
    if ask:
        from gtools3 import askYN
        askYN()
    if exit:
        sys.exit()
    return msg
    # ### EOB def ddbug(msg="", *args, ask=False, exit=False): ### #


# ############
def dbug(xvar="", *args, exit=False, ask=False, prnt=True, **kwargs):
    # ########
    """
    To test run: python3 -m doctest -v dbug.py
    # >>> a = "xyz"
    # >>> dbug_var(a)
    DEBUG: [dbug.py; <module>:1] a:xyz
    '1'
    """
    """--== Imports ==--"""
    from gtools3 import bool_val, askYN, kvarg_val, boxed, centered  # kvarg_val 
    """--== Config ==--"""
    center = bool_val(['center', 'centered'], args, kwargs) 
    box = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    color = kvarg_val('color', kwargs, dflt='')
    box_color = kvarg_val('box_color', kwargs, dflt="bold white on rgb(60,60,60)")
    # if 'center' in args or 'centered' in args:
    #     center = True
    DBUG = kvarg_val(['dbug', 'DBUG'], kwargs, dflt=True)  # True unless specified as False
    if not DBUG:
        # the idea here is if dbug looks like this: {where DBUG is True or >0) dbug(..., dbug=DBUG) then this func will honor the value of DBUG (ie True or False)
        # this should ease the pain for change ... now you can do this
        # DBUG = bool_val('dbug', args)
        # and then dbug(f"whatever here", dbug=DBUG)
        # ddbug(f"DBUG: {DBUG} therefore I am returning [empty handed sort of speak]")
        # further... you could put DBUG = 0 (or False) in GLOBAL vars and use docopts to turn on or off DBUG
        return
    EXIT = bool_val('exit', args, kwargs, dflt=False)
    ask_b = bool_val('ask', args, kwargs, dflt=False)
    lineno_b = bool_val(['lineno_b', 'lineno', 'line_no', 'line_number'], args, kwargs, dflt=False)
    here_b = bool_val('here', args, kwargs, dflt=False)
    if str(xvar) == 'lineno':
        lineno_b = True
    if str(xvar) == 'here':
        here_b = True
    if str(xvar) == 'ask':
        ask_b = True
        # see below where msg_literal gets changed when it is == 'ask'
    # fullpath filename
    i_filename = str(inspect.getfile(currentframe().f_back))
    # filename without path
    filename = os.path.basename(i_filename)
    # fname = function name
    fname = str(getframeinfo(currentframe().f_back).function)
    lineno = str(inspect.currentframe().f_back.f_lineno)
    if lineno_b:
        return lineno
    if here_b:
        # if 'only' in str(xvar).lower():
        #    return f"{filename}:{fname}:{lineno}"
        # if 'now' in str(xvar).lower():
        #    return f"DEBUG: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{filename}:{fname}:{lineno}]"
        return f"DEBUG: [{filename}:{fname}:{lineno}]"
    # this inconsistently holds what we want for the most part ...just wrong format
    # you would have to put this directly into your code and include a msg
    # ie eg:  <frame at 0x7f4d6e4b25e0, file '/home/geoffm/././t.py', line 3000, code tdbug>
    frame = inspect.currentframe().f_back
    def do_prnt(rtrn_msg, *args, ask=ask_b):  # , ask=ask_b, centered=centered):
        to_prnt = f"{rtrn_msg}"
        if "\n" in to_prnt:
            to_prnt = "\n" + to_prnt
        to_prnt = f"DEBUG: [{filename}:{fname}:{lineno}] {rtrn_msg}"
        if box:
            to_prnt = boxed(to_prnt, color=color, box_color=box_color)
        if center:
            # num_rows, columns = os.popen("stty size", "r").read().split()
            # lfill = (int(columns) - len(to_prnt)) // 2
            # to_prnt = " " * lfill + to_prnt
            to_prnt = centered(to_prnt)
        if isinstance(to_prnt, list):
            for l in to_prnt:
                print(l)
        else:
            print(f"{to_prnt}")
        if ask_b:
            if not askYN("Continue?: ", "y", centered=center):
                sys.exit()
        if EXIT:
            sys.exit()
        # title = kvarg_val('title', kvargs, "")
    line_literal = inspect.getframeinfo(frame).code_context[0].strip()  # the literal string including dbug(...)
    msg_literal = re.search(r"\((.*)?\).*", line_literal).group(1)  # ?non-greedy search
    # ddbug(f"msg_literal: {msg_literal}")
    if msg_literal.replace("'", "") == 'ask' or msg_literal.replace('"', '') == "ask":
        # ddbug(f"msg_literal: {msg_literal} args: {args}")
        ask_b = True
        rtrn_msg = "Enter or 'y' to continue... anything else to exit... "
        to_prnt = f"DEBUG: [{filename}:{fname}:{lineno}] {rtrn_msg}"
        if not askYN(to_prnt):
            sys.exit()
        return
    try:
        import pyparsing as pp
        all_args = pp.commaSeparatedList.parseString(msg_literal).asList()
        msg_literal = all_args[0]
        import abracadabra
    except Exception as Error:
        all_args = msg_literal.split(",")
        msg_literal = all_args[0]
    lvars = inspect.currentframe().f_back.f_locals
    if msg_literal.startswith('f"') or msg_literal.startswith("f'"):
        do_prnt(xvar, args, ask=ask_b)
        return
    if msg_literal.startswith('"') or msg_literal.startswith("'"):
        # ddbug(f"msg_literal: {msg_literal}")
        msg_literal = msg_literal[1:-1]
    for k, v in lvars.items():
        # ddbug(f"testing msg_literal: {msg_literal} against k: {k}")
        if msg_literal == k:
            rtrn_msg = f"{msg_literal}: {xvar}"
            do_prnt(rtrn_msg, args, ask=ask_b)
            return
    # ddbug(f"msg_literal: {msg_literal}")
    try:
        import pandas as pd
        if isinstance(xvar, pd.DataFrame) or isinstance(xvar, pd.core.series.Series):
            rtrn_msg = f"{msg_literal}: {xvar}"
            do_prnt(rtrn_msg, args, ask=ask_b)
            return  # yes, this return is needed otherwise bool prnts 2x
    except Exception as e:
        ddbug(f"Error: {e}")
    # ddbug(f"msg_literal: {msg_literal}")
    if msg_literal != xvar or not isinstance(msg_literal, str):
        # ddbug(f"msg_literal: {msg_literal}")
        if isinstance(xvar, type):
            rtrn_msg = f"{msg_literal}: {xvar}"
            do_prnt(rtrn_msg, args, ask=ask_b)
            return  # yes, this return is needed otherwise bool prnts 2x
        try:
            if re.search(r'^f["].*"$', msg_literal) or re.search("^'.*'$", msg_literal):
                # catches an f-strg (assumes that it is an f-str
                rtrn_msg = xvar  # default to this
                do_prnt(rtrn_msg, args, ask=ask_b)
                return
            else:
                # ddbug(f"msg_literal: {msg_literal} xvar: {xvar}")
                # if msg_literal == 'ask':
                if msg_literal.replace("'", "") == 'ask' or msg_literal.replace('"', '') == "ask":
                    rtrn_msg = ""
                    ddbug(f"rtrn_msg: {rtrn_msg}")
                else:
                    rtrn_msg = f"{msg_literal}: {xvar}"
                do_prnt(rtrn_msg, args, ask=ask_b)
                return
        except Exception as Error:
            rtrn_msg = f"{msg_literal}: {xvar}"
            ddbug(rtrn_msg)
            do_prnt(rtrn_msg, args, ask=ask_b)
            return
        return
    rtrn_msg = f"{msg_literal}"
    do_prnt(rtrn_msg, args, ask=ask_b)
    return
    # ### EOB def dbug(): ### #


# # ################################
# def dbug(msg="", *args, **kwargs):
#     # ############################
#     """
#     purpose: used for debugging
#     use: msg = "This is my message"
#     -    dbug(msg)           <-- displays DEBUG: [file:function:line] msg: This is my message
#     -    dbug(msg, 'ask')    <-- displays DEBUG: [file:function:line] msg: This is my message - and asks if you want to Continue
#     -    dbug('ask')         <-- displays DEBUG: [file:function:line] - and asks if you want to continue
#     -    footer=dbug('here') <-- displays nothing but returns DEBUG: [file:function:line]
#     options: boxed, centered, box_color=..., 'ask', 'here' 
#     returns: DEBUG: [filename:function_name:line_number] {msg}
#     """
#     """--== debug ==--"""
#     funcname()
#     # ddbug(f"We are in dbug() with msg: {msg} args: {args} and kwargs: {kwargs}")
#     """--== SEP_LINE ==--"""
#     centered_b = bool_val(['centered', 'center'], args, kwargs, dflt=False)
#     boxed_b = bool_val(['boxed', 'box'], args, kwargs, dflt=False)
#     ask_b = bool_val(['ask'], args, kwargs, dflt=False)
#     box_color = kvarg_val(["box_clr", 'box_color'], kwargs, dflt="")
#     """--== SEP_LINE ==--"""
#     cf = currentframe()
#     frame = cf.f_back
#     line_literal = inspect.getframeinfo(frame).code_context[0].strip()  # the literal string including dbug(...)
#     msg_literal = re.search(r"\((.*)?\).*", line_literal).group(1)  # ?non-greedy search
#     ddbug(f"msg_literal: {msg_literal} type(msg_literal): {type(msg_literal)} msg: {msg} args: {args} len(args): {len(args)}")
#     if "), " in msg_literal:
#         msg_literal = msg_literal.split("), ", 1)[0] + ")"
#         # ddbug(f"msg_literal): {msg_literal}")
#     # ddbug(f"msg_literal: {msg_literal} type(msg_literal): {type(msg_literal)} msg: {msg} len(args): {len(args)}")
#     i_funcname = str(getframeinfo(currentframe().f_back).function)
#     i_filename = getfile(cf.f_back)
#     filename = os.path.basename(i_filename)
#     mylineno = cf.f_back.f_lineno
#     pre_msg = f"DEBUG: [{filename}:{i_funcname}:{mylineno}] " 
#     if isinstance(msg, str) and msg == 'ask':
#         askYN(pre_msg + " Continue? ", 'quit')
#         return str(pre_msg)
#     if isinstance(msg, str) and msg == 'here':
#         # ddbug(f"Returning pre_msg: {pre_msg} msg: {msg} msg_literal: {msg_literal}")
#         return str(pre_msg)  # returns dbug string 
#     # ddbug(f"msg_literal: {msg_literal} msg: {msg}")
#     if isinstance(msg_literal, str) and msg_literal.endswith(")"):
#         msg = f"{msg_literal}: {msg}"
#         # ddbug(f"just set msg: {msg}")
#     lvars = cf.f_back.f_locals
#     for k, v in lvars.items():
#         # ddbug(f"k: {k} v: {v} msg_literal: {msg_literal}")
#         if k == msg_literal:
#             # ddbug("k: {k} == msg_literal: {msg_literal}")
#             msg = f"{msg_literal}: {msg}"
#         # else:
#             # # ddbug(f"We got here with msg_literal: {msg_literal} and msg: {msg}")
#             # msg = msg_literal + ": " + str(msg)
#     msg = pre_msg + str(msg)
#     lines = []
#     if boxed_b or centered_b:
#         if boxed_b:
#             lines = boxed(msg, box_color=box_color)
#         if centered_b:
#             lines = centered(lines)
#         for line in lines:
#             print(line)
#         if ask_b:
#             askYN(msg, 'quit', centered=centered_b)
#     else:
#         if ask_b:
#             askYN(msg, centered=centered_b)
#         else:
#             printit(msg, boxed=boxed_b, centered=centered_b, box_color=box_color)
#     # ### def dbug(msg="", *args, **kwargs): ### #
# 

def dbug_demo():
    """
    purpose: A quick-n-dirty demo of using dbug()
    """
    msg = "This will use: dbug(f'msg: {msg} msg_len: {len(msg)}"
    print(f"NOTE: msg = {msg}")
    dbug(f"msg: {msg} msg_len: {len(msg)}")
    print("-" * 40)
    msg = "This will use: dbug(msg)"
    print(f"NOTE: msg = {msg}")
    dbug(msg)
    print("-" * 40)
    msg = "This will use: dbug(f'msg: {msg}')"
    print(f"NOTE: msg = {msg}")
    dbug(f"msg: {msg}")
    print("-" * 40)
    msg = "This will use dbug(len(msg))"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg))
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed')
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed', 'centered')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed', 'centered')
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed', 'centered', box_color='red! on black')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed', 'centered', box_color="red! on black")
    print("-" * 40)
    msg = "This will use dbug(type(['one', 'two', 'three']), 'boxed')"
    print(f"NOTE: msg = {msg}")
    dbug(type(['one', 'two', 'three']), 'boxed')
    print("-" * 40)
    msg = "This will use dbug(type(['one', 'two', 'three']), 'ask')"
    print(f"NOTE: msg = {msg}")
    dbug(type(['one', 'two', 'three']), 'ask')
    print("-" * 40)

# #################
def funcname(n=0):
    # #############
    """
    Use: eg:
    from dbug import dbug, fname
    def myfunc():
        dbug(f"This is function name: {funcname()}")
        pass
    """
    # using this sys method is faster than inspect methods
    return sys._getframe(n + 1).f_code.co_name


# #######################################
def gselect(selections, *args, **kwargs):
    # ###################################
    """
    purpose: menu type box for selecting by index, key, or value
    required:
    - selections: list or dictionary
    options: 
    - prompt, center, title, footer, dflt, width, box_color, color, show, 
    - rtrn='k|key' or 'v|val|value' <-- tells gselect whether you want it to return a key or a value from a supplied list or dictionary
            This is an important option and allows control over what gets returned. See the Notes below.
    - show="k|key" or 'v|val|value' <-- tells gselect whether to display a list of keys or a list of values
    - quit: bool <-- add "q)uit" to the prompt and will do a sys.exit() if ans in ("q","Q","exit")
    - multi <-- allows multiple selections and returns them as a list
    - default|dflt='':   # allows you to /declare a default if enter is hit
    - quit
    - rtrn="v" str       # return the selected 'k'ey or 'v'alue
    - show='k' str       # wh/ether to show or display 'k'eys or 'v'alues
    - title
    - footer
    - color
    - box_color
    - width
    Notes: with a simple list by default it will return the value in the list - if you want the menu number then use rtrn='k' option!!!
    returns: either key(s) or value(s) as a string or list (if multiple), your choice
    examples:
    > tsts = [{1: "one", 2: "two", 3: "three"},["one", "two", "three"], {"file1": "path/to/file1", "file2": "path/to/file2"} ]
    > for tst in tsts:
    ...     ans = gselect(tst, rtrn="v")
    ...     ans = gselect(tst, rtrn="k")
    """
    """--== dbug ==--"""
    # dbug(funcname())
    # dbug(kwargs)
    # dbug(selections)
    """--== Config ==--"""
    prompt = kvarg_val("prompt", kwargs, dflt="Please select")
    center = bool_val(["center", "centered"], args, kwargs, dflt=False)
    title = kvarg_val("title", kwargs, dflt=" Selections ")
    footer = kvarg_val("footer", kwargs, dflt="")
    default = kvarg_val(["dflt", "default"], kwargs, dflt="")
    width = kvarg_val(["width"], kwargs, dflt=0)
    box_color = kvarg_val(["box_color"], kwargs, dflt="bold white on rgb(60,60,60)")
    color = kvarg_val(["color"], kwargs, dflt="white on rgb(20,20,30)")
    quit = bool_val(["quit", "exit"], args, kwargs, dflt=False)
    rtrn = kvarg_val(["return", "rtrn"], kwargs, dflt="v")  # can be key|k or value|v|val
    show = kvarg_val(['show', 'show_type', 'shw', 'shw_type'], kwargs, dflt="k")
    multi = bool_val(["choose", "choices", "multi"], args, kwargs, dflt=False)
    # dbug(quit)
    """--== Init ==--"""
    selections_d = {}
    lines = []
    rtrn_ans = ""
    keys = []
    vals = []
    """--== Type Mngmt ==--"""
    " we will turn a list into a dict "
    if isinstance(selections, list):
        for n, elem in enumerate(selections, start=1):
            selections_d[str(n)] = elem
            keys.append(str(n))
            vals.append(elem)
    if isinstance(selections, dict):
        # dbug(selections)
        n = 1
        for k, v in selections.items():
            # dbug(f"n: {n} k: {k} v: {v}")
            if show in ("v", "val", "value", "values"):
                selections_d[k] = v
            else:
                selections_d[str(n)] = k
            keys.append(k)
            vals.append(v)
            n += 1
    """--== Process ==--"""
    # dbug(selections_d)
    elems = list(selections_d.values())
    # dbug(elems)
    for n, elem in enumerate(elems, start=1):
        lines.append(f"{n:>3}). {elem}")
    if isinstance(width, str):
        col_num = get_columns()
        if width.endswith("%"):
            width_pct = int(width.replace("%", ""))
            width = int(col_num * (width_pct/100))
            # dbug(f"width: {width} col_num: {col_num} width_pct: {width_pct}")
        else:
            width = int(col_num) - 2
        # dbug(f"width: {width} col_num: {col_num}")
    if int(width) == 0:
        col_num = get_columns()
        width = int(col_num * .8)
    if int(width) > 0:
        lines = gcolumnize(lines, width=width, color=color)
    # dbug(width)
    def display_selections():
        printit(lines,
            "boxed",
            center=center,
            title=title,
            footer=footer,
            box_color=box_color,
            color=color)
    if quit:
        prompt = prompt + " or q)uit"
    if default != "":
        prompt += f" default: [{default}] "
    prompt += ": "
    # dbug(f"multi: {multi} default: {default}")
    if multi:
        selected_l = []
        footer_l = []
        ans = "none"
        while ans not in ("q", "Q"):
            # dbug(rtrn)
            if footer == "":
                footer = " Please add selections one at a time. "
            display_selections()
            if center:
                ans = cinput(prompt, center=center, quit=quit)
            else:
                ans = input(prompt)
                if ans in ("q", "Q", "exit"):
                    sys.exit()
            if ans in ("q", "Q", ""):
                if ans == "":
                    ans = default
                break
            # dbug(ans)
            if rtrn in ("k", "K", "keys"):
                dbug(ans)
                ans = keys[int(ans)]
                dbug(ans)
            # else:
            #     ans = vals[int(ans)]
            footer_l.append(int(ans))
            footer = f" Selected: {footer_l} "
            ans = vals[int(ans) - 1]
            # dbug(ans)
            selected_l.append(ans)
        # dbug(f"Returning: {selected_l}")
        return selected_l
    else:
        display_selections()
        if center:
            ans = cinput(prompt, center=center, quit=quit)
        else:
            ans = input(prompt)
        if ans == "":
            ans = default
        # ans = cinput(prompt, center=center, quit=quit)
    # dbug(repr(ans))
    if quit and ans in ("q", "Q", "quit", "Quit", "exit"):
        sys.exit()
    if not isnumber(ans):
        # dbug(f"Returning ans: {ans}")
        return ans
    # dbug(ans)
    ans = int(ans) - 1
    # dbug(ans)
    if rtrn in ("k", "key", "keys"):
        # dbug(ans)
        rtrn_ans = keys[ans]
    if rtrn in ("v", "val", "vals", "values", "value"):
        # dbug(vals)
        rtrn_ans = vals[ans]
    # dbug(f"Returning rtrn_ans: {rtrn_ans}")
    return rtrn_ans
    # ### EOB def gselect(selections, *args, **kwargs): ### #


def gselect_demo():
    my_l = list_files("./", "*.*")
    my_l = my_l[:3]
    my_d = {"one": "ONE", "two": "TWO", "three": "THREE"}
    ans = ""
    printit(f"Using a simple list: {my_l[:3]} for gselect; center the display and offer q)uit as part of the prompt", 'centered')
    ans = gselect(my_l, 'centered', 'quit', rtrn="v", title="Example of gselect using a simple list", footer=dbug('here'))
    dbug(f"Your ans: {ans}", 'centered')
    dbug("Now lets show what can be done with a dictionary", 'centered')
    printit(f"Using a dictionary: {my_d} for gselect; center the display and offer q)uit as part of the prompt", 'centered')
    ans = gselect(my_d, 'centered', 'quit', rtrn="v", title="Example of gselect using a simple list", footer=dbug('here'))
    dbug(f"Your ans: {ans}", 'centered')
    return



# # ##############
# def changelog(file=__file__):
#     # ##########
#     """
#     prints out the global CHANGELOG string with dbug centered
#     this is for fun - shows off Live too
#     """
#     from rich.table import Table
#     from rich.live import Live
#     from rich.align import Align
#     try:
#         dbug(CHANGELOG, 'centered')
#     except Exception as Error:
#         dbug(Error, 'centered')
#     table = Table(header_style="on rgb(50,50,50)", title="Functions", border_style="bold white on rgb(50,50,60)", row_styles=["on black", "on rgb(20,20,20)"])
#     # table = rtable([], 'header', 'center", title="funcs", prnt=False)
#     table_centered = Align.center(table)
#     table.add_column("funcname", style="bold cyan on black") 
#     table.add_column("funcname.__doc__", style="yellow")
#     funcs = []
#     with open(file) as f:
#         lines = f.readlines()
#         with Live(table_centered, refresh_per_second=4) as live:
#             for l in lines:
#                 if l.startswith("def"):
#                     funcs.append(l)
#                     l = l.rstrip("\n")
#                     funcname = re.search(r"def (.*?)\(.*", l).group(1)
#                     if funcname in ("handleOPTS", 'changelog', "main", "docvars"):
#                         continue
#                     fdoc = eval(f"{funcname}.__doc__")
#                     table.add_row(funcname, fdoc)
#                     time.sleep(0.25)
# 


# #######################################
def kvarg_val(key, kwargs_d={}, dflt=""):
    # ###################################
    """
    purpose: returns a value when the key in a key=value pair matches any key given
    NOTE: key can be a string or a list of strings 
    option: dflt="Whatever default value you want"
    use: used in function to get a value from a kwargs ky=value pair
    - eg:
        def my_function(*args, **kwargs):
            txt_center = kvarg_val(["text_center", "txt_cntr", "txtcntr"], kwargs, dflt=1)
    - so if you call my_function(txt_center=99) then txt_center will be set to 99
    ---
    If any key in the list is set = to a value, that value is returned
    see: bool_val which process both args and kvargs and returns bool_val
    input key(string), kvargs_d(dictionary of key,vals), default(string; optional)
    purpose: return a value given by a key=value pair using a matching key (in key list if desired)
    options:
    -  key provided can be a string or a list of strings
    -  dflt="Whatever default value you want - can be a string, list, int, float... whatever" <-- this is optional, if not declared "" is returned
    if key in kvargs:
        return val
    else:
        return default
    returns str(key_val) or default_val(which is "" if none is provided)
    """
    # dbug(funcname)
    # print(kwargs_d)
    # dbug(default)
    my_val = ""
    my_default = ""
    if not isinstance(kwargs_d, dict):
        dbug(f"Supplied kwargs_d: {kwargs_d} MUST be a dictionary! Returning...")
        return
    if 'dflt' in kwargs_d:
        # dbug(f"found dflt in kwargs_d: {kwargs_d} ")
        # dbug(type(kwargs_d))
        # dbug(f"setting my_default to: {kwargs_d['dflt']} ")
        my_default = kwargs_d['dflt']
    #if 'default' in kwargs_d:
    #    # dbug(f"found default in kvargs_d: {kvargs_d} setting my_default to: {kvargs_d['default']} ")
    #    my_default = kwargs_d['default']
    # if default != "":
    #     my_default = default
    if dflt != "":
        my_default = dflt
    my_val = my_default
    # dbug(f"key: {key} kvargs_d: {kvargs_d} my_default: {my_default} <-------------------------------------------")
    if isinstance(key, list):
        keys = key
    else:
        keys = [key]
    for k in keys:
        # dbug(keys)
        # dbug(k)
        # test each key in list
        if k in kwargs_d:
            # dbug(type(k))
            # dbug(f"k: {k} is in kvargs_d: {kvargs_d}")
            my_val = kwargs_d[k]
    # dbug(f"Returning my_val: {my_val} <=================")
    return my_val


# ###########################################
def bool_val(s, args_l, kvargs={}, **kwargs):
    # #######################################
    """
    s can be a str or list
    args_l must be provided
    kvargs is optional
    used to see if a string or a list of stings might be declared true
    by being in args or seeing it has a bool value set in kvargs
    return: bool_val (False unless stipulated to be otherwise or declared in kwargs with 'dflt' or 'default')
    use:
        DBUG = bool_val('dbug', args, kvargs)
        or
        DBUG = bool_val(['dbug', 'DBUG'], args, kvargs)
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(f"s: {s} args_l: {args_l} kvargs: {kvargs} kwargs: {kwargs}")
    """--== Config ==--"""
    bool_v = kvarg_val(["default", "dflt"], kwargs, dflt=False)
    # dbug(f"default for bool_v: {bool_v}")
    opposite_words = kvarg_val(['opposite', 'opposites'], kwargs, dflt=[])
    """--== Convert ==--"""
    if isinstance(s, str):
        s_l = [s]  # make it a list
    if isinstance(s, list):
        s_l = s
    # if isinstance(opposite_words, str):
        # opposite_words = [opposite_words]
    """--== Process ==--"""
    # dbug(s_l)
    # bool_val = False
    # if "default" in kwargs:
    #     bool_val = kwargs['default']
    # if "dflt" in kwargs:
    #     bool_val = kwargs['dflt']
    # dbug(f"bool_v s: {s}: args: {args_l} kwargs: {kwargs}")  # for debugging
    for s in s_l:
        # dbug(f"s: {s} args_l: {args_l} kvargs: {kvargs}")
        if s in args_l:
            bool_v = True
        if s in kvargs:
            if isinstance(kvargs[s], bool):
                bool_v = kvargs[s]
    opposite_b = False
    for word in opposite_words:
        # dbug(f"word: {word} opposite_words: {opposite_words} args_l: {args_l} kvargs: {kvargs}")
        if word in args_l:
            opposite_b = True
            # dbug(f"word: {word} opposite_b: {opposite_b}")
        if word in kvargs:
            if isinstance(kvargs[word], bool):
                opposite_b = kvargs[word]
            # dbug(f"word: {word} opposite_b: {opposite_b}")
    # dbug(opposite_b)
    if opposite_b:
        bool_v = False
    # dbug(f"Returning bool_v: {bool_v}")
    return bool_v


def bool_val_demo():
    def my_function(*args, **kwargs):
        print(f"args: {args}    kwargs: {kwargs}")
        prnt = bool_val(["prnt", "print", "show", "verbose"], args, kwargs, dflt=False)
        print(f"prnt={prnt}")
        centered_b = bool_val(["center", "centered"], args, kwargs, dflt=False)
        print(f"centered_b: {centered_b}")
    msg = """
    The purpose of this function is to allow easy configuration to a function.
    All that is needed for a function is *args and **kwargs ... eg:
    -    def my_function(*args, **kwargs):
    -        my_bool_val = bool_val(["bool", 'bool_val', 'bval'], args,kwargs)
    -        centered = bool_val(["center", 'centered', 'cntr', 'cntrd'], args,kwargs)
    Now if the function is called in any of the following ways my_bool_val will be True and as written here centered will be True
    Keep in mind python insists the quoted single arguments must preceed key=value pairs.
    - my_function('bval', 'centered')
    - my_function('cntr', bval=True, 'cntr')
    - my_function('bool_val', center=True)
    - my_function('centered', bool_val=True)
    - my_function('bool', centered=True, my_other_args)
    .  etc...
    Within a function use this to determine True or False in arguments provided: boo_val(['arg1', 'arg2', ...], args, kwargs, dflt='Your Default')
    """
    printit(msg, 'boxed', 'centered')
    printit(f"Calling my_function('print'):")
    my_function('print') 
    print("-" * 40)
    printit(f"Calling my_function('show', 'centered'):")
    my_function('show', 'centered')
    print("-" * 40)
    printit(f"Calling my_function('prnt)', centered=False):")
    my_function('print', centered=False)


def docvars(*args, **kvargs):
    """
    purpose: wrapper for function to allow variable substitution within its doc
    I use this in front on a function I call handleOPTS(args)
    which works with the module docopts
    Thank you to stackoverflow.com: answered Apr 25 '12 at 1:54 senderle
    this is a very useful way to allow variables in your __doc__ strings
    wrap a function with this and use if this way
    eg: 
    @docvars(os.path.basename(__file__), anotherarg, myarg="abcd")
    def myfunc():
        \"""
        Usage: {0} [-hijk]\"
   
        Notes:
             anotherarg: {1}
             myarg: {myarg}
        \"""
        return \"Done\"
    """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kvargs)
        return obj
    return dec


def fstring(s):
    """
    purpose: alternative to f-strings
    use: fsting(s)
    returns: formated s string
    """
    # alternate to f-strings
    # requires: from inspect import currentframe
    # this is an alternative to f-string
    # use: [instead of f"my string contains {myvar}"]
    # f("my string contains {myvar}")
    frame = currentframe().f_back
    return eval(f"f'{s}'", frame.f_locals, frame.f_globals)


# #########################
def handleCFG(cfg_file="", *args, **kwargs):
    # #####################
    """
    purpose:  if no cfg_file given it will find the default and return cfg_d (dictionary of dictioanries: cfg.sections; cfg.elem:vals)
    input: cfg_file: str
    defaults: cfg_file if it exists is: {myappname.basename}.cfg
    returns: cfg_d: dict (dictionary of dictionaries - cfg.sections with key, val pairs)
    use:
        cfg_d = handleCFG("/my/path/to/myapp.cfg")
        title = cfg_d['menu']['title']
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    section = kvarg_val('section', kwargs, dflt="")
    key = kvarg_val(['key'], kwargs, dflt="")
    dflt = kvarg_val(['dflt'], kwargs, dflt=None)
    """--== SEP_LINE ==--"""
    if isinstance(cfg_file, dict):
        cfg_d = cfg_file
        # dbug(cfg_d)
        # dbug(args)
        # dbug(kwargs)
        # user passed the cfg_d back probably with a section and key
        if len(key) > 0:
            try:
                if isinstance(key, str):
                    key = [key]
                for k in key:
                    # dbug(f"Chkg k: {k}")
                    rtrn = cfg_d[section][k]
                # rtrn = cfg_d[section][key]
                # dbug(f"Returning {rtrn}")    
                return rtrn
            except Exception as Error:
                # dbug(cfg_d)
                # dbug(f"Exception Error: {repr(Error)}")
                # dbug(f"Returning {dflt}")    
                return dflt
    """--== SEP_LINE ==--"""
    if cfg_file == "" or not file_exists(cfg_file):
        dbug(f"No cfg_file provided or not found (cfg_file: {cfg_file})... returning None ...")
        # cfg_file = os.path.splitext(__file__)[0]
        # cfg_file += ".cfg"
        return None
    config = configparser.ConfigParser()
    # cfg_file = "/home/geoffm/dev/data/devices.conf"  # for debugging
    # dbug(cat_file(cfg_file))
    try: 
        config.read(cfg_file, encoding='utf-8')
        # config.read(cfg_file)
    except Exception as Error:
        dbug(f"Problem with cfg_file: {cfg_file} Error: {Error}")
    # dbug(config.sections())
    """--== SEP_LINE ==--"""
    cfg_d = {}
    if len(config['DEFAULT']) > 0:
        # DEFAULT is treated differently by configparser... got me why
        # I don't suggest using it as values don't seem to be parsed the same way (needs quoting??)
        # lowercase 'default' will work fine - use it instead?
        for key in config['DEFAULT']:
            cfg_d['DEFAULT'] = {}
            val = config['DEFAULT'][key]
            cfg_d['DEFAULT'][key] = val
    for section in config.sections():
        cfg_d[section] = {}
        for key in config[section]:
            val = config[section][key]
            cfg_d[section][key] = val
    # dbug(f"Returning: {cfg_d} using file: {cfg_file}")
    return cfg_d
    # ### EOB def handleCFG(cfg_file=""): ### #


def browseit(url):
    """
    purpose: opens the url in your browser
    requires: url: str
    returns: none
    """
    import webbrowser
    # webbrowser.open_new(url)
    webbrowser.open(url, new=0)


@docvars(os.path.basename(__file__))
def handleOPTS(args):
    """
    Usage:
        {0} [-hEP] [--dir] [<filename>]
        {0} -s <func>
        {0} -S <func>
        {0} -t [<func>]
        {0} -T <func> [<fargs>...] 

    Options
        -h                Help
        --dir             prints all the functions here and exits
        -t                runs all doctest calls
        -T <func>         runs specified func
        -v, --version     Prints version
        -s <func>         Show code block
        -S <func>         Show __doc__

    """
    # dbug(args)
    if args["-t"]:
        try: 
            import doctest
        except Exception as Error:
            dbug(f"Error: {Error}")
            return
        # dbug()
        if args['<func>']:
            func = args['<func>']
            name = f"{os.path.basename(__file__)}.{func}()"
            gb = globals()
            # don't lose this next line --- iC<Plug>ocRefresht took time to find it!
            doctest.run_docstring_examples(globals()[func], gb, verbose=True, name=name, optionflags=doctest.ELLIPSIS)
            do_close()
        else:
            doctest.testmod(verbose=True, report=False, raise_on_error=False, exclude_empty=False)
        do_close()
    if args['-T']:
        """
        this is to test a single function
        Put this in Usage section:
          {0} -T <funcname> [<fargs>...]
        """
        # dbug(args)
        funcname = args['-T']
        do_this = funcname
        # this_doc = f"print('Function doc: ',{do_this}.__doc__)"
        this_doc = f"{do_this}.__doc__"
        # dbug(this_doc)
        msg = eval(this_doc)
        # dbug(msg)
        if msg is None:
            msg = "No doc available..."
        printit(f"Function doc: {funcname}()  " + msg, 'centered', 'boxed')
        # you may have to escape (\) any quotes around fargs
        fargs = args['<fargs>']
        # dbug(fargs)
        if fargs is not None and len(fargs) > 0:
            fargs = ",".join(fargs)
            # dbug(fargs)
            evalthis = f"{do_this}({fargs})"
            # dbug(evalthis)
        else:
            evalthis = f"{do_this}()"
        # dbug(evalthis)
        eval(evalthis)
        do_close("", 'center')
    if args["--dir"]:
        # import sys
        sys.path.append("/home/geoffm/dev/python/gmodules")
        import gtools3
        print("dir(gtools3): " + "\n".join(dir(gtools3)))
        print("file: " + __file__)
        return
    if args["-E"]:
        do_edit(__file__)
        sys.exit()
    if args['-s']:
        func = args['-s']
        script = sys.argv[0]
        lines = from_to(script, f"def {func}", f"def {func}", include="both")
        printit(lines)
    if args['-S']:
        func = args['-S']
        print(eval(f"{func}.__doc__"))
    # specific code
    return None
    # ### EOB def handleOPTS(args): ### #


# #####################
def path_to(app):
    # #################
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    full_path = which(app)
    # print("full_path: " + full_path)
    # returns None type if it fails?
    if full_path is not None:
        return full_path
    return None


# ############################
def centered(msgs, *args, **kwargs):
    # ########################
    """
    purpose: calculates screen placement for msgs: list|str
    options: 
        length=columns: int 
        shift=0: int 
        'str'|'string'=False: bool 
        'lst'|'list'=True: bool
    returns: line|lines
    note: replaces deprecated centerit()
    """
    # dbug(funcname())
    # dbug(msgs)
    if msgs is None:
        dbug(f"msgs: {msgs} appear to be empty... returning")
        return None
    # try:
    #    # sometimes there is no stty... like with wsgi
    #     rows, columns = os.popen("stty size", "r").read().split()
    # finally:
    #     rows = 0
    #     columnns = 0
    """--== Config ==--"""
    shift = kvarg_val('shift', kwargs, dflt=0)
    columns = get_columns(shift=shift)
    length = kvarg_val(['width', 'length'], kwargs, dflt=int(columns))
    lst = bool_val(['lst', 'list'], args, kwargs, dflt=True)
    string_b = bool_val(['str', 'string'], args, kwargs, dflt=False)
    # margin = 0
    """--== Init ==--"""
    # reset = sub_color("reset")
    """--== Process ==--"""
    if isinstance(msgs, str):
        msgs = [msgs]
    lines = []
    for ln in msgs:
        # l_pad_len = (columns - nclen(ln)) // 2
        l_pad_len = (length - nclen(ln)) // 2
        l_pad_len += shift
        l_pad = " " * l_pad_len
        lines.append(l_pad + ln)
    if not lst or string_b:
        rtrn = "".join(lines)
    else:
        rtrn = lines
    # dbug(lines)
    return rtrn
    # ### EOB def centered(msgs): ### #


# #############
def ruleit():
    # #########
    """
    This is for development purposes
    It draws a rule across the screen and that is all it does
    It fails to prepare your meals or schedule your week\'s agenda, sorry.
    """
    from math import floor
    # try:
    #     rows, columns = os.popen("stty size", "r").read().split()
    # finally:
    #     rows = columns = 0
    columns = get_columns()
    cols = int(columns)
    iters = int(floor(int(cols)) / 10)
    cntr = cols / 2
    printit(f"cols: {cols} center: {cntr}", center=True)
    diff = int(columns) % 10
    for i in range(0, iters):
        for x in range(0, 10):
            print(x, end="")
    for i in range(0, diff):
        print(i, end="")
    print()
    for i in range(0, iters):
        for x in range(0, 10):
            if x == 9:
                print("|", end="")
            else:
                print(" ", end="")
    print()
    cnt = 10
    for i in range(0, iters):
        for x in range(0, 10):
            if x == 0:
                padding = 10 - len(str(cnt))
                print(f"{' ' * padding}{str(cnt)}", end="")
                cnt += 10
            # if x == 9:
            #     print(f"{cnt}", end="")
            #     cnt += 10
            # else:
            #     if x == 0 and cnt and cnt > 10:
            #         print(" ", end="")
    print()
    return cntr


# ######################################
def do_close(msg="", *args, hchr="=", color="", box_color="", rc=0, **kwargs):
    # ##################################
    """
    purpose: to provide a boxed closing message
    returns: None
    # dflt_msg = "Enjoy!"
    input msg or it uses dflt_msg
    options: 'center' | 'centered' color='red' rc=return code to exit with 
    >>> do_close()
        ======
        Enjoy!
        ======
    """
    """--== Init ==--"""
    dflt_msg = "Wanted: Software Developer. Python experience is a plus. Pay commensurate with skill set. Apply within."
    # dflt_msg = "All is well that ends well!"
    """--== Config ==--"""
    centered = bool_val(['center', 'centered'], args, kwargs, dflt=True)
    shadowed = bool_val(['shadow', 'shadowed'], args, kwargs)
    figlet = bool_val(['figlet'], args, kwargs)
    """--== Process ==--"""
    if msg == "":
        msg = dflt_msg
    if figlet:
        from pyfiglet import figlet_format
        msg = figlet_format(msg, width=1000)
    printit(msg, 'box', center=centered, shadow=shadowed, box_color=box_color, color=color)
    sys.exit(rc)


def convert_temp(temp, convert2="f"):
    """
    expects a string with either an ending.lower() of "f" or "c" to declare what to return
    returns rounded(converted_temp)
    always returns a string with 2 places (inlcuding 0s)
    """
    temp = str(temp)
    if convert2.lower() == "f":
        # this seems counter intuitive but it tells the func that the float(temp) is currently Celcius so convert it
        temp = temp + "c"
    if convert2.lower() == "c":
        # this seems counter intuitive but it tells the func that the float(temp) is currently Fahrenheit so convert it
        temp = temp + "f"
    if temp.lower().endswith("f"):
        # convert to Celcius
        temp = float(temp[:-1])
        temp_C = (temp - 32) / 1.8 
        converted_temp = temp_C
        temp_C = round(float(converted_temp), 2)
        return(f"{converted_temp:.2f}")
    if temp.lower().endswith("c"):
        # convert to Fahrenheit
        temp = float(temp[:-1])
        temp_F = (temp * 1.8) + 32
        converted_temp = temp_F
        converted_temp = round(float(converted_temp), 2)
        return(f"{converted_temp:.2f}")
    else:
        dbug("temp must end with [CcFf] or declare ForC=[FfCc]")
        return None


# #############################################
def do_logo(content="", *args, hchr="-", prnt=True, figlet=False, center=True, shadow=False, **kwargs):
    # #########################################
    """
    require: nothing but you should provide some default content: str|list
    option: content: str|list, prnt: bool, figlet: bool, center: bool, shadow: bool, box_color: str, color: str, fortune: bool, quote: bool
        fotune: bool <-- requires the fortune app
        quote: str   <-- requires a filename with quote lines within it - one will be randomly selected
    if content = "" and /usr/local/etc/logo.nts does not exist then we use "Your Organization Name"
    if content == "" then open default file: /usr/local/etc/logo.nts
    if content is a filename then use the lines in that file
    if content is a str and not a file then use pyfiglet to turn it into ascii letters of print lines
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(center)
    """--== Config ==--"""
    shadow = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=shadow)
    quote = kvarg_val('quote', kwargs, dflt="")
    fortune = bool_val('fortune', args, kwargs)
    color = kvarg_val('color', kwargs)
    box_color = kvarg_val('box_color', kwargs)
    prnt = bool_val('prnt', args, kwargs, dflt=True)
    title = kvarg_val('title', kwargs, dflt="")
    footer = kvarg_val('footer', kwargs, dflt="")
    figlet = bool_val('figlet', args, kwargs, dflt=figlet)
    """--== Convert ==--"""
    if "\n" in content:
        content = content.split('\n')
    if isinstance(content, list):
        lines = content
    else:
        lines = [content]
    # dbug(lines)
    if isinstance(content, str) and content == "":
        filename = "/usr/local/etc/logo.nts"
        if file_exists(filename):
            with open(filename) as f:
                lines = [line.rstrip() for line in f]
        else:
            lines = ["Your Organization Name", dtime]
    else:
        if isinstance(content, str) and file_exists(content):
            with open(content) as f:
                lines = [line.rstrip() for line in f]
        else:
            # dbug(lines)
            if figlet:
                # dbug("found pyfiglet")
                from pyfiglet import figlet_format
                lines = figlet_format(content, width=1000)
            # else:
            #     lines.append(content)
    if len(lines) < 1:
        dbug(f"Problem: nothing to print lines: {lines}")
    if isinstance(lines, str):
        lines = lines.split("\n")
    """--== Process ==--"""
    lines = printit(lines, 'boxed', box_color=box_color, title=title, footer=footer, color=color, shadow=shadow, prnt=False)
    if fortune:
        cmd = "fortune -s"
        out = run_cmd(cmd)
        f_box = printit(out, "boxed", title=" Fortune ", prnt=False, box_color=box_color, color=color, shadow=shadow)
    if quote != "":
        # quote needs to be a path/filename -- path can include "~/" for $HOME
        if isinstance(quote, str):
            file = os.path.expanduser(quote)
        else:
            dbug(f"quote: {quote} must be a valid filename: str containing quote lines", 'centered')
            return None
        quote = get_random_line(file)
        quote = wrapit(quote, length=80)
        q_box = printit(quote, 'boxed', title=" Quote ", prnt=False, shadow=shadow, box_color=box_color, color=color)
    if quote or fortune:
        lines.append("   ")
    if quote and fortune:
        columns = [f_box, q_box]
        boxes_l = gcolumnize(columns, color=color)  # color affects the 'fill color'
        boxes = boxed(boxes_l, box_color=box_color, color=color, shadow=shadow, top_pad=1, bottom_pad=1)
        # dbug(lines)
        # printit(boxes)
        # dbug('ask')
        lines.extend(boxes)
    else:
        if fortune:
            lines.extend(f_box)
        if quote:
            lines.extend(q_box)
    if prnt:
        printit(lines, center=center)
    return lines
    # ### EOB def do_logo(content="", *args, hchr="-", prnt=True, figlet=False, center=True, box=True, shadow=False, color='red', **kwargs): ### #


def do_logo_demo():
    file = "~/data/lines.dat"
    quote = askYN("Do you want to include a quote from file: {file} <-- must exist ", "n", 'centered')
    fortune = askYN("Do you want to include a  fortune from the script fortune <-- must be installed ", "n", 'centered')
    if quote:
        do_logo("Do Logo Demo", color="White! on rgb(20,20,50)", box_color="red!", fortune=fortune, quote=file)  # , rgb(20,20,50)")
    else:
        do_logo("Do Logo Demo", 'figlet', color="White! on rgb(20,20,50)", box_color="red!", fortune=fortune)  # , rgb(20,20,50)")
    # dbug("EOB do_logo_demo", 'ask')


# #########
def cls():
    # #####
    """
    Clears the terminal screen.
    """
    import platform
    # Clear command as function of OS
    command = "-cls" if platform.system().lower() == "windows" else "clear"
    # Action
    os.system(command)
    # print(ansi.clear_screen()) # this works but puts it at the same cursor position
    # location


# # #######################
# def sudoit(user='root'):
#     # ##################
#     """
#     user='root'
#     forces this app to run as root
#     this should be right at the top of the script
#     keep in mind that the PYTHONPATH will be root's (probably empty)
#     so you may have to sys.path.append() before importing needed personal modules
#     eg
#         sys.path.append('/home/geoffm/dev/python/gmodules')
#     This function is like my (gwm) bash chkID function
#     aka force_super
#     """
#     import subprocess
#     import shlex
#     import getpass
#     current_user = getpass.getuser()
#     # dbug(user)
#     if current_user != user:
#         # sys.path.append('/home/geoffm/dev/python/gmodules')
#         # print(f"Running this app as {user} using sudo...")
#         cmd = "sudo --preserve-env=HOME,PYTHONPATH -u " + user + " " + " ".join(sys.argv)
#         subprocess.call(shlex.split(cmd))
#         sys.exit()
#     # print("This script was called by: " + current_user)
#     return
# 

# ########################
def askYN(msg="Continue", *args, dflt="y", center=False, auto=False, timeout=0, **kwargs):
    # ####################
    """
    auto var can be used to automatically invoke the default
    TODO: timeout=10  # times out in 10 secs and invokes dflt - this still requires you to hit enter : TODO
    # >>> askYN()
    # Continue [y]: True
    """
    # dbug(funcname())
    # dbug(f"msg: {msg}")
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    dflt = kvarg_val(["default", "dflt"], kwargs, dflt=dflt)
    if len(args) > 0:
        if args[0] in ["n", "N", "Y", "y"]:
            dflt = args[0]
    center = bool_val(['center', 'centered'], args, kwargs, dflt=center)
    auto = True if 'auto' in args else auto
    quit = kvarg_val('quit', kwargs)
    exit = kvarg_val('exit', kwargs, dflt=False)
    timeout = kvarg_val("timeout", kwargs, dflt=timeout)
    """--== Process ==--"""
    if dflt.upper() == "Y" or dflt.upper() == "YES":
        dflt_msg = " [Y]/n "
    else:
        dflt_msg = " y/[N] "
    if center:
        # dbug(msg)
        # dbug(center)
        # dbug(auto)
        if auto:
            ans = dflt
            # dbug(f"setting ans: {ans}")
        else:
            prompt = RESET + msg + dflt_msg
            # dbug(prompt)
            ans = cinput(prompt)
    else:
        # dbug(msg)
        if auto:
            ans = dflt
            # dbug(f"setting ans: {ans}")
        else:
            if timeout > 0:
                from threading import Timer
                t = Timer(timeout, print, ['Sorry, time is up... '])
                t.start()
                ans = input(msg + dflt_msg)
                t.cancel()
            else:
                if isinstance(msg, list):
                    msg = "".join(msg)
                if isinstance(dflt_msg, list):
                    dflt_msg = "".join(dflt_msg)
                prompt = RESET + msg + dflt_msg
                # dbug(prompt)
                ans = input(prompt)
    if ans.upper() == "":
        ans = dflt
    if msg != "":
        if msg == "Continue" and ans.lower() == "n":
            print("Exiting at user request...")
            sys.exit()
        if ans.upper() == "Y":
            return True
        if quit or exit:
            # if quit is true and user hits 'q' then exit out as requested
            printit("Exiting as requested", 'shadow', center=center, box_color="red on black", color="yellow")
            if ans in ['q', 'Q']:
                sys.exit()
    return False
    # ### EOB def askYN(msg="Continue", dflt="y", *args, center=False, auto=False, timeout=0):  ### #


def askYN_demo():
    """
    purpose: demo of using askYN() function
    """
    new_line = "Sample new line..."
    if askYN(f"Do you want to add this new_line: {new_line} ?", 'y', 'centered'):
        printit(f"Here we would call a function to add the new line: {new_line}", 'boxed', 'centered', box_color="yellow!")
    if not askYN("Do you want to continue", 'centered', 'box'):
        printit("User does not want to contimue...", 'centered')
        return
    dbug("Testing dbug with ask and centered", 'ask', 'centered')
    r = askYN("Test of using askYN() ", 'centered')
    print(f"The result was: {r}")
    print("Using just 'Continue' as the msg will allow sys.exit when it is not a 'y' or 'Y'")
    printit("This next one is perhaps useful for developing creating a forced breakpoint... it is just 'askYN()' with no arguments anything but 'Y' will exit", 'centered', 'boxed')
    askYN()
    if askYN("Here I am asking if you like birds", 'centered', 'boxed'):
        print("You like birds...")
    else:
        print("You do not like birds...")


# ########################
def cat_file(fname, *args, prnt=False, lst=False, **kwargs):
    # ####################
    """
    purpose: reads a file and return lines or rows_lol (list of list) or as a df (dataframe)
    options: 
    -    prnt: bool,  # prints out the file contents
    -    lst: bool,   # returns a list of lines or you could use: txt.split('\n') to make it a list 
    -    csv: bool,   # treat the file as a csv (or for me, a dat file) 
    -    dat: bool,   # this one will seem strange, it treats the first line as a commented out header line
    -    xlsx: bool,  # returns df of a spreadsheet file
    -    hdr: bool,   # whether to include header line or header data in the return  
    -    df: bool,    # return a df
    -    rtrn: str, (can be "str", "string", "lst", "df" 
    returns the text of a file as a str or rows_lol (if it is a cvs: bool file) or returns a df if requested
    Note: if the result df has the header/colnames repeated in row[0] then make sure you included 'hdr' or hdr=True
    #>>> t = cat_file("/etc/timezone")
    #>>> print(t)
    America/New_York
    <BLANKLINE>
    """
    """--== debugging ==--"""
    # dbug(funcname())
    """--== Config ==--"""
    csv_b = bool_val(['csv', 'csv_file', 'csvfile'], args, kwargs, dflt=False)
    dat = bool_val(['dat', 'datfile', 'dat_file'], args, kwargs, dflt=False)
    dat = kvarg_val("dat", kwargs, dflt=dat)
    lst = bool_val(['lst', 'list'], args, kwargs, dflt=lst)
    xlsx = bool_val('xlsx', args, kwargs, dflt=False)
    prnt = bool_val('prnt', args, kwargs, dflt=prnt)
    hdr_b = bool_val('hdr', args, kwargs, dflt=False)
    # dbug(hdr_b)
    df_b = bool_val('df', args, kwargs, dflt=False)  # rtrn as df?
    rtrn = kvarg_val('rtrn', kwargs, dflt='')  # rtrn value is  df or str  same as above, just another way to do it
    purify_b = bool_val(['purify', 'decomment', 'pure', 'uncomment'], args, kwargs, dflt=True)
    # dbug(f"fname: {fname} csv: {csv} df_b: {df_b} hdr_b: {hdr_b} rtrn: {rtrn} purify_b: {purify_b}")
    """--== Local Functions ==--"""
    def decomment(csvfile):
        # purify
        for row in csvfile:
            raw = row.split('#')[0].strip()
            if raw:
                yield raw
    """ Process  """
    if not file_exists(fname):
        dbug(f"Ooops... fname: {fname} not found... returning None ...")
        return
    # dbug(f"fname: {fname} rtrn: {rtrn}")
    if (csv_b or fname.endswith(".csv") or fname.endswith(".dat")) and rtrn not in ("str", "string"):
        # if it is a csv or ".dat" file return rows_lol (list of lists) unless df_b
        import csv
        rows_lol = []
        with open(fname) as f:
            # dbug(lines)
            if purify_b:
                # dbug(purify_b)
                csv_reader = csv.reader(decomment(f), delimiter=",")
            else:
                # dbug(purify_b)
                csv_reader = csv.reader(f, delimiter=",")
                # dbug(csv_reader)
            # dbug(csv_reader)
            for row in csv_reader:
                # dbug(row)
                # csv_reader has already decommented - see above - so using lines[0] instead
                rows_lol.append(row)
            # rows_lol = list(csv_reader)
        if fname.endswith('.dat') or dat or isinstance(dat, str):
            # TODO: this is too kludgy
            # dbug(rows_lol)
            with open(fname) as fn:
                lines = fn.readlines()  # remember this takes the file pointer to EOF
            # dbug(lines)
            if lines[0].startswith("#"):
                # treat this file like it is a .dat file ie firstline is a commented out list of colnames
                if "," in lines[0]:
                    colnames = lines[0].lstrip("#").split(",")
                else:
                    if isinstance(dat, str):
                        colnames = lines[0].lstrip("#").split(dat)
                    else:
                        colnames = lines[0].lstrip("#").split()
                colnames = [elem.strip() for elem in colnames]
                # dbug(colnames)
                rows_lol.insert(0, colnames)
                # dbug(f"file: {fname} Adding the first row: {colnames} to rows_lol: {rows_lol}")
        else:
            colnames = rows_lol[0]
            # dbug(colnames)
        if rtrn == "df" or df_b:
            import pandas as pd
            if hdr_b:
                # assumes colnames is set above AND first row is colnames
                df = pd.DataFrame(rows_lol)
                df = df.iloc[1:]
                df.columns = colnames  # from above
                # dbug(f"Returning df: {df}")
                return df
            else:
                df = pd.DataFrame(rows_lol, columns=rows_lol[0])
                # dbug(f"Returning df: {df}")
                return df
        else:
            # dbug("returning lol")
            return rows_lol
    if xlsx:
        import pandas as pd
        df = pd.read_excel(fname)
        return df
    """--== treat this as just a text file ==--"""
    f = open(fname, "r")
    text = f.read()
    f.close()
    if prnt:
        print(f" ---- cat_file({fname}) ---- ")
        printit(text)
        print(f" ---- end cat_file({fname}) ---- ")
    if lst:
        # dbug(f"text): [{text}]")
        text_l = text.splitlines()
        # dbug(text_l)
        return text_l
    return text
    # ### EOB def cat_file(fname, *args, prnt=False, lst=False, **kwargs): ### #


# ###############################
def file_exists(file, type="file", *args, **kwargs):
    # ###########################
    """
    Note: type can be "file" or "dir" (if it isn't file the assumption is dir)
        should rename this to path_exists... argghh
    #>>> file_exists('/etc/hosts')
    True
    """
    if type == "file":
        try:
            os.path.isfile(file)
        except Exception as e:
            print("Exception: " + str(e))
            return False
        return os.path.isfile(file)
    if type in ('X', 'x', 'executable'):
        try:
            os.path.isfile(file, X_OK)
        except Exception as e:
            print("Exception: " + str(e))
            return False
    if type == 'dir':
        # check file or dir
        return os.path.exists(file)
    # to move a file use: os.rename(source, target)
    # or shutil.move(source, target)
    return True


# #####################
def do_list(lst, *args, mode="", prnt=True, center=False, title="", **kwargs):
    # ##############o#
    """
    # >>> lst = ['one','two','three']
    # >>> do_list(lst, "nc")
    # ===========
    # || one   ||
    # || two   ||
    # || three ||
    # ===========
    """
    """--== Config ==--"""
    prnt = bool_val(['prnt', 'show'], args, kwargs, dflt=prnt)
    center = bool_val(['centered', 'center'], args, kwargs, dflt=prnt)
    title = kvarg_val('title', kwargs, dflt=title)
    # footer = kvarg_val('footer', kwargs, dflt=title)
    """--== SEP_LINE ==--"""
    if mode == "v":
        lst_d = {}
        for n, elem in enumerate(lst):
            lst_d[n] = elem
        lst = lst_d
    lines = gtable([lst], prnt=prnt, centered=center)
    return lines


# ####################
def purify_file(file):
    # ################
    """
    purpose: de-comments a file, aka removes all comments denoted by "#" ...
    input: file: str
    return lines: list
    """
    purified_lines = []
    with open(file, "r") as myfile:
        for line in myfile:
            line = line.rstrip('\n')
            purified_line = purify_line(line)
            # dbug(purified_line)
            if purified_line.isspace() or purified_line == '':
                continue
            purified_lines.append(purified_line)
    # dbug(purified_lines)
    # this is a cool alternative - used in n=mngdata.py
    # import csv
    # data = []
    # def decomment(csvfile):
    #     for row in csvfile:
    #         raw = row.split('#')[0].strip()
    #         if raw:
    #             yield raw
    # with open(file) as csvfile:
    #     reader = csv.reader(decomment(csvfile))
    #     for row in reader:
    #         data.append(row)
    # def decomment(file):
    #     # this does the same thing as purify
    #     with open(file, "r") as f:
    #         for row in f:
    #             # dbug(row)
    #             raw = row.split('#')[0].strip()
    #             # dbug(raw)
    #             if raw:
    #                 yield raw
    # to use
    # for elem in decomment(file):
    #     do_something(elem)
    return purified_lines


# ####################
def purify_line(line):
    # ################
    """
    strips off and comments
    """
    line = str(line).rstrip('\n')
    m = re.match(r'^([^#]*)#(.*)$', line)
    # note: m.group(0) is the orig line
    if m:  # The line contains a hash ie comment
        stripped_line = m.group(1)
        # note: m.group(2) is the comment
        return stripped_line.strip()
    else:
        return line.strip()


# #######################
def pretty_array(array):
    # ##################
    """
    prints out nested arrays into readable format using yaml
    """
    import yaml
    print(yaml.dump(array, default_flow_style=False))


# ###################################
def ireplace(s, indices=[], char="|"):
    # ###############################
    """
    purpose: index replace
    To get indices use eg:
        iter = re.finditer(rf"{c}", s)
        indices = [m.start(0) for m in iter]
        # next line removes first two and last two indices - just an example
        indices = indices[2:-2]
    then use this func with:
        s: is the string to do the replacements
        indices: list of indexed positions
        char: is the char to replace with
    """
    # if replace != "":
    #     iter = re.finditer(rf"\{replace}", s)
    #     indices = [m.start(0) for m in iter]
    s_l = list(s)
    # dbug(f"indices: {indices} chr: {chr} len(s): {len(s)} s: {s}")
    if len(indices) > 0:
        # dbug(len(s_l))
        for i in indices:
            # dbug(f"i: {i}")
            # dbug(s_l[i])
            s_l[i] = char
        s = "".join(s_l)
    return s


# ###############################
def do_kv_rows(d, length=0, prnt=False, color="", title="", edge="+", footer=""):
    # ###########################
    """
    deprecated, use kv_cols instead
    purpose:
        prints out boxed dictionary of key value pairs
    # >>> d = {"one": 1.00, "two": "2.000", "three": 3.00, "four is where the world changes for the better": "4.4444"}
    # >>> lines = do_kv_rows(d, length=21)
    """
    dbug("deprecated: use kv_cols() instead...")
    # dbug(d, ask=True)
    # dbug(type(d))
    # dbug(length)
    box_color = sub_color(color)
    if color == "":
        RESET = ""  # noqa:
    else:
        RESET = Style.RESET_ALL  # noqa:
    reset = RESET
    # dbug(f"{color} TEST {reset}")
    def pad(e1, e2, chr=" "):
        diff = len(str(e2)) - len(str(e1))
        # dbug(diff)
        if diff > 0:
            pad = diff * chr
            return pad
        return ""
    # try:
    #     rows, columns = os.popen("stty size", "r").read().split()  # noqa:
    # finally:
    #     rows = columns = 0
    lines = []
    # keys_line = "||"
    num_processed = 0
    k_rows = []
    v_rows = []
    # d_len = len(d)
    # for i in range(d_len):
    def get_len_k_row(d):
        k_row = f"{box_color}||{reset}"
        for k, v in d.items():
            add_this = f" {k} " + pad(k, v) + f"{box_color}|{reset}"
            k_row += add_this
        k_row += f"{box_color}|{reset}"
        line_len = nclen(k_row)
        # dbug(f"returning line_len: {line_len} k_row: {k_row}")
        return line_len
    def extend_row(k_row, v_row, length):
        # dbug(f"extend_row() length: {length} len(k_rows): {len(k_rows)} k_row: {k_rows}")
        # extend a row
        # do not add ending edge
        diff = length - nclen(k_row)
        padding = "-" * diff
        end_with = f"{padding}{box_color}|{reset}"
        k_row += end_with
        # dbug(k_row)
        if nclen(v_row) != nclen(k_row):
            diff = nclen(k_row) - nclen(v_row) - 1
            padding = "-" * diff
        end_with = f"{padding}{box_color}|{reset}"
        v_row += end_with
        return k_row, v_row
        #
    def do_kv_row(d, line_len):
        """
        returns: k_row, v_row, num_processed
        """
        # dbug(line_len)
        k_row = ""
        v_row = ""
        num_processed = 0
        if line_len < 1:
            dbug(f"line_len: {line_len} has to be greater than 0")
            return k_row, v_row, num_processed
        # dbug(d)
        k_row = f"{box_color}||{reset}"
        v_row = f"{box_color}||{reset}"
        for k, v in d.items():
            num_processed += 1
            add_this = f" {k} " + pad(k, v)
            tst_k_row = k_row + add_this
            if nclen(tst_k_row) > line_len:
                # dbug(f"ooops tst_k_row: {tst_k_row}\nnclen(tst_k_row): {nclen(tst_k_row)} too long for line_len: {line_len}")
                # dbug(f"Returning: k_row: {k_row}\nv_row: {v_row}")
                # return k_row, v_row, num_processed - 1
                num_processed -= 1
                if num_processed < 1:
                    # dbug("Perhaps one key is too long... ")
                    return
                # dbug(f"Breaking loop with: k_row: {k_row} nclen(k_row): {nclen(k_row)} line_len: {line_len}\nv_row: {v_row}")
                break
            else:
                # dbug(add_this)
                k_row += add_this
                # dbug(k_row)
                v_row += f" {v} " + pad(v, k)  # " + f"{box_color}|{reset}"
            # extend if needed
            # k_row, v_row = extend_row(k_row, v_row, line_len)
            #
            padding = ""
            if len(k_rows) > 0:
                # so we can use the first row
                if nclen(k_row) < line_len:
                    # dbug(k_row)
                    # dbug(f"HERE WE ARE nclen(k_row): {nclen(k_row)} line_len: {line_len} len(k_rows): {len(k_rows)} nclen(k_rows[0]): {nclen(k_rows[0])}")
                    extend_by = line_len - nclen(k_row) - 7
                    # dbug(extend_by)
                    padding = " " * extend_by
            end_with = f"{padding}{box_color}|{reset}"
            k_row += end_with
            # dbug(k_row)
            if nclen(v_row) != nclen(k_row):
                diff = nclen(k_row) - nclen(v_row) - 1
                padding = " " * diff
            end_with = f"{padding}{box_color}|{reset}"
            v_row += end_with
        if nclen(k_row) > line_len + 4:
            dbug(f"""It looks like this last k_row: [{k_row}] is still too long nclen(k_row):
                    {nclen(k_row)} line_len: {line_len}... try a slightly larger length""")
            # dbug(k_row)
            sys.exit()
        # dbug(f"Returning: k_row: {k_row} nclen(k_row): {nclen(k_row)} line_len: {line_len}\nv_row: {v_row}")
        return k_row, v_row, num_processed
    """--== SEP LINE ==--"""
    def slice_d(d, start=0, end=0):
        if not isinstance(d, dict):
            dbug(d)
        # dbug(f"d: {d} start: {start} end: {end}")
        if end == 0:
            end = len(d)
        new_d = {}
        for n, (k, v) in enumerate(d.items()):
            if n >= start and n <= end:
                # dbug(f"adding k: {k} v: {v}")
                new_d[k] = v
        return new_d
    """--== SEP LINE ==--"""
    def assemble_table(k_rows, v_rows):
        lines = []
        line_len = nclen(k_rows[0])
        # top_line = "=" * line_len
        top_line = do_title(title=title, chr="=", length=line_len, prnt=False, box_color=box_color, edge=edge)
        # printit(top_line)
        # sep_row = f"{box_color}||" + "-" * (line_len - 4) + f"||{reset}"
        sep_line = "||" + "-" * (line_len - 4) + "||"
        # bot_line = f"{box_color}+" + "=" * (line_len - 2) + f"+{reset}"
        bot_line = do_title(title=footer, prnt=False, length=line_len, box_color=box_color, edge=edge)
        # printit(bot_line)
        lines.append(top_line)
        # printit(lines)
        # dbug(f"line_len: {line_len} len(k_rows): {len(k_rows)} len(v_rows): {len(v_rows)} lines: {lines}")
        # dbug(v_rows)
        for n, k_row in enumerate(k_rows):
            # dbug(n)
            # dbug(k_rows[n])
            lines.append(k_rows[n])
            chr = '|'
            iter = re.finditer(rf"\{chr}", escape_ansi(k_rows[n]))
            indices = [m.start(0) for m in iter]
            indices = indices[2:-2]
            sep_line = ireplace(sep_line, indices, char="|")
            lines.append(f"{box_color}{sep_line}{reset}")
            # dbug(f"just added sep_row: {sep_row}")
            # dbug(v_rows[n])
            lines.append(v_rows[n])
            if n < len(k_rows) - 1:
                line = box_color + "||" + "=" * (line_len - 4) + "||" + reset
                lines.append(line)
            # dbug(n)
        lines.append(bot_line)
        return lines
    line_len = get_len_k_row(d)
    # dbug(f"max_len: {max_len} line_len: {line_len}")
    if length > 0 and line_len > length:
        line_len = length
    # dbug(line_len)
    tst_len = nclen(title) + 6
    if nclen(footer) + 6 > tst_len:
        tst_len = nclen(footer) + 6
    if tst_len > line_len:
        line_len = tst_len
    # dbug(line_len)
    tot_processed = 0
    new_d = d
    n = 0
    # dbug(k_row_len)
    # dbug(line_len)
    while tot_processed < len(d):
        # dbug(f"Begining loop with new_d: {new_d} tot_processed: {tot_processed} line_len: {line_len}")
        k_row, v_row, num_processed = do_kv_row(new_d, line_len)
        # dbug(f"Just got back num_processed: k_row: {k_row} nclen(k_row): {nclen(k_row)} num_processed: {num_processed}")
        if nclen(k_row) > line_len + 2:
            dbug(f"nclen(k_row): {nclen(k_row)} is Too long for line_len: {line_len}... bailing...")
            sys.exit()
        tot_processed += num_processed
        # dbug(f"new_d: {new_d} num_processed: {num_processed} tot_processed: {tot_processed}\nNow running slice(d, tot_processed, len(d)) ")
        new_d = slice_d(d, tot_processed, len(d))
        # dbug(new_d)
        k_rows.append(k_row)
        v_rows.append(v_row)
        n += 1
    lines = assemble_table(k_rows, v_rows)
    if prnt:
        printit(lines)
    return lines
    # ### EOB def do_kv_rows(d, length=0, prnt=False, color="", title="", edge="+", footer=""):


# ########################################
def first_matched_line(filename, pattern, upto=1):
    # ####################################
    """
    purpose: return: just the first matched line(s) from a filename using pattern
    required:
        - filename: str
        - pattern: str
    options: 
        - upto: int default=1  # How many matching lines to return
    returns: matching lines
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    matched_l = []
    line_n = 1
    for line in lines:
        # dbug(f"Processing line: {line_n} of {len(lines)}")
        r = re.match(pattern, line)
        if r:
            matched_l.append(line.rstrip("\n"))
            if len(matched_l) >= upto:
                return matched_l
        line_n += 1
    return matched_l
    # ### EOB def first_matched_line(filename, pattern, upto=1): ### #


# ###################################
def pp_d(d, between=" ", kv_s=": "):
    # ###############################
    """
    purpose: pretty print a dictionary
    deprecated as gtable does this
    with between (str) placed between elems
    and kv_s (str) between k and v
    >>> d = {"one": 1, "two": 2, "three": 3}
    >>> print(pp_d(d))
    one: 1  two: 2  three: 3
    """
    dbug("Who uses this? ")
    s = between.join([f'{k}{kv_s}{v}' for (k, v) in d.items()])
    return s


# ###########################################
def kv_cols(my_d, cols=3, *args, **kwargs):
    # #######################################
    """
    input: my_d: dict cols:default=3 <-- both args ie: dict and cols are required!
    options: 
        - title, header, pad, box_style, box_color: str, color: str, neg: bool,
        - prnt: bool,  footer,title: str, rjust_cols: list, sep,pad: str, max_col_width: int,
        - centered: bool, box_style: str, human: bool, rnd: bool, box_title: bool (requires title), sep: str
    returns: lines tabalized key-value pairs 
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(cols)
    # dbug(my_d)
    """--== Config ==--"""
    cols = kvarg_val("cols", kwargs, dflt=cols)
    title = kvarg_val("title", kwargs, dflt="")
    # dbug(title)
    # footer = kvarg_val("footer", kwargs, dflt=funcname() + "()")
    footer = kvarg_val("footer", kwargs, dflt="")
    header_b = bool_val(['header', 'hdr'], args, kwargs, dflt=False)
    # dbug(header_b)
    # pad = kvarg_val("pad", kwargs, dflt=2)
    box_style = kvarg_val("box_style", kwargs, dflt="single")
    box_color = kvarg_val(["box_color", "box_clr"], kwargs, dflt="")
    mstr_box_color = kvarg_val(["mstr_box_color", "mstr_box_clr", 'main_box_color', 'main_box_clr', "mstrclr", 'mstr_clr'], kwargs, dflt="")
    color = kvarg_val(["color"], kwargs)
    neg = bool_val("neg", args, kwargs, dflt=False)
    prnt = bool_val(["prnt", "print"], args, kwargs, dflt=False)
    boxed_b = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    center = bool_val(["centered", "center"], args, kwargs, dflt=False)
    sep = kvarg_val("sep", kwargs, dflt=1)
    rjust_cols = kvarg_val(["rjust_cols", "rjust", "rjust_values", 'rjust_vals'], kwargs, dflt=[])
    box_title = bool_val(["box_title", "boxed_title", "title_boxed"], args, kwargs)
    max_width = kvarg_val(["max_col_width", "col_width", "maxwidth", "max_width", "colwidth", "max", 'col_limit', 'width'], kwargs, dflt=30)
    rnd = kvarg_val(['rnd', 'round'], kwargs, dflt="")
    human = bool_val(['h', 'human', "H"], args, kwargs, dflt=False)
    """--== Init ==--"""
    if mstr_box_color != "":
        boxed_b = True
    # RESET = sub_color('reset')
    myd_len = len(my_d)
    num_rows = ceil(myd_len / int(cols))
    if neg and rjust_cols == []:
        rjust_cols = [1]  # if neg numbers are to be processed then it is highly likely that the values should all be rjustified
    myd = []  # new dict for columned my_d
    lines = []
    for n in range(cols + 1):
        # dbug(n)
        myd.append({})
    # cnt = 0
    row_num = 1
    """--== Convert list k, v elems  with proper widths ==--"""
    if isinstance(my_d, list):
        dbug(f"Input: my_d: {my_d} appears to be a list. This function: {funcname()} requires a dict.")
        return
    # TODO: clean this up, maybe sep max_width into k_width and v_width
    # dbug(max_col_width)
    new_d = {}
    for k, v in my_d.items():
        # dbug(f"k: {k} repr(v): {repr(v)}")
        key = escape_ansi(k)
        pat = str(key) + "(?!;)(?!m)"
        # codes = k.split(key)
        codes = re.split(pat, str(k))
        prefix_code = codes[0]
        postfix_code = codes[1]
        new_k = k
        if len(key) > max_width:
            new_k = str(key)[:max_width]
            new_k = prefix_code + new_k + postfix_code
        if isinstance(v, list):
            v = ",".join(str(v))
        val = escape_ansi(v)
        # prefix_code = postfix_code = ""
        if len(val) > 0 and len(val) < 30:
            # dbug(f"k: {k} v: {v} val: {val}")
            if val.startswith("^"):
                val = val.replace("^", "")
            if val.startswith("+"):
                val = val.replace("+", "")
            val = val.replace("?", "\?")
            v = str(v).replace("^", "")
            codes = split_codes(v)
            prefix_code = codes[0]
            if len(codes) > 1:
                postfix_code = codes[1]
        else:
            v = " "
        new_v = v
        if len(val) > max_width:
            new_v = str(val)[:max_width]
            new_v = prefix_code + new_v + postfix_code
        # dbug(f"repr(k): {repr(k)}, repr(key): {repr(new_k)} repr(v): {repr(v)} repr(val): {repr(val)} repr(new_v): {repr(new_v)}")
        new_d[new_k] = new_v
    my_d = new_d
    # myd = new_d
    """--== Process ==--"""
    # dbug(my_d)
    col = 0
    for k, v in my_d.items():
        # builds myd which is a list of dicts
        # dbug(k)
        if len(str(k)) < 1:
            # skip a bogus (k)ey
            continue
        # dbug(f"col: {col} k: {k} v: {v}")
        myd[col][k] = v
        # dbug(myd)
        if row_num >= num_rows:
            row_num = 1
            col += 1
            # dbug("continuing...")
            continue
        row_num += 1
    # dbug(myd)
    tables = []
    col = 0
    for col in range(cols):
        if len(myd[col]) < 1:
            continue
        if len(myd[col]) < num_rows:
            diff = (num_rows) - len(myd[col])
            for n in range(diff):
                # dbug("adding a new ... row")
                myd[col]["." * (n + 1)] = "..."
        # dbug(f"myd[{col}]: {myd[col]}")
        # dbug(header_b)
        table = gtable(
            myd[col],
            prnt=False,
            header=header_b,
            box_style=box_style,
            neg=neg,
            rnd=rnd,
            human=human,
            box_color=box_color,
            color=color,
            rjust_cols=rjust_cols,)
        tables.append(table)
    columns_l = gcolumnize(tables, sep=sep)
    width = nclen(columns_l[0])
    if title != "" and not boxed_b:
        # dbug(width)
        if box_title:
            titlebox = boxed(title)
            lines = centered(titlebox, width=width, box_color=box_color, color=color)
        else:
            gline_title = gline(width, msg=title, just='center')
            lines.insert(0, gline_title)
    lines.extend(columns_l)
    if footer != "" and not boxed_b:
        # dbug(footer)
        # dbug(width)
        line = gline(width, msg=footer, just='center')
        lines.append(line)
    if boxed_b:
        lines = boxed(lines, title=title, footer=footer, box_color=mstr_box_color)
    if center:
        lines = centered(lines)
    if prnt:
        printit(lines)
    return lines
    # ### EOB def kv_cols(my_d, cols=3, *args, **kvargs): ### #


def kv_cols_demo():
    large_d = {}
    for x in range(30):
        large_d[f'key_{x}'] = f'value_{x}'
    cols = 2    
    kv_cols(large_d, cols, 'prnt', title=f"{funcname()} Demo: {cols} no header ", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', title=f"{funcname()} Demo: {cols} w/header ", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'centered', title=f"{funcname()} Demo: {cols} centered", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', 'centered', title=f"{funcname()} Demo: {cols} w/header and centered ", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'centered', 'boxed', title=f"{funcname()} Demo: {cols} no header cntered and boxed ", mstr_box_clr="red! on black", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', 'centered', 'boxed', title=f"{funcname()} Demo: {cols} w/header cntered and boxed ", mstr_box_clr="yellow! on black", footer=dbug('here'))



# #################################
def key_swap(orig_key, new_key, d):
    # #############################
    """
    purpose: switch or change the keyname on an element in a dictionary
    args:
        orig_key  # original key name
        new_keyA  # new key name
        d         # dictionay to change
    returns: the altered dictionary
    """
    # dbug(f"orig_key: {orig_key} new_key: {new_key}")
    d[new_key] = d.pop(orig_key)
    return d
    # END def keys_swap(orig_key, new_key, d):


# ########################################################
def gcolumnize(msg_l, *args, width=0, color="", **kwargs):
    # ####################################################
    """
    purpose: This will columnize (vertically) a list
    input: msg_l: list|lol, width=0: int, color="": str
    options: 
        - sep: str
        - prnt|print|show = False: bool 
        - centered = False: bool  # only invoked if prnt == True
        - title = "": str   # only invoked if prnt == True
        - footer = "": str  # only invoked if prnt == True
    return: lines: list
    required: import columnize
    If it is a list of lists ( like several boxes made up of lines ) then
    it will list them next to each other
    box1 = +------+
           | box1 |
           +------+
    box2 = +------+
           | box2 |
           +------+
    boxes = box1 + box2
    lines = gcolumnize(boxes)
    printit(lines)
    +------+  +------+
    | box1 |  | box2 |
    +------+  +------+
    # ### or ### #
    mylist = ["One potato", "Two potato", "Three potato", "Four", "Now close the door"] 
    lines = gcolumnize(mylist, width=40)
    printit(lines)
    One potato    Four
    Two potato    Now close the door
    Three potato
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # for box in msg_l:
    #     printit(box)
    """--== Config ==--"""
    sep = kvarg_val(['sep'], kwargs, dflt=1)
    cntr_cols = kvarg_val(["cntr_cols", "center_cols", "cols_cntr", "cols_center"], kwargs, dflt=[])
    my_lol = msg_l
    prnt = bool_val(['prnt', 'print', 'show'], args, kwargs, dflt=False)
    boxed_b = bool_val(['boxed', 'box'], args, kwargs, dflt=False)
    box_color = kvarg_val(['box_color', 'box_clr', 'border_color', 'border_style'], kwargs, dflt="")
    centered_b = bool_val(['center', 'centered', 'cntr', 'cntrd'], args, kwargs, dflt=False)
    title = kvarg_val(['title'], kwargs, dflt="")
    footer = kvarg_val(['footer'], kwargs, dflt="")
    # dbug(my_lol, 'ask')
    # dbug(color)
    """--== Init ==--"""
    col_len = get_columns()
    if width == 0:
        width = int(int(col_len) * 0.8)
    """--== Convert ==--"""
    islol = any(isinstance(el, list) for el in my_lol)
    # dbug(islol, 'ask')
    if not islol:
        import columnize  # I would like to get rid of this someday
        lines = columnize.columnize(msg_l, displaywidth=width)
        lines = lines.split("\n")
        # dbug(type(lines))
        return lines
        # middle_index = len(my_lol) // 2
        # box1 = my_lol[:middle_index]
        # box2 = my_lol[middle_index:]
        # boxes = [box1, box2]
    """--== Process ==--"""
    """--== Init Vars ==--"""
    lines = []
    line_num = 0
    boxes_len = []
    max_box_lines = 0
    # dbug(color)
    color = sub_color(color)
    # dbug(repr(color))
    # clr_tst(color)
    sep_chr = " "
    sep_chrs = color + (sep_chr * sep) + RESET  # between cols
    # dbug(sep_chrs)
    pad_char = gclr(color, " ")  # used to position 'boxes' properly when one has more lines than the other
    # dbug(pad_char)
    # dbug(repr(pad_char))
    """--== Calculate box widths(boxes_len: list) and max box num of lines (max_box_lines: int) ==--"""
    for box_num, box in enumerate(msg_l):
        if len(box) > max_box_lines:
            max_box_lines = len(box)
        # must be the first line
        this_box_width = 0
        for line in box:
            if nclen(line) > this_box_width:
                this_box_width = nclen(line)
        # dbug(this_box_width)
        boxes_len.append(this_box_width)  # number of lines in each box
        # max_len = max(boxes_len)
        # dbug(f"max_box_lines: {max_box_lines} this_box_width: {this_box_width} box_num: {box_num} boxes_len: {boxes_len}")
    """--== Process ==--"""
    while True:
        line = ""
        num_boxes = len(msg_l)  # aka num of cols?
        for box_num, box in enumerate(msg_l):
            # assumes each box is a column
            # printit(box, 'boxed', box_color="red! on yellow!", title=dbug('here'))
            just='left'
            if  box_num in cntr_cols:
                just='center'
            box = allmax(box, justify=just)  # maximizes each string len 
            # dbug(box[line_num])
            if line_num > len(box) - 1:
                # dbug(f"box_num: {box_num} line_num: {line_num} len(box): {len(box)} boxes_len: {boxes_len}")
                pad_len = boxes_len[box_num]
                # dbug(f"box_num: {box_num} line_len: {nclen(line)} pad_len: {pad_len}")
                col_padding = pad_char * pad_len
                # dbug(col_padding)
                # dbug(f"adding col_padding: {col_padding} [len(box): {len(box)}] for box_num: {box_num} boxes_len: {boxes_len}")
                line += col_padding
                # dbug(f"box_num: {box_num} line_num: {line_num} line): [{line}]")
            else:
                # dbug(f"box_num: {box_num} box_len: {len(box)} line_num: {line_num}")
                line += box[line_num]
                # dbug(f"box_num: {box_num} line_num: {line_num} line): [{line}]")
            if box_num < num_boxes - 1:
                # dbug(f"box_num: {box_num} num_boxes: {num_boxes} line_num: {line_num}")
                line += sep_chrs
            # dbug(line)
            if width > col_len:
                dbug(f"Houston, we have a problem... width: {width} exceeds col_len: {col_len}")
                return
        line_num += 1
        # dbug(f"appending line: [{line}]")
        lines.append(line)
        if line_num > max_box_lines - 1:
            # dbug("Done!!!")
            break
    # for line in lines:
    #     dbug("[" + line + "]")
    if prnt:
        printit(lines, boxed=boxed_b, centered=centered_b, title=title, footer=footer, box_color=box_color)
    return lines
    # ### EOB def gcolumnize(boxes, width=0): ### #

# for now, create and alias TODO
gcolumnized = gcolumnize


# #################################
def sayit(msg, *args, prnt=True, **kwargs):
    # #############################
    """
    purpose: will use computer voice to "say" the msg
    options
    - prnt: will print as well
    returns: None
    """
    """--== Imports ==--"""
    import pyttsx3
    """--== Config ==--"""
    rate = kvarg_val(['rate'], kwargs, dflt=150)
    volume = kvarg_val(['vol', 'volume'], kwargs, dflt=0.8)
    gender = kvarg_val(['gender'], kwargs, dflt="m")
    """--== Init ==--"""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)   # rate is w/m 
    engine.setProperty('volume', volume) 
    # use espeak --voices to see them all then add +m|f1-? 
    engine.setProperty('voice', f'english-us+{gender}3')   
    #genders = ["m", "f"]
    #tonals = ["1", "2", "3", "4", "5"]
    #for gender in genders:
    #    for tone in tonals:
    #        voice =  f"'english-us+{gender}{tone}'"
    #        engine.setProperty('voice', voice)
    #        msg = f"The time is {date.today().strftime('%B %d %Y')}. My voice is {voice}"
    #        print(msg)
    #        engine.say(msg)
    """--== Process ==--"""
    engine.say(msg)
    engine.runAndWait()
    if prnt:
        printit(msg)



# ################################
def printit(msg, *args, **kwargs):
    # ############################
    """
   purpose: prepares and prints (option) msg: str|list and can put in unicode color box, centered in terminal and with color
   required: msg: str|list (can contain color codes (see below)
   options: 
        "boxed" | boxed=False  # prepares a box around msg
        "centered" | centered=False  # centers horizontally msg on a termial screen 
        "shadowed" | shadowed=True  # adds a shadow typically around a box
        "prnt" | prnt=True  # print line(s) or just return them as a str
           (useful for input(printit("What do you want? ", 'centered', prnt=False, rtrn_type="str")))
        txt_center: int  # tells how many lines from the top to center within a list
        box_color: str  # eg "blink red on black"
        color: str  # eg "bold yellow on rgb(40,40,40)"
        title: str  # puts a title at top of a box
        footer: str  # puts a footer at the bottom of a box
        style: str  # to select box style - not fully functional yet
        shift: int  # how far to the left (neg) or to right (pos) to shift a centered msg
        width: int  # forces msg to fit in this width using text wrap
        rtrn_type: "list" | "str"  # default is list
        function is pretty extensive...
        color coding: activates decoding using color tag(s) 
            eg msg = "my  message[blink red on black]whatever goes here[/]. The end or close tag will reset color")
    returns: msgs  # list [default] or str depending on rtrn_type
    """
    # dbug(funcname())
    # dbug(msg)
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    mycentered = bool_val(['centered', 'center'], args, kwargs, dflt=False)
    txt_center = kvarg_val(['text_center', 'txt_center', 'txt_cntr', 'box_center', 'center_txt'], kwargs, dflt=0)
    if not isinstance(mycentered, bool):
        txt_center = mycentered
    prnt = bool_val('prnt', args, kwargs, dflt=True)
    boxed_b = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    box_color = kvarg_val(['box_color', 'box_clr', 'border_color', 'border_style'], kwargs, dflt="")
    title = kvarg_val(['title'], kwargs, dflt="")
    footer = kvarg_val(['footer'], kwargs, dflt="")
    # ddbug(f"footer: {footer}")
    color = kvarg_val(['color', 'txt_color', 'text_style'], kwargs, dflt="")
    # dbug(color)
    # color_coded = bool_val(['clr_coded', 'colorized', 'color_coded', 'colored', 'coded'], args, kwargs, dflt=False)
    shadow = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=False)
    style = kvarg_val(['style', 'box_style'], kwargs, dflt="round")
    width = kvarg_val(['width', 'length'], kwargs, dflt=0)
    columnize = bool_val(['columnize', 'columns'], args, kwargs, dflt=False)
    # pad = kvarg_val(['pad'], kwargs, dflt=0)
    shift = kvarg_val('shift', kwargs, dflt=0)
    rtrn_type = kvarg_val(['rtrn_type'], kwargs, dflt='list')
    # end = kvarg_val('end', kwargs, dflt="\n")
    """--== Convert to list (msgs) ==--"""
    if box_color != "" or footer != "" or title != '':
        boxed_b =True
    # dbug(color)
    if isinstance(msg, tuple):
        msgs = list(msg)
    if msg is None or len(str(msg)) == 0:
        # dbug(f"Nothing to do, msg is empty? ... msg: {msg}")
        return None
    if isinstance(msg, list):
        msgs = msg
    if isinstance(msg, float) or isinstance(msg, int):
        msg = str(msg)
    if isinstance(msg, str):
        if not columnize and width > 0:
            msgs = wrapit(msg, width-2)
        if "\n" in msg:
            msgs = msg.split("\n")
        else:
            msgs = [msg]
    if isinstance(msg, dict):
        # wip?
        msgs = []
        for k, v in msg.items():
            msgs.append(f"k: {k} v: {v}") 
    """--== Process ==--"""
    color_coded = False  # init color_coded before test
    for msg in msgs:
        # this is not fully tested, but seems to work... until we curl wttr....
        if re.search(r"\[.+?\].+\[/]", str(msg)):
            # dbug(f"msg: {msg} appears to be color_coded")
            color_coded = True
    if color_coded:
        # from gcolors import clr_coded
        msgs = [clr_coded(msg) for msg in msgs]
    if columnize:
        if width < 1:
            # scr_len = get_columns(rows=False)
            scr_len = get_columns()
            width = ceil(scr_len * 0.8)
        # dbug(f"gcolumnize(msgs: {msgs} width: {width})")
        msgs = gcolumnize(msg, width=width)
        # dbug(f"gcolumnized msgs: {msgs}")
    if boxed_b:
        # dbug(msgs)
        # dbug(txt_center)
        # dbug(color)
        # dbug(footer)
        msgs = boxed(msgs, title=title, footer=footer, color=color, box_color=box_color, txt_center=txt_center, width=width, style=style)
    else:
        # dbug(color)
        COLOR = sub_color(color)  # TODO fix this so that it is not needed
        msgs = [COLOR + str(m) for m in msgs]
        # dbug(f"This is a test of color: {color} using repr(COLOR): {repr(COLOR)} " + COLOR + " testing color " + RESET)
    if shadow:
        msgs = shadowed(msgs)
    if mycentered:
        msgs = centered(msgs, shift=shift)
    # dbug(prnt)
    # prnt = True
    if prnt:
        [print(ln) for ln in msgs]
    # dbug(rtrn_type)
    if rtrn_type == 'str':
        # NOTE: If you made this invisible (not prnt) then you may want to add this option as well rtrn_type="str"
        # there are times when you want no prnt but still return lines (like in gcolumnize) so these two options need to be used carefully
        msgs = "\n".join(msgs)  # cinput() needs this to be a str
    return msgs
    # #### EOB def printit(msg, *args, **kwargs): ### #


def clr_coded(msg_s):
    """
    purpose: takes any msg string containing tags for colors and decodes them into a colorized string
    requires: msg_s: str
    returnd: colorized string
    decode a string - replace \[color\].*[\/] with code and reset
    requires a space before the first bracket
    """
    """--== debug ==--"""
    # dbug(funcname() + f" msg_s: {msg_s} ")
    """--== Process ==--"""
    rgx = True
    # this loop algorythm seems lame to me but it works
    while rgx:
        # dbug(msg_s)
        msg_s = msg_s.replace("[/]", gclr('reset'))
        pattern = r'\[([^\[]+?)\]'  # works!
        rgx = re.search(pattern, msg_s)
        if rgx:
            color = rgx.group(1)
            color = color.strip()
            # dbug(f"sending color: {color} to gclr()" + RESET)
            clr_code = gclr(color)
            # dbug(f"Got this back from gclr({color}) repr(color_code): {repr(clr_code)} clr_code: {clr_code}" + RESET)
            bracketed_color = f'\[\s*{color}\s*?\]'
            # # dbug(bracketed_color)
            msg_s = re.sub(bracketed_color, clr_code, msg_s)
    # dbug(f"returning: {repr(msg_s)}")  # may have RESET appended to it already
    return msg_s
    # ### EOB def clr_coded(msg_s): ### #


def gclr(color='normal', text="", **kwargs):
    """
    Purpose: to return color code + text (if any) NOTE: sub_color() uses this!
    input: 
        text: str = ""  # if "" then the color code alone is returned
        color: str = 'normal'  # examples: 'red on black', 'bold green on normal', 'bold yellow on red', 'blink red on black' etc 
    Notes:
        color is the first argument because you may just want to return the color code only
        run gcolors.demo() to see all color combinations 
    returns: color coded [and text]
    """
    """--== debug ==--"""
    # ddbug(f"funcname(): {funcname()}")
    # ddbug(f"color: {color}")
    """--== Config ==--"""
    reset_b = kvarg_val('reset', kwargs, dflt=False)  # add a RESET to the end of text
    """--== Init ==--"""
    color = color.lower()
    PRFX = "\x1b["
    PRFX2 = "\033["
    RESET = PRFX + "0m"
    fg = bg = ''
    STYLE_CODES = ""
    color = color.strip()
    text = str(text)
    """--== Process ==--"""
    if color == "":
        return "" + text
    if color == 'reset':
        return RESET + text
    if PRFX in color or PRFX2 in color:
        # dbug(f"Found either PRFX or PRFX2 in color: {repr(color)}")
        return color + text
    """--== Pull out and Xlate STYLE ==--"""
    if "fast_blink" in color:
        # we have to do this special case first - otherwise "blink" will get pulled out incorrectly from "fast_blink"
        STYLE_CODES += f"{PRFX}{styles_d['fast_blink']}m"
        color = fg.replace("fast_blink", "")
    for s in styles_d:
        # ddbug(f"chkg for style: {s} in fg_color: {color}...")
        if s in color:
            fg = fg.replace(s, "").strip()
            # print(f"s: {s}")
            if s != 'normal':
                STYLE_CODES += f"{PRFX}{styles_d[s]}m" 
            color = color.replace(s, "")  # pull out style
    """--== Process split fg from bg ==--"""
    if color.startswith("on "):
        color = 'normal ' + color  # make fg = normal
        # print(f"myDBUG: funcname: {funcname()} lineno: {lineno()} color is now: {color}")
    """--== Split color into fgbg_l ==--"""
    fg_color = bg_color = ""  # init these first
    fgbg_color = color.split(" on ")  # create a fgbg list split on " on "
    # ddbug(f"fgbg_color): {fgbg_color}")
    fg_color = fgbg_color[0]
    if len(fgbg_color) > 1:
        bg_color = fgbg_color[1]
    # ddbug(f"fgbg_color: {fgbg_color} repr(fg_color): {repr(fg_color)}" + RESET + f" repr(bg_color): {repr(bg_color)}" + RESET)
    """--== Process FG_CODE ==--"""
    if fg_color.strip() == "" or fg_color.strip() == 'normal':
        # ddbug(f"fg_color: [{fg_color}]")
        FG_CODE = ""
    else:
        fg_color = xlate_clr(fg_color)
        # ddbug(fg_color)
        # ddbug(f"fg_color: [{fg_color}]")
        FG_CODE = ""
        fg_rgb_substring = re.search(r".*rgb\((.*?)\).*", fg_color)
        if fg_rgb_substring:
            # found an rgb(...) inclusion
            rgb_color = fg_rgb_substring.group(1)
            r, g, b = rgb_color.split(",")
            FG_RGB_CODE = rgb(r, g, b, prfx=False)  # returns with "m" on it
            # ddbug(f"FG_RGB_CODE: {FG_RGB_CODE}")
            FG_CODE = PRFX + "38" + FG_RGB_CODE  # has "m" on it already
            # ddbug(f"repr(FG_CODE): {repr(FG_CODE)}")
        else:
            # ddbug(f"fg_color: [{fg_color}]")
            # if PRFX in fg_color or PRFX2 in fg_color or fg_color == "":
            if PRFX in fg_color or PRFX2 in fg_color:
                FG_CODE = fg_color
            else:
                # ddbug(f"fg_color: [{fg_color}]")
                if " on" in fg_color: 
                    # ddbug("this is should never happen right?")
                    fg_color = fg.replace(" on", "")
                # ddbug(f"fg_color: [{fg_color}]")
                fg_color = fg_color.strip()
                # ddbug(f"fg_color: [{fg_color}]")
                FG_CODE = PRFX + fg_colors_d[fg_color] + "m"  # fg_colors do not need "38"
    # ddbug(f"Test fg_color: [{fg_color}] {RESET}{FG_CODE}This should be in assigned fg_color {RESET}Here is the repr(FG_CODE): {repr(FG_CODE)}")
    """--== Process BG ==--"""
    # ddbug(f"bg_color: {bg_color}")
    if bg_color.strip() == "":
        BG_CODE = ""
    else:
        # bg_color is not blank
        bg_color = xlate_clr(bg_color)
        # ddbug(bg_color)
        bg_rgb_substring = re.search(r".*rgb\((.*?)\).*", bg_color)
        if bg_rgb_substring:
            rgb_color = bg_rgb_substring.group(1)
            r, g, b = rgb_color.split(",")
            BG_RGB_CODE = rgb(r, g, b, bg=False, prfx=False)  # returns with "m" on it 
            # ddbug(f"repr(BG_RGB_CODE): {repr(BG_RGB_CODE)}")
            BG_CODE = PRFX + "48" + BG_RGB_CODE  # has "m" on it already
            # ddbug(f"repr(BG_CODE): {repr(BG_CODE)}")
        else:
            # bg_color is not an rgb color
            # ddbug(f"bg_color: {bg_color}")
            if PRFX in bg_color or PRFX2 in bg_color or bg_color == "":
                BG_CODE = bg
            else:
                # bg_color is not pre-CODED
                if bg == "dim black":
                    # hey, it's ugly, but it works the way I want
                    BG_RGB_CODE = rgb(0, 0, 0, bg=True, prfx=False)
                    BG_CODE = PRFX + "48" + BG_RGB_CODE  # has "m" on it already
                else:
                    # bg_color is not == dim black
                    bg_color = bg_color.strip()
                    # dbug(bg_color, 'ask')
                    BG_CODE = bg_colors_d[bg_color]
                    # ddbug(f"repr(BG_CODE): {repr(BG_CODE)}")
                    BG_CODE = PRFX + BG_CODE + "m"  # understood to be BG so "48" not needed
                    # ddbug(f"Testing repr(BG_CODE): {repr(BG_CODE)} {BG_CODE} TEST TEXT {RESET}")
                    # dbug('ask')
    # ddbug(f"Test bg_color: [{bg_color}] {RESET}{BG_CODE}This should be in assigned bg_color {RESET}Here is the repr(BG_CODE): {repr(BG_CODE)}" + RESET)
    """--== SEP_LINE ==--"""
    CODE = STYLE_CODES + FG_CODE + BG_CODE
    # clr_tst(CODE, color=color)
    rtrn = CODE + text
    if " " in STYLE_CODES + FG_CODE + BG_CODE:
        ddbug("WWWWWWWWWWWWHHHHHHHHHHHHAAAAAAAAAAAATTTTTTTTTTT")
        rtrn = STYLE_CODES.replace(" ", "")
        rtrn = FG_CODE.replace(" ", "")
        rtrn = BG_CODE.replace(" ", "")
    if "on" in rtrn:
        dbug("Problem: found 'on' in rtrn", 'ask')
    if reset_b:
        # dbug(reset_b)
        rtrn = rtrn + RESET
    # ddbug(f"color: {color} repr(rtrn)): {repr(rtrn)} rtrn: {rtrn} This should be in rtrn color" + RESET)
    return rtrn
    # ### EOB def gclr(color='normal', text=""): ### #


def clr_tst(CODE, color="unknown"):
    """
    purpose: strickly for developer use - given an ansi color CODE will display it in a way to see if it works as expected
    displays COLOR_TEST: This should be displayed using CODE
    returns: None
    """
    # This is strictly for developer testing
    if not CODE.startswith(PRFX):
        dbug(f"clr_tst(CODE, color='unknown') - apprently CODE does not seem like a color CODE... returning...")
        return
    from inspect import (getframeinfo, currentframe, getouterframes)
    cf = currentframe()
    fname = str(getframeinfo(currentframe().f_back).function)
    msg = " called from line: ["+str(cf.f_back.f_lineno) + " Func:" + fname + "] "
    SAMPLE_CODE = '\x1b[38;2;0;0;255m\x1b[47m'
    sample_txt = f"{RESET}COLOR TEST: {repr(SAMPLE_CODE)}{SAMPLE_CODE}    This should be displayed using SAMPLE_COLOR    {RESET}{repr(RESET)}"
    print(sample_txt)
    print("-----------------------------------")
    sample_txt = f"{RESET}COLOR TEST: {repr(CODE)}{CODE}    This should be displayed in color: {color}    {RESET}{repr(RESET)}"
    print(sample_txt)
    print(f"------{msg}-------")


def shades(color, num=16):
    """
    purpose: returns a list of increasing intensity color shades 
    requires = color: str
    options:
    -   num=16  <-- number to divide into 255 ~ the number of color intensities
    -   rtrn???  TODO return codes or text... CODES | strings/text/txt
    returns list # of ncreasing colors
    """
    colors = []
    step = 255 // num
    for shade in range(0, 255, step):
        if color.lower() == 'red':
            my_color = f'rgb({shade}, 0, 0)'
        if color.lower() == 'green':
            my_color = f'rgb(0, {shade}, 0)'
        if color.lower() == 'blue':
            my_color = f'rgb(0, 0, {shade})'
        if color.lower() == 'yellow':
            my_color = f'rgb({shade}, {shade}, 0)'
        if color.lower() in ('cyan', 'green-blue', 'blue-green'):
            my_color = f'rgb(0, {shade}, {shade})'
        if color.lower() in ('violet', 'magenta'):
            my_color = f'rgb({shade},0,{shade})'
        colors.append(my_color)
    return colors
            

def rgb(r=80, g=80, b=140, text="", fg=False, bg=False, prfx=False, reset=False):
    """
    purpose: translated rgb(r,g,b) text into ansi color CODE
    input: r, g, b, text 
        prfx: bool = False
        bg: bool = False # if set to true the color is applied to bg
    returns: rgb color coded text 
    """
    # global RESET
    # dbug(f"r: {r} g: {g} b: {b}")
    # PRFX = "\033["
    PRFX = "\x1b["
    # global PRFX
    # number = 16 + 36 * r + 6 * g + b
    # dbug(f"{PRFX}{number}m{number}")
    fgbg_num = ""
    if fg:
        fgbg_num = 38
    r = int(r) 
    g = int(g)
    b = int(b)
    if bg:
        fgbg_num = 48
    if prfx:
        rtrn = f"{PRFX}{fgbg_num};2;{r};{g};{b}m"
    else:
        # user will probably want to prefix this with a ";"
        if fgbg_num == "":
            rtrn = f";2;{r};{g};{b}m"
        else:
            rtrn = f"{fgbg_num};2;{r};{g};{b}m"
    # dbug(f"my color {rtrn} is this and my text: {text}")
    if not reset:
        RESET = "" 
    if len(text) > 0:
        rtrn += text + RESET
    # dbug(f"rtrn: {rtrn}")
    return rtrn


def xlate_clr(color):
    """
    purpose: translates special color names to rgb(r,g,b) for processing
    requires: special color eg:
    - greyXX | grayXX  # where XX is a precent gradient of gray from 0,0,0 for black! to 255,255,255 white
    - white!           # solid 255,255,255 white
    - black!           # solid 0,0,0 black
    - red!             # solid bright 255,0,0 red
    - green!           # solid bright 0,255,0 green
    - blue!            # solid bright 0,0,255 blue
    - blue!            # solid bright 0,0,255 blue
    - blue!            # solid bright 0,0,255 blue
    - yellow!          # solid bright 255,255,0 yellow
    - magenta!         # solid bright 255,0,255 magenta
    - cyan!            # solid bright 0,255,255 cyan
    returns: rgb(r,g,b) text string instead of supplied color

    --== Xlate special colors to rgb() ==--
    """
    grey_tone = re.search(r"(gr[ea]y)(\d+)", color)
    if grey_tone:
        grey_word = grey_tone[1]
        grey_tone = grey_tone.group(2)
        # ddbug(f"grey_word: {grey_word} grey_tone: {grey_tone}")
        # grey = f"rgb({grey_tone}, {grey_tone}, {grey_tone})"
        # dbug(f"Found grey in color: {color}")
        # color = re.sub(r"gr[ea]y(\d+)", grey, color)
        r = g = b = int(grey_tone)
        grey_color = f"rgb({r}, {g}, {b})"
        color = re.sub(f"{grey_word}{grey_tone}", grey_color, color)
        # ddbug(f"grey_color: {grey_color} TEST {RESET} repr(grey_color): [{repr(grey_color)}] {RESET} repr(color): {repr(color)} {RESET}")
    """--== SEP_LINE ==--"""
    rgx = re.search(r"gr[ea]y", color)
    # If it is just "grey" or "gray"
    if rgx:
        # dbug(f"color: {color}")
        r = g = b = 100
        rgb_color = f"rgb({r},{g},{b})"
        color = re.sub(r"gr[ea]y", rgb_color, color)
        # dbug(f"repr(color): {repr(color)}")
    # dbug(f"color: {color} repr(color): {repr(color)} text: {text}")
    if 'white!' in color:
        r = g = b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('black!', myrgb)
    if 'black!' in color:
        r = g = b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('black!', myrgb)
    if 'red!' in color:
        r = 255
        g = 0
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('red!', myrgb)
    if 'green' in color:
        # doing this because the defailt green is more of a washed out brown 
        r = 0
        g = 215
        b = 0
    if 'green!' in color:
        r = 0
        g = 255
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('green!', myrgb)
    if 'blue!' in color:
        r = 0
        g = 0
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('blue!', myrgb)
    if 'yellow!' in color or 'bold yellow' in color:
        r = 255
        g = 255
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('yellow!', myrgb)
    if 'magenta!' in color:
        r = 255
        g = 0
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('magenta!', myrgb)
    if 'cyan!' in color:
        r = 0
        g = 255
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('cyan!', myrgb)
    if 'white!' in color:
        r = 255
        g = 255
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('white!', myrgb)
    return color



# #################
def sub_color(clr, *args, **kwargs):
    # #############
    """
    purpose: substiture ansi color CODE for given color
    returns ansi-CODE
    """
    # dbug(funcname())
    # dbug(f"clr: {clr} repr(clr): {repr(clr)}")
    rset_b = bool_val(['reset', 'rst', 'rset'], args, kwargs, dflt=False)
    PRFX = "\x1b["
    # PRFX2 = "\033["
    if clr.startswith(PRFX):
    # dbug("clr starts with PRFX")
        return clr
    RESET = PRFX + "0m"
    if rset_b and clr == "":
        return RESET
    # if PRFX in clr or PRFX2 in clr or clr == "":
    #     dbug(clr)
    #     return clr
    clr = escape_ansi(clr)
    # dbug(clr)
    if clr.upper() == "RESET" or clr.upper() == "NORMAL":
        # dbug(clr)
        return RESET
    # dbug(clr)
    COLOR_CODE = gclr(text="", color=clr)
    # dbug(f"clr: {clr} COLOR_CODE [test]: {COLOR_CODE}[test] {repr(COLOR_CODE)}{RESET}")
    return COLOR_CODE


RESET = gclr("reset")
BLACK = gclr("rgb(0,0,0)")


# ###############################
def wrapit(sentence, length=20, color=""):
    # ###########################
    """
    input is sentence which can be a string or list
    returns lines list wrapped using length and color if provided
    NOTE: all color codes will get stripped out before processing
    """
    # dbug(f"sentence: [{sentence}] length: {length}")
    if length < 1:
        dbug(f"length: {length} is a problem")
    sentence = escape_ansi(sentence)
    RESET = COLOR = ""
    if color != "":
        COLOR = sub_color(color)
        RESET = sub_color('reset')
    import textwrap
    wrapper = textwrap.TextWrapper(width=length)
    lines = []
    if isinstance(sentence, str):
        # dbug(f"sentence: [{repr(sentence)}] length: {length}")
        if "\n" in sentence:
            sentence = sentence.split("\n")
            # this will get passed to the next block
        else:
            sentence = sentence.lstrip()
            lines = wrapper.wrap(text=sentence)
            # dbug(lines)
            return lines
    if isinstance(sentence, list):
        for line in sentence:
            line = line.rstrip()
            # dbug(line)
            # dbug(type(line))
            if "\n" in line:
                # dbug("found new`line in line")
                new_lines = line.split("\n")
                for new_line in new_lines:
                    if len(line) > length:
                        lines.extend[wrapper.wrap(text=new_line)]
                # dbug("continuing")
                continue
            if len(line) > length:
                # dbug("did not find newline in line")
                line = line.rstrip()
                # dbug(f"line: {line} length: {length} len(line): {len(line)}")
                try:
                    lines.extend[wrapper.wrap(text=line)]
                except:
                    # dbug(lines)
                    lines.append(line)
                    # dbug(lines)
            else:
                lines.append(line)
    lines = [f"{COLOR}{line}{RESET}" for line in lines]
    # dbug(lines)
    return lines


def get_columns(*args, **kwargs):
    """
    gets screen/terminal cols OR rows
    returns int(columns)| int(rows: bool) | int(cols), int(rows) both: bool
    """
    """--== Config ==--"""
    shift = kvarg_val("shift", kwargs, dflt=0)  # this is probably never used
    rows_b = bool_val("rows", args, kwargs, dflt=False)
    both_b = bool_val("both", args, kwargs, dflt=False)
    """--== Init ==--"""
    columns = 80
    # rows = 40
    """--== Process ==--"""
    try:
        num_rows, columns = os.popen("stty size", "r").read().split()
    except Exception as e:
        print(f"Error: {e}")
    # print(f"returning columns: {columns}")
    if rows_b:
        return int(num_rows)
    if both_b:
        return int(columns), int(num_rows)
    columns = int(columns)
    # dbug(columns)
    columns = columns + int(shift)
    # dbug(columns)
    return  int(columns)


def replace_all(msg, with_d):
    """
    replaces ever dict key with dict value in a string
    with_d eg: {'\t', '  ', 'foo', 'bar'}
    TODO need more doc info here
    """
    for i, j in with_d.iteritems():
        msg = msg.replace(i, j)
    return msg


# ##############################################################################
def boxed(msgs, *args, cornerchr="+", hchr="=", vchr="|", padmin=1, color="", title="", footer="", style="single", shadow=False, **kwargs):
    # ##########################################################################
    """
    purpose: draw a unicode box around msgs
    args: msgs
    options:
        centered | center: bool  # centers box on the screen
        prnt: bool
        txt_center: int  # num of lines from top to center in the box
        color: str  # text color
        box_color: str  # color of border
        title, footer: str # goes in topline or bottom line centered of box 
        width forces the width size defaults to # screen columns
        shadowed | shadow: bool # adds a shadow right and bottom    
        ... some other options; see below
    returns boxed lines: list
    NOTES: this function does not print - it returns the box lines
    """
    # dbug(funcname())
    # reset = "\x1b[0m"
    # from math import ceil
    # dbug(footer)
    """--== Config ==--"""
    center = kvarg_val('center', kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print'], args, kwargs, dflt=False)
    shadow = bool_val(["shadow", "shadowed"], args, kwargs, dflt=False)
    txt_center = kvarg_val(["txt_center", "text_center"], kwargs, dflt=0)
    # dbug(txt_center)
    if isinstance(center, int) and center > 0:
        txt_center = center
    # dbug(txt_center)
    title = kvarg_val(['title'], kwargs, dflt=title)
    box_color = kvarg_val(['bclr', 'box_color', 'border_color', 'box_clr', 'border_clr'], kwargs, dflt="")
    shadow = kvarg_val(['shadow', 'shadowed'], kwargs, dflt=shadow)
    pad = kvarg_val(['pad'], kwargs, dflt=" ")
    top_pad = kvarg_val("top_pad", kwargs, dflt=0)  # "semi" (ie " ") blank lines to add at top
    bottom_pad = kvarg_val(["bottom_pad", "bot_pad", "botpad"], kwargs, dflt=0)  # "semi" (ie " ") blank lines to add to the bottom
    width = kvarg_val("width", kwargs, dflt=0)
    """--== Init ==--"""
    PRFX = "\x1b["
    box_chrs = get_boxchrs(box_style=style)
    # tl = top left         = box_chrs[0]
    # hc = horz char        = box_chrs[1]
    # tr = top right        = box_chrs[2]
    # vc = vert char        = box_chrs[3]
    # rs = right separator  = box_chrs[4]
    # ms = mid sep          = box_chrs[5]
    # bl = bot left         = box_chrs[6]
    # bs = bot sep          = box_chrs[7]
    # br = bot right = box_chrs[0
    tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    """--== Convert ==--"""
    if isinstance(msgs, list):
        new_msgs = []
        for msg in msgs:
            # Get rid of completely blank lines - leave it if it has even a space in it
            # dbug(f"\n[msg]")
            # ruleit()
            # dbug(nclen(msg))
            if nclen(msg) == 0:
                continue
            new_msgs.append(msg)
        msgs = new_msgs
    if len(msgs) < 1:
        # dbug(f"msgs: {msgs} appears empty... returning...")
        return
    if isinstance(msgs, int) or isinstance(msgs, float):
        msgs = str(msgs)
    if "\n" in str(msgs):
        msgs = msgs.splitlines()
        # dbug(f"msgs: {msgs}")
    if isinstance(msgs, str):
        if '\t' in msgs:
            msgs = msgs.replace('\t', '  ')
        # dbug(f"msgs: {msgs} type(msgs): {type(msgs)}")
        if '\n' in msgs:
            msgs = msgs.split('\n')
            # dbug(msgs)
        else:
            # cast it to list
            msgs = [msgs]
            # dbug(msgs)
    if isinstance(msgs, list):
        msgs = [str(x) for x in msgs]
        msgs = [msg.replace('\t', '  ') for msg in msgs if msg != ""]  # this took a while to figure out!
        # for msg in msgs:
        #     dbug(f"[{msg}]")
    """--== Process ==--"""
    max_msg_len = 0
    for msg in msgs:
        # dbug(msg)
        if nclen(msg) > max_msg_len:
            max_msg_len = nclen(msg)
    if nclen(title) > max_msg_len:
        # if len(title) is longer than max_msg_len...
        max_msg_len = nclen(title)
    if nclen(footer) > max_msg_len:
        # if len(footer) is longer than max_msg_len...
        max_msg_len = nclen(footer)
    # dbug(max_msg_len)
    columns = get_columns()
    # dbug(width)
    if width == 0:
        # dbug(width)
        reduce_by = 6
        if shadow:
            reduce_by += 2
        if max_msg_len >= int(columns):
            max_msg_len = int(columns) - reduce_by
        width = (max_msg_len + 2 + (2 * padmin))  # or declared which makes max_msg_len = width - 2 - (2 * padmin)
        if width >= int(columns):
            width = int(columns) - reduce_by
    # dbug(max_msg_len)
    # dbug(width)
    """--== SEP LINE ==--"""
    # for msg in msgs:
    #     dbug(f"[{msg}]")
    lines = []
    msg = title
    topline = gline(width, lc=tl, rc=tr, fc=hc, title=title, center=True, box_color=box_color, color=color)
    # dbug(topline)
    lines.append(topline)
    new_lines = []
    """--== SEP LINE ==--"""
    for m in msgs:
        if nclen(m) > width - 4 and m is not None:
            wrapped_lines = wrapit(m, length=int(width - 4), color=color)  # I discovered that the -x is needed for extra measure
            if wrapped_lines is not None:
                for line in wrapped_lines:
                    if line is not None:
                        new_lines.append(line)
        else:
            # dbug(f"m: [{m}]")
            new_lines.append(m)

    """--== SEP LINE ==--"""
    # dbug(lines)
    if top_pad > 0:
        for n in range(top_pad):
            # adds semi blank lines at the top... spaces are needed because other functions will drop completely blank lines 
            # this can be useful if you gcolumize boxes and then want to combine them into another 'parent' box
            # dbug(f"top line pad requested top_pad: {top_pad}")
            new_lines.insert(0, "   ")
    if bottom_pad > 0:
        for n in range(bottom_pad):
            new_lines.append("    ")
    for cnt, msg in enumerate(new_lines):
        if txt_center:
            center = 99
        if isinstance(txt_center, int) and cnt < txt_center:
            # if center is a number then center every line less than int(center)
            doline_center = True
            msg = msg.strip()
        else:
            doline_center = False
        if msg.startswith(PRFX) and not msg.endswith(RESET):
            # dbug(repr(RESET))
            msg = msg + RESET
        # dbug(repr(msg))
        # dbug(f"msg: {msg}")
        line = gline(width, lc=vc, rc=vc, fc=" ", pad=pad, msg=msg.replace("\n", ""), box_color=box_color, center=doline_center, color=color)
        # dbug(line)
        # dbug(repr(line))
        lines.append(line)
    # bottomline = doline(width, echrs=[bl, br], hchr=hc, footer=footer, box_color=box_color, color=color, center=True)
    bottomline = gline(width, lc=bl, rc=br, fc=hc, footer=footer, box_color=box_color, color=color, center=True)
    lines.append(bottomline)
    # dbug(lines)
    if shadow:
        # dbug(shadowed)
        lines = shadowed(lines)
    # dbug(lines)
    if prnt:
        printit(lines)
    return lines
    # ### EOB def boxed(msgs, *args, ..., **kvargs): ### #


# ##################################
def gline(width=0, msg="", *args, **kwargs):
    # ##############################
    """
    args: width: int, msg: str <-- msg has to be a key=val pair! eg: gline(60, msg="My Message", just='center')
    options: width, lc, rc, fc, box_color, color, pad, lpad, rpad, lfill_color,  rfill_color, just: str
    returns: line: str
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # if "TEST" in msg:
    # dbug(f"msg: [{msg}]")
    """--== Config ==--"""
    msg = kvarg_val(['msg', 'title', 'footer'], kwargs, dflt=msg)
    # dbug(repr(msg))
    width = kvarg_val(['width', 'length'], kwargs, dflt=width)
    lc = kvarg_val(['lc', 'ec', 'echr'], kwargs, dflt="")
    rc = kvarg_val(['rc', 'tr', 'br', 're'], kwargs, dflt=lc)
    fc = kvarg_val(['fc', 'fill_chr', 'hc'], kwargs, dflt=" ")
    box_color = kvarg_val(['box_color'], kwargs, dflt="")
    # color = kvarg_val(['color'], kwargs, dflt="reset")
    color = kvarg_val(['color'], kwargs, dflt="")
    # dbug(f"Config... color: [{color}color_coded]{sub_color('reset')})")
    pad = kvarg_val(['pad'], kwargs, dflt="")
    lpad = kvarg_val(['lpad'], kwargs, dflt=pad)
    lfill_color = kvarg_val(['lfill_color'], kwargs, dflt=color)
    rpad = kvarg_val(['rpad'], kwargs, dflt=pad)
    rfill_color = kvarg_val(['rfill_color'], kwargs, dflt=color)
    # the order here for just is important
    just = kvarg_val("just", kwargs, dflt='ljust')
    centered = bool_val(["centered", "center"], args, kwargs, dflt=False)
    if centered:
        # change just to 'center' - the bool val centered get ignored after this
        just = 'center'
    just = kvarg_val(['ljust'], kwargs, dflt=just)
    just = kvarg_val(['rjust'], kwargs, dflt=just)
    """--== Init ==--"""
    RESET = sub_color('reset')
    # if rfill_color == "":
    #     rfill_color = color
    # if lfill_color == "":
    #     lfill_color = color
    """--== Process ==--"""
    if color == "":
        color = 'reset'
    COLOR = sub_color(color)
    if box_color == "":
        box_color = 'reset'
    BOX_COLOR = sub_color(box_color)
    LFILL_COLOR = sub_color(lfill_color)
    RFILL_COLOR = sub_color(rfill_color)
    """--== color_coded??? ==--"""
    color_coded = False
    if re.search(r"\[.+?\].+\[/]", str(msg)):
        # dbug(f"msg: {msg} appears to be color_coded")
        color_coded = True
    if color_coded:
        msg = clr_coded(msg)
    """--== EOB ==--"""
    if nclen(msg) > 0:
        # nc_msg = escape_ansi(msg)
        # dbug(repr(msg))
        # dbug(repr(nc_msg))
        # dbug(f"msg: [{msg}]")
        msg = lpad + msg + RFILL_COLOR + rpad
        # dbug(f"msg: [{msg}]")
    # dbug(len(msg))
    msg_len = nclen(msg)
    # dbug(msg_len)
    flen = width - msg_len - len(rc) - len(lc)
    # dbug(f"width: {width} just: {just} msg_len: {msg_len} flen: {flen} repr(msg): [{repr(msg)}] len(lpad): {len(lpad)} len(pad): {len(pad)} len(rpad): {len(rpad)}", 'ask')
    # if flen < width:
    #     flen = flen
    if just == 'center':
        llen = rlen = (flen // 2)
        diff = flen - (llen + rlen)
        rlen += diff
        # dbug(f"just: {just} width: {width} msg_len: {msg_len} diff: {diff} =  flen: {flen} - ( llen: {llen} - rlen: {rlen} )")
    if just == 'ljust':
        # llen = len(lpad)
        llen = 0  # lpad has already been applied
        rlen = flen  # - len(rpad)  # ???? not sure about this.... 20220803
        # dbug(f"just: {just} width: {width} msg_len: {msg_len}  llen: {llen} = len(lpad): {len(lpad)}  rlen: {rlen} = flen: {flen} - len(lpad): {len(lpad)} len(rpad): {len(rpad)}")
    if just == 'rjust':
        rlen = 0
        llen = flen
    # dbug(llen)
    # dbug(width)
    # dbug(rlen)
    # dbug(f"fc: [{fc}] pad: [{pad}] msg: {msg}")
    # dbug(f"msg: [{msg}]")
    if nclen(msg) > 0:
        # dbug(repr(msg))
        # if "TEST" in msg:
        #     dbug(f"msg): [{msg}]")
        #     dbug(repr(LFILL_COLOR))
        #     dbug(repr(RFILL_COLOR))
        if fc == ' ':  # then treat it as a pad... use COLOR instead of BOX_COLOR
            # dbug(f"{RESET}repr(BOX_COLOR): [{repr(BOX_COLOR)}] repr(COLOR): [{repr(COLOR)}] fc: [{fc}] rc: [{rc}] msg: [{msg}] repr(LFILL_COLOR): [{repr(LFILL_COLOR)}] rlen: {rlen} repr(RFILL_COLOR): [{repr(RFILL_COLOR)}]")
            # if "Quote" in msg:
            #     dbug(f"msg: [{msg}]")
            line = RESET + BOX_COLOR + lc + RESET + LFILL_COLOR + (fc * llen) + msg +  RFILL_COLOR + (fc * rlen) + RESET + BOX_COLOR + rc + RESET
            # dbug(f"line: [{line}]")
        else:
            # dbug(f"{RESET}BOX_COLOR: " + BOX_COLOR + "box color " + RESET + "COLOR: " + COLOR + f"color fc: [{fc}] msg: [{msg}]")
            # line = BOX_COLOR + COLOR + lc + (fc * llen) + msg + BOX_COLOR + (fc * rlen) +  RESET + rc + RESET
            line = RESET + BOX_COLOR + lc + (fc * llen) + COLOR + msg + BOX_COLOR + (fc * rlen) + rc + RESET
        # dbug(repr(line))
    else:
        line = RESET + BOX_COLOR + lc + (fc * llen) + (fc * rlen) + rc + RESET
    # dbug(f"repr(color): {repr(color)} repr(box_color): {repr(box_color)}  line: [{line}]")
    return line
    # ### EOB def gline(width=0, *args, **kwargs): ### #


# #############
class MenuBox:
    # #########
    """
    purpose:
        sets up a menu selection box
        executes selected function and arguments
        quits (returns) on "Enter" "Q" or "q"
    arguments:
        bclr: box color eg "reb" "blue" "green"
        clines: number of lines to center in the box
        center: center menu default is True
    methods:
        add_selection(["selection_name", func, arg1, arg2,...])  # needs an entry for arg(s) even if it is ''
        show()
    useage:
        mainmenu = Menu("Main")
        mainmenu.add_selection(["get statistics", get_stats, f"{symbol}"])
        mainmenu.add_selection(["display_chart", do_chart, f"{symbol}"])
        mainmenu.add_selection(["display_chart", run_fun, ""])
        ans = ""
        while ans is not None:
            ans = mainmenu.show()
    """
    def __init__(self, name):
        self.name = name
        self.title = ""  # default: f"Menu: {self.name}"
        self.selections = {}
        self.msgs = []
        self.cnt = 0
        self.clines = 2
        self.bclr = ""
        self.center = True
    """--== SEP_LINE ==--"""
    def add_selection(self, selection):
        # selection should be [ "title", func, arg1, arg2, arg3, ... ]
        # dbug(f"selection: {selection}")
        # dbug(f"selection[0]: {selection[0]}")
        # self.selections[selection[0]] = selection[1]
        if isinstance(selection, str):
            selection = selection.split(",")
        if not isinstance(selection, list):
            dbug(f"Selection submission must be a list with ['name', func, 'arg1', 'arg2', ..] selection: {selection}")  # noqa:
            sys.exit()
        else:
            if len(selection) < 3:
                dbug(f"Too few items in selection - must be > 2 you submitted [{len(selection,)}] selection: {selection}")  # noqa:
                sys.exit()
        self.cnt += 1
        self.selections[str(self.cnt)] = selection
    """--== SEP_LINE ==--"""
    def show(self):
        self.title = f"Menu: {self.name}"
        msgs = []
        msgs.append(f"{self.title}")
        msgs.append("=" * nclen(self.title))
        # dbug(f"self.selections: {self.selections}")
        cnt = 0
        for selection in self.selections:
            cnt += 1
            # dbug(f"selection: {selection}")
            item = self.selections[selection][0]
            # dbug(f"item: {item} type(item): {type(item)}")
            # dbug(f"type(self.selections[selection][2:],): {type(self.selections[selection][2:],)}: {self.selections[selection][2:]}",)  # noqa:
            cmd = self.selections[selection][1]
            arguments = self.selections[selection][2:]
            # if len(arguments) == 1:
            #     dbug(f"cmd: {cmd} arguments: {arguments}")
            # dbug(f"cmd: {cmd} arguments: {arguments}")
            msgs.append(f"{cnt}. {item}")
            # cmd(*arguments)
        printit(centered(boxed(msgs, center=2, bclr=self.bclr)))
        # if center:
        #     printit(centered(boxed(msgs, center=2, bclr="red")))
        # else:
        #     printit(boxed(msgs, center=2, bclr="red"))
        ans = input(printit("Please select:  ", center=True, prnt=False))
        if ans.upper() == "Q" or ans == "":
            return None
        item = self.selections[ans][0]
        cmd = self.selections[ans][1]
        arguments = self.selections[ans][2:]
        # dbug(arguments)
        # dbug(arguments)
        # dbug(*arguments)
        if arguments[0] == '':
            cmd()
        else:
            if "ask" in arguments[0]:
                arguments = input("Please enter arguments: ")
            # dbug(arguments)
            # dbug(*arguments)
            cmd(*arguments)
        return ans


# # ##########################################################
# def do_menu(my_list, *args, box=True, title=" Menu ", footer="", center=True, color="", tst=False, dflt="q", shadow=False, width=0, box_color="", **kvargs):
#     # ######################################################
#     """
#     deprecated: 
#     select from any list
#     USE:
#     selections_l = lst = ["one", "two", "three", "four", "five"]
#     # or
#     selections_d = {"Function One": func1(), "Function Two": func2()}
#     # selection =  do_menu(lst)
#     s = ""
#     while 1:
#         s = do_menu(lst)
#         # dbug(s)
#         if s in ["q", "Q", ""]:
#             break
#         cmd = selections_d[s]
#         # dbug(cmd)
#         out = os.popen(cmd).read()
#         cls()
#         printit(out)
#         askYN()
#     #
#     TODO: add dflt="" option
#       and friendly to list or dict
#       if dict return value
#       if list (current behaviour) return element
#     >>> lst = ['one', 'two', 'three']
#     >>> r = select_from(lst, tst=True, width=20)
#     +--------------+
#     |   1.) one    |
#     |   2.) two    |
#     |   3.) three  |
#     +--------------+
#     >>> print(f"{r}")
#     (3, 'three')
#     
#     """
#     dbug("...is this still used? ...")
#     # dbug(dflt)
#     # dbug(f"my_list: {my_list}",ask=True)
#     my_d = my_list
#     if isinstance(my_list, dict):
#         my_list = list(my_d.keys())
#         # dbug(my_d)
#         # dbug(my_list)
#     if center == "":
#         center = 0
#     if box:
#         msgs = []
#         # width = 80
#         msgs = my_list
#         if len(msgs) == 0:
#             dbug("msg appears empty")
#             return
#         if width > 1:
#             # dbug(my_list)
#             # dbug(width)
#             my_list = [f"{n + 1:>2}) {elem}" for n, elem in enumerate(my_list)]
#             # names_l = columnize.columnize(my_list, displaywidth=width)
#             names_l = gcolumnize(my_list, width=width)
#             # dbug(my_list)
#             # print(lines)
#         else:
#             # names_d = {}
#             names_l = []
#             # cnt = 0
#             for n, msg in enumerate(msgs):
#                 n = n + 1
#                 if isnumber(dflt) and n == int(dflt):
#                     names_l.append(f"[{n}]. {msg}")
#                 else:
#                     names_l.append(f"{n:>3}. {msg}")
#             # names = list(enumerate(my_list, 1))
#             # dbug(msgs)
#             # dbug(names_l)
#         lines = boxed(names_l, title=title, footer=footer, color=color, box_color=box_color, enter=center)
#         if shadow:
#             lines = shadowed(lines, color='grey', style=4)
#         # if center:
#         #     lines = centered(lines)
#         printit(lines, center=center)
#     if tst:  # here only for doctest
#         choice = 1
#     else:
#         prompt = "Please enter your choice: [q=quit] "
#         # pad_left = ""
#         if center:
#             choice = cinput(prompt)
#         else:
#             choice = input(prompt)
#     # choice = str(choice)
#     # dbug(f"choice: [{choice}]")
#     # dbug(f"dflt: [{dflt}]")
#     if choice == "":
#         # dbug(f"choice: [{choice}]")
#         # dbug(f"dflt: [{dflt}]")
#         if dflt != "q" and isinstance(dflt, str):
#             return dflt
#         if dflt == "q":
#             sys.exit()
#         choice = dflt
#         # dbug(choice)
#         # dbug(msgs)
#         selected = msgs[int(choice) - 1]
#         return selected
#     if str(choice).lower() == "q" or str(choice).lower() == "quit":
#         printit("Exiting as requested...", center=center, shadow=shadow)
#         sys.exit()
#         # return "q"
#     # dbug(msgs)
#     # dbug(dflt)
#     if is_number(choice):
#         # dbug(choice)
#         # if isinstance(my_list, dict):
#         if isinstance(my_d, dict):
#             # dbug(msgs)
#             # dbug(choice)
#             # msgs = list(msgs)
#             selected = msgs[int(choice) - 1]  # this and the next are needed
#             selected = my_d[selected]
#         else:
#             selected = msgs[int(choice) - 1]
#         # selected = msgs[int(choice) - 1]
#         # dbug(selected)
#         return selected
#     else:
#         return choice
#     # ### EOB def do_menu(my_list, box=True, title=" Menu ", footer="", center=True, color="", tst=False, dflt="q"): ### #
# 

# # ##################################
# def doline(length=0, msg="nomsg", *args, **kvargs):
#     # ##############################
#     """
#     WIP  this is to replace do_line within boxed() etc
#     TODO: this all needs to be cleaned up or burned down :)
#     line fmt will be:
#         {lchrs}{lfill...}{msg}{rfill...}{rchrs} 
#     possible kvargs:
#         msg=""
#         title=""  # same as msg except it gets box_color
#         footer=""  # same as msg except it gets box_color
#         color=""
#         box_color=""
#         center=False
#         ljust=True
#         rjust=False
#         chr=lfill=rfill=fchr=hchr=""
#         edge=echr=lchrs=rchrs=corner=""
#     """
#     dbug("deprecated: use gline() instead")
#     # dbug(funcname())
#     # dbug(f"length: {length} msg: {repr(msg)}")
#     # dbug(args)
#     # dbug(kvargs)
#     """-== config ==--"""
#     box_color = kvarg_val(['box_color', 'box_color'], kvargs, dflt="")
#     color = kvarg_val(['color'], kvargs, dflt="")
#     title = kvarg_val(["title"], kvargs, dflt="")
#     footer = kvarg_val('footer', kvargs, dflt="")
#     # echr = kvarg_val(["echr", 'edge', 'corner'], kvargs, dflt="")
#     echrs = kvarg_val(["echrs"], kvargs, dflt=[])
#     # chr = kvarg_val(["chr"], kvargs, dflt="")
#     fchr = kvarg_val(["fchr", 'fill_chr', 'chr'], kvargs, dflt=" ")
#     hchr = kvarg_val(["hchr", "hor_chr"], kvargs, dflt=" ")
#     lchr = kvarg_val(["lchr", 'lchrs', 'echr'], kvargs, dflt="")
#     rchr = kvarg_val(["rchr", 'rchrs', 'echr'], kvargs, dflt="")
#     length = kvarg_val(["width", 'length'], kvargs, dflt=length)
#     # dbug(f"lchr: {repr(lchr)} hchr: {repr(hchr)} rchr: {repr(rchr)} fchr: {repr(fchr)}")
#     prnt = bool_val('prnt', args, dflt=False)
#     if isinstance(length, int):
#         length = length
#     else:
#         length = 60
#     # dbug(length)
#     prnt = kvarg_val('prnt', kvargs, dflt=False)
#     msg = kvarg_val('msg', kvargs, dflt=msg)
#     if msg == "nomsg":
#         msg = "" * 40
#     center = kvarg_val('center', kvargs, dflt=True)
#     ljust = kvarg_val('ljust', kvargs, dflt=False)
#     rjust = kvarg_val('rjust', kvargs, dflt=False)
#     """--== Initialize ==--"""
#     if echrs != []:
#         lchr = echrs[0]
#         rchr = echrs[1]
#     color = sub_color(color)
#     box_color = sub_color(box_color)
#     reset = sub_color('reset')
#     # dbug(reset)
#     # dbug(repr(reset))
#     msg_clr = lchr_clr = rchr_clr = lfill_clr = rfill_clr = color
#     lchr_clr = rchr_clr = lfill_clr = rfill_clr = box_color
#     if nclen(title) > 1:
#         # msg = box_color + title
#         msg = title
#     if nclen(footer) > 1:
#         # msg = sub_color(box_color) + footer
#         msg = footer
#     if hchr != "":
#         lfill_chr = rfill_chr = fchr = hchr
#     # dbug(f"lchr: {repr(lchr)} hchr: {repr(hchr)} rchr: {repr(rchr)} fchr: {repr(fchr)} lfill_chr: {lfill_chr} rfill_chr: {rfill_chr}")
#     # dbug(repr(msg))
#     msg_len = nclen(msg)
#     lchr_len = nclen(lchr)
#     rchr_len = nclen(rchr)
#     fill_len = length - lchr_len - rchr_len
#     lfill_len = 1  # we need at least one lfill_chr
#     if center:
#         lfill_len = ((fill_len - msg_len) // 2)
#     if ljust:
#         lfill_len = 0
#     if rjust:
#         lfill_len = fill_len
#     lfill = lfill_chr * lfill_len
#     rfill_len = fill_len - lfill_len - msg_len
#     rfill = rfill_chr * rfill_len
#     # dbug(f"length: {length} fill_len: {fill_len} lfill_len: {lfill_len} msg_len: {msg_len} rfill_len: {rfill_len} lfill_chr: {lfill_chr} rfill_chr: {rfill_chr}")
#     # dbug(rfill_clr)
#     # ruleit()
#     if lfill.isspace():
#         lfill_clr = color
#     if rfill.isspace():
#         rfill_clr = color
#     # dbug(f"lchr: {repr(lchr)} rchr: {repr(rchr)}")
#     if lchr_clr != "" or rchr_clr != "" or msg_clr != "" or lfill_clr != "" or rfill_clr != "":
#         line = f"{reset}{lchr_clr}{lchr}{reset}{lfill_clr}{lfill}{reset}{msg_clr}{msg}{reset}{rfill_clr}{rfill}{reset}{rchr_clr}{rchr}{reset}"
#     else:
#         line = f"{reset}{lchr_clr}{lchr}{reset}{lfill_clr}{lfill}{reset}{msg_clr}{msg}{reset}{rfill_clr}{rfill}{reset}{rchr_clr}{rchr}{reset}"
#     if prnt:
#         printit(line)
#     return line
#     # ### EOB def doline(length, **kvargs): ### #
# 

# ##################################
def do_title_three_line(msg, *args, hchr="=", length=120, color="", box_color="", prnt=True, center=False, **kvargs):
    # ##############################
    """
    This is deprecated and will be removed
    Use: do_title_three_line(msg,length=120)
    This should probably be made into a class and combined with do_title
    # >>> do_title_three_line("mytitle",30)
    ==============================
               mytitle
    ==============================
    ['==============================',
     '           mytitle',
     '==============================']
    """
    dbug("deprecated?")
    # dbug(funcname())
    # dbug(hchr)
    # dbug(kvargs)
    if 'centered' in args:
        center = True
    # dbug(f"{color}color {box_color}box_color")
    # color = sub_color(color)
    # box_color = sub_color(box_color)
    # reset = ""
    # if color != "":
    #     reset = sub_color('reset')
    # dbug(f"{color}color {box_color}box_color")
    lines = []
    # new_lines = []
    # dbug(length)
    # dbug(len(msg))
    # dbug(f"length: {length} fchr-hchr: {hchr} color: {color} box_color: {box_color}")
    top_bottom_line = doline(msg="", length=length, fchr=hchr, tst="This is a test", color=color, box_color=box_color, prnt=False)
    lines.append(top_bottom_line)
    line = doline(length, msg, color=color, box_color=box_color)
    lines.append(line)
    lines.append(top_bottom_line)
    # if center:
    #     columns = get_columns()
    # for line in lines:
    #     new_lines.append(line)
    if prnt:
        printit(lines, center=center)
    return lines
    # ### def do_title_three_line(msg, *args, hchr="=", length=120, color="", box_color="", prnt=True, center=False, **kvargs): ### #


# ##################
def do_title(title="", hchr="=", length=120, color="", one_three_line=1, prnt=False, center=True, edge="=", **kvargs):
    # ##############
    """
    deprecated and will be removed
    20210208-1203 significant refactoring done
    A quick-n-dirty utility to print out a title line using
    title = as the title string
    c = as the repeated character
    length defaults to 120
    color defaults to ""
    do_title(title, hchr, length, color)
    # >>> do_title("mytitle","-",40,color="")
    --------------- mytitle ----------------
    '--------------- mytitle ----------------'
    """
    dbug("deprecated?")
    # dbug(color)
    box_color = color
    if 'box_color' in kvargs:
        box_color = kvargs['box_color']
    # dbug(box_color)
    line = doline(length, msg=title, hchr=hchr, edge=edge, center=center, prnt=prnt, box_color=box_color)
    # dbug(line)
    return line
    # ### EOB def do_title(title="", hchr="=", length=120, color="", one_three_line=1, prnt=True, center=False, hchr="=", edge="=",): ### #



def isnumber(x):
    """
    purpose: determines if x is a number even if it is a percent, or negative, or is 2k or 4b or 10M etc
    input: x: str|float|int
    returns: True|False
    notes: tests... pos, neg, floats, int, scientific, B(illion), T(trillions), G(ig.*) Kb(ytes|its), Mb(ytes)
    Can be used on financial data which often includes M(illions) or B(illions)
    In tables I use this to decide if "x" should get right justified
    >>> nums = [0.00, "0.00", "1.2", "+1.2", "-1.2", "1.2B", " 1.2M ", "1.2Kb ", "1.2Mb", "1.2e-9", "1.2%", 42.25, 1.1116174459457397, "2022-01-01"]
    >>> for num in nums:
    ...     isnumber(num)
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    False
    """
    # dbug(repr(x))
    # dbug(type(x))
    x = escape_ansi(x).strip()
    # dbug(x)
    x = str(x).strip()
    if x.startswith(("-", "+")):
        x = x.lstrip(r"[+-]")
    if x.endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
        x = x.rstrip(r"[BMKGb%]")
    x = x.replace('.', '', 1).replace(",", "").replace("e-", "", 1).replace("%", "", 1)
    # dbug(repr(x))
    r = x.isdigit()
    # dbug(f"Returning: {r}")
    return r


# ###################################################
def get_boxchrs(box_style="single", *args, **kwargs):
    # ###############################################
    """
    purpose: given a box_style (ansi, single, solid, double) will return a set of chars for creating a box
    input: box_style: str
    return:
        [tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br]  as a list in the order shown
    Note: boxed() uses this
    tl = top_left, hc=horizontal_char, ts=top_separator, tr=top_right, vc=vertical_char, 
    ls=left_separator, rs=right_separator, ms=middle_separator
    bl=bottom_left, bs=bottom_sep, br=bottom_right
    """
    box_color = kvarg_val("box_color", kwargs, dflt="") 
    reset = sub_color('reset')
    box_chrs = [9484, 9472, 9516, 9488, 9474, 9500, 9508, 9532, 9492, 9524, 9496]
    if box_style == 'none':
        box_chrs = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    if box_style == 'ascii':
        box_chrs = ["+", "=", "=", "+", "|", "|", "|", "|", "+", "=", "+"]
    if box_style == "single":
        # box_chrs = [tl, hc, ts, tr, vc, le, re, ms, bl, bs, br]
        box_chrs = [9484, 9472, 9516, 9488, 9474, 9500, 9508, 9532, 9492, 9524, 9496]
    if box_style == "solid":
        box_chrs = [9487, 9473, 9523, 9491, 9475, 9507, 9515, 9547, 9495, 9531, 9499]
    if box_style == "double":
        box_chrs = [9556, 9552, 9574, 9559, 9553, 9568, 9571, 9580, 9562, 9577, 9565]
    box_chrs = [chr(n) for n in box_chrs]
    if box_color != "":
        # you should avoid this becuase every char gets wrapped with color codes
        box_chrs = [box_color + c + reset for c in box_chrs]
    # tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    return box_chrs


# #########################################################################
def gtable(lol, *args, **kwargs):
    # #####################################################################
    """
    purpose: returns lines or displays a colorized table from a list_of_lists, df, or dictionary
    input: rows: str|list|dict|list_of_lists|list_of_dicts|dataframe
    options: 
        - color: str, 
        - box_style: 'single', 'double', 'solid', 
        - box_color: str, 
        - header: bool_val,  # header | hdr 
        - colnames: list | str,  'firstrow' | 'firstline' | 'keys'
        - col_colors: list,   # gtable will use this list of colors to set each column, repeats if more cols than colors
        - neg: bool_val, 
        - alt: bool_val, 
        - alt_color: str, 
        - title: str, 
        - footer: str,
        - indexes: bool, 
        - box_style: str,  
        - max_col_len|col_limit|col_len...: int,  default=60
        - human: bool, 
        - rnd: int, 
        - sortby: str, 
        - filterby: dict {'field': 'contains'}
        - select_cols: list    # specify which columns to include - table will be in same order
        - excluded_cols: list  # specify which columns to exclude
        - write_csv: str,
        - skip: bool           # tells gtable to skip lines of the wrong length - be careful w/this
        - cell_pad=' ': str    # you can set the padding char(s)
        - strip: bool          # strip all white space off of ever element in every row
    returns lines: list
    Notes:
        if colnames="firstrow" then the firstrow will be extracted and used for the header
        if colnames="keys" and we are passed a dictionary then the colnames will be the dictionary keys
    I frequenly use this function for financial data analysis or csv files 
    TODO: add head: int and tail: in
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(lol)
    # dbug(type(lol))
    """--== Config ==--"""
    color = kvarg_val('color', kwargs, dflt="")
    lfill_color = kvarg_val("lfill_color", kwargs, dflt=color)
    # rfill_color = kvarg_val("rfill_color", kwargs, dflt=color)
    box_color = kvarg_val(['box_color', 'border_color'], kwargs, dflt="bold white on rgb(40,40,40)")
    header = bool_val(['header', 'headers', 'hdr'], args, kwargs, dflt=False)
    # dbug(header)
    # header_color = kvarg_val(['header_color', 'hdr_color'], kwargs, dflt=box_color)
    header_color = kvarg_val(['header_color', 'hdr_color'], kwargs, dflt="white! on grey40")
    colnames = kvarg_val(["col_names", "colnames"], kwargs, dflt=[])  
    # NOTE: if colnames (str) in ("firstrow", "first_row", "firstline", "first_line" then use firstline as colnames
    # NOTE: if colnames (str) in ("keys") then use dictionary keys as colnames
    selected_cols = kvarg_val(['selected_cols', 'selectedcols', 'slctd_cols', 'slctdcols', 'select', 'selected'], kwargs, dflt=[])
    # dbug(selected_cols)
    excluded_cols = kvarg_val(['excluded_cols', 'excludedcols', 'xcld_cols', 'excdcols', 'exclude', 'excluded'], kwargs, dflt=[])
    # dbug(excluded_cols)
    centered = bool_val(['center', 'centered'], args, kwargs, dflt=False)
    shadowed = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print'], args, kwargs, dflt=False)
    rjust_cols = kvarg_val(['rjust_cols'], kwargs, dflt=[])
    col_colors = kvarg_val(['col_colors', 'colors', "col_color"], kwargs, dflt=["white!", "cyan", "red", "green", "blue", "bold red", " bold green", "bold blue"])
    # col_colors = kvarg_val(['col_colors', "col_color"], kwargs, dflt=[])
    title = kvarg_val('title', kwargs, dflt="")
    # dbug(title)
    footer = kvarg_val('footer', kwargs, dflt="")
    indexes = bool_val(['indexes', 'index', 'idx', 'id', 'indx'], args, kwargs, dflt=False)
    # dbug(indexes)
    # dbug(indexes)
    box_style = kvarg_val(['style', 'box_style'], kwargs, dflt='single')
    alt_color = kvarg_val(['alt_color', 'alt_clr', "altclr"], kwargs, dflt="on rgb(35,35,50)")
    # alt_color = kvarg_val(['alt_color', 'alt_clr', "altclr"], kwargs, dflt="on rgb(55,25,55)")
    if len(alt_color) > 2 and not alt_color.strip().startswith("on"):
        alt_color = "on " + alt_color
    alt = bool_val('alt', args, kwargs, dflt=False)
    max_col_len = kvarg_val(['max_col', 'max_col_len', 'width', 'col_limit', 'max_limit', 'max_len', 'col_len'], kwargs, dflt=60)
    wrap_b = bool_val(["wrap", "wrapit"], args, kwargs, dflt=False)
    neg = bool_val('neg', args, kwargs, dflt=False)
    rnd = kvarg_val(['rnd', 'round'], kwargs, dflt="")
    human = bool_val(['h', 'human', "H"], args, kwargs, dflt=False)
    sortby = kvarg_val(["sortby", "sort_by", "sorton", "sort_on", "sort", 'sorted_by', 'sortedby'], kwargs, dflt='')
    sortby_n = kvarg_val(["sortbyn", "sort_byn", "sortby_n", "sortby_n", "sort_n"], kwargs, dflt='')
    filterby_d = kvarg_val(['filterby', 'filter_by'], kwargs, dflt={})
    # dbug(filterby_d)
    # dbug(f"sortby: {sortby} sortby_n: {sortby_n}")
    write_csv = kvarg_val(["write_csv", 'csv_file'], kwargs, dflt='')  # write a csv file with gtable data
    write_out = kvarg_val(["write_out", 'out_file'], kwargs, dflt='')  # write table out to file
    end_hdr = bool_val(['end_hdr', "endhdr", 'hdr_last'], args, kwargs, dflt=False)
    cell_pad = kvarg_val(['cell_pad', 'cellpad', 'pad'], kwargs, dflt=' ')
    strip_b = bool_val(['strip'], args, kwargs, dflt=False)
    # dbug(f"neg: {neg} rnd: {rnd} human: {human} title: {title}")
    """--== Init ==--"""
    # dbug(f"header: {header} colnames: {colnames}")
    if not isinstance(filterby_d, dict):
        dbug("filterby must be a dictionary")
        return None
    if len(colnames) > 1 and header:
        header = True
    RESET = sub_color('reset')
    COLOR = sub_color(color)
    if box_color == "":
        box_color = 'reset'
    BOX_COLOR = sub_color(box_color)
    # dbug(f"header_color: {header_color} header: {header} box_color: {box_color}")
    HEADER_COLOR = sub_color(header_color)
    # dbug(col_colors)
    # dbug(f"color: {repr(color)} box_color: {repr(box_color)} header_color: {repr(header_color)}")
    box_chrs = get_boxchrs(box_style)
    tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    lines = []
    max_elem_len = []  # init... will hold max len for each col
    # cell_pad = " "  # add before and after @ elem - this has to come after sub_color(color)
    max_width = 0
    skip = bool_val(['skip'], args, kwargs, dflt=False)  # skip non-compliant lines/rows?
    """--== Convert to lol ==--"""
    # dbug(header)
    # dbug(lol)
    # dbug(type(lol))
    import pandas as pd
    import numpy as np
    if len(lol) == 0:
        dbug(f"lol: {lol} appears to be empty.... returning....", 'centered')
        return
    if isinstance(lol, dict):
        # dbug(f"type(lol): {type(lol)} len(lol): {len(lol)} : {header} colnames: {colnames} len(colnames): {len(colnames)} header: {header}")
        # dbug(type(lol))
        if isinstance(colnames, str) and colnames in ("keys"):
            colnames = list(lol.keys())
        my_vals = list(lol.values())
        # dbug(my_vals)
        # if isinstance(my_vals[0], str) and header:
        if not isinstance(my_vals[0], dict) and not isinstance(my_vals[0], list):  # and header:
            # we tested val[0] to makes sure this is not a dictionary (dol) of lists or of dictionaries (dod) 
            # so this must be a simple dictionary.
            if len(colnames) == len(lol):  # and header:  # then make two rows  
                # looks like user wants to add a row for column names
                # lol = [colnames, my_vals]
                lol = [my_vals]  #  colnames will get added as row one later
                # dbug(lol)
            else:
                # dictionary and we probably want to list the keys in column 1 and the values in col 2
                # dbug(f"dictionary before it is turned in an lol... lol: {lol}")
                my_lol = []
                # dbug(colnames)
                if colnames == [] and header:
                    my_lol = [["Key", "Value"]]
                n = 0
                for k, v in lol.items():
                    if n == 0 and isinstance(colnames, str) and colnames in ("firstrow", "firstline", "first_row", "first_line"):
                        colnames = [k, v]
                    else:
                        # dbug(f"k: {k} v: {v}")
                        my_lol.append([k, v])
                    n += 1
                # lol = [list(lol.keys()), list(lol.values())]
                lol = my_lol
                # dbug(lol)
        # else:
        if isinstance(lol, dict):
            # if we still have a dictionary (ie it did not get changed to an lol above)
            # dbug(header)
            mylol = []
            for k, v in lol.items():
                mylol.append([k, v])
            # lol = list(lol.items())
            lol = mylol
    # dbug(lol)
    if isinstance(lol, list):
        # if isinstance(lol[0], str):
        if not isinstance(lol[0], list):
            # perhaps this is a simple list (one row)
            lol = [[str(elem) for elem in lol]]
            # dbug(lol)
        if isinstance(lol[0], list):
            # this is already a list_of_lists (lol)
            # dbug(colnames)
            if colnames != [] and isinstance(colnames, list):
                lol.insert(0, colnames)
            if isinstance(colnames, str) and colnames in ("firstrow", "firstline", "first_row", "first_line"):
                # dbug(lol)
                colnames = lol[1]
                # dbug(colnames)
                lol = lol[:1]
                header = True
            # dbug(lol)
        if indexes:
            new_lol = []
            for n, row in enumerate(lol):
                row.insert(0, str(n))
                new_lol.append(row)
            lol = new_lol
    # dbug(lol)
    if isinstance(lol, pd.DataFrame):
        df = lol
        # dbug(df)
        # dbug(colnames)
        # if isinstance(colnames, str) and colnames in ("firstrow", "firstline", "first_row", "first_line"):
            # # dbug(colnames)
            # df, df.columns = df[1:], df.iloc[0]  # uses the first row as colnames and uses the rest of the rows for the df
            # colnames = list(df.columns)
            # header = True
            # # dbug(colnames)
        if isinstance(df.index, pd.DatetimeIndex):
            # dbug("Datetime Index")
            lol = lol.reset_index()
        if indexes:
            # dbug(indexes)
            # columns = [df.index.name] + [str(i) for i in df.columns]
            # dbug(df)
            lol = df.reset_index().values.tolist()
            # dbug(lol[0])
            # dbug(lol[1])
            # dbug('ask')
            # rows = [[i for i in row] for row in df.itertuples()]
            # dbug(rows)
            # # dbug(rows)
            # lol = rows
        else:
            lol = df.values.tolist()
        # dbug(colnames)
        colnames = list(df.columns.values)
        # dbug(lol)
        # dbug(colnames)
        if header:
            if colnames[0] not in ("id", "Id", "ID", "Index"):
                # dbug(indexes)
                if indexes:
                    colnames.insert(0, "id")
                # else:
                    # dbug(colnames)
            lol.insert(0, colnames)
    # dbug(lol[0])
    # dbug(lol[1])
    # dbug(lol)
    if isinstance(lol[0], dict):
        if colnames == [] and header:
            colnames = list(lol.keys())
        colnames = [*lol[0]]
        # dbug(colnames)
        rows_l = []
        for row in lol:
            row_l = []
            for k, v in row.items():
                row_l.append(v)
            rows_l.append(row_l)
        lol = rows_l
        if header:
            lol.insert(0, colnames)
    # dbug(lol)
    if isinstance(lol[0], str) or isinstance(lol[0], int) or isinstance(lol[0], float):
        lol = [(lol)]  # lol maybe a simple list so turn it into an lol with one row
    if isinstance(lol, np.ndarray):
        lol = lol.tolist()
    # now lol[0] will be the header names (colnames)
    max_row_lines = []
    for row in lol:
        max_row_lines.append(1)  # initializes a max_row_lines number for each row default=1
    """--== get rid of blank rows and condition any elems in each row ==--"""
    new_lol = []
    for row in lol:
        if len(row) == 0:
            continue
        else:
            new_lol.append(row)
        lol = new_lol
    """--== Test row lengths ... do columns = num or elems throughout ==--"""
    # dbug(lol[0])
    # dbug(lol[1])
    # dbug('ask')
    if isinstance(lol[0], list):
        row_len = len(lol[0])  # this will be the number of columns
        # dbug(row_len)
    else:
        row_len = len(lol)
        dbug(row_len)
    err_cnt = 0
    """--== Test row lengths ... do cols = num or elems throughout ==--"""
    # let's test lol rows to make sure number of col matches
    for row in lol:
        if not isinstance(row, list):
            dbug("Why is this block here?")
            dbug(lol)
            dbug(row)
        if len(row) != row_len:
            dbug(f"Returning as it looks like row has the wrong number of items. row_len: {row_len} len(row): {len(row)}")
            dbug(f"lol[0]: {lol[0]}")
            dbug(f"row: {row}")
            # if len(lol[0]) > len(row):
                # for n, elem in enumerate(lol[0]):
                    # dbug(f"lol[0][{n}]: {lol[0][n]} row[{n}]: {row[n]}")
            # else:
                # for n, elem in enumerate(row):
                    # dbug(f"lol[0][{n}]: {lol[0][n]} row[{n}]: {row[n]}")
            if skip:
                err_cnt += 1
                dbug(f"Error cnt: {err_cnt}")
                continue
            else:
                return
    """--== limit length of each elem to max_col_len ==--"""
    # dbug(lol[0])
    # dbug(lol[1])
    # dbug('ask')
    new_lol = []
    # dbug(f"wrap_b: {wrap_b} max_col_len: {max_col_len}")
    for row in lol:
        # truncate elems in each row if needed
        new_row = []
        for elem in row:
            if strip_b:
                elem = str(elem).strip()
                # dbug(f"strip elem: {elem}")
            if wrap_b:
                if isinstance(elem, str):
                    if nclen(str(elem)) > max_col_len - 5:  # for padding
                        # dbug(f"wrap_b: {wrap_b} max_col_len: {max_col_len} elem: {elem} nclen(elem): {nclen(elem)}")
                        elem = wrapit(elem, length=int(max_col_len - 5))
                        # dbug(f"elem: {elem}")
            if isinstance(elem, list):
                # this is a multi_line elem
                # dbug(f"This must be a multiline elem: {elem} so build a new_elem")
                new_elem = []
                for item in elem:
                    # should test len(item) here? and wrapit if  needed
                    item = str(item)
                    # dbug(item)
                    item = item[:max_col_len]  # trim it if it is too long
                    # dbug(item)
                    new_elem.append(item)
                elem = new_elem
                # dbug(f"elem): [{elem}] new_elem: [{new_elem}]")
            else:
                # elem is not a list type
                if nclen(elem) > max_col_len:
                    if not isnumber(elem) and not isinstance(elem, dict):
                        # dbug(elem)
                        elem = elem[:max_col_len]
            # dbug(elem)
            new_row.append(elem)
        # dbug(new_row)
        new_lol.append(new_row)
    # dbug(f"wrap_b: {wrap_b} max_col_len: {max_col_len}")
    """--== SEP_LINE ==--"""
    lol = new_lol
    """--== Local Functions ==--"""
    def bld_row_line(row):
        # dbug(f"Starting bld_row_line(row: {row})")
        lfill_color = color
        for col_num, elem in enumerate(row):
            # dbug(f"col_num: {col_num} elem: {elem} row: {row}")
            if col_num == 0:
                msg = ""
            mycolor = color  # the default passed as a Config above
            if col_colors != []:
                # now change mycolor to appropriate col_colors
                color_num = col_num % len(col_colors)
                col_color = col_colors[color_num]
                mycolor = col_color
                myCOLOR = sub_color(col_color)
                # dbug(f"mycolor: {mycolor} ... myCOLOR [test]: {myCOLOR}[test]{RESET}")
            # dbug(f"mycolor [test]: {mycolor}[test]{RESET}")
            if alt:
                # now add in alt color
                line_num = row_num
                # dbug(line_num)
                if header:
                    line_num = row_num + 1
                if line_num % 2:
                    # dbug(repr(mycolor))
                    # dbug(f"mycolor [test]: {mycolor}[test]{RESET}")
                    # dbug(mycolor)
                    # dbug(alt_color)
                    mycolor = mycolor + " " + alt_color
                    # dbug(mycolor)
                    myCOLOR = sub_color(mycolor)
                    # clr_tst(myCOLOR, mycolor)
                    # dbug(repr(myCOLOR), 'ask')
            # dbug(MYCOLOR)
            fill_len = max_elem_len[col_num] - nclen(elem)
            fill = " " * fill_len 
            myfill = fill
            mypad = cell_pad
            elem = str(elem)
            if col_num in rjust_cols or isnumber(elem):
                # right justify this elem
                justified_elem = myfill + str(elem)
            else:
                # left justify this elem
                justified_elem = str(elem) + myfill
            if col_num + 1 == len(row):
                # last column
                add_this = mypad + justified_elem + mypad
                msg += myCOLOR + add_this
                # marker_line += hc * nclen(add_this)
                rfill_color = mycolor
            else:
                # not the last column
                add_this = mypad + justified_elem + mypad
                msg += myCOLOR + add_this + BOX_COLOR + vc + RESET
                if col_num == 0:
                    lfill_color = mycolor
            if col_num == len(row) - 1:
                # this is the last col_num (column)
                rfill_color = mycolor
                # dbug(f"mycolor: {mycolor} lfill_color: {lfill_color} rfill_color: {rfill_color}")
                line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=mycolor, lfill_color=lfill_color, rfill_color=rfill_color)
                # dbug("Adding line: [{line}] to lines:")
                lines.append(line)
        return msg
        # ### EOB def bld_row_line(row): ### #
    """--== Process ==--"""
    # dbug(lol[0])
    # dbug(lol[1])
    # dbug('ask')
    # dbug(lol)
    # dbug(len(lol))
    """--== sortby ==--"""
    # dbug(sortby)
    if sortby != '' or sortby_n != "":
        if sortby_n != "":
            sortby = sortby_n
        # dbug(lol)
        hdr = lol[0]
        # dbug(hdr)
        rows = lol[1:]
        # dbug(f"Before sort of rows: {rows}")
        if isinstance(sortby, int):
            sortby_i = int(sortby) 
        if isinstance(sortby, str):
            sortby_i = hdr.index(sortby)
            # dbug(f"sortby: {sortby} sortby_i: {sortby_i}")
        else:
            sortby_i = int(sortby)
        # dbug(sortby_i)
        if sortby_n != "":
            # dbug(rows)
            rows = sorted(rows, key=lambda x: float(x[sortby_i]))
        else:
            rows = sorted(rows, key=lambda x: x[sortby_i])
        # dbug(f"After sort of rows: {rows}")
        lol = [hdr] + rows
        # dbug(lol, 'ask')
    """--== filterby ==--"""
    # dbug(len(filterby_d))
    if len(filterby_d) == 1:
        # dbug(filterby_d)
        filterby_col = list(filterby_d.keys())[0]
        filterby_str = list(filterby_d.values())[0]
        hdr = lol[0]
        filterby_i = hdr.index(filterby_col)  # filterby col index number
        # dbug(filterby_i)
        new_lol = []
        for row in lol:
            # dbug(row[filterby_i])
            if filterby_str in str(row[filterby_i]):
                new_lol.append(row)
        new_lol.insert(0, hdr)
        # dbug(new_lol)
        lol = new_lol
    """--== selected columns routine ==--"""
    # dbug(lol)
    if len(selected_cols) > 1:
        # dbug(selected_cols)
        new_lol = []
        hdr = lol[0]
        hdr_indxs_l = []
        if indexes:
            hdr_indxs_l = [0]
            lol[0][0] = "id"
        for col in selected_cols:
            # uses the order given in selected_cols
            if col in hdr:
                hdr_i = hdr.index(col)
                hdr_indxs_l.append(hdr_i)
        # dbug(hdr_indxs_l)
        for row in lol:
            new_row = []
            new_row = [row[x] for x in hdr_indxs_l]
            new_lol.append(new_row)
        # dbug(new_lol, 'ask')
        lol = new_lol        
    num_cols = len(lol[0])
    # dbug(lol[0])
    # dbug(lol[1])
    # dbug('ask')
    """--== excluded_cols ==--"""
    # dbug(lol)
    if len(excluded_cols) > 0:
        # dbug(excluded_cols)
        new_lol = []
        hdr = lol[0]
        hdr_indxs_l = []
        for col in hdr:
            if col not in excluded_cols:
                hdr_i = hdr.index(col)
                hdr_indxs_l.append(hdr_i)
        # dbug(hdr_indxs_l)
        for row in lol:
            new_row = []
            new_row = [row[x] for x in hdr_indxs_l]
            new_lol.append(new_row)
        # dbug(new_lol, 'ask')
        lol = new_lol        
    num_cols = len(lol[0])
    # dbug(lol)
    # dbug(num_cols)
    """--== condition any numbers ==--"""
    # Condition any numbers before measuring the lenght (see next block)
    if neg or rnd != "" or human:
        new_lol = []
        for row in lol:
            new_row = []
            for elem in row:
                if isnumber(elem):
                    elem = cond_num(elem, rnd=rnd, human=human, neg=neg)
                new_row.append(elem)
            new_lol.append(new_row) 
        lol = new_lol
    """--== get max_elem_len[col] length for each col ==--"""
    # Now get max length for each column - in a series of steps using lol[0]
    for idx in range(num_cols):
        # initializes a max_elem_len for each col using row one (lol[0])
        hdr_elem = str(lol[0][idx])
        hdr_elem_len = nclen(hdr_elem)
        max_elem_len.append(hdr_elem_len)
    # dbug(max_elem_len)
    new_lol = []
    for row_num, row in enumerate(lol):
        new_row = []
        # for each row in lol... get length
        # dbug(f"max_row_lines[{row_num}]: max_row_lines[row_num]") 
        # calc max_elem_len for each col
        if row == []:
            # skip a blank or empty row
            continue
        for col_num, elem in enumerate(row):
            # for each elem in row
            # dbug(elem)
            my_elem = elem
            if not isinstance(elem, list):
                # if str(elem) has line breaks, make it a list
                if "\n" in str(my_elem):
                    my_elem = str(elem).split("\n")
            """--== is this a muti_line row? ==--"""
            if isinstance(my_elem, list):
                # for measuring length purposes only
                # dbug(f"trying max for my_elem: [{my_elem}]")
                if len(my_elem) > 1:
                    max_row_lines[row_num - 1] = len(elem)  # sets the max_row_lines number to len of my_elem list - makes it multi_line
                    my_elem = max(my_elem, key=len)  # this makes my_elem the longest str in the list
                    # dbug(f"nclen(my_elem): {nclen(my_elem)}")
                    # dbug(my_elem)
                    # dbug("done trying max", 'ask')
                    if nclen(my_elem) > max_elem_len[col_num]:
                        max_elem_len[col_num] = nclen(my_elem) + 2  # adding some padding
                        # dbug(f"elem: {my_elem} len(my_elem): {len(my_elem)} max_elem_len[{col_num}]: {max_elem_len[col_num]}")
            # now set max_elem_len[col_num] for each elem
            if nclen(str(my_elem)) > max_elem_len[col_num]:
                max_elem_len[col_num] = nclen(str(my_elem))  # set max col width
                # dbug(f"elem: {my_elem} len(my_elem): {len(str(my_elem))} max_elem_len[{col_num}]: {max_elem_len[col_num]}")
            new_row.append(elem)    
        # dbug(new_row)
        new_lol.append(new_row)
    # dbug(max_elem_len)
    # dbug(max_row_lines)
    lol = new_lol
    # dbug(lol)
    if nclen(title) + 4 > max_width:
        max_width = nclen(title) + 4
    if nclen(footer) + 4 > max_width:
        max_width = nclen(footer) + 4
    """--== Build Table ==--"""
    for row_num, row in enumerate(lol):
        # line = vc
        msg = ""
        """--== is this a multi_line row, if so then make it multi_line ==--"""
        if max_row_lines[row_num - 1] > 1:
            # dbug(f"OK this is a multi_line row... row_num: {row_num} row: {row}") 
            # now add needed rows
            elem_line_num = 0  # init
            # dbug(f"we just set elem_line_num: {elem_line_num}  ... init :row: {row} ")
            for add_row_num in range(max_row_lines[row_num - 1]):
                # add new_line rows
                new_row = []  # init
                # dbug(f"len(row): {len(row)} elem_line_num: {elem_line_num} row: {row} add_row_num: {add_row_num}")
                # add each needed row
                for elem_num, elem in enumerate(row):
                    # dbug(elem)
                    # for each elem in row - is it a list type ?
                    if isinstance(elem, list):
                        # dbug(f"And then here elem: {elem} as we iterate over elems in row: {row}")
                        # start adding multi_line rows...  this is a multi_line elem (it is of list type)
                        # dbug(f"row: {row} elem: {elem} elem_line_num: {elem_line_num} elem_num: {elem_num}")
                        # this is a multi_line elem so use the first item in that elem and increment elem_line_num
                        # elem_num_lines[elem_num] = len(elem)
                        # dbug(f"elem_num: {elem_num} elem_line_num was == {elem_line_num - 1} new elem_line_num: {elem_line_num} so added new_elem: [{new_elem}] elem: {elem} elem_line_num: {elem_line_num}")
                        new_elem = elem[add_row_num]
                        # dbug(f"elem_num: {elem_num} elem_line_num was == {elem_line_num - 1} new elem_line_num: {elem_line_num} so added new_elem: [{new_elem}] elem: {elem} elem_line_num: {elem_line_num}")
                    else:
                        # elem is not multi_line (ie not a list)
                        if add_row_num > 0:
                            # elem is not type list  and we are past the first row so just add the blank elem 
                            new_elem = " "
                        else:
                            new_elem = elem[:max_elem_len[elem_num]]
                            elem_line_num = 0
                    # dbug(f"Adding new_elem: {new_elem} to new_row: {new_row} max_elem_len[{elem_num}]: {max_elem_len[elem_num]}")
                    new_row.append(new_elem)
                # dbug("end of looping through elems in row")
                # this is one of the multi_line rows to add - there will be max_row_lines added
                # dbug(f"Ending loop for adding new_row: {new_row}")
                elem_line_num += 1
                # dbug(new_row)
                last_msg = bld_row_line(new_row) 
            # dbug(f"ending loop for adding multi_line rows last_msg: {last_msg}")
        if row_num == 0 and header:
            # dbug(f"Working on header row: {row} header: {header}")
            hdr_line = vc
            for col_num, elem in enumerate(row):
                # dbug(ln)
                if isinstance(elem, list):
                    msg_len = nclen(max(elem, key=len))  # uses the longes str in a list
                else:
                    msg_len = nclen(elem)
                fill_len = max_elem_len[col_num] - msg_len
                # fill = " " * fill_len
                """--== SEP_LINE ==--"""
                if header:
                    # First row and header is true
                    # dbug(header_color)
                    COLOR = HEADER_COLOR
                    rfill = lfill = " " * ((max_elem_len[col_num] - nclen(elem)) // 2)
                    elem = str(elem)
                    justified_elem = rfill + elem + lfill
                    if nclen(rfill) + nclen(lfill) < fill_len:
                        diff = (fill_len) - (nclen(lfill) + nclen(rfill))
                        diff_fill = " " * diff
                        justified_elem += diff_fill
                    if col_num == len(row) - 1:
                        # column, not the last
                        msg += COLOR + cell_pad + justified_elem + cell_pad
                    else:
                        # last column
                        msg += COLOR + cell_pad + justified_elem + cell_pad + BOX_COLOR + vc 
            hdr_line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=COLOR, lfill_color=lfill_color)
            lines.append(hdr_line)
            # dbug(f"row: {row} header: {header} hdr_line: {hdr_line}")
            last_msg = msg
        else:
            # not the first row and not header
            msg = ""
            # dbug(f"row: {row} row_num: {row_num} max_row_lines: {max_row_lines}")
            """--== is this a multi_line row, if so then make it multi_line ==--"""
            if max_row_lines[row_num - 1] == 1:
                # dbug(f"row_num: {row_num} max_row_lines: {max_row_lines}")
                for col_num, elem in enumerate(row):
                    if col_num == 0:
                        msg = ""
                    mycolor = color  # the default passed as a Config above
                    if col_colors != []:
                        # now change mycolor to appropriate col_colors
                        color_num = col_num % len(col_colors)
                        col_color = col_colors[color_num]
                        mycolor = col_color
                        myCOLOR = sub_color(col_color)
                        # dbug(f"mycolor: {mycolor} ... myCOLOR [test]: {myCOLOR}[test]{RESET}")
                    else:
                        mycolor = ""
                        myCOLOR = sub_color("")
                    # dbug(f"mycolor [test]: {mycolor}[test]{RESET}")
                    if alt:
                        # now add in alt color
                        line_num = row_num
                        if header:
                            line_num = row_num + 1
                        if line_num % 2:
                            mycolor = mycolor + " " + alt_color
                            myCOLOR = sub_color(mycolor)
                            # dbug(repr(myCOLOR), 'ask')
                    # dbug("mycolor: {mycolor} MYCOLOR: {MYCOLOR} {repr(mycolor)}")
                    fill_len = max_elem_len[col_num] - nclen(elem)
                    fill = " " * fill_len 
                    myfill = fill
                    mypad = cell_pad
                    elem = str(elem)
                    # dbug(f"we are here msg: {msg}")
                    if col_num in rjust_cols or isnumber(elem):
                        # right justify this elem
                        justified_elem = myfill + str(elem)
                    else:
                        # left justify this elem
                        justified_elem = str(elem) + myfill
                    if col_num + 1 == len(row):
                        # last column
                        add_this = mypad + justified_elem + mypad
                        msg += myCOLOR + add_this
                        # marker_line += hc * nclen(add_this)
                        rfill_color = mycolor
                    else:
                        # not the last column
                        add_this = mypad + justified_elem + mypad
                        # dbug(myCOLOR + add_this + RESET)
                        msg += myCOLOR + add_this + BOX_COLOR + vc + RESET
                        if col_num == 0:
                            lfill_color = mycolor
                    if col_num == len(row) - 1:
                        # this is the last col_num (column)
                        rfill_color = mycolor
                        # dbug(f"mycolor: {mycolor} lfill_color: {lfill_color} rfill_color: {rfill_color}")
                        if len(str(msg)) > 2:
                            last_msg = msg
                        line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=mycolor, lfill_color=lfill_color, rfill_color=rfill_color)
                        lines.append(line)
            # dbug(f"No ?last_msg: {last_msg}")
    """--== marker line ==--"""
    # printit(lines)
    # dbug('ask')
    if end_hdr and header:
        lines.append(hdr_line)
    # add a sep_line after this header line
    marker_line = ""
    # dbug(lol)
    last_msg = escape_ansi(last_msg)
    for ch in last_msg:
        # we are changing every ch to a hc except vc will get a "@" marker. result eg: -----@---@-------@------
        if ch == vc:
            c = "@"  # This is just an arbitrary marker for proper positioning
        else:
            c = hc
        marker_line += c
    # marker_line = gline(max_width, lc=ls, msg=marker_line, hc=hc, rc=rs, box_color=box_color, color=box_color)  # color=box_color because the msg is part of the box
    # dbug(marker_line)
    marker_line = escape_ansi(gline(max_width, msg=marker_line, fc=hc, lc=tl, rc=tr))
    marker_line = marker_line[1:-1]  # strip off beginning and ending vc
    """--== sep_line ==--"""
    sep_line = marker_line.replace("@", ms)
    sep_line = gline(max_width, lc=ls, msg=sep_line, hc=hc, rc=rs, box_color=box_color, color=box_color)  # color=box_color because the msg is part of the box
    # dbug(sep_line)
    # dbug(f"appending sep_line: {sep_line}")
    if header:
        # insert the sep_line right under the hdr_line
        lines.insert(1, sep_line)
    if end_hdr:
        lines.insert(-1, sep_line)
    """--== marker_line ==--"""
    # dbug(marker_line)
    """--== top_line ==--"""
    # dbug(header)
    top_line = ""
    msg = title
    msg_len = nclen(msg)
    # dbug(marker_line)
    my_marker_line = marker_line.replace("@", ts)
    # dbug(f"top sep = {ts}")
    my_marker_line = tl + my_marker_line + tr
    # dbug(my_marker_line)
    if msg_len > 0:
        my_marker_line_len = nclen(my_marker_line)
        non_title_len = my_marker_line_len - msg_len
        lside_len = rside_len = non_title_len // 2
        lside = my_marker_line[:lside_len]
        diff = my_marker_line_len - (lside_len + msg_len + rside_len)
        rside_len = rside_len + diff
        rside = my_marker_line[(my_marker_line_len - rside_len):]
        top_line = BOX_COLOR + lside + COLOR + msg + BOX_COLOR + rside + RESET
    else:
        top_line = BOX_COLOR + my_marker_line + RESET
    # dbug(top_line)
    # lines[0] = top_line
    lines.insert(0, top_line)
    """--== bot_line ==--"""
    bot_line = ""
    msg = footer
    msg_len = nclen(msg)
    my_marker_line = marker_line.replace("@", bs)
    my_marker_line = bl + my_marker_line + br
    my_marker_line_len = nclen(my_marker_line)
    # dbug(f"sep_line: {sep_line} my_marker_line: {my_marker_line} my_marker_line len: {my_marker_line_len}")
    if msg_len > 0:
        non_title_len = my_marker_line_len - msg_len
        side_len = non_title_len // 2
        lside = my_marker_line[:side_len]
        diff = my_marker_line_len - ((side_len * 2) + msg_len)
        side_len = side_len + diff
        rside = my_marker_line[my_marker_line_len-side_len:]
        bot_line = BOX_COLOR + lside + COLOR + msg + BOX_COLOR + rside + RESET
        # dbug(bot_line)
    else:
        bot_line = BOX_COLOR + my_marker_line + RESET
    # dbug(f"appending line: {bot_line}")
    lines.append(bot_line)
    new_lines = lines
    # printit(new_lines)
    # dbug('ask')
    if prnt:
        printit(lines, centered=centered, shadowed=shadowed)
    if write_csv != "":
        CSV_FILE = write_csv
        # dbug(f"Writing csv file: {CSV_FILE}")
        with open(CSV_FILE, 'w', newline='\n') as f:
            # if we used import csv then use next 2 lines
            # writer = csv.writer(f)
            # writer.writerows(rows)
            for row in lol:
                f.write(",".join(row))
                # for elem in row:
                #     f.write(str(elem) + ',')
                f.write("\n")
            f.write(f'\n# This file was written out: {dtime} \n')
        # printit(f"Done writing csv file: {CSV_FILE}")
    if len(new_lines) == 0:
        return None
    if write_out != "":
        with open(write_out, 'w', newline='\n') as f:
            for line in new_lines:
                f.write(line + "\n")
    return new_lines
    # ### EOB def do_watch_syms(filename=WATCH_FILE, outfile=WATCH_OUT_FILE): ### #



def split_codes(val, *args, **kwargs):
    """
    purpose to split out ansi codes and return them
    - used in color_neg()
    input: elem: str (that contains ansi codes for color)
    options: TODO include elem dflt=False
    returns: codes: list (unless elem=True, then it is a dictionary with preffix, elem, and suffix as key/value pairs)
    """
    asdict_b = bool_val(['elem', 'with_elem', 'asdict'], args, kwargs, dflt=False)
    # dbug(repr(val))
    pat = "(?P<prefix>\x1b[\[\d\;]+m)(?P<elem>.*)(?P<suffix>\x1b.*m)"
    r = re.match(pat, val)
    if r:
      my_d = r.groupdict()
    else:
      my_d = {'prefix': "", 'elem': val, 'suffix': ""}
    if asdict_b:
        return my_d
    else:
        return [my_d['prefix'], my_d['suffix']]


# #################
def color_neg(elem, *args, **kwargs):
    # #############
    """
    purpose: this conditions (colorizes and adds commas) elems if they are numbers 
    input: elem 
    options: "neg_color=red on black!": str, pos_color="green! on black!": str, rnd=0: int
    -   color: bool        # will color the number ... default red for negative and green for positive
    -   neg_color: str     # you can change the color for negative numbers
    -   pos_color: str     # you can change the color for positive numbers
    -   human: bool        # adds commas, reduces large numbers to 10000000 to 1M etc
    -   nan: str           # allows you to change "nan" or "NaN" to any string you want. default=""
    returns: elem (conditioned; colored)
    use:
    -   for n, row in enumerate(lol):
    -       ...
    -       if neg:
    -           row = [color_neg(elem) for elem in row]
    -       # table.add_row(*row)
    -       table_lol.append(*row)
    NOTE: this may return an elem with a different length 
    """
    # dbug(funcname())
    # dbug(repr(elem))
    """--== Config ==--"""
    clr_b = bool_val(["neg", "color", "clr", "colorize", "pos"], args, kwargs, dflt=True)  # "neg" and 'pos'are remanants of past code
    rnd = kvarg_val(['round', 'rnd'], kwargs, dflt=0)
    neg_color = kvarg_val(['neg_color'], kwargs, dflt='red! on rgb(0,0,0)')
    pos_color = kvarg_val(['pos_color'], kwargs, dflt='green! on rgb(0,0,0)')
    human = bool_val(["human", "H", "h"], args, kwargs, dflt=False)
    nan = kvarg_val(["nan", "NaN"], kwargs, dflt="")
    # dbug(human)
    rset = bool_val(['rset', 'reset'], args, kwargs, dflt=False)
    # dbug(rnd)
    # if "%" in elem:
    #     elem = elem
    """--== Init ==--"""
    RESET = sub_color('reset')
    if clr_b:
        elem = escape_ansi(elem)
        # dbug(f"pos_color: {pos_color} neg_color: {neg_color}")
        NEG_COLOR = sub_color(neg_color)
        POS_COLOR = sub_color(pos_color)
    else:
        elem = str(elem)
        NEG_COLOR = ""
        POS_COLOR = ""
    # dbug(f"rnd: {rnd} neg_color: {neg_color} NEG_GOLOR: {NEG_COLOR}{repr(NEG_COLOR)}pos_color: {pos_color} POS_COLOR: {POS_COLOR}{repr(POS_COLOR)} elem: {elem}")
    # NOTE! IMPORTANT! If you want a number to be treated like a string, ie ignored here, precede it with an underscore (_) or surround it with [] or someother means
    #   or set neg to False in rtable
    # pos_sym = False
    # dbug(elem)
    # dbug(f"neg: {neg} rnd: {rnd} human: {human} elem: {elem}")
    # if not neg:
    #     dbug(elem)
    #     return elem
    if nan != "":
        # dbug(f"elem: {elem} nan: {nan}")
        if str(elem).lower() == "nan":
            elem = str(nan)
    if isnumber(elem) and not str(elem).startswith("_"):
        suffix = prefix = ""
        # dbug(f"neg: {neg} rnd: {rnd} human: {human} elem: {elem} repr(elem): {repr(elem)}")
        # flag_prcnt = False
        if str(elem).endswith("G"):
            elem = elem.replace("G", "")
            suffix = "G"
        if str(elem).endswith("M"):
            elem = elem.replace("M", "")
            suffix = "M"
        if str(elem).endswith("K"):
            elem = elem.replace("K", "")
            suffix = "K"
        if str(elem).endswith("%"):
            elem = elem.replace("%", "")
            suffix = "%"
        if str(elem).startswith("+"):
            prefix = "+"
            elem = elem.lstrip("+")
        elem_val = escape_ansi(elem)
        # codes = split_codes(elem)
        # pat = elem_val + "(?!;)(?!m)"
        # dbug(elem_val)
        # dbug(repr(elem))
        # dbug(pat)
        # codes = re.split(pat, elem)
        # codes = [codes_elem_d['prefix'], codes_elem_d['suffix']]
        # dbug(codes)
        if clr_b and not re.search(r"[BMK]", elem_val):
            if "." in str(elem_val):
                clean_val = elem_val.replace(",", "")
                elem_val = float(clean_val)
            else:
                if isnumber(elem):
                    elem_val = int(elem_val)
            if elem_val < 0:
                # codes[0] = NEG_COLOR
                prefix = NEG_COLOR
                # dbug(f"setting {NEG_COLOR}color{RESET}")
                # elem = f"{NEG_COLOR}{elem_val}"
            else:
                # codes[0] = POS_COLOR
                prefix = POS_COLOR
                # dbug(f"POS_COLOR: {POS_COLOR} {repr(POS_COLOR)}")
                # elem = f"{POS_COLOR}{elem_val}"
        # dbug(repr(elem))
        if rnd != "" or rnd == 0:
            # number = escape_ansi(elem) 
            # pre_post_codes = str(elem).split(number)
            # dbug(len(pre_post_codes))
            if not str(elem_val).endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
                # TODO consider this: rgx = re.search(r'[a-zA-Z%\+,]+', "-4.3%")
                if "," not in str(elem_val):
                    elem_val = round(float(elem_val), 2)
                    elem_val = f"{elem_val:.2f}"
            # elem_val = pre_post_codes[0] + f"{round(float(number), 2)}" + pre_post_codes[1]
        # dbug(repr(elem_val))
        if human:
            # number = escape_ansi(elem) 
            # pre_post_codes = str(elem).split(number)
            # dbug(repr(elem))
            # dbug(repr(number))
            # elem = pre_post_codes[0] + f"{float(number):,}" + pre_post_codes[1]
            if "," in str(elem_val):
                elem_val = str(elem_val).replace(",", "")
                # dbug(elem_val)
            if str(elem_val).replace(".", "").isnumeric():
                elem_val = f"{float(elem_val):,}"
            # dbug(elem_val)
        # dbug(human)
        elem = prefix + str(elem_val) + suffix
        # dbug(elem)
    if rset:
        elem += RESET
    # dbug(f"Returning elem: {elem}")
    return elem
    # ###  EOB def color_neg(elem, *args, **kwargs): ### #


# alias for above
cond_num = color_neg


# def dict2str(d):
    # dbug("who uses this?")
    # string = " "
    # for k, v in d.items():
        # string += f"{k}: {v} "
    # return string
        

# ####################################
def get_random_line(file, prnt=False):
    # ################################
    """ 
    purpose: grabs one random line from a file
    requires:
        from gtools purify_file, centered, boxed, printit, cat_file
        import random
    returns: line 
    Note: file has all comments removed first (purified)
    """
    """--== Imports ==--"""
    import random
    """--== sanity check ==--"""
    if isinstance(file, str):
        file = os.path.expanduser(file)
    """--== Process ==--"""
    r_l = purify_file(file)
    line = random.choice(r_l)
    if prnt:
        lines = boxed(line, title=" Quote ")
        printit(centered(lines))
    return line
    # ### EOB def get_random_line(file, prnt=False): ### #


# # ###################################
# def print_table(my_d, prnt=False, col_l=None, title=""):  # noqa:
#     # ################################
#     """
#     Pretty_print a list of dictionaries (my_d) as a dynamically sized table.  # noqa:
#     If column names (colList) aren't specified, they will show in random order.
#     Author: Thierry Husson - Use it as you want but don't blame me.
#     #>>> print_table({"one":1,"two":2,"three":3})
#     =================================================
#     || one                  |                 1.00 ||
#     || two                  |                 2.00 ||
#     || three                |                 3.00 ||
#     =================================================
#     """
#     dbug("who uses this")
#     # if not colList: colList = list(myDict[0].keys() if myDict else [])
#     # myList = [colList] # 1st row = header
#     # for item in myDict: myList.append([str(item[col] or '') for col in colList])  # noqa:
#     # colSize = [max(map(len,col)) for col in zip(*myList)]
#     # formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
#     # myList.insert(1, ['-' * i for i in colSize]) # Seperating line
#     # for item in myList: print(formatStr.format(*item))
#     llen = 49
#     lines = []
#     if prnt:
#         top_line = "=" * llen
#         if len(title) > 1:
#             top_line = do_title(title=title, chr="=", length=llen, prnt=False)
#         print(top_line)
#     lines.append("=" * llen)
#     # dbug(my_d)
#     # dbug(type(my_d))
#     for k, v in my_d.items():
#         if k == "" and v == "":
#             continue
#         k = k.replace("\n", '')
#         if isnumber(v):
#             # dbug(f"k:{k} v:{v}")
#             if int(v) > 1000000:
#                 v = int(v / 1000000)
#                 v = str(v) + "M"
#                 # print(f"|| {k:<20} | {v:>20} ||")
#                 line = "|| {:<20} | {:>20} ||".format(k, v)
#                 # print("|| {:<20} | {:>20} ||".format(k, v))
#                 if prnt:
#                     print(line)
#                 lines.append(line)
#             else:
#                 # print(f"|| {k:<20} | {v:>20.2f} ||")
#                 if isinstance(v, str):
#                     line = "|| {:<20} | {:>20} ||".format(k, v)
#                     # print("|| {:<20} | {:>20} ||".format(k, v))
#                 else:
#                     line = "|| {:<20} | {:>20.2f} ||".format(k, v)
#                     # print("|| {:<20} | {:>20.2f} ||".format(k, v))
#                 if prnt:
#                     print(line)
#                 lines.append(line)
#         else:
#             if v is None:
#                 v = "na"
#             # dbug(f"k:{k} v:{v}")
#             # print(f"|| {k:<20} | {v:>20} ||")
#             line = "|| {:<20} | {:>20} ||".format(k, v)
#             if prnt:
#                 print(line)
#             lines.append(line)
#     line = "=" * llen
#     if prnt:
#         print(line)
#     lines.append(line)
#     return lines
#     # EOB #


# #########################################
def run_cmd_threaded(cmd, *args, **kwargs):
    # #####################################
    """
    purpose: runs a cmd as a thread
    options:
        - lst: bool  # returned output lines will be put into a list rather than a str
    return: output from cmd
    Note: Please, be aware that a result will be returned only after this finishes
    so put it "later" rather than "sooner" in your app
    """
    """--== debugging ==--"""
    dbug("who uses this?")
    """--== Config ==--"""
    lst = bool_val(['lst', 'list'], args, kwargs, dflt=False)
    """--== Process ==--"""
    t = ThreadWithReturn(target=run_cmd, args=(cmd,))
    t.start()
    result = t.join()
    if lst:
        result = result.split("\n")
    return result


# ###############
def run_cmd(cmd, *args, prnt=False, runas="", **kwargs):
    # ###########
    """
    purpose: runs cmd and returns output
      eg: out = run_cmd("uname -o",False)
      # now you can print the output from the cmd:
      print(f"out:{out}")
    options:
        - lst: bool   # ouput will return as a list of line rather than a str
        - rc: bool    # returns the cmd return code instead of output
        - runas: str  # you can declare who to run the cmd as 
    returns: output from command
    Note: if runas == sudo then the command will be sun with sudo...
    -  this function strips out all ansi code and filters all errors
    Test:
    >>> r = run_cmd("uname -o")
    >>> print(r)
    GNU/Linux
    <BLANKLINE>
    """
    # dbug(funcname)
    # dbug(cmd)
    """--== Config ==--"""
    return_l = bool_val(['list', 'lines', 'lst'], args, kwargs)
    return_rc = bool_val(['rc', 'return_rc', 'rtrn_rc'], args, kwargs)
    runas = kvarg_val(["runas", "sudo"], kwargs, dflt=runas)
    """--== Notes ==--"""
    # so many ways to do this...
    # resource: https://janakiev.com/blog/python-shell-commands/
    # simplest is os.system(cmd) but lacks flexibility like capturing the output
    # stream = os.popen(cmd)
    # print(stream.read())
    #   or
    # print(os.popen(cmd.read())) # returns one str
    #   but subprocess is the recommended method
    # import subprocess
    # import shlex
    # dbug(prnt)
    # NOTE: declaring runas will require that user to have sudo for the cmd
    # eg in /etc/sudoers of /etc/sudoers.d/www-data
    #   # user HOSTS=USER(S) OPTION: cmds
    #   www-data ALL=(user) NOPASSWD: /path/to/cmd
    # note: the env vars will be limited to the named user 
    if runas != "":
        cmd = f"sudo -u {runas} {cmd}"
    try:
        # process gets used below
        # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
        (out, err) = process.communicate()
        rc = process.returncode
        # dbug(out)
        # dbug(err)
        # dbug(rc)
    except Exception as Error:
        # if process fails then run one of these
        # out = os.system(cmd)
        # out = os.popen(cmd)
        out = subprocess.check_output(cmd.split(), universal_newlines=True) + f" Error: {Error}"
        # dbug(Error)
        return out
    # dbug(f"cmd.split():{cmd.split()} process:{process}")
    #out = ""
    #while True:
    #    output = process.stdout.readline()
    #    if output == "" and process.poll() is not None:
    #        break
    #    if output:
    #        if prnt:
    #            print(output.strip())
    #        # out += output.decode()
    #        try:
    #            out += output
    #        except Exception as e:
    #            dbug(f"Error: {e}")
    # rc = process.poll()
    # if rc != 0:
    #   return str(rc)
    # dbug(prnt)
    # dbug(out)
    # dbug(f"Running os.system({cmd})")
    # r = os.system(cmd)
    # dbug(f"Done: Running os.system({cmd})  r: {r}")
    # dbug(f"note: out: {out} rc: {rc}")
    if return_l:
        # dbug(return_l)
        out = out.split("\n")
    if return_rc:
        return out, rc
    return out


def grep_lines(lines, pattern, *args, **kwargs):
    """
    purpose: searches lines for pattern 
    options: 
    -    ic: bool (insensitive case)
    -        rtrn_bool=False: bool    #  (whether to rtrn lines [default] or bool result)
    -        csv: bool                # will convert a list of lists to a list of csv style lines before searching
    -                                 #   and but returns the line as a list, just the way we got it
    returns: matched line(s) (or True False if rtrn_bool is True)
    Note: if only one line is matched then it will return that one line otherwise it will return a list of matched_lines
    """
    # used in do_watch and maybe others
    # dbug(funcname())
    """--== Config ==--"""
    ic = bool_val(['ic', 'ci', 'case_insensitive', 'ignore_case'], args, kwargs) 
    rtrn_b = bool_val(['rtrn_bool', 'rtrn_d', 'bool', 'rtrn'], args, kwargs, dflt=False)
    csv_b = bool_val(['csv'], args, kwargs, dflt="")
    """--== Xlate filename to lines ==--"""
    if isinstance(lines, str):
        lines = cat_file(lines, 'lst')
    """--== Process ==--"""
    matched_lines = []
    for line in lines:
        # dbug(line)
        # this might have been taken from a list of list (lol) so convert the list to a csv style line
        if csv_b or isinstance(line, list):
            # dbug(line)
            csv_b = True
            orig_line = line
            # dbug(orig_line)
            line = ", ".join(line)
        # dbug(line)
        if ic:
            # ignore case
            rex_b = re.search(pattern, line, re.I)
        else:
            # case sensitive
            rex_b = re.search(pattern, line)
        if rex_b:
            # use the regex set above
            if csv_b:
                matched_lines.append(orig_line)
            else:
                matched_lines.append(line)
    if rtrn_b:
        if len(matched_lines) > 0:
            return True
        else:
            return False
    if len(matched_lines) == 1:
        matched_lines = matched_lines[0]
    if len(matched_lines) == 0:
        matched_lines = None
    return matched_lines



# # ###########################################################
# def sshp(cmd='uptime', rhost="192.168.86.61", user="geoffm"):
#     # #######################################################
#     """
#     purpose: 
#     - ssh parallel
#     - uses paramiko module
#     input: cmd, remote_host, user
#     returns: output of the command
#     WIP
#     """
#     dbug("who uses this")
#     import paramiko
#     ssh = paramiko.SSHClient()
#     timeout = 2
#     # printit(f"Running cmd: {cmd} on server: {rhost} with ssh and user: {user}...")
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
#     ssh.connect(rhost, port=22, timeout=timeout, username=user)  # , password="password")
#     stdin, stdout, stderr = ssh.exec_command(cmd)
#     out = stdout.readlines()
#     out = "".join(out).strip()
#     # dbug(f"[{out}]")
#     return out
# 

# ###############################
def list_files(dirs, file_pat="*", *args, **kwargs):
    # ###########################
    """
    purpose: prints a list of enumerated basename filenames (sorted by name)
    input:
        dirs=list|str
    options: 
        pattern: str|list = "*"  # glob pattern
        return_msgs<bolean> = False 
        prnt<bolean> = False
        dirs: bool               # include dirs
        dir_only: bool           # only dirs
        links: bool              # include links
    returns:
        a sorted list of those names
        or
        return_msgs and sorted names
    use: list_files("/tmp")
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(dirs)
    # dbug(file_pat)
    # dbug(args)
    # dbug(kwargs)
    # dbug(file_pat)
    """--== Config ==--"""
    ptrns = kvarg_val(['file_pat', 'patterns', 'pattern', 'ptrn', 'ptrns', 'pat'], kwargs, dflt=[file_pat])
    links = bool_val('links', args, kwargs, dflt=False)  # should links be followed
    dirs_b = bool_val(["dirs_b", "dirs"], args, kwargs, dflt=False)
    dirs_only = bool_val(["dirsonly", "dirs_only", "dironly", "dir_only"], args, kwargs, dflt=False)
    """--== Inits ==--"""
    msgs = []
    files_l = []
    """--== Converts ==--"""
    if isinstance(ptrns, str):
        ptrns = [ptrns]
    if isinstance(dirs, str):
        dirs = dirs.split()
    """--== Process ==--"""
    for ptrn in ptrns:
        for dir in dirs:
            # dbug(f"chkg ptrn: {ptrn} in dir: {dir}")
            # file_pat = f"{file_pat}*"
            # dbug(f"Searching dir: {dir} for file pattern: {file_pat}...")
            pathname = f"{dir}/{ptrn}"
            # dbug(pathname)
            for n, file in enumerate(glob.glob(pathname)):
                if dirs_b:
                    if os.path.isdir(file):
                        files_l.append(file)
                        # d_l = os.listdir(file)
                        # dbug(d_l)
                        continue
                # dbug(f"Checking file: {file} in pathname: {pathname}")
                if os.path.islink(file):
                    # dbug(f"File: {file} found in dir: {dir} is a link.... skipping...")
                    if links:
                        files_l.append(file)
                    else:
                        continue
                # abs_file = f"{dir}/{file}"
                # dbug(f"Found file {file} appending to files_l: {files_l}")
                if not dirs_only:
                    if os.path.isfile(file):
                        files_l.append(file)
                        msgs.append("{:>2})  {}".format(n, file))
            files_l = sorted(files_l)
            if len(files_l) > 0:
                msg = "Found these files:"
                for f in files_l:
                    msg += f"\n   {f}"
    # if return_msgs:
    #     return msgs, names
    else:
        return files_l
    # ### EOB def list_files(dirs, file_pat="*", *args, **kwargs): ### #


# # ##########################################################
# def select_from(my_list, box=True, center=False, shadow=False, tst=False, title="", footer="", prompt="Please make your selection: [q to Quit] "):
#     # ######################################################
#     """
#     deprecated: see gselect
#     purpose: select from any list
#     >>> lst = ['one', 'two', 'three']
#     >>> r = select_from(lst, tst=True)
#     +--------------+
#     |   1.) one    |
#     |   2.) two    |
#     |   3.) three  |
#     +--------------+
#     >>> print(f"{r}")
#     (3, 'three')
#     # Always returns a tuple
#     """
#     # dbug(f"my_list: {my_list}")
#     if box:
#         msgs = []
#         msgs = my_list
#         if len(msgs) == 0:
#             return False
#         selections = []
#         names = {}
#         names = list(enumerate(my_list, 1))
#         for num, elem in enumerate(my_list, 1):
#             selections.append(f"{num:>2}.) {elem}")
#         selections
#         # dbug(names)
#         lines = boxed(selections, title=title, shadow=shadow)
#         printit(lines, center=center)
#     if tst:  # here only for doctest
#         choice = 0
#     else:
#         pad_left = ""
#         if center:
#             columns = get_columns()
#             pad_left = " " * ceil((int(columns) - len(prompt)) / 2)
#         choice = input(pad_left + prompt)
#     choice = str(choice)
#     # if choice.lower() == "q" or choice.lower() == "quit":
#     if choice in ("", "q", "Q"):
#         # note if choice is blank this allows the coder to add a default
#         return (choice.lower(), "")
#     else:
#         selected = names[int(choice)-1]
#     # returns a tuple eg (1, "selection one") so you can use either selected[0] or selected[1]
#     return selected  # a tuple: (number, item)
# 

# ####################################################
def select_file(path="./",
                *args,
                pattern="*",
                prnt=True,
                color="",
                boxed=False,
                box_color="",
                title="",
                footer="",
                shadow=False,
                center=False,
                displaywidth=0,
                rtrn="value",
                **kwargs
                ):
    # ################################################
    """
    purpose: select a file (or dir) from using pattern(s) 
    required: 
    options:
        - path: str|list  (defaults to "./")
        - pattern: str|list
        - prompt: str
        - mtime: bool      # include mtime in listing
        - centered
        - dirs: bool       # include dirs
        - dirs_only: bool  # only directories
        - prnt: bool
        - shadow
        - footer
        - width=0
    use: f = select_file("/home/user","*.txt")
    prints a file list and then asks for a choice
    returns basename of the filename selected
    Note: this uses list_files
    """
    """--== Config ==--"""
    ptrns = kvarg_val(['pattern', 'patterns', 'pat', 'ptrn', 'ptrns'], kwargs, dflt=pattern)
    prompt = kvarg_val('prompt', kwargs, dflt="Please select: ")
    mtime = bool_val(['ll', 'long', 'long_list', 'mtime'], args, kwargs, dftt=False)
    centered = bool_val(['centered', 'center'], args, kwargs, dflt= center)
    # choose = bool_val(['choose', 'select', 'pick'], args, kwargs, dflt=True)
    dirs_b = bool_val(['dirs_b', 'dirs', 'dir'], args, kwargs, dflt=False)
    dirs_only = bool_val(['dirs_only', 'dirsonly', 'dironly', 'dir_only', 'only_dirs'], args, kwargs, dflt=False)
    width = kvarg_val(["displaywidth", "width"], kwargs, dflt=0)
    """--== Process ==--"""
    file_l = list_files(path, ptrns=ptrns, dirs_b=dirs_b, dirs_only=dirs_only)
    # dbug(file_l)
    # if not choose:
    #     # just use list_files() instead
    #     return file_l
    file_d = {}
    for file in file_l:
        base_filename = os.path.basename(file)
        if mtime:
            mtime = os.path.getmtime(file)
            mtime = time.ctime(mtime)
            base_filename += f" ({mtime})"
        file_d[base_filename] = file
    # from rtools import rselect
    if width == 0:
        width = int(get_columns() * .8)
    if title == "":
        title = " File Selection "
    # dbug(file_d)
    if len(file_d) == 1:
        return file_d
    ans = gselect(file_d, rtrn=rtrn, width=width, box_color=box_color, color=color, centered=centered, shadow=shadow, title=title, footer=footer, prompt=prompt)
    # dbug(ans)
    return ans


# ##################################
def reduce_line(line, max_len, pad):
    # ##############################
    """
    reduce a line to no more than max_len with and no broken words
    then return the reduced_line, and remaining_line
    Note - use textwrap for this now -- reduce_line should be depracated
    """
    this_line = ""
    remaining_line = ""
    msg_len = len(line)
    msg = line
    if msg_len + pad > max_len:
        # dbug("msg: " + msg)
        # dbug(f"msg_len [{msg_len}] > max_len [{max_len}] and pad: {pad}")
        words = msg.split(" ")
        word_cnt = len(words)
        cnt = 0
        for word in words:
            # dbug("word: " + word)
            # dbug("len(this_line): " + str(len(this_line)))
            if len(this_line) + pad + len(word) + 4 > max_len:
                remaining_line = " ".join(words[cnt:])
                break
            else:
                cnt += 1
                # dbug("adding word: " + word)
                if len(this_line) == 0:
                    this_line += word
                else:
                    this_line += " " + word
                if cnt > word_cnt:
                    break
        # dbug("this_line: " + this_line)
        # dbug("remaining_line: " + remaining_line)
    return this_line, remaining_line


# ####################
def escape_ansi(line, *args, **kvargs):
    # ################
    """
    purpose: Removes ansii codes from a string (line)
    aka: name should be escape_ansii
    returns: "cleaned no_code" line
    TODO: allow option to return clr_codes[1], nocode(elem), clr_codes[2]
    see: split_codes()
    """
    """--== debugging`` ==--"""
    # dbug(line)
    # dbug(type(line))
    """--== Converts ==--"""
    line = str(line)  # this is needed
    # if isinstance(line, list):
    #     dbug(f"line: {type(line)} should be a string, not a list....")
    #     return None
    # else:
    #     line = str(line)
    """--== Process ==--"""
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    # ansi_escape2 = re.compile(r"\[\d+.*?m")  # not needed???????
    # ansi_escape2 = re.compile(r"(?:\x1b[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    # ansi_escape3 = re.compile(r"(?:\033[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    ncline = ""
    if isinstance(line, list):
        new_lines = []
        for new_line in line:
            if not isinstance(new_line, str):
                # dbug(new_line)
                new_lines.append(new_line)
            else:
                if isinstance(new_line, list):
                    if len(new_line) == 0:
                        new_line.append(" ")
                        dbug(f"length of newline was 0 so now new_line: [{repr(new_line)}]... continuing...")
                        continue
                # new_lines.append(ansi_escape.sub("", new_line))
                new_line = ansi_escape.sub("", new_line)
                new_line = re.compile(r"\[\d+.*m")
                # new_line = ansi_escape.sub("", ncline)
                # dbug(new_line)
                #new_line = ansi_escape2.sub("", ncline)
                # dbug(new_line)
                new_lines.append(new_line)
                # new_lines.append(escape_ansi(new_line))
        return new_lines
    if isinstance(line, str):
        # rgx = re.findall(ansi_escape, line)
        # dbug(rgx)
        ncline = ansi_escape.sub("", line)
        # ncline = ansi_escape2.sub("", ncline)
    # dbug(repr(ncline))
    return ncline


# ##############
def nclen(line, *args):
    # ##########
    """
    purpose: finds the length of a string minus any ansi-codes and returns that lenght
    returns: length
    no color len of line (length w/o ansii codes)
    if 'rich' in args then stip rich color code
    """
    """--== debugging ==--"""
    # dbug(line)
    # dbug(type(line))
    # dbug(len(line))
    """--== Inits ==--"""
    nclen = 0
    """--== Converts ==--"""
    line = str(line)
    # dbug(repr(line))
    # if isinstance(line, str):
    """--== Process ==--"""
    nc_line = escape_ansi(line)
    nclen = len(nc_line)
    # dbug(repr(nc_line))
    # dbug(f"returning nclen: {nclen}")
    # dbug(nclen)
    return nclen


# ########################
def do_edit(file, lnum=0):
    # ####################
    """
    purpose: launches vim editor with file
        a quick-n-dirty utility to edit a file
    options:
        - lnum: line number
    Initiate edit on a file - with lineno if provided
    """
    if lnum:
        # cmd = f"vim {file} +{str(lnum)}"
        cmd = "vim i" + file + " " + str(lnum)
    else:
        # cmd = f"vim {file}"
        cmd = "vim " + file
    try:
        r = subprocess.call(cmd, shell=True)
    except:
        # this is unlikely and really not a solution because fails on syntax occur on compilation
        cmd = f"vimit {file}"
        r = subprocess.call(cmd, shell=True)
    # print(f"{cmd}")
    return r
    # ### EOB def do_edit(file, lnum=0): ### #``


# ##################################
def cinput(prompt, *args, **kwargs):
    # ##############################
    """
    aka: centered input
    purpose: gets input from user using provided promt - centers the prompt on the screen
    options:
        - shift: int   # allows you to shift the position of the prompt (from the center) eg shift=-5
        - quit|exit|close: bool   # will quit with do_close() if availaable or just sys.exit()
    returns: user response
    """
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    quit = bool_val(['quit', 'exit', 'close'], args, kwargs, dflt=False)
    shift = kvarg_val('shift', kwargs, dflt=0)
    """--== Process ==--"""
    if prompt == "":
        prompt = "Hit Enter to continue..."
    ans = input(printit(prompt, 'centered', prnt=False, shift=shift, rtrn_type='str')) or ""
    if quit and ans.lower() == "q":
        try:
            do_close("Exiting as requested...", 'centered')
        except:
            sys.exit()
    return ans


# ##############################################
def do_prcnt_bar(amnt, full_range=100, *args, bar_width=40, show_prcnt=True, **kwargs):
    # ##########################################
    # aliased below to prcnt_bar(...)
    """
    purpose: displays a percentge bar
    args: amnt (prcnt)
    options: full_range=100 if you submit this prcnt will be based on it
        - bar_width=40: int   # declares width of bar
        - color: str          # text color
        - done_color:         # color of done portion
        - undone_color:       # color of undone portion
        - done_chr: str       # done character
        - undone_chr: str     # undone character
        - prompt: str         # prompt (before the bar)
        - suffix: str         # suffix (afterr the bar)
        - brackets=["[", "]"]: list 
        - show_prcnt=True: bool  # include the percentage at the end
        - prnt=False: bool  # False to allow use in dashboards  # you can tell this to not print so you can include in in a box etc
    returns: percent bar line as a str 
    #>>> rh = 56
    #>>> rl = 50
    #>>> cp = 51
    #>>> amnt = cp - rl
    #>>> full_range = rh - rl
    #>>> print(f"rl {do_prcnt_bar(amnt,full_range)} rh")
    # rl [██████----------------------------------]16% rh
    """
    """--== Config ==--"""
    full_range = kvarg_val(["full_range", "total", "tot"], kwargs, dflt=full_range)
    bar_width = kvarg_val(["bar_width", 'length', 'width'], kwargs, dflt=bar_width)
    color = kvarg_val(['color'], kwargs, dflt="")
    done_color = kvarg_val(['done_color', 'done_clr'], kwargs, dflt=color)
    # done_chr = u'\u2588'   # █ <-- full, solid shadow
    # done_chr = "\u2593"    # ▓ <-- full, light shadow
    done_chr = "\u2592"      # ▒ <-- full, medium shadow
    # done_chr = "\u2591"    # ░ <-- full, dark shadow 
    # done_chr = "\u2584"    # ▄ <-- Lower five eighths bloc
    # rdone_chr = "\u2585"   # ▆ <-- Lower five eighths bloc
    # done_chr = "\u2586"    # ▆ <-- 3/4 high solid block
    # done_chr = "\u2582"    # ▂ <-- lower 1/4 block
    done_chr = kvarg_val(['done_chr', 'chr'], kwargs, dflt=done_chr)
    undone_color = kvarg_val(['undone_color', 'undone_clr', 'fill_color'], kwargs, dflt="")
    undone_chr = "\u2015"    # ― <-- horizontal line
    undone_chr = kvarg_val(['fill', 'fc', 'undone_chr'], kwargs, dflt=undone_chr)
    # done_color = sub_color(done_color + " on rgb(255,255,255)")
    # done_chr = done_color + done_chr
    prompt = kvarg_val(["prefix", 'prompt', 'title'], kwargs, dflt="")
    suffix = kvarg_val(["suffix", 'ending', 'end_with'], kwargs, dflt="")
    # brackets = kvarg_val(["brackets"], kwargs, dflt=["", ""])
    brackets = kvarg_val(["brackets"], kwargs, dflt=["[", "]"])
    show_prcnt = bool_val("show_prcnt", args, kwargs, dflt=show_prcnt)
    prnt = bool_val(["prnt", 'print', 'show'], args, kwargs, dflt=False)
    centered = bool_val(["centered", 'center'], args, kwargs, dflt=False)
    """--== Init ==--"""
    # dbug(done_color)
    DONE_COLOR = sub_color(done_color)
    UNDONE_COLOR = sub_color(undone_color)
    RESET = sub_color('reset')
    """--== Converts ==--"""
    if isinstance(amnt, str):
        amnt = amnt.replace("*", "")
    """--== Process ==--"""
    amnt = float(escape_ansi(amnt))
    full_range = float(full_range)
    try:
        prcnt = float(amnt / full_range)
    except Exception as Error:
        dbug(f"prcnt calc failed... amnt: {amnt} / full_range: {full_range}... returning None")
        return None
    # dbug(f"amnt: {amnt} full_range: {full_range} prcnt: {prcnt} bar_width: {bar_width}")
    # done_len = int(prcnt / 100 * bar_width)
    done_len = int(prcnt * bar_width)
    done_len = ceil(prcnt * bar_width)
    undone_len = int(bar_width - done_len)
    # dbug(f"done_len: {done_len} undone_len: {undone_len}")
    done_fill = DONE_COLOR + done_chr * done_len
    undone_fill = UNDONE_COLOR + undone_chr * undone_len
    bar = done_fill + undone_fill  # <--bar
    bar = brackets[0] + bar + brackets[1]
    rtrn = bar
    if show_prcnt:
        prcnt = str(ceil(prcnt * 100)) + "%"
        rtrn = UNDONE_COLOR + prompt + bar + UNDONE_COLOR + f"{prcnt:>4}" + suffix
    if prnt:
        txt = printit(RESET + rtrn + RESET, prnt=False, centered=centered, rtrn_type='str')
        sys.stdout.write('\x1b[?25l')  # Hide cursor
        sys.stdout.write(txt)
        sys.stdout.flush()
    return RESET + rtrn + RESET
    # ### EOB def do_prcnt_bar(amnt, full_range=100, *args, bar_width=40, show_prcnt=True, **kwargs): ### #


# alias for above
prcnt_bar = do_prcnt_bar


# #############################################
def progress(progress, *args, **kwargs):
    # #########################################
    """
    # prcnt = 0.20
    # progress(prcnt, width=60)
    Percent: [############------------------------------------------------] 20%
    # or
    >>> for i in range(100):
    ...     time.sleep(0.1)
    ...     progress(i/100.0, width=60)
    Percent: [############################################################] 99%
    """
    width = kvarg_val(['bar_width', 'length', 'width'], kwargs, dflt=40)  # Modify this to change the length of the progress bar  # noqa:
    prompt = kvarg_val(['prompt', 'prefix'], kwargs, dflt="")
    color = kvarg_val(['color', 'text_color', 'txt_color', 'txt_clr'], kwargs, dflt="")
    done_color = kvarg_val(['done_color'], kwargs, dflt="")
    undone_color = kvarg_val(['fill_color', 'fcolor', 'fclr', 'undone_color'], kwargs, dflt="")
    COLOR = sub_color(color)
    DONE_COLOR = sub_color(done_color)
    UNDONE_COLOR = sub_color(undone_color)
    RESET = sub_color('reset')
    # FILL_COLOR = sub_color(fill_color)
    done_chr = kvarg_val(['done_chr', 'chr'], kwargs, dflt="\u2588")
    undone_chr = kvarg_val(['fill_chr', 'fc', 'undone_chr'], kwargs, dflt=" ")
    status = kvarg_val(['status', 'done_msg', 'done_txt', 'done_text', 'post_prompt', 'suffix'], kwargs, dflt="")
    center_b = bool_val(["centered", "center"], args, kwargs, dflt=False)
    shift = kvarg_val("shift", kwargs, dflt=0)
    """--== SEP_LINE ==--"""
    if isinstance(progress, int):
        progress = float(progress)
        # if not isinstance(progress, float):
        # progress = 0
        # status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
        sys.stdout.write('\x1b[?25h')  # retore cursor
        sys.stdout.flush()
    if progress >= 1:
        progress = 1
        status = f"{status}\r\n"
        status += "\x1b[?25h"          # Restore cursor
        sys.stdout.write('\x1b[?25h')  # retore cursor
        sys.stdout.flush()
        # dbug(status)
    done_len = int(round(width * progress))
    done_fill = done_chr * done_len + RESET
    undone_fill = undone_chr * (width - done_len) + RESET
    shift = abs(shift)
    prcnt = progress * 100
    """--== SEP_LINE ==--"""
    if center_b:
        # ruleit() 
        shift -= (int(get_columns()) - (width + nclen(prompt))) // 2
        # dbug(shift)
        lfill = " " * shift
        prompt = lfill + prompt
    txt = COLOR + f"\r{prompt}[{RESET}" + DONE_COLOR + f"{done_fill}" + RESET + UNDONE_COLOR + f"{undone_fill}" + COLOR + f"] {prcnt}%"
    txt = txt + f" {status}" + RESET
    """--== SEP_LINE ==--"""
    sys.stdout.write('\x1b[?25l')  # Hide cursor
    sys.stdout.write(txt)
    sys.stdout.flush()
    # dbug(txt)
    return
    # ### EOB def progress(progress, *args, **kwargs): ### #


# ################################
def from_to(filename, begin, end, *args, include="none", **kwargs):
    # ############################
    """
    purpose: returns lines from a *file* from BEGIN pattern to END pattern" (between BEGIN and END)
    options:
    -  include: can be equal to "none", top|begin|start, bottom|end, or 'both'
    --    include='top' will include the begin pattern line, 
    --    include='bottom' will include the end pattern line
    --    include='both' will include top and end pattern matching lines
    returns: lines between (or including) begin pattern and end pattern from filename (or a list of lines)
    """
    # dbug(funcname())
    # dbug(filename)
    # dbug(begin)
    # dbug(end)
    """--== Config ==--"""
    begin = kvarg_val(['from', 'after'], kwargs, dflt=begin)
    end = kvarg_val(['to', 'before'], kwargs, dflt=end)
    """--== Init ==--"""
    include = include.lower()  # can be 'top', 'bottom', or both to include the {begin} and or {after}
    lines = []
    return_lines = []
    start_flag = False
    # dbug(f"begin: [{begin}] end: [{end}]")
    # askYN()
    """--== SEP_LINE ==--"""
    if isinstance(filename, list):
        lines = filename
    else:
        lines = cat_file(filename, 'lst')
        # with open(filename) as fp:
        #     lines = fp.readlines()
    # dbug(lines)
    for line in lines:
        line = line.strip("\n")
        beg_regex = re.search(begin, line) 
        end_regex = re.search(end, line) 
        # dbug(f"chkg line: {line} begin: {begin} end: {end}")
        # if end in line and start_flag:
        if end_regex and start_flag:
            # dbug(f"Found {end} in [line]")
            # askYN()
            if include in ("bottom", "end", "both"):
                return_lines.append(line)
                # dbug(f"Added [{line}]")
            # return_lines = [line.strip() for line in return_lines]
            return return_lines
        if start_flag:
            return_lines.append(line)
            # dbug(f"Added [{l}]")
        # if begin in line:
        if beg_regex:
            # dbug(f"Found {begin} in {line}")
            start_flag = True
            if include in ("top", "start", "begin", "both"):
                return_lines.append(line)
                # dbug(f"Added [{line}]")
            else:
                continue
    return return_lines  # return lines if end not found
    # ### END def from_to(filename, begin, end): ### #


# ############################################################
def add_content(file, content="", header="", **kvargs):
    # ########################################################
    """
    I wrote this because I am constantly building csv files with a header line 
    consider add_or_replace() function
    Required:
        file
        content=str|list
    Options:
        after=pattern
        before=pattern
        replace=pattern
        position=##
        if none of those content is appended to the file
        if header is also included it will be added to the begining of the file if it does not already exitst
    used_to_be: add_line()
    """
    # dbug(funcname(), 'centered')
    """--== set needed vars ==--"""
    position = kvarg_val('position', kvargs, dflt=None)
    after = kvarg_val("after", kvargs, dflt="")
    before = kvarg_val("before", kvargs, dflt="")
    replace = kvarg_val("replace", kvargs, dflt="")
    backup = kvarg_val("backup", kvargs, dflt=False)
    pattern = ""
    if after != "":
        pattern = after
    if before != "":
        pattern = before
    if replace != "":
        pattern = replace
    # dbug(f"file: {file} header: {header} after: {after} before: {before} pattern: {pattern} position: {position}")
    show = kvarg_val('show', kvargs, dflt=False)
    DBUG = show
    # dbug(position)
    """--== functions ==--"""
    def insert_line(file, line, position=None):
        # dbug(position)
        lines = []
        lines = cat_file(file, 'list')
        # lines.insert(position, line)
        if position is None:
            if isinstance(line, list):
                line = "\n".join(line)
            f = open(file, "a")
            f.write(line)
            if not line.endswith("\n"):
                f.write("\n")
            # f.write(line)
            f.close()
            return
        new_lines = []
        if len(lines) > 0:
            for n, l in enumerate(lines):
                # dbug(f"position: {position} n: {n} l: {l}")
                if n == position and position == 0:
                    new_lines.append(line)
                if (n + 1) != position:
                    new_lines.append(l)
                else:
                    line_l = []
                    line_l = line.split("\n")
                    new_lines.extend(line_l)
                    new_lines.append(l)
        else:
            if isinstance(line, list):
                new_lines.extend(line)
            else:
                new_lines.append(line)
        f = open(file, "w")
        for line in new_lines:
            f.write(line + "\n")
        f.close()
    """--== code ==--"""
    if isinstance(content, dict):
        # assumes this is key, value pairs for one intended line str
        # turn the dict into a string of lines using the values, set header= keys
        content_d = {str(key): str(value) for key, value in content.items()}
        # values = content_d.values()
        # dbug(values)
        content_s = ",".join(content_d.values())
        header = list(content_d.keys())
        # dbug(content_s)
        content = content_s
        # dbug(header)
    if isinstance(content, list):
        # turn list into string of lines
        content = "\n".join(content)
    """--== handle backup ==--"""
    if backup:
        if file_exists(file):
            import shutil
            bak_ext = "-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            trgt_file = file + bak_ext
            # shutil.copy(file, trgt_file)
            shutil.copyfile(file, trgt_file)
            dbug(f"Backed up file: {file} to {trgt_file}", dbug=DBUG)
        else:
            dbug(f"file: {file} does not exist yet ... backup skipped...", dbug=DBUG)
    """--== write new file ==--"""
    if not file_exists(file):
        f = open(file, "w")
        f.write(content)
        f.close()
    else:
        # dbug(f"position: {position} pattern: {pattern}")
        if pattern != "":
            for line_no, line in enumerate(cat_file(file, 'list'), start=1):
                if pattern in line:
                    if before != "":
                        position = line_no
                        insert_line(file, content, position)
                    if after != "":
                        position = line_no + 1
                        insert_line(file, content, position)
                    if replace != "":
                        import in_place
                        with in_place.InPlace(file) as f:
                            for f_line in f:
                                new_line = line.replace(f_line, content)
                                f.write(new_line)
                    break
        if position is None and pattern == "":
            insert_line(file, content, position)
    """--== assure header is first ==--"""
    if isinstance(header, list):
        header = ",".join(header)
        # header = "# " + header.replace(",", ":")
    if header != "":
        with open(file, "r") as f:
            first_line = f.readline()
            for line in f:
                # skip the rest
                pass
        if header not in first_line:
            # dbug(f"Header not found ... so inserting header: {header} at position 0")
            insert_line(file, header, position=0)
        # else:
            # dbug(f"Header already exists in the first_line: {first_line}", dbug=DBUG)
    if show:
        printit(cat_file(file), 'boxed', title=f" {funcname()}() ")
    return
    # ### def add_content(file, content="", header="", **kvargs): ### #


# ###############
def sorted_add(filename, line, after="", before=""):
    """
    purpose: to insert a line between two patterns in a sorted way
    20210531 WIP!
    TODO if after and before are empty just use the whole file
    purpose: insert line into filename between after and before patterns
    the patterns need to be regex ie: r"pattern"
    assumes the block from after to before is sorted
    returns new_lines
    eg:
    >>> line = 'Insert this line (alphabetically) after "^-alt" but before "^-[a-zA-Z0-9] within block'
    >>> filename = "/home/geoffm/t.f"
    >>> after = r"^-alt"
    >>> before = r"^-[a-zA-Z0-9]"
    >>> lines = sorted_add(filename, line, after, before)
    >>> printit(lines)
    """
    tst_lines = from_to(filename, begin=after, end=before)
    # dbug(tst_lines)
    lines = cat_file(filename, lst=True)
    insert_line = line
    # dbug(insert_line)
    srch_block = False
    inserted = False
    new_lines = []
    last_line = "0"
    begin = after
    end = before
    beg_regex = False
    end_regex = False
    end_flag = False
    for ln in lines:
        # dbug(f"working ln: {ln}")
        # if beg_regex and end_regex:
        #     dbug("Done line should have been inserted... but will append ln")
        # else:
        if beg_regex and not end_regex:
            # dbug(f"now chkg ln: {ln} for end_regex")
            end_regex = re.search(end, ln)
            if end_regex and not inserted:
                new_lines.append(insert_line)
                inserted = True
                # dbug(f"Inserted: {insert_line}")
            if not end_regex and not inserted:
                if len(ln) > 0:
                    # case insensitive
                    if insert_line.lower() < ln.lower():
                        # dbug(f"insert_line: \n{insert_line}\n <\nln: {ln}")
                        new_lines.append(insert_line)
                        inserted = True
                        # dbug(f"Inserted: {insert_line}")
        else:
            beg_regex = re.search(begin, ln)
        # dbug(f"beg_regex: {beg_regex} end_regex: {end_regex}")
        #if  ln == "" or ln.startswith("#"):
        #    # retain these lines but don't test/check them
        #    new_lines.append(ln)
        #    continue
        #if srch_block and re.match(before, ln):
        #    # Turn off srch_block ... must be before Turn on srch_block
        #    srch_block = False
        #    dbug(f"Turning off srch_block ln: {ln}", 'ask')
        #    new_lines.append(ln)
        #    continue
        #if srch_block and not inserted:
        #    # test and *insert*
        #    if insert_line[0] <= ln[0] and insert_line[0] >= last_line[0]:
        #        if insert_line[1] <= line[1]:
        #            # print("=" * 10)
        #            # print(last_line)
        #            # print(insert_line)
        #            # print(line)
        #            # print("=" * 10)
        #            new_lines.append(insert_line)
        #            inserted = True
        #            dbug(f"Inserted: {insert_line}")
        #            dbug("", 'ask')
        #if re.match(after, line) and not srch_block:  # this has to be after Turn off srch_block
        #    # Found the begining pattern (ie {after}) Turning on srch_block
        #    srch_block = True
        #    dbug(f"Turning on srch_block...line: {line}", 'ask')
        last_line = ln
        new_lines.append(ln)
    # printit(new_lines)
    return new_lines
    # ### EOB def sorted_add() ### #


# ###############
def try_it(func, *args, attempts=1, **kwargs):
    # ###########
    """
    BROKEN BROKEN BROKEN
    This is a wrapper function for running any function that might fail
    - this will report the error and move on
    use:
        @try_it
        def my_func():
            print("if this failed an error would be reported ")
        my_func()
    """
    def inner(*args, **kwargs):
        # for n in range(attempts):
        #     try:
        #         r = func(*args, **kwargs)
        #         dbug(f"Returning r: {r}")
        #     except Exception as e:
        #         dbug(f"Error: {e} in: {func}")
        #         return None
        #     return r
        rsps = func(*args, **kwargs)
        return rsps
    r = inner(*args, **kwargs)
    dbug(f"returning {r}")
    return r


# ##############################
def max_width_lol(input_table):
    # ##########################
    """
    max_width for each "column" in a list of lists
    this is a way of truncating "columns"
    need more info here
    """
    # dbug(type(input_table))
    # dbug(input_table)
    columns_size = [0] * len(input_table[0])
    last_row_len = len(input_table[0])
    for row in input_table:
        if len(row) < last_row_len:
            dbug("WARNING: Found inconsistent row lengths... returning")
            dbug(f"last_row_len: {last_row_len} this row len: {len(row)}")
            dbug(row)
            dbug(f"First row len: {len(input_table[0])}")
            return
        # dbug(len(row))
        # dbug(type(row))
        for j, column_element in enumerate(row):
            columns_size[j] = max(columns_size[j], len(str(column_element)))
    return columns_size


# ##################################
def get_elems(lines, delimiter=',', index=False, col_limit=20):
    # ##############################
    """
    Input:
        lines (as a list) and
        optionally a delimiter (default is a comma)
        optionally a  col_limit (size)
    Returns:
        an array: list of list (lol - lines of elements aka rows and columns)
    """
    # dbug(f"delimiter: {delimiter} lines: {lines}")
    # dbug(f"delimiter: {delimiter} col_limit: {col_limit}")
    my_array = []
    import pyparsing as pp
    for line in lines:
        if isinstance(line, list):
            dbug(f"seems ok line: {line}")
        else:
            dbug(f"problem? line: {line}")
        # dbug(f"delimiter: {delimiter} ... working on line: {line}")
        # elems = line.split(r',(?=")')
        if delimiter == ",":
            # dbug(f"Using pp.commaSeparatedList on line: {line}")
            elems = pp.commaSeparatedList.parseString(line).asList()
            # dbug(elems)
        else:
            if delimiter == '" "' or delimiter == "' '" or delimiter == " ":
                # dbug(f"splitting on delimiter: {delimiter}")
                # dbug(line)
                line = line.strip()
                # dbug(line)
                elems = line.split()
            else:
                elems = line.split(delimiter)
        # dbug(f"line: {line} elems: {elems}")
        elems = [e[:int(col_limit)] for e in elems]
        # dbug(len(elems))
        my_array.append(elems)
        # dbug("exiting",exit=True)
    if index:
        for n, row in enumerate(my_array):
            # dbug(f"n: {n}")
            row.insert(0, str(n))
    # dbug(f"len(lines): {len(lines)} len(my_array): {len(my_array)} delimiter: {delimiter}\nmy_array: {my_array}")
    return my_array


def pyscraper(url, pat):
    """
    I may deprecate this as I rarely use it
    example: pat
    # pat = '<span class="Trsdu\(0.3s\) Fw\(b\) Fz\(36px\) Mb\(-4px\) D\(ib\)" data-reactid=".*?".*?>.*?</span.*?>'   # noqa:
    Be careful... pay attention to the html page when using a script ... many sites detect the script and block real output
    Required:
        from urllib.request import urlopen
        import re
    """
    # dbug(type(url))
    html = ""
    if file_exists(url):
        # treat this as a file instead of an url
        html = cat_file(url)
    if isinstance(url, list):
        html = "".join(url)
    if isinstance(url, str):
        if html == "" and url.startswith("http"):
            for attempts in range(3):
                try:
                    page = urlopen(url)
                    html = page.read().decode("utf-8")
                    break
                except Exception as e:
                    dbug(f"Attempt: {attempts} ... Retrieving url: {url} failed Error: {e}")
    match_results = re.search(pat, html, re.IGNORECASE)
    if match_results is None:
        print()
        warn = f"\n\nUsing url: {url}\nNo matches found with pat: [{pat}]\n"
        dbug(warn)
        if askYN("Do you want to see the returned html content?", "y"):
            dbug(html)
        return None
    r = match_results.group()
    # now remove html tags
    r = re.sub("<.*?>", "", r)  # Remove HTML tags
    return r
    # ### def pyscraper(url, pat): ### #


# ############################################################
def try_to_get(driver, pat="", by_type="link", action="none"):
    # ########################################################
    """
    may deprecate this as I rarely use it
    This is for use with selenium
    requires:
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    """
    """--== debugging ==--"""
    dbug(funcname())
    """--== Process ==--"""
    # from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    # dbug(driver.title)
    time_to_wait = 10
    try:
        if by_type == "link":
            element = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located((By.LINK_TEXT, pat)))
            element.send_keys(Keys.RETURN)
            # do_nc(element)
        if by_type == "id":
            element = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located((By.ID, pat)))
        # if action == "click":
        #    element.send_keys(Keys.RETURN)
        # dbug(f"Looking by: {by_type} for pat: {pat}")
        return element
    except Exception as e:
        dbug(f"Failed to find pattern: {pat}")
        dbug(driver.title)
        driver.close()
        do_close(f"Failed... Error: {e}")
        # return False
    # ### EOB def try_to_get(driver, pat, by_type, action) ### #


# ######################
def purge(dir, pattern):
    # ##################
    """
    removes files and dirs that match the pattern given from the location=dir
    requires:
        import os
        import shutil
    Becareful with this!
    """
    for f in os.listdir(dir):
        if re.search(pattern, f):
            if os.path.isdir(os.path.join(dir, f)):
                # dbug(f" removing dir: {os.path.join(dir, f)} ")
                shutil.rmtree(os.path.join(dir, f))
            else:
                # dbug(f" removing: {os.path.join(dir, f)} ")
                os.remove(os.path.join(dir, f))


def has_alnum(string):
    """
    Is a string blank or all white space...
    isspace() does the samething
    """
    for char in string:
        if char.isalnum():
            return True
    return False


def retry(howmany, *exception_types, **kwargs):
    """
    there is a module called retrying that deserves more research and it provides a wrapper function called @retry()
    use: 
    @retry(5, MySQLdb.Error, timeout=0.5)
    def the_db_func():
        # [...]
        pass
    untested - unused - completely expimental
    the same as 
    for attempts in range(3):
        try:
            do_work()
            break
        except Exception as e:
            print(f"Attempts: {attempts}. We broke with error: {e}")
    """
    timeout = kwargs.get('timeout', 0.0)  # seconds
    try:
        import decorator
    except Exception as e:
        dbug(f"Failed to import decorator Error: {e}")
    @decorator.decorator
    def tryIt(func, *fargs, **fkwargs):
        for _ in range(howmany):
            try: 
                return func(*fargs, **fkwargs)
            except exception_types or Exception:
                if timeout is not None:
                    time.sleep(timeout)
    return tryIt


# ########################################################################
def get_html_tables(url="", *args, show=False, timeout=10, **kwargs):
    # ####################################################################
    """
    input: url, display (tables with tabulate), access defaults to selenium which is slow but gets by bot blocks to url request
    returns: list of panda dataframes
    requires:
        import pandas as pd
        from selenium import webdriver
        # from fake_useragent import UserAgent
    """
    # dbug(funcname())
    try:
        import pandas as pd
    except Exception as e:
        print(f"Needs pandas ... Error: {e}")
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    # options = webdriver.FirefoxOptions()
    # options.set_headless()
    # driver = webdriver.Firefox(executable_path="./bin/geckodriver", firefox_options=options)
    try:
        # driver = webdriver.Firefox(executable_path="./bin/geckodriver")
        driver = webdriver.Firefox()
        driver.get(url)
    except Exception as e:
        dbug("See: \nhttps://selenium-python.readthedocs.io/installation.html#drivers ... for drivers")
        dbug(f"Web driver failed on url: {url}... Error: {e}")
        dbug("We look for the geckodriver in your PATH")
        dbug("Note: install the browser (firefox) executable manually... not with snap")
        dbug(f"Get url: {url} failed.... Error: {e}")
        return
    content = driver.page_source
    """--== SEP_LINE ==--"""
    time.sleep(1)
    tables = pd.read_html(content)
    # here is what you can do with returned df tables
    if show:  # this is for debugging
        dbug(url)
        dbug(f"There are {len(tables)} tables")
        from tabulate import tabulate
        cnt = 0
        for table in tables:
            # dbug(type(table))
            dbug(f"Printing table: {cnt} of {len(tables)} tables from url: {url}")
            print(tabulate(table, headers='keys', tablefmt='psql', showindex=False))
            cnt += 1
    try:
        driver.close()
    except Exception as Error:
        dbug(Error)
    return tables
    # ### EOB def get_html_tables(url="", access="selenium", show=False): ### #


def get_html_tst():
    """
    Options
    start-maximized: Opens Chrome in maximize mode
    incognito: Opens Chrome in incognito mode
    headless: Opens Chrome in headless mode
    disable-extensions: Disables existing extensions on Chrome browser
    disable-popup-blocking: Disables pop-ups displayed on Chrome browser
    make-default-browser: Makes Chrome default browser
    version: Prints chrome browser version
    disable-infobars: Prevents Chrome from displaying the notification ‘Chrome is being controlled by automated software
    """
    url = "http://www.python.org"
    url = "http://google.com"
    # url = "http://olympus.realpython.org/profiles/poseidon"
    url = "https://finance.yahoo.com/quote/%5EDJI/"
    url = "https://ycharts.com/indicators/us_total_market_capitalization"
    """--== SEP_LINE ==--"""
    r = requests.get(url) 
    content = r.text
    status_code = r.status_code
    dbug(status_code)
    if status_code == 200:
        printit(content)
        """--== SEP_LINE ==--"""
        import pandas as pd
        tables = pd.read_html(content)
        dbug(tables)
    else:
        dbug(status_code, 'boxed', 'centered')
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    browser = webdriver.Firefox(executable_path="./bin/geckodriver")
    browser.get(url)
    print('Title: %s' % browser.title)
    browser.quit()



# #################################
def display_in_cols(lst, cols=0, reverse="", on="value"):
    # #############################
    """
    deprecated as gtable may take it's place
    input: takes a list or a dict and prints in order across cols
    options:
        order default for list is is as-is
        if it is a dict
            you can sort "on" default "value" or on "key"
            , or reverse=True or reverse=False
    returns: lines (sorted if dict)
    example:
    # >>> lst = [*range(1,20)]
    # >>> display_in_cols(lst)
    then print lines eg printit(lines)
    """
    # dbug(lst)
    # dbug(type(lst))
    if isinstance(lst, dict):
        from collections import OrderedDict
        my_lst = []
        # so this is a dict, lets change it to a list and continue on, but sort it first
        if on == "value":
            on = 1
        else:
            # sort based on key
            on = 0
        if reverse:
            my_sd = {k: v for k, v in sorted(lst.items(), key=lambda item: item[on], reverse=True)}
            # dbug(my_sd)
        if not reverse:
            # dbug(f"Sorting dict: {lst}")
            # my_sd = {k: v for k, v in sorted(lst.items(), key=lambda item: item[on], reverse=False)}
            my_sd = OrderedDict(sorted(lst.items(), key=lambda t: t[0]))
            # dbug(my_sd)
        if reverse == "":
            my_sd = lst
        # lst = []
        # dbug(my_sd)
        max_k = len(max(lst.keys(), key=len)) 
        vals = list(lst.values())
        vals = [str(elem) for elem in vals]
        max_v = len(max(vals, key=len))
        # dbug(f"max_k: {max_k} max_v: {max_v}")
        for k, v in my_sd.items():
            # dbug(f"k: {k} v: {v}")
            msg = f"[{k:<{max_k}}]: {v:>{max_v}} "
            my_lst.append(msg)
        lst = my_lst
        # dbug(my_lst)
    import math
    tot_num = len(lst)
    screen_cols = get_columns()
    # dbug(lst)
    if cols == 0 or cols == "":
        # dbug(max_len)
        max_elem_len = len(max(lst, key=len))
        # dbug(max_elem_len)
        if screen_cols > max_elem_len:
            cols = math.floor(screen_cols / max_elem_len)
        else:
            cols = max_elem_len
        # dbug(f"screen_cols: {screen_cols} cols: {cols} max_elem_len: {max_elem_len}")
        # cols -= 1
    # cols = int(cols)
    # dbug(cols,ask=True)
    col = 0
    rows_num = math.ceil(tot_num / cols)
    # dbug(tot_num)
    # dbug(rows_num,ask=True)
    # matrix_tot = cols * rows_num
    max_elem_len = len(max(lst, key=len))
    rows = []
    for num in range(0, tot_num):
        # dbug(f"Processing num: {num}")
        row = []
        this = 0
        col = 0
        # for col in range(cols):
        while col < cols:
            # dbug(f"Processing col: {col} tot cols: {cols} current col:{col}")
            this = num + (rows_num * col)
            col += 1
            if this >= tot_num:
                this_e = " " * max_elem_len
            else:
                elem = lst[this]
                if len(elem) > max_elem_len:
                    elem = elem[max_elem_len:]
                if len(elem) < max_elem_len:
                    elem = elem + " " * (max_elem_len - len(elem))
                this_e = elem
            row.append(this_e)
        # dbug(row,ask=True)
        rows.append(row)
        col += 1
        if len(rows) >= rows_num:
            break
    # dbug(rows)
    # print("-"*screen_cols)
    lines = []
    for r in rows:
        lines.append("".join(r))
    return lines
    # ### EOB def display_in_cols(lst, cols=0, reverse="", on="value"): ### #


# #######################
def shadowed(lines=[], style=4, color="grey"):
    # ###################
    """
    purpose: adds shadowing typically to a box
    requires:
    input: lines as a list
    output: lines as a list
    Use this to see all the styles:
        msg = "this is \nmy message"
        for n in range(0,5):
            printit(centered(shadowed(boxed(msg + f"\nstyle: {n}"),style=n)))
    """
    reset = sub_color('reset')
    if isinstance(lines, str):
        lines = lines.split('\n')
    styles = []
    # the terminal you use significantly influences this!
    # top_right, vertical, bottom_left, horizontal, bottom_right
    #            .... tr[0] ,      v[1],    bl[2] ,     h[3] ,      br[4]]
    styles.append([chr(9699), chr(9608), chr(9701), chr(9608), chr(9608)])
    styles.append([chr(9617), chr(9617), chr(9617), chr(9617), chr(9617)])
    styles.append([chr(9618), chr(9618), chr(9618), chr(9618), chr(9618)])
    styles.append([chr(9619), chr(9619), chr(9619), chr(9619), chr(9619)])
    styles.append([chr(9608), chr(9608), chr(9600), chr(9600), chr(9600)])
    styles.append([chr(9608), chr(9608), chr(9600), chr(9600), chr(9624)])
    #               
    shadow_chrs = []
    shadow_chrs = styles[style]
    new_lines = []
    cnt = 0
    color = sub_color(color)
    for line in lines:
        if cnt == 0:
            width = len(escape_ansi(line))
            line = line + " "  # add a space to help when centering
        if cnt == 1:
            line = line + color + shadow_chrs[0]
        if cnt > 1:
            line = line + color + shadow_chrs[1]
        new_lines.append(line)
        cnt += 1
    # now add bottom shadow line
    # new_lines.append(" " + color + shadow_chrs[2] + shadow_chrs[3] * (width - 2) + shadow_chrs[3] + reset)
    new_lines.append(" " + color + shadow_chrs[2] + shadow_chrs[3] * (width - 2) + shadow_chrs[4] + reset)
    return new_lines
    # ### EOB def shadowed(lines=[], style=4, color="grey"): ### #


# ###################################################################
def add_or_replace(filename, action, pattern, new_line, *args, backup=True, **kwargs):
    # ###############################################################
    """
    purpose: Adds or replaces a line in a file where pattern occurs
    required: filename, action: str [before|after|replace|either] ,pattern, new_line
    action: before|after|replace|either (either will replace if it is found or add if it is not)
    options: 
    -   backup: bool=True, 
    -   ask: bool=False, 
    -   centered: bool=False, 
    -   shadowed: bool=False
    pattern: needs to be unique regex?
    returns: "done" or None depending on use
    """
    # dbug(pattern)
    # dbug(new_line)
    """--== Config ==--"""
    ask = bool_val('ask', args, kwargs, dflt=False)
    shadow_b = bool_val('shadowed', args, kwargs, dflt=False)
    center_b = bool_val('centered', args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print', 'show', 'verify', 'verbose'], args, kwargs, dflt=False)
    """--== Init ==--"""
    linenum = 0
    cnt = 0
    pattern_found = False
    """--== Process ==--"""
    import shutil
    if backup:
        try:
            shutil.copy(filename, f"{filename}.bak")
            printit(centered(f"Copied [{filename}] to {filename}.bak"))
        except Exception as e:
            dbug(f"Something went wrong? Error: {e}")
            return
    """--== Replace ==--"""
    # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
    if action == 'replace' or action == 'either':
        reading_file = open(filename, "r")
        # dbug(reading_file)
        new_file_content = ""
        for line in reading_file:
            cnt += 1
            # stripped_line = line.rstrip()
            # dbug(f"Chkg pattern: [{pattern}] if in line: {line}")
            regex = re.search(pattern, line)
            # if pattern in line:
            if regex:
                linenum = cnt
                o_line = line
                if o_line.endswith("\n"):
                    n_line = new_line + "\n"
                else:
                    n_line = new_line
                pattern_found = True
                # dbug(f"Replacing line: {line} with {new_line} in new_file_content...")
                # dbug(f"Found pattern: {pattern} in line: {line}", 'ask')
            else:
                n_line = line
            new_file_content += n_line
        reading_file.close()
        # dbug(new_file_content)
        if not pattern_found and action == 'replace':
            dbug(f"Pattern: {pattern} was not found, action: [{action}]... file not changed")
            return False
        if pattern_found:
            lines = [f"Replace: {o_line}", f"New    : {new_line}"]
            if prnt:
                printit(lines, 'boxed', title=f"Action: {action}. Proposed replace/new content ", centered=center_b, shadowed=shadow_b, footer=dbug('here'))
        if ask:
            if askYN(centered(f"Shall we change [{action}] to the new content? ", "y")):
                writing_file = open(filename, "w")
                writing_file.write(new_file_content)
                writing_file.close()
                # dbug(center_b)
                printit(f"Linenum: {linenum} line: {line} was replaced in {filename}", centered=center_b)
                # WIP TODO need to inform user here
                # dbug()
                return "done"
            else:
                return None
        """--== SEP_LINE ==--"""
        if linenum == 0:
            linenum = len(new_file_content)
        if pattern_found:
            writing_file = open(filename, "w")
            writing_file.write(new_file_content)
            writing_file.close()
            # dbug(center_b)
            if prnt:
                printit(f"Linenum: {linenum} line: {o_line} was replaced in {filename} in file: {filename}", 'boxed', centered=center_b, footer=dbug('here'), center_txt=99)
            return "done"
    """--== Add ==--"""
    if not pattern_found and action in ('both', 'either', 'addreplace', 'replaceadd', 'replaceoradd'):
        # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
        n_line = new_line.rstrip("\n")
        # dbug(f"Pattern: [{pattern}] not found. Adding n_line: {n_line}")
        new_file_content = cat_file(filename, rtrn='str')
        lines = [f"Add: {n_line}"]
        if prnt:
            printit(boxed(lines, title=f"Action: {action}. Proposed add/new content "), centered=center_b, shadowed=shadow_b, footer=dbug('here'))
        # dbug(filename)
        # dbug(new_file_content)
        # dbug(type(new_file_content))
        if isinstance(new_file_content, list):
            dbug(len(new_file_content))
            if len(new_file_content) == 1:
                new_file_content = "\n".join(new_file_content)[0]
        if new_file_content.endswith("\n"):
            new_file_content += n_line + "\n"
        else:
            new_file_content += "\n" + n_line
        linenum = " [linenum: end of file ] "
        if ask:
            if askYN(centered(f"Shall we change [action: {action}] to the new content? ", "y")):
                writing_file = open(filename, "w")
                writing_file.write(new_file_content)
                writing_file.close()
                printit(f"Line: {linenum} was added in {filename}")
                return "done"
            else:
                dbug("Returning... nothing done...")
                return None
        else:
            # just do it then
            writing_file = open(filename, "w")
            writing_file.write(new_file_content)
            writing_file.close()
            if prnt:
                printit(f"Line: {line} {linenum} was added to {filename}", 'centered')
            return "done"
    # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
    # assuming this is action == 'add'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    # dbug(filename)
    for line in contents:
        # dbug(line)
        cnt += 1
        # dbug(pattern)
        if pattern.startswith("^"):
            # dbug(pattern)
            pattern = pattern[1:]
            # dbug(pattern)
            if line.startswith(pattern):
                pattern_found = True
                break
        else:
            if pattern in line:
                # old_line = line
                pattern_found = True
                break
    # dbug(type(contents))
    # dbug(f"patter: {pattern} action: {action} cnt: {cnt}")
    # dbug(pattern_found)
    """--== Before ==--"""
    if action == 'before':
        # dbug(f"Adding new_line before cnt: {cnt}")
        contents.insert(cnt - 1, new_line + "\n")
        # new_content = new_line + '\n' + old_line
    """--== After ==--"""
    if action == 'after':
        # dbug(f"Adding new_line after cnt: {cnt}")
        contents.insert(cnt, new_line + "\n")
        # new_content = old_line + '\n' + new_line
    """--== Add to end of file ==--"""
    if action == "" or action == "add" or action == "end" or action == "either":
        # dbug(f"Adding new_line at end of file: {cnt}")
        if isinstance(contents, list):
            if contents[-1].endswith("\n"):
                contents.append(new_line)
            else:
                contents.append("\n" + new_line)
    contents = "".join(contents)
    # printit(boxed(new_content, title=" Proposed new/replacement content "), 'center', 'shadow')
    if ask:
        if askYN(printit(f"Pattern: [{pattern}] found: [{pattern_found}]. Shall we change [action: {action}] to the new content?: ", "y", 'str', 'centered', prnt=False)):
            f = open(filename, "w")
            f.write(contents)
            f.close()
            # dbug(f"Done ... action: {action}", 'ask')
            # dbug(contents)
            return "done"
    else:
        # just do it then
        f = open(filename, "w")
        f.write(contents)
        f.close()
        # dbug(f"Done ... action: {action}", 'ask')
        # dbug(contents)
        return "done"
    return None
    # ### def add_or_replace(filename, action, pattern, new_line, backup=True): ### #


# ###############################################
def regex_col(file_lines, pat="", col=7, sep=""):
    # ###########################################
    """
    regex for a patern in a word|column
    file_lines can be a filename or lines (list)
    col starts at 0 to be consistent with coding standards
    returns lines where pat matches col number word ie words[col]
    """
    if isinstance(file_lines, list):
        lines = file_lines
    else:
        # assume it is a filename
        with open(file_lines) as f:
            lines = f.readlines()
    ret_lines = []
    # ### for testing ### #
    # import datetime
    # from dateutil import relativedelta
    # yr = datetime.datetime.now().strftime("%y")
    # nextmonth = datetime.datetime.now() + relativedelta.relativedelta(months=1)
    # mon = nextmonth.strftime("%b").lower()
    # pat = yr + mon
    # dbug(pat)
    # lines = [f"one line here with many words {pat} in it", f"another;line;there;with;many;words;{pat};in;it"]
    # sep = ";"
    # ### #
    for line in lines:
        # dbug(f"chkg line: {line}")
        if sep != "":
            words = line.split(sep)
            dbug(words)
        else:
            words = line.split()
        if len(words) > col:
            if re.search(pat, words[col]):
                ret_lines.append(line)
    # printit(ret_lines)
    return ret_lines
    # ### EOB def regx_col(pat="",col=7,sep=""): ### #
    

def v4k(my_d, k):
    """
    purpose: return a value form a dictionary (my_d) for a given key (k)
    return value for key in dict ie v for my_d[k]
    returns None is not found
    """
    # if k in my_d:
    if my_d.has_key(k):
        v = my_d[k]
    else:
        v = None
    dbug(v)
    return v


# #####################
def rootname(filename, *args, **kwargs):
    # #################
    """
    purpose: returns the root name of a full filename (not path, no extension)
    input: filename: str
    returns: ROOT_NAME: str
    >>> print(rootname(__file__))
    gtools3
    """
    dir = bool_val(['dir'], args, kwargs, dflt=False)
    base = bool_val(['base', 'basename'], args, kwargs, dflt=False)
    REALNAME = os.path.realpath(filename)
    #dbug(REALNAME)
    if dir:
        DIRNAME = os.path.dirname(REALNAME)
        return DIRNAME
    if base:
        BASENAME = os.path.basename(REALNAME)
        return BASENAME
    else:
        BASENAME = os.path.basename(REALNAME)
        ROOTNAME = os.path.splitext(BASENAME)[0]
        return ROOTNAME
        

# def mod_info():
#    pat = r"def .*[\(?].*[\)?]:"
#    # r = re.search(pat, )
#    dir(__file__)
#    dbug("------------")
#    help(__file__)


# ############## 
def maxof(my_l):
    # ##########
    """
    purpose: returns length of longest member of a list (escape_ansi)
    saves me from having to look up how to do this all the time
    """
    #max_len = len(max(escape_ansi(my_l), key=len))
    # or
    max_len = max(nclen(elem) for elem in my_l)
    return max_len


# #################################
def allmax(msgs_l, justify='left'):
    # #############################
    """
    purpose: justifies using nclen all strs in msgs_l and maximizes each string length to the longest string
    input: msg_l: list, justify: str ('left'|'center'|'right')
    output: new_msgs: list of strngs justified
    """
    max_len = maxof(msgs_l)
    new_msgs = []
    for msg in msgs_l:
        diff = max_len - nclen(msg)
        pad = " " * diff
        if justify == 'left':
            # dbug(msg)
            msg = msg + pad
        if justify == 'center':
            pad = " " * (diff // 2)
            msg = pad + msg + pad
        if justify == 'right':
            pad = pad + msg
        new_msgs.append(msg)
    return new_msgs


# #####################################################
def find_file_in_dirs(filename, dirs_l=[], prnt=False):
    # #################################################
    """
    purpose: this is for future use as something like find_file_in_dirs(filename, dirs_l)
    if dirs_l is empty it defaults to ["./"]
    """
    found_file = ""
    # script_basename = Path(__file__).stem
    # cfg_file = os.path.splitext(__file__)[0]
    # cfg_file += ".cfg"
    # from pathlib import Path
    # home = str(Path.home())
    # poss_dirs = [home, home + "/dev/dotfiles"]
    if dirs_l == []:
        dirs_l = ["./", os.path.dirname(__file__)]
    poss_dirs = dirs_l
    # dbug(poss_dirs)
    for dir in poss_dirs:
        # dbug(dir)
        if dir.endswith("/"):
            tst_for_file = dir + filename
        else:
            tst_for_file = dir + "/" + filename
        # dbug(f"Looking for: {tst_for_file}", "ask")
        if os.path.isfile(tst_for_file):
            found_file = tst_for_file 
            if prnt:
                printit(f"Found file: {found_file} ...", "center")
            break
    return found_file
    # ### EOB def find_file_in_dirs(filename, dirs_l=[], prnt=False): ### #


        
def long_proc(msg="testing long process"):
    # dbug(funcname())
    # dbug(msg)
    # with Spinner():
    #     time.sleep(2)
    time.sleep(2)
    return msg
    #dbug(f"Finished with {funcname()}")


# ###########################################
def usr_update(my_d, fix_l=[], *args, **kwargs):
    # #######################################
    """
    purpose: given a dict, and a list of keys to change - allow user update(s) to values in  my_d dictionary
        go through the list of keys to fix and prompt user for new value, present the current value as default
    args: my_d: dict    # dict to have updated
          fix_l=[]: list   # list of keys to prompt user for change; if empty use all the my_d keys
    returns: my_d (with user updates)
    NOTE: what is in the passed dict values is what will be presented as the default.
    """
    # dbug(funcname())
    """--== Config ==--"""
    max_size = kvarg_val(["max", " max_size"], kwargs, dflt=40)
    """--== Process ==--"""
    if len(fix_l) == 0:
        fix_l = list(my_d.keys())
    # dbug(fix_l)
    fix_d = {}
    max_k = 0
    max_v = 0
    for k in fix_l:
        # put in values from supplied my_d
        fix_d[k] = my_d[k] 
        if nclen(k) > max_k:
            max_k = nclen(k)
        if nclen(my_d[k]) > max_v:
            max_v = nclen(my_d[k])
    new_d = {}
    for k, v in fix_d.items():
        ans = cinput(f"Please enter new [{k:<{max_k}}] default: [{v:>{max_v}}]: ") or v
        ans = str(ans)
        if ans.lower() == "q":
            # do_close(center=True, box_color="red on black")
            break
        new_d[k] = ans
    for k, v in new_d.items():
        my_d[k] = v
    return my_d
    # ### EOB def usr_update(my_d, fix_l, *args, **kwargs): ### #


# #############################################
def remap_keys(my_d, remap_d, *args, **kwargs):
    # #########################################
    """
    purpose: remaps keys names AND can select only the k.v pairs you want (ie option: 'mapped_only')
    options: 
        mapped_only: bool, 
        rnd: int # rounds out numbers to rnd scale
    returns: my_d (remapped and optionally selected pairs)
    notes: remap_d should be dict {orig_key: new_key, ...} but can be a list only (assumes and sets mapped_only=True)
    created: 20220423 gwm
    """
    # dbug(funcname())
    """--== Config ==--"""
    mapped_only_b = bool_val(["mapped_only","mapped"], args, kwargs, dflt=True)
    rnd = kvarg_val("rnd", kwargs, dflt=0)
    # my_d = {'oldname1': 'data1', 'oldname2': 'data2', 'goodname3': 'data3'}
    # gtable(my_d, 'prnt', title=dbug('here'))
    # gtable(remap_d, 'prnt', title=dbug('here'))
    # remap_d = {'oldname1': 'key_1', 'oldname2': 'key_2'}
    # dbug(remap_d)
    # my_d = dict((remap_d[key], my_d[key]) if key in remap_d else (key, value) for key, value in my_d.items())
    new_d = {}
    if isinstance(remap_d, list):
        for elem in remap_d:
            new_d[elem] = elem
        remap_d = new_d
        mapped_only_b = True
    new_d = {}
    # for k, v in remap_d.items():
    for orig_key, new_key in remap_d.items():
        for my_d_key in my_d.keys():
            if orig_key == my_d_key:
                val = my_d[orig_key]
                if val is not None and isnumber(val) and rnd > 0:
                    # dbug(f"rnd: {rnd} val: {val} ")
                    val = round(val, rnd)
                new_d[new_key] = val
            else:
                if not mapped_only_b:
                    new_d[orig_key] = my_d[orig_key]
        #try:
        #    tst = new_d[new_key]
        #except:
        #    # I do not like this ... there should be a better solution 
        if new_key not in new_d:
            new_d[new_key] = f"None"
    return new_d
    # ### EOB def remap_keys(my_d, remap_d, *args, **kwargs): ### #


# ####################################
def quick_plot(data, *args, **kwargs):
    # ################################
    """
    purpose: quick display of data in  a file or in dataframe
        displays a plot on a web browser if requested
    args: data: df | str(filename: csv or dat)
    options: show: bool, choose: bool, footer: str, footer: str tail: int (for the last n rows of the df)
        choose invokes gselect multi mode to allow selections of columns to display in the plot (graph)
        tail, title and footer only affect the gtable if show is True
        - dat: bool | str      # I sometimes use a commented firstline for headers - 
                               # using 'dat' declares this to be true, if character is used ie dat=":" 
                               # then that will be used as the delimiter
    returns: df
    NOTE: if a filename is used as data it will get "purified" by removing all comments first (except the first line of a dat file.)
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(data)
    # dbug(f"type(data): {type(data)}")
    # dbug(args)
    # dbug(kwargs)
    """--== Imports ==--"""
    import matplotlib.pyplot as plt
    import plotly.express as px
    import pandas as pd
    """--== debug ==--"""
    # dbug(funcname())
    """--== Config ==--"""
    show = bool_val(["prnt", "print", "show"], args, kwargs, dflt=False)
    choose = bool_val(["choose", "multi"], args, kwargs, dflt=False)
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("footer", kwargs, dflt="")
    tail = kvarg_val("tail", kwargs, dflt=35)
    centered = bool_val(["centered", "center"], args, kwargs, dflt=True)
    web_b = bool_val(['web', 'browser'], args, kwargs, dflt=False)
    colnames = kvarg_val(['colnames', 'col_names', 'columns'], kwargs, dflt=[])
    kind = kvarg_val(['kind', 'type', 'style'], kwargs, dflt='line')  # line, bar, barh, hist, box, kde, density, area, pie, scatter, hexbin
    dat = kvarg_val(["dat"], kwargs, dflt=False)
    dat = bool_val(["dat"], args, kwargs, dflt=dat)  # this needs to be here in combination w/above
    # dbug(colnames)
    """--== Convert to df ==--"""
    if isinstance(data, pd.DataFrame):
        df = data
        src = "df"
    if isinstance(data, str):
        # this is probably a path-filename
        if file_exists(data):
            # assumes it is a csv file
            # df = pd.read_csv(data, thousands=',', comment="#", header=0, on_bad_lines='warn', engine='python', infer_datetime_format=True)
            # dbug(dat)
            df = cat_file(data, 'df', 'hdr', dat=dat)
            # dbug(df)
            src = f"File: {data}"
    if isinstance(data, dict):
        df = pd.DataFrame.from_dict(data)
        src = "df"
    if isinstance(data, list):
        # dbug(data)
        if isinstance(data[0], list):
            if len(data[0]) == 1:
                # this is a lol so... 
                data = [[n, elem] for n, elem in enumerate(data)]
                # dbug(data)
            df = pd.DataFrame(data)
            # dbug(f"df): {df}")
        else:
            # dbug(data)
            new_data_lol = []
            for n, item in enumerate(data):
                new_data_lol.append([n, item])
            data = new_data_lol
            # dbug(data)
            df = pd.DataFrame(data)
        src = "df"
    # dbug(df)
    if show:
        footer += f" Source: {src} "
        # dbug(type(df))
        # dbug(df)
        gtable(df.tail(int(tail)), 'hdr', 'centered', 'prnt', title=title, footer=footer, centered=centered)
    if colnames != []:
        # dbug(colnames)
        if len(colnames) != len(df.columns):
            dbug(f"Check the number of supplied colnames, should be {len(df.columns)}")
            colnames = df.columns.to_list()
        else:
            df.columns = colnames
    colnames = df.columns.to_list()
    # dbug(type(colnames))
    # dbug(colnames)
    # choices_l = colnames[1:].tolist()
    choices_l = colnames[1:]
    if choose:
        selections_l = gselect(choices_l, centered=centered, width=140, title=title, prompt="Add the desired column", quit=True, multi=True)
        # dbug(selections_l)
    else:
        selections_l = choices_l
    if selections_l == []:
        selections_l = df.columns.to_list()
    # dbug(f"colnames: {colnames}")
    # dbug(type(df))
    # dbug(df)
    # dbug(df.dtypes)
    # dbug(df.info)
    if web_b:
        """--== for browser display ==--"""
        fig = px.line(df, x=colnames[0], y=selections_l, title=title)
        fig.show()
    else:
        if "date" in str(colnames[0]).lower() or "time" in str(colnames[0]).lower():
            my_df = df.set_index(colnames[0])
        # else:
            # dbug(colnames[0])
        for col in colnames[1:]:
            my_df[col] = my_df[col].astype(float)
        # dbug(footer)
        # if footer != "":
        # dbug(colnames)
        # dbug(selections_l)
        # dbug(df)
        ax = my_df.plot(figsize=(15, 5), kind=kind, xlabel=colnames[0] + "\n" + footer, y=selections_l, title=title)
        ax.plot()
        plt.show()
    # dbug(f"Returning df: {df}")
    return df
    # ### EOB def quick_plot(data, *args, **kwargs): ### #


def quick_plot_demo():
    import random
    lst_len = 2000
    sums = []
    for i in range(0, lst_len):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        sum = die1 + die2
        sums.append(sum)
        # dbug(f"roll: {i} die1: {die1} + die2: {die2} = {sum}")
    from collections import Counter
    import pandas as pd
    import matplotlib.pyplot as plt
    quick_plot(sums, 'show', colnames=["item", "data"], title="Demo of Sum (2) dice Plot", footer=dbug('here'))
    data = Counter(sums)
    df = pd.pandas.DataFrame.from_dict(data, orient='index')
    df.columns = ["Sums"]
    df = df.sort_index()
    kinds = ['line', 'bar', 'barh', 'area']
    for kind in kinds:
        quick_plot(df, 'show', kind=kind, colnames=["Sum"], title=f"Demo of Frequency of Sum (2) dice kind: {kind}", footer=f"kind: {kind} {dbug('here')}")
    

def boxed_demo():
    """
    purpose: demo of using boxed()
    """
    do_logo(box_color="yellow! on black", color="black on white")
    print()
    do_logo("Your Organization", 'figlet', box_color="red! on black", color="yellow! on rgb(90,90,90)", fortune=True, quote="~/data/lines.dat")
    print()
    msg = "This is box1"
    color = "blue! on white"
    box_color = "red! on yellow!"
    msg += " " + dbug('here')
    box1 = boxed(msg, 'prnt', color=color, box_color=box_color, title="box1", footer=dbug('here'))
    print()
    box2 = boxed(msg, 'prnt', 'shadowed', color=color, box_color=box_color, title="box1 shadowed", footer=dbug('here'))
    gcolumnize([box1, box2], 'prnt', 'centered', 'shadowed', title="Box unshadowed and Box shadowed", footer=dbug('here'))
    print()
    quote = get_random_line("~/data/lines.dat")
    color = "yellow! on rgb(50,50,90)"
    box_color = "red! on black!"
    title = clr_coded("[white! on black!] Quote  Box[/] ")
    q_box = printit(quote, 'boxed', title=title, prnt=False, shadow=True, box_color=box_color, color=color)
    printit(q_box, 'centered')
    ans = cinput("How many boxes would like printed on a single row: ")
    boxes = []
    for n, box in enumerate(range(int(ans)), 1):
        boxes.append(boxed(f"This is\nBox {n}"))
    printit(gcolumnize(boxes), 'centered')


def gtable_demo():
    """--== SEP_LINE ==--"""
    tst_d = {"simple": "table", "goes": "here", "line three": "this is a very very long exstensive and verbose line or string", "line four": "If you thought that last line was long it was only because you had not come across this very long, exstensively verbose, long line."}
    gtable(tst_d, 'prnt', 'centered', title="tst_d dict no wrap defaut col_limit=60", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', title="tst_d dict no wrap col_limit=140", col_limit=140, footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap and col_limit=30", footer=dbug('here'), col_limit=30)
    dbug('ask', 'centered')
    printit("Now run gtable with: tst_d dict w/hdr & end_hdr, wrap, alt, index and clolimit=30", 'centered')
    box1 = gtable(tst_d, 'header', 'wrap', title="Short title w/wrap", footer=dbug('here'), end_hdr=True, col_limit=30)
    box2 = gtable(tst_d, 'header', 'index', 'alt', 'wrap', title="Short title w/wrap, alt, and w/index", footer=dbug('here'), end_hdr=True, col_limit=30)
    gcolumnize([box1, box2], 'prnt', 'centered', 'boxed', title="Two gtables boxed and centered", box_color="yellow! on black", footer=dbug('here'))
    dbug('ask', 'centered')
    """--== SEP_LINE ==--"""
    my_lol = [["name", "value", "make", "model"], ["two", "2", "foo", "bar"], ["twenty_two", "22", "bing", "bang"], 
            ["one", "1", "boom", "bam"], ["five", "5", "tik", "tok"], ["three", "3", "string", "strum"], ["four", "4", "ping", "pong"]]
    title = "with hdr and alt"
    gtable(my_lol, 'prnt', 'centered', 'hdr', 'alt', alt_clr="rgb(50,50,50)", title=title, footer=dbug('here'))
    """--== SEP_LINE ==--"""
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": "col5 with a very very long winded line that has man many chacters in it. Do not be alarmed by it's length", "col6": ["This is six", "another line"], "col7": 7} 
    colnames = ["col1", "col2", "col3", "col4", "col5", "col6"]
    gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/colnames and now with header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    title = "with hdr and sortby=1"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortby=1, title=title, footer=dbug('here'))
    dbug('ask')
    title = "with hdr and sortby=value"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortby="value", title=title, footer=dbug('here'))
    title = "with hdr and sortby_n=value"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", title=title, footer=dbug('here'))
    dbug('ask')
    title = "with hdr and sortby_n=value filterby value: 2"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", filterby={'value': '2'}, title=title, footer=dbug('here'))
    title = "with hdr and sortby_n=value filterby value: 2 select_cols=[name, value, make]"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", filterby={'value': '2'}, select=['name', 'value', 'make'], title=title, footer=dbug('here'))
    dbug('ask')
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'end_hdr', sortbyn="value", filterby={'value': '2'}, select=['name', 'value', 'make'], title=title, footer="with end_hdr" + dbug('here'))

    """--== SEP_LINE ==--"""
    printit(gtable.__doc__, 'boxed', 'centered', title=" gtable() doc ", footer=dbug('here'), box_color="yellow! on black!")
    askYN("Continue: ", 'centered')
    csv_lines = """
    sym,lpr,chg,pchg,trgt,ask,iv,pom,cp,date,blks,pc,pp,sr,pe,fpe,div,roe,rl,rh,fv,mv,peg,shrs,acnt,misc,misc2,status,score,rng_pcnt,avg,mcap,ps,pb,cps,cr,dr,beta,eps,div5yr,pinst,pinsdr,ma200,ma50,notes,rundate
AVGO,  520.86,  -29.27,  -5.32,  450.0,  70,  31.0,  95,  535.48,  20220730,  1,  P,  __,  A+,  25,  12,  15.9,  39,  463,  678,  302,  624,  1.09,  xxx,  1510,  ,  ,  ,  80.0,  26.91,  76.5,  210936823808,  7.03,  10,  22.3,  2,  188.02,  1.1,  20.19,  2.96,  82.11,  2.35,  570.38,  517.43,  *t,  20220827
ALSN,  37.14,  -1.24,  -3.23,  30.0,  045,  50.0,  82,  35.30,  20220412,  2,  P,  __,  C_,  08,  06,  0.8,  62,  32,  42,  69,  ___,  0.55,  xxx,  1510,  ,  ,  ,  60.0,  51.4,  54.0,  3574528256,  1.4,  5,  1.28,  2,  336.98,  0.92,  4.62,  1.62,  102.23,  0.84,  38.2,  38.49,  *t,  20220827
AMAT,  98.80,  -6.2,  -5.9,  85.0,  60,  47.0,  87,  98.80,  20220828,  1,  P,  __,  B+,  13,  12,  1,  55,  82,  168,  112,  142,  1.1,  xxx,  1510,  22sep85in@60,  , ofrd22sep_P:NO,  80.0,  19.53,  80.0,  85950767104,  3.42,  7,  4.11,  2,  45.2,  1.51,  7.47,  1.18,  78.48,  0.35,  124.2,  99.13,  ,  20220828
BABA,  98.00,  -1.89,  -1.89,  75.0,  129,  73.0,  80,  89.37,  20220730,  1,  P,  ___,  _+,  45,  11,  0,  02,  73,  183,  32,  100,  316.17,  xxx,  1510,  audit_probs_SEC,  ,  ,  30.0,  22.73,  53.5,  260032233472,  0.3,  0,  174.82,  2,  16.91,  0.58,  2.16,  None,  16.44,  0.01,  109.8,  102.31,  *t,  20220827
BAC,  34.03,  -1.11,  -3.16,  28.0,  11,  35.0,  92,  33.05,  20220727,  1,  P,  __,  C+,  10,  09,  0.84,  10,  29,  51,  48,  41,  1.58,  xxx,  1510,  ,  ,  ,  60.0,  22.86,  68.5,  273439211520,  2.99,  1,  88.88,  0.0,  0.0,  1.4,  3.2,  2,  70.88,  0.12,  39.99,  33.29,  *t,  20220827
    """
    csv_l = csv_lines.split("\n")
    csv_l = [line for line in csv_l if line != '' and not line.isspace()]  # get rid of empty lines
    csv_lol = []
    for row in csv_l:
        elems = row.split(",")
        elems = [str(elem).strip() for elem in elems] 
        csv_lol.append(elems)
    selected = csv_lol[0][:20]
    selected.append('div5yr')
    gtable(csv_lol, 'hdr', 'prnt', 'centered', 'alt', title="Selected data from a csv file and selected columns w/alt", footer="alt_color: default " + dbug('here'), selected=selected)
    print()
    gtable(csv_lol, 'hdr', 'prnt', 'centered', 'alt', alt_color="on rgb(60,60,100)", pad='', title="Selected columns, alt and w/o padding", footer="alt_color: 'on rgb(60,60,100)' " + dbug('here'), selected=selected)
    print()
    gtable(csv_lol, 'prnt', 'hdr', 'centered', pad='', col_colors=[], title="Selected columns and w/o padding no column_colors", footer=dbug('here'), selected=selected)
    dbug('ask')
    """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000, "col 7": "    this has lots of white space    "}
    gtable(my_d, 'prnt', 'centered', title="Simple Dictionary", footer=dbug('here'))
    print()
    box1 = gtable(my_d, 'prnt', 'centered', 'strip', pad='', title="cell_pad=''")
    dbug('ask')
    box2 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    print()
    box3 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header colnames=keys", footer=dbug('here'), colnames="keys")
    print()
    gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header colnames=keys exclude=['three']", exclude=['three'], footer=dbug('here'), colnames="keys")
    print()
    gtable(my_d, 'prnt', title="Simple Dictionary colnames=keys", footer=dbug('here'), colnames="keys")
    print()
    printit(gcolumnize([box1, box2]), 'boxed', box_color="red! on black", title="Two Boxes", footer=dbug('here'))
    print()
    printit(gcolumnize([box1, box2]), 'boxed', 'centered', box_color="red! on black", title="Two Boxes centered", footer=dbug('here'))
    dbug('ask')
    """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000, "col 7": "    this has lots of white space    "}
    colnames = ["column one", "column two", "column three", "column four", "column five", "column six", "column seven"]
    box1 = gtable(my_d, 'prnt', title="Simple Dictionary", footer=dbug('here'))
    print()
    box2 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    print()
    printit(gcolumnize([box1, box2]), 'centered')
    print()
    dbug('ask')
    box3 = gtable(my_d, 'prnt', title="Simple Dictionary", footer=dbug('here'))
    box4 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    box5 = gtable(my_d, 'prnt', title="Simple Dictionary w/colnames='keys'", footer=dbug('here'), colnames="keys")
    box6 = gtable(my_d, 'prnt', title="Simple Dictionary w/colnames", footer=dbug('here'), colnames=colnames)
    dbug("GOing to box7...", 'ask')
    dbug(my_d)
    box7 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/colnames w/header", footer=dbug('here'), colnames=colnames)
    dbug("Stop",'ask', 'boxed', box_color="red! on rgb(80,30,80)")
    print()
    printit(gcolumnize([box1, box2]) + box3, 'centered', 'boxed', title="Two boxes in one row and another box in the next", footer=dbug('here'))
    print()
    gtable(my_d, 'prnt', 'centered', 'hdr', title="Simple dictionary w/header", footer=dbug('here'))
    dbug('ask', 'centered')
    my_l = list(my_d.values())
    my_l.append(12345)
    my_l.append(123.45)
    # dbug(my_l)
    colnames = ["column one", "column two", "column three", "column four", "column five", "column six", "big column", "Integer", "Float"]
    # dbug(colnames)
    # dbug(my_l)
    gtable(my_l, 'prnt', 'centered', title="Simple list of values", footer=dbug('here'))
    print()
    gtable(my_l, 'prnt', 'centered', 'hdr', title="Simple list of values w/header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    colnames = []
    for x in range(len(my_l)):
        colnames.append(x)
    # dbug(colnames)
    # dbug(my_l)
    gtable(my_l, 'prnt', 'centered', 'hdr', title="Simple list of values w/header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    # dbug(list(my_d.values()))
    dbug('ask', 'centered')
    """--== SEP_LINE ==--"""
    my_lol = [
            ["col1", "col2", "col3", "col4", "col5", "col6", "col7"],
            [1, 2, 3,4 , 5, 6, 7],
            ["11", "22", "33", "44", "55", "66", "77"],
            ["111", "222", "333", "444", "555", "666", "777"],
            ["1111", "2222", "3333", "4444", "5555", "6666", "7777"]
            ]
    gtable(my_lol, title="Simple list of lists (lol)", footer=dbug('here'))
    print()
    gtable(my_lol, 'prnt', 'hdr', title="Simple list of lists (lol) w/header", footer=dbug('here'))
    selected_cols = ["col2", "col4", "col6"]
    printit(f"Simple list of lists (lol) w/header & selected_cols: {selected_cols}")
    gtable(my_lol, 'prnt', 'hdr', selected_cols=selected_cols)
    dbug('ask', 'centered')
    """--== SEP_LINE ==--"""
    tst_d = {"simple": "table", "goes": "here", "line three": "this is a very very long exstensive and verbose line or string", "line four": "If you thought that last line was long it was only becuse you had not come across this very long, exstensively verbose, long line."}
    gtable(tst_d, 'prnt', 'centered', title="tst_d dict no wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap and col_limit=30", footer=dbug('here'), col_limit=30)
    printit("Now run gtable with: tst_d dict w/hdr & end_hdr, wrap, alt, index and clolimit=30")
    gtable(tst_d, 'prnt', 'header', 'index', 'alt', 'wrap', alt_color='on rgb(25,25,25)', title="Short title", footer=dbug('here'), end_hdr=True, col_limit=30)
    print()
    dbug('ask', 'centered')
    """--== SEP_LINE ==--"""
    tst_d = {"first": ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line '], "one": 1, "two": [2, 2], "three": 3, "four": ['pupose: re-writes a file with an added line (after or before a pattern) or   replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line ']}
    gtable(tst_d, 'prnt', 'centered' 'wrap', footer=dbug('here'))
    tst_d = {'add_content': ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I a  m constantly building csv files with a header line '], "next": 4}
    gtable(tst_d, 'prnt', 'wrap', 'centered')
    dbug('ask', 'centered')
    """--== SEP_LINE ==--"""
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": 5, "col6": [6, "This is six", "another line"]} 
    gtable(my_d, "prnt", 'centered', title="testing", footer=dbug('here'))
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": "col5 with a very very long winded line that has man many chacters in it. Do not be alarmed by it's length", "col6": ["This is six", "another line"], "col7": 7} 
    gtable(my_d, "prnt", 'centered', 'wrap', title="testing", footer=dbug('here'))
    # dbug('ask')
    kv_cols(my_d, 2, 'prnt','centered',  title="kv_cols 2 columns", footer=dbug('here'))
    kv_cols(my_d, 2, 'prnt', 'centered', 'boxed', title="kv_cols 2 columns boxed ", footer=dbug('here'), mstr_box_color="blue! on white")
    dbug('ask')
    # nums = [1, 20, 40, 3, 33, 55, 11, "21"]
    # dbug(nums)
    # dbug(sorted(nums, key=lambda x: float(x)))
    """--== SEP_LINE ==--"""
    import pandas as pd
    my_df = pd.DataFrame(my_lol)
    # my_df.rename(columns=my_df.iloc[0]).drop(my_df.index[0])  # uses the first row as colnames and uses the rest of the rows for the df
    gtable(my_df, 'prnt', 'centered', 'end_hdr', colnames="firstrow", title="Using a df", footer="with end_hdr")
    my_d = {"col1": 1, "col2": 2, "col3": 3} 
    gtable(my_d, 'prnt', 'hdr', 'centered', 'shadowed', 'human', title=dbug('here'), footer="gtable demo", colnames=["Key", "Value"])
    dbug('ask')
    sym = "CVS"
    with Spinner(f"Working on getting info for Ticker: {sym} then gtable(sym.info...): ", 'elapsed', 'centered'):
        try:
            import yfinance as yf
            sym = yf.Ticker(sym)
            my_d = sym.info
            # dbug(my_d)
            # dbug(type(my_d))
            # dbug(len(my_d))
            # dbug(type(my_d[0]))
            print()
            gtable(my_d, 'prnt', 'centered', 'hdr', 'shadowed', title=dbug('here'), footer=" gtable demo ")
            # if r is None:
            #    dbug('ask')
        except Exception as Error:
            dbug(Error)
            dbug('ask')
    print()
    kv_cols(my_d, 2, 'prnt', 'centered', title="kv_cols(my_d)", footer=dbug('here'))
    dbug('ask')
    """--== SEP_LINE ==--"""
    my_lol = [["Asset", "type", "value", "age"],
            ["house", "cape cod", "120,000", "55yrs"],
            ["car", "CX5", 3000, 7], 
            ["Vermeer", "The Girl with a Pearl Earing", 30000000, 357],
            ["Magic Kit", "With case", 300.4657, 82],
            ["coin", "kugarand", "[1600]", 45]]
    """--== SEP_LINE ==--"""
    title = "  Need a very long, desparately long, and  wider than usaual title " + dbug('here')
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'human', title=title, footer=" gtable demo " + dbug('here'))
    """--== SEP_LINE ==--"""
    # dbug(f"Now run gtable for my_lol[0]: {my_lol}")
    gtable(my_lol[0], 'prnt', 'centered', title="keys only ", footer=dbug('here'))
    # dbug(my_lol[0])
    dbug('ask')
    """--== SEP_LINE ==--"""
    title = "list-of-lists"
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'human', rnd=2, title=title, footer=" gtable demo ")
    # gtable(my_lol, 'prnt', 'hdr', 'human', rnd=2,  title=title, footer=" gtable demo " + dbug{'here'})
    """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000}
    kv_cols(my_d, 2, 'prnt', 'centered', title="kv_cols(my_dictionary, cols=2)", footer=dbug('here'))
    kv_cols(my_d, 2, 'prnt', 'centered', 'boxed', box_color="red!", mstr_box_clr="yellow!", title="kv_cols(my_dictionary, cols=2) boxed", footer=dbug('here'))
    # ### EOB def gtable_demo(): ### #
    

# #############
def clr_demo():
    # #########
    """
    Color Demo 
    clr_demo doc 
    used for testing only
    """
    my_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'violet']
    for c in my_colors:
        colors = shades(c)
        with Spinner(f"Demo of shade({c}) ", 'centered', 'prog', 'elapsed', style='vbar', colors=colors):
            time.sleep(3)
    lines1 = []
    lines2 = []
    lines3 = []
    lines4 = []
    lines5 = []
    lines6 = []
    for shade in range(0, 255, 15):
        red_shade = f'rgb({shade}, 0, 0)'
        green_shade = f'rgb(0, {shade}, 0)'
        blue_shade = f'rgb(0, 0, {shade})'
        red_green_shade = f'rgb({shade}, {shade}, 0)'
        red_blue_shade = f'rgb({shade}, 0, {shade})'
        green_blue_shade = f'rgb(0, {shade}, {shade})'
        lines1.append("color: " + gclr(red_shade) + red_shade + RESET)
        lines2.append("color: " + gclr(green_shade) + green_shade + RESET)
        lines3.append("color: " + gclr(blue_shade) + blue_shade + RESET)
        lines4.append("color: " + gclr(red_green_shade) + red_green_shade + RESET)
        lines5.append("color: " + gclr(green_blue_shade) + green_blue_shade + RESET)
        lines6.append("color: " + gclr(red_blue_shade) + red_blue_shade + RESET)
    printit(gcolumnize([lines1, lines2, lines3, lines4, lines5, lines6]), 'boxed', 'centered', box_color="blue on rgb(150,150,200)")
    lines = []
    lines.append("Way to add color: ")
    lines.append("this is [yellow! on grey99]yellow! on grey99[/] done")
    # dbug(repr(msg))
    lines.append('gclr("yellow! on grey30")' + gclr('yellow! on grey30') + 'This is yellow! on grey30')
    lines.append(gclr("yellow!") + "Just yellow!" + RESET)
    lines.append(gclr("on yellow!") + "Just on yellow!" + RESET)
    lines.append(gclr("yellow! on black") + "yellow! on black" + RESET + f"repr(gclr('yellow! on black'): {repr(gclr('yellow! on black'))}")
    lines.append("[yellow! on grey90]yellow! on grey90[/]" + RESET)
    lines.append("[yellow! on black]yellow! on black[/]" + RESET)
    lines.append("[yellow on black]yellow on black[/]" + RESET)
    lines.append(' = [grey99]This is grey99[/]')
    printit(lines, 'boxed', 'centered', box_color="blue on rgb(150,150,200)")
    printit("This is [white! on grey99]white! on grey90[/] ...done", 'boxed', 'centered', box_color="white! on grey90", title=dbug('here'))
    print()
    printit("This is [grey100]grey100[/] ...done", 'boxed', 'centered', box_color="white! on grey90", title=dbug('here'))
    print()
    """--== SEP_LINE ==--"""
    colors = [['red', 'dim red', 'bold red', 'red!', 'rgb(255,0,0)'], 
            ['green', 'dim green', 'bold green', 'green!', 'rgb(0,255,0)'],
            ['blue', 'dim blue', 'bold blue', 'blue!', 'rgb(0,0,255)'],
            ['yellow', 'dim yellow', 'bold yellow', 'yellow!', 'rgb(255,255,0)'],
            ['magenta', 'dim magenta', 'bold magenta', 'magenta!', 'rgb(255,0,255)'],
            ['cyan', 'dim cyan', 'bold cyan', 'cyan!', 'rgb(0,255,255)'],
            ['white', 'dim white', 'bold white', 'white!', 'rgb(255,255,255)']]
    color_lol = []
    for row in colors:
        new_row = []
        for color in row:
            new_row.append(sub_color(color) + color)
        color_lol.append(new_row)
    color_lol.insert(0, ['color', 'dim color', 'bold color', 'color!', 'rgb representation'])
    gtable(color_lol, 'prnt', 'hdr', 'centered', title=' Fundamental Colors ', footer=" Color Demo ")


# ##################
def spinner_demo():
    # ##############
    """
    purpose: demo of Spinner
    """
    styles = ["ellipsis", "dot", "bar", "vbar", "moon", "pipe", "arrow", "balloons", 'braille', 'pulse', 'box', 'clock']
    # colors = ["red", "blue", "green", "yellow", "magenta", "white", "cyan"]
    # with Spinner(f"Demo progressive vbar ", 'centered', 'prog', 'elapsed', style='vbar', colors=colors):
    #     time.sleep(5)
    red_shades = ['rgb(20,0,0)', 'rgb(40,0,0)', 'rgb(60,0,0)', 'rgb(80,0,0)', 'rgb(100,0,0)', 'rgb(120,0,0)', 'rgb(140,0,0)', 'rgb(160,0,0)', 'rgb(180,0,0)', 'rgb(200,0,0)', '  rgb(220,0,0)', 'rgb(240, 0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)']
    while True:
        style = gselect(styles, 'centered', 'quit', rtrn="v")
        # style = gselect(styles, 'centered', rtrn="v", colors=colors)
        if style in ("q", "Q", ""):
            break
        wait_time = cinput("For how many seconds: (default=15) ") or 15
        color = cinput("Input a spinner color Note: if you enter a list (eg ['red', 'green', 'blue']) then the spinner will rotate colors accordingly, default is shades of red: ") or red_shades
        txt_color = cinput("Input a text color, default is normal: ") or 'normal'
        time_color = cinput("Input a time color, default is 'yellow! on black': ") or 'yellow! on black'
        printit("Note: some spinner styles will not use the progressive setting...", 'centered')
        prog = askYN("Should we try progressive?", "n", 'centered')
        printit([f"Demo: Spinner(style: {style}", f"txt_clr: {txt_color}", f"spinner_clr: {color[:4]}...", f"time_clr: {time_color}", f"Progressive: {prog}... "], 'centered')
        with Spinner("Demo: Spinner: working... ): ", 'centered', 'elapsed', color=color, txt_color=txt_color, elapsed_clr=time_color, style=style, prog=prog):
            # with Spinner(f"Demo: Spinner(style: {style} txt_clr: {txt_color} spinner_clr: {color} time_clr: {time_color}... ): ", 'centered', 'elapsed', color=color, txt_color=txt_color, elapsed_clr = time_color, style=style):
            time.sleep(wait_time)  # to simulate a long process


# ########
def tst():
    # ####
    """
    This is for testing only
    """
    msg = "Testing only for debugging"
    printit(msg, 'boxed', 'centered', 'shadowed')
    s = "[red on black] this is red on black[/]" + sub_color("green") + "and now green" + "[dim red] dim red" + sub_color("bold red") + " bold red and this is really [red!]red[/]" + "\x1b[36m \x1b[31m\x1b[2mdim red     \x1b[37;48;2;40;40;40m\x1b[1m"
    printit(s)
    lines = ['\x1b[37;48;2;2;20;40m \x1b[33myellow  \x1b[37;48;2;40;40;40m\x1b[1m│\x1b[36m \x1b[33m\x1b[2mdim yellow  \x1b[37;48;2;40;40;40m\x1b[1m│\x1b[31m \x1b[33m\x1b[1mbold yellow  \x1b[37;48;2;40;40;40m\x1b[1m│\x1b[32m \x1b[38;2;255;255;0myellow!  \x1b[37;48;2;40;40;40m\x1b[1m│\x1b[34m \x1b[38;2;255;255;0mrgb(255,255,0)     ']
    printit(lines)
    dbug(repr(lines))
    s1 = "\x1b[37;48;2;40;40;40m\x1b[1m│\x1b[36m \x1b[33m\x1b[2mdim yellow"
    printit(s1)
    s1 = "\x1b[37m\x1b[1m│\x1b[0;33m dim yellow"
    printit(s1)
    dbug('ask')
    myd = {'div_rate': '\x1b[;37m0.0\x1b[0m', 'peg': '\x1b[38;2;0;255;0m0.0\x1b[0m', 'trlg_peg': '\x1b[38;2;0;255;0m0.0\x1b[0m', 'p2bv': '\x1b[38;2;255;255;0m22.88\x1b[0m'}
    gtable(myd, 'prnt')
    with Spinner("Working ", 'elapsed', elapsed_clr="yellow! on black"):
        long_proc()
    t_d = {"one": 1, "two": 2, "three": 3, "one thousand": 1000}
    kv_cols(t_d, 3, 'prnt', title="kv_cols with 3 cols")
    """--== SEP_LINE ==--"""


# ##################
def do_func_docs():
    # ##############
    """
    purpose: to get funtion docs
    """
    """--== SAMPLE TABLE ==--"""
    tst_d = {"first": "1st", "one": 1, "two": [2, 2], "three": 3, "four": ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line ']}
    gtable(tst_d, 'prnt', 'wrap')
    """--== SAMPLE TABLE 2 ==--"""
    tst_d = {"first": ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line '], "one": 1, "two": [2, 2], "three": 3, "four": ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line ']}
    gtable(tst_d, 'prnt', 'wrap')
    """--== SAMPLE TABLE 3 ==--"""
    tst_d = {'add_content': ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line '], "next": 4}
    gtable(tst_d, 'prnt', 'wrap')
    """--== SEP_LINE ==--"""
    """--== Get a list of all func except a few... ==--"""
    my_lines = grep_lines(__file__, r"^def .*\(")
    my_funcs_l = [x.replace("def ", "") for x in my_lines]
    funcs_l = [re.sub(r"\((.*)\):.*", "", x) for x in my_funcs_l]
    funcs_l = [x for x in funcs_l if x.strip() not in ("main", 'tst')]
    funcs_l = [x for x in funcs_l if x.strip() if "demo" not in x]
    funcs_l = sorted(funcs_l)
    funcs_d = {}
    for n, func in enumerate(funcs_l):
        if n > 4:
            break
        # dbug(func)
        eval_this = func + '.__doc__'
        dbug(eval_this)
        doc = eval(eval_this)
        if doc.startswith("\n"):
            doc = doc.lstrip("\n")
        # box1 = boxed(func)
        doc = doc.split("\n")
        doc = [line.lstrip() for line in doc if len(line) > 4]
        func_d = {func: doc}
        gtable(func_d, 'prnt', 'wrap', footer=dbug('here'))
        funcs_d[func] = doc
    gtable(funcs_d, 'prnt', 'wrap', 'center', col_limit=120, footer=dbug('here'))
    dbug('ask')
    """--== user select ==--"""
    # func = gselect(stripped_funcs_l, 'centered', title="Which Function would you like information on:")
    func = gselect(funcs_l, 'centered', title="Which Function would you like information on:")
    if func not in ("", "q", "Q"):
        # dbug(func)
        func_args = grep_lines(my_funcs_l, "^" + func + "\(")[0]
        # dbug(func_args)
        my_args = "(" + func_args.split("(")[1] + ")"
        # r = re.search(r"\((.*)\):", func)
        # my_args = r.group(1)
        func = func.replace("():", "")
        eval_this = func + '.__doc__'
        doc = eval(eval_this)
        # clean up doc first
        doc = doc.split("\n")
        doc = [line.strip() for line in doc if line.strip() != '']
        doc_d = {"Func Name": func + "(" + my_args + ")", "Func Doc": doc}
        gtable(doc_d, 'prnt', 'wrap', 'hdr', 'center', col_limit=120, colnames="firstrow")


def chk_substr(chk_l, strgs_l, action='exclude'):
    """
    purpose: given a list of strings to check (chk_l) and a list of substrings to compare
            if any "compare" substring is in any string in check list of strings then 
                do action either 'exclude' or 'include'
    return: new_list
    """
    new_l = []
    for string_s in chk_l:
        if any(sub_s in string_s for sub_s in strgs_l):
            if action == 'include':
                new_l.append(string_s)
        else:
            if action == 'exclude':
                new_l.append(string_s)
    return new_l


# ##################
def do_func_demos():
    # ##############
    my_lines = grep_lines(__file__, r"^def .*\(")  # get all func names
    funcs_l = [x.replace("def ", "") for x in my_lines]  # strip off "def "
    # stripped_funcs_l = [re.sub(r"\((.*)\):.*", "", x) for x in funcs_l]
    exclude_l = ["main", 'tst', 'do_func_demos']
    funcs_l = chk_substr(funcs_l, exclude_l, action='exclude') 
    demo_funcs_l = [x.strip(":") for x in funcs_l if "demo" in x]  # only include _demo funcs
    ans = gselect(demo_funcs_l, 'centered', footer=dbug('here'))
    if ans in ("", "q", "Q"):
        return
    func = ans.replace("_demo()", "")
    doc = eval(f"{func}.__doc__")
    printit(doc, 'centered', 'boxed', title=f"Doc for {ans} function")
    askYN("", 'centered')
    eval(ans)
    if askYN(f"Do you want to see the code for this demo: {ans}? ", 'center'):
        # dbug(ans)
        func = ans.replace('()', '\(')
        # dbug(func)
        start_pat = f"^def {func}"
        # dbug(start_pat)
        demo_code = from_to(__file__, "^def quick_plot_demo()", "^$", include='top')
        demo_code = from_to(__file__, start_pat, "^$", include='top')
        printit(demo_code, 'boxed', 'centered', box_color='yellow!', title=f"Code for this demo: {ans}", footer=dbug('here'))


def gcontains(string_s, pattern_m):
    """
    purpose: to determine if any pattern (str|list) is a substring of string (string_s)
    options: none
    returns: bool
    """
    if not isinstance(pattern_m, list):
        pattern_l = [pattern_m]
    else:
        pattern_l = pattern_m
    for pat in pattern_l:
        if pat in string_s:
            # dbug(f"Found pat: {pat} in string_s: {string_s} returning True")
            return True
    return False


def get_mod_docs(mod="gtools", *args, fn="*", **kwargs):
    """
    purpose: lists all functions and the docs from a module
    Note: except some functions eg _demo
    returns cnt
    """
    """--== Imports ==--"""
    import inspect
    from inspect import getmembers, isfunction
    # from gtools import wrapit, chk_substr, boxed
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=True)
    # dbug(kwargs)
    # dbug(boxed_b, 'ask')
    """--== SEP_LINE ==--"""
    md = __import__(mod)
    funcs = [f for _, f in getmembers(md, isfunction) if f.__module__ == md.__name__]
    excludes = ['_demo', 'tst']
    funcs = [f_o for f_o in funcs if not gcontains(f_o.__name__, excludes)]
    cnt = 0
    for f_o in funcs:
        try:
            name = f_o.__name__
            diff = 20 - len(name)
            name = name + ":" + " "*diff
            box1 = [name]
            doc = f_o.__doc__
            doc_l = doc.split("\n")
            doc_l = [ln.strip() for ln in doc_l if ln.strip() != '']
            if boxed_b:
                box2 = boxed(doc_l, width=80)
            else:
                # dbug(f"Here we go boxed_b {boxed_b}")
                box2 = doc_l
            lines = gcolumnize([box1, box2])
            lines.append(("--------------"))
            lines = [escape_ansi(ln) for ln in lines]
            printit(lines)
            cnt += 1
        except Exception as e:
            dbug(f"func: {name}  e: {e}")
    return cnt
    # ### EOB def get_mod_docs(mod="gtools", fn="*"):# ## #


# ##### Main Code #######
def main(args):  # ######
    # ###################
    """
    purpose: allows user to see some of the fuctionality of this tool set
    """
    do_logo("companionway", 'figlet', box_color="red! on black!")
    credits_caveats = """    I offer sincere thanks to any and all who have shared or posted code that has helped me produce this file.   
    I am sure there are much better ways to achieve the results provided in every function or class etc in this file.   
    Please let me know of any problems, issues, improvements or suggestions.     geoff.mcanamara@gmail.com
    """
    printit(credits_caveats, 'centered', 'boxed', box_color="blue on black!")
    ans = ""
    while ans not in ("q", "Q"):
        ans = gselect(["Docs", "Demos", "All_functions_w/docs"], 'centered', 'quit')
        if ans == "Docs":
            do_func_docs()
        if ans == "Demos":
            do_func_demos()
        if ans == "All_functions_w/docs":
            file = "./gtools-docs.txt"
            if askYN(f"Do you want to save this info to file: {file}", "n", 'centered'):
                if file_exists(file):
                    os.remove(file)
                    cat_file(file, 'prnt')
                    # dbug('file should be gone', 'ask')
                transcript_start(file)
                # get_mod_docs("gtools", fn="*")
                # dbug("Launching get_mod_docs..")
                get_mod_docs("gtools", fn="*", boxed=False)
                transcript_stop
                print()
                sys.exit()
            else:
                cnt = get_mod_docs("gtools", fn="*", boxed=True)
                # cnt = get_mod_docs("gtools", fn="*")
        print(f"Count of functions: {cnt}")
    do_close(box_color="yellow! on black")


if (__name__ == "__main__"):  # allow this code to run independently or as a module  # noqa:
    from docopt import docopt
    args = docopt(handleOPTS.__doc__)
    handleOPTS(args)
    main(args)
