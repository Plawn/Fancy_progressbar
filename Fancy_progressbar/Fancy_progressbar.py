# -*- coding: utf-8 -*-


from time import sleep
import sys
import os
from threading import Thread, Event



def length_of_terminal():
    # columns = int(subprocess.check_output(['stty', 'size']).decode().split()[1]) #linux and osx only
    columns = os.get_terminal_size().columns  # should be bulletproof
    return(columns)


def rows_of_terminal():
    rows = os.get_terminal_size().lines
    return(rows)


# Some What bad
if sys.version[0:3] < "3.0":
    import fcntl, termios, struct
    def length_of_terminal():
        rows, columns, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return (columns)
    def rows_of_terminal():
        rows, columns, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return(rows)

"""
    Written by <Plawn>
"""


def console_write(string):
    sys.stdout.write(string)
    sys.stdout.flush()


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


def clear_line():
    console_write("\r" + " " * (length_of_terminal()) +"\r")


def clear_n_lines(n):
    for i in range(n):
        clear_line()
        down()
        clear_line()
    for i in range(n):
        up()


def up():
    console_write('\x1b[1A')
    # sys.stdout.write('\x1b[1A')
    # sys.stdout.flush()


def down():
    console_write('\n')
    # I could use '\x1b[1B' here, but newline is faster and easier
    # sys.stdout.write('\n')
    # sys.stdout.flush()





class Progress_bar_options():
    def __init__(self, *args, **kwargs):
        self.default_animation = ["[|]","[/]", "[-]", "[\\]"]
        self.options = {"taskname": '', "current": '',
                        "style": "", "max_lenght": None,"animation":self.default_animation}
        self._options = ['hidden', 'blank', 'done',
                         'pointer', "kill_when_finished","animated"]
        self._args = []
        self.dict = {}
        self.add_argument(args=args, dict=kwargs)

    def add_argument(self, *args, **kwargs):
        args = kwargs.get('args', args)
        kwargs = kwargs.get('dict', kwargs)
        for item in args:
            if item in self._options:
                self._args.append(item)
        for item in kwargs:
            self.options.update({item: kwargs[item]})
        self.dict = {"args": self._args, "kwargs": self.options}

    def display(self):
        print(self.options)
        print(self._args)


class Progress_bar():
    def __init__(self, *args, **kwargs):

        self.task_name = kwargs.get('taskname', '') + " :"
        self.fill = kwargs.get('fill', '█')[0] if len(
            kwargs.get('fill', '█')) > 0 else '█'
        self._done = False
        self.hidden = True if "hidden" in args else False
        self.textd = kwargs.get("text", "")
        self.text_only = True if len(self.textd) > 0 else False
        self.blankk = True if "blank" in args else False
        self.pointer = True if "pointer" in args else False  # not supported yet
        self._style = ""  # terminal colors
        self.end_style = ""  # terminal colors
        self._kill_when_finished = True if "kill_when_finished" in args else False
        self._current = ''
        self.progress = 0
        self.finished = False
        self._updated = False
        self.event_kill = None
        self.kill_sleep = 0.001
        self._end_style = "\033[m"  # terminal colors
        self.current_activated = False
        self.max_lenght = None
        self.style(kwargs.get('style', ''))
        self._animate = True if "animated" in args else False
        self._animation_counter = 0
        self._default_animation = ["[|]","[/]", "[-]", "[\\]"]
        self._animation = kwargs.get("animation",self._default_animation)
        for arg in args :
            if "Progress_bar_options" in str(type(arg)):
                self.set_options(arg)
        # <------------------>
        options = kwargs.get('options', None)
        if options != None:
            self.set_options(options)
            # print("setting options")

    def set_options(self, options):
        if "hidden" in options.dict["args"]:
            self.hidden = True
        if "blank" in options.dict["args"]:
            self.blankk = True
        if "done" in options.dict["args"]:
            self.done = True
        if "pointer" in options.dict["args"]:
            self.pointer = True
        if "kill_when_finished" in options.dict["args"]:
            self._kill_when_finished = True
        if "animated" in options.dict["args"]:
            self._animate = True
        self.task_name = options.dict["kwargs"].get('taskname', '') + " :"
        self.fill = options.dict["kwargs"].get('fill', '█')[0] if len(
            options.dict["kwargs"].get('fill', '█')) > 0 else '█'
        self.textd = options.dict["kwargs"].get('text', '')
        self.max_lenght = options.dict["kwargs"].get('max_lenght', None)
        self._animation = options.dict["kwargs"].get('animation', self._default_animation)
        if len(self.textd) > 0:
            self.text_only = True
        self.style(options.dict["kwargs"].get('style', ''))
        self.current(str(options.dict["kwargs"].get('current', '')))
        # print(self.blankk,self.text_only,self.textd,self._kill_when_finished)
    def name(self,string):
        self.task_name = string
    def kill_when_finished(self):
        self._kill_when_finished = True
    def no_style(self):
        self._style = ""
        self.end_style = ""

    def style(self, style):
        if "Style" in str(type(style)):
            self.end_style = self._end_style
            self._style = style.str()
        else:
            if len(style) > 0:
                self.end_style = self._end_style
                self._style = style

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def delete(self):
        self._done = True
        self.hidden = True
    def finish(self, **kwargs):
        if self.event_kill != None and self._kill_when_finished:
            self.event_kill.set()
        if not self.current_activated:
            if kwargs.get('showing', False) or kwargs.get('message') != None:
                self._current = kwargs.get('message', 'Done')
                self.current_activated = True
        else:
            self.textd = kwargs.get('message', 'Done')
            self._current = kwargs.get('message', 'Done')
            self.current_activated = True
        self.finished = True
        if self._kill_when_finished:
            sleep(0.001)

    def current(self, currentt):
        if len(currentt) > 0:
            self._current = str(currentt)
            self.current_activated = True
    def done(self):
        self._done = True
    def is_finished(self):
        return(self.finished)
    def text(self, string):
        self.text_only = True
        self.textd = string

    def blank(self):
        self.text_only = True
        self.blankk = True

    def update(self, progress):
        self.progress = progress
        self._updated = True
    def is_done(self):
        return(self._done)

    def print_bar(self):
        if self.pointer:
            try:
                progress = self.progress[0]  # not working now
            except:
                raise ValueError
                self._done = True
        else:
            progress = self.progress
        # self.length = int(os.popen('stty size', 'r').read().split()[1]) #windows command must be added
        if self.max_lenght != None:
            l = length_of_terminal()
            if l < self.max_lenght:
                length = l
            else:
                length = self.max_lenght
        else:
            length = length_of_terminal()
        output = "\r" + self._style
        animation = ""
        if self._animate:
            self._animation_counter += 1
            if self._animation_counter == len(self._animation):
                self._animation_counter = 0
            animation = self._animation[self._animation_counter] + " "

        if not self.text_only:
            dec = str(int(int((progress % 1) * 100)))
            if len(dec) == 1:
                dec += '0'

            progress_str = str(int(progress)) + dec
            length = int(length) - len(self.task_name) - \
                len(str(progress_str)) - len(dec) - 3 - len(animation) - 1
            if progress > 100:
                filledLength = length
            else:
                filledLength = int(length * progress / 100)

            bar = self.task_name + animation + self.fill * filledLength + '-' * \
                (length - filledLength) + " " + \
                str(int(progress)) + '.' + str(dec) + "%"

            if not self.current_activated:
                output += bar
            else:
                l = length_of_terminal()
                bottom = str(self._current) + " " * (l - len(str(self._current)))
                if len(bottom) > l:
                    bottom = bottom[0:l - 1] + ">"
                output += bar + "\n" + bottom

        else:
            if not self.blankk:
                if len(self.textd) > length:

                    output += self.textd[0:length-1] + ">" +self.end_style
                else:
                    output += self.textd + " " * \
                        (length - len(str(self.textd)))
            else:
                return("\r" + " " * length)
        output += self.end_style
        return(output)


class Progress_bar_handler(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        self.event_kill = Event()
        self.event_on_change = Event()
        self.progress_bar_list = []
        self.lines  = 0
        # self.actualisation_time = 0.5
        self.dead = False
        self.test  = 0
        self.paused = False
        self.old_lines = 0
        self.default_kill_sleep = 0.001
        presets = {'fast': 0.1, 'very fast': 0.01, "slow": 1,
                   'very slow': 3, 'medium': 0.8, 'default': 0.5}
        self.actualisation_time = kwargs.get('refresh', 0.5)
        # for sig in ('TERM', 'HUP', 'INT'):
        #     signal.signal(getattr(signal, 'SIG'+sig), quit)
        if len(args) > 0 :
            self.append(args)
        try:
            self.preset = kwargs['preset']
            try:
                self.actualisation_time = presets[self.preset]
            except:
                print('preset unknown -> will use default settings aka 0.5')
        except:
            pass
    def _auto_set(self,bar):
        if bar not in self.progress_bar_list:
            self.progress_bar_list.append(bar)
            bar.event_kill = self.event_kill
            bar.kill_sleep = self.default_kill_sleep

    def append(self, *progress_bar):
        # Dirty AF sorry guys don't  really have more time :) at least you can enter anything :p
        # --> you  can enter things as a list, tuple or typical *args
        if  ('tuple' in str(type(progress_bar)) or 'list' in str(type(progress_bar))) and ('list' in str(type(progress_bar[0])) or 'tuple' in str(type(progress_bar[0]))):
            progress_bar = progress_bar[0]
            if  ('tuple' in str(type(progress_bar)) or 'list' in str(type(progress_bar))) and ('list' in str(type(progress_bar[0])) or 'tuple' in str(type(progress_bar[0]))):
                progress_bar = progress_bar[0]
                for bar in progress_bar:
                        self._auto_set(bar)
            else:
                for bar in progress_bar:
                    self._auto_set(bar)
        else:
            self._auto_set(progress_bar[0])





    def remove(self, progress_bar):
        try:
            self.progress_bar_list.remove(progress_bar)
            return(True)
        except:
            return(False)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def kill(self):
        self.event_kill.set()
        sleep(self.default_kill_sleep)
        print('killed')
        print(self.event_kill.is_set())
    def list(self):
        return(self.progress_bar_list)

    def exchange_by_index(self, index1, index2):
        try:
            self.progress_bar_list[index1], self.progress_bar_list[
                index2] = self.progress_bar_list[index2], self.progress_bar_list[index1]
            return(True)
        except:
            return(False)
    def stop(self):
        self.kill()
    def exchange_by_bar(self, bar1, bar2):
        try:
            index1, index2 = self.progress_bar_list.index(
                bar1), self.progress_bar_list.index(bar2)
            self.exchange_by_index(index1, index2)
            return(True)
        except:
            return(False)

    # def run(self):
    #     line = 1
    #     just_killed = False
    #     do_it = False
    #     while not self.event_kill.is_set() or not just_killed:
    #         if not self.paused:
    #             if line < self.old_lines:
    #                 clear_n_lines(line)
    #                 self.old_lines = line
    #
    #
    #             max_line = rows_of_terminal()
    #             line = 0
    #             first_line = True
    #             new_line  = 0
    #             n, i  = len(self.progress_bar_list), 0
    #
    #             # while i < n and line < max_line - 2:
    #             #     bar = self.progress_bar_list[i]
    #             # # for bar in self.progress_bar_list:
    #             #     if not bar.hidden and i < max_line:
    #             #         new_line += 1
    #             #         if bar.current_activated and not bar.text_only:
    #             #             new_line += 1
    #             #     i += 1
    #             # if line < self.old_lines:
    #             #     clear_n_lines(self.old_lines + 2)
    #             #     self.old_lines = new_line
    #
    #
    #             n, i  = len(self.progress_bar_list), 0
    #             while i < n and line < max_line - 2:
    #                 bar = self.progress_bar_list[i]
    #                 if not first_line:
    #                     if not bar.hidden :
    #                         if not bar._done:
    #                             line += 1
    #                             if bar.current_activated and not bar.text_only:
    #                                 line += 1
    #                                 pass
    #                             console_write(bar.print_bar())
    #                             down()
    #                         else:
    #                             self.progress_bar_list.remove(bar)
    #                     else:
    #                         clear_line()
    #
    #                     i += 1
    #                 else:
    #                     first_line = False
    #                     line += 1
    #                     clear_line()
    #                     down()
    #
    #
    #             if line == max_line - 2 :
    #                 lenght = length_of_terminal()
    #                 # down()
    #                 clear_line()
    #                 console_write(" v" * (int(lenght / 2) - 2)+"\r")
    #                 line += 2
    #                 up()
    #
    #
    #         for i in range(line):
    #             up()
    #         # for i in range(new_line+1):
    #         #     up()
    #         # up
    #
    #         if self.event_kill.is_set() and not just_killed:
    #             just_killed = True
    #         else:
    #             self.event_kill.wait(self.actualisation_time)
    #
    #     for i in range(line):
    #         console_write("\n")
    #     self.dead = True

    def run(self):
        just_killed = False
        old_lines = 0
        final = False
        while not self.event_kill.is_set() or not just_killed:
            if not self.paused :



                i, n = 0, len(self.progress_bar_list)
                clear_line()
                down()
                clear_line()
                line = 1
                max_line = rows_of_terminal() - 2
                while i < n  and line < max_line:
                    bar = self.progress_bar_list[i]
                    if not bar.hidden :
                        if not bar._done :
                            current_activated, text_only, print_bar = bar.current_activated,bar.text_only,bar.print_bar()
                            line += 1
                            console_write(print_bar)
                            down()
                            if current_activated and not text_only:
                                line += 1
                    i += 1
                # down()
                clear_line()
                # line += 1
                # up()
                # console_write('\rend\r')
                # if i < n :

                if line > max_line - 4 :
                    final = True
                    console_write(" v" * (int(length_of_terminal() / 2) - 2)+"\r")
                else:
                    clear_line()
                    # line += 1
                # self.test  = line
                    # up()
                # if final :
                #     old_lines += 1
                if line < old_lines :
                    clear_n_lines(old_lines-line)
                # else:
                #     clear_n_lines(1)

                old_lines = line




                for i in range(line):
                    up()







            if self.event_kill.is_set() and not just_killed:
                just_killed = True
            else:
                self.event_kill.wait(self.actualisation_time)

        for i in range(line):
            down()
        self.dead = True
