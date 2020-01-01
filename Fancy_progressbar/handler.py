# -*- coding: utf-8 -*-

"""
    Written by <Plawn>
"""

from time import sleep
import sys
import os
from threading import Thread, Event
from . import utils
from .utils import console_write, length_of_terminal, rows_of_terminal, down, clear_line, clear_n_lines, up
from .options import ProgressBarOptions
from typing import List, Tuple, Dict, Union
from .bar import ProgressBar
from .family import ProgressBarFamily

class ProgressBarHandler(Thread):
    """
    """
    presets = {'fast': 0.1, 'very fast': 0.01, "slow": 1,
               'very slow': 3, 'medium': 0.8, 'default': 0.5}

    def __init__(self, bars: List[ProgressBar], refresh='default'):
        Thread.__init__(self)
        self.event_kill = Event()
        self.event_on_change = Event()  # not supported yet
        self.progress_bar_list: List[ProgressBar] = []
        self.lines = 0
        self.dead = False
        self.test = 0
        self.paused = False
        self.old_lines = 0

        self.default_kill_sleep = 0.001

        self.actualisation_time = 0
        self.append(*bars)

        try:
            self.preset = refresh
            try:
                self.actualisation_time = self.presets[self.preset]
            except:
                raise Exception(
                    'preset unknown -> will use default settings -> 0.5')
        except:
            pass

    def _auto_set(self, bar: Union[ProgressBar, ProgressBarFamily]):
        if bar not in self.progress_bar_list:
            self.progress_bar_list.append(bar)
            if isinstance(bar, ProgressBarFamily):
                bar.top_bar.event_kill = self.event_kill
                bar.top_bar.kill_sleep = self.default_kill_sleep
            else:
                bar.event_kill = self.event_kill
                bar.kill_sleep = self.default_kill_sleep

            bar.to_suppr = self.progress_bar_list  # odd

    def append(self, *args):
        for bar in args:
            self._auto_set(bar)
        self.re_arrange()

    def re_arrange(self):
        pass
        # to order the bars in the correct order

    def remove(self, progress_bar: ProgressBar):
        self.progress_bar_list.remove(progress_bar)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def exchange_by_index(self, index1: int, index2: int):

        self.progress_bar_list[index1], self.progress_bar_list[
            index2] = self.progress_bar_list[index2], self.progress_bar_list[index1]

    def stop(self):
        self.event_kill.set()
        sleep(self.default_kill_sleep)

    def exchange_by_bar(self, bar1: ProgressBar, bar2: ProgressBar):
        index1, index2 = self.progress_bar_list.index(
            bar1), self.progress_bar_list.index(bar2)
        self.exchange_by_index(index1, index2)

    def _render_bar(self, bar: ProgressBar):
        if not bar.hidden:
            if not bar._done:
                current_activated, text_only, print_bar, func, act_func = bar.current_activated, bar.text_only, bar.print_bar(), bar.func, bar.act_func
                self.lines += 1
                if act_func:
                    bar.func()
                console_write(print_bar)
                down()
                if current_activated and not text_only:
                    self.lines += 1

    def _render_family(self, family:ProgressBarFamily):
        family.update()
        self._render(family.top_bar)
        for bar in family:
            self._render(bar)

    def _render(self, item: Union[ProgressBar, ProgressBarFamily]):
        if isinstance(item, ProgressBarFamily):
            self._render_family(item)
        else:
            self._render_bar(item)

    def run(self):
        just_killed = False
        old_lines = 0
        while not self.event_kill.is_set() or not just_killed:
            if not self.paused:
                clear_line()
                down()
                clear_line()
                self.lines = 1
                max_line = rows_of_terminal() - 2

                for bar in self.progress_bar_list:
                    if self.lines < max_line:
                        self._render(bar)
                    else:
                        break

                clear_line()
                if self.lines > max_line - 1:
                    console_write(
                        " v" * (int(length_of_terminal() / 2) - 2) + "\r")
                else:
                    clear_line()

                if self.lines < old_lines:
                    clear_n_lines(old_lines-self.lines)
                old_lines = self.lines
                for i in range(self.lines):
                    up()
            if self.event_kill.is_set() and not just_killed:
                just_killed = True
            else:
                self.event_kill.wait(self.actualisation_time)

        for i in range(self.lines):
            down()
        self.dead = True
