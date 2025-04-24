# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import tkinter

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import core
import interface
from basic import i18n


class Recoil (object):
    def __init__ (self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.recoil)
        self.build()

    @once
    def build (self):
        self.v_sensitivity = tkinter.DoubleVar()
        self.v_horizontal = tkinter.DoubleVar()
        self.v_vertical = tkinter.DoubleVar()
        self.v_smoothing = tkinter.IntVar()
        self.v_leading_delay = tkinter.DoubleVar()
        self.v_duty_cycle = tkinter.DoubleVar()

        self.label_sensitivity = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_sensitivity)
        self.label_horizontal = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_horizontal)
        self.label_vertical = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_vertical)
        self.label_smoothing = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_smoothing)
        self.label_leading_delay = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_leading_delay)
        self.label_duty_cycle = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_duty_cycle)

        self.scale_sensitivity = tkinter.Scale(self.frame, from_=core.config.recoil_sensitivity.ranges.min, to=core.config.recoil_sensitivity.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_sensitivity)
        self.scale_horizontal = tkinter.Scale(self.frame, from_=core.config.recoil_horizontal.ranges.min, to=core.config.recoil_horizontal.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_horizontal)
        self.scale_vertical = tkinter.Scale(self.frame, from_=core.config.recoil_vertical.ranges.min, to=core.config.recoil_vertical.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_vertical)
        self.scale_smoothing = tkinter.Scale(self.frame, from_=core.config.recoil_smoothing.ranges.min, to=core.config.recoil_smoothing.ranges.max, resolution=1, orient=HORIZONTAL, variable=self.v_smoothing)
        self.scale_leading_delay = tkinter.Scale(self.frame, from_=core.config.recoil_leading_delay.ranges.min, to=core.config.recoil_leading_delay.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_leading_delay)
        self.scale_duty_cycle = tkinter.Scale(self.frame, from_=core.config.recoil_duty_cycle.ranges.min, to=core.config.recoil_duty_cycle.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_duty_cycle)

        self.spinbox_sensitivity = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_sensitivity.ranges.min, to=core.config.recoil_sensitivity.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_sensitivity)
        self.spinbox_horizontal = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_horizontal.ranges.min, to=core.config.recoil_horizontal.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_horizontal)
        self.spinbox_vertical = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_vertical.ranges.min, to=core.config.recoil_vertical.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_vertical)
        self.spinbox_smoothing = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_smoothing.ranges.min, to=core.config.recoil_smoothing.ranges.max, width=8, increment=1, justify=RIGHT, textvariable=self.v_smoothing)
        self.spinbox_leading_delay = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_leading_delay.ranges.min, to=core.config.recoil_leading_delay.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_leading_delay)
        self.spinbox_duty_cycle = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_duty_cycle.ranges.min, to=core.config.recoil_duty_cycle.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_duty_cycle)

        self.label_sensitivity.grid(row=0, column=0, padx=4, pady=(4, 4), sticky=W)
        self.label_horizontal.grid(row=1, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_vertical.grid(row=2, column=0, padx=4, pady=(0, 4), sticky=W)
        # self.label_smoothing.grid(row=3, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_leading_delay.grid(row=4, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_duty_cycle.grid(row=5, column=0, padx=4, pady=(0, 4), sticky=W)

        self.scale_sensitivity.grid(row=0, column=1, padx=4, pady=(4, 4), sticky=EW)
        self.scale_horizontal.grid(row=1, column=1, padx=4, pady=(0, 4), sticky=EW)
        self.scale_vertical.grid(row=2, column=1, padx=4, pady=(0, 4), sticky=EW)
        # self.scale_smoothing.grid(row=3, column=1, padx=4, pady=(0, 4), sticky=EW)
        self.scale_leading_delay.grid(row=4, column=1, padx=4, pady=(0, 4), sticky=EW)
        self.scale_duty_cycle.grid(row=5, column=1, padx=4, pady=(0, 4), sticky=EW)

        self.spinbox_sensitivity.grid(row=0, column=2, padx=4, pady=(4, 4), sticky=W)
        self.spinbox_horizontal.grid(row=1, column=2, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_vertical.grid(row=2, column=2, padx=4, pady=(0, 4), sticky=W)
        # self.spinbox_smoothing.grid(row=3, column=2, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_leading_delay.grid(row=4, column=2, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_duty_cycle.grid(row=5, column=2, padx=4, pady=(0, 4), sticky=W)

        self.frame.grid_columnconfigure(1, weight=1)
        self.v_sensitivity.set(core.config.recoil_sensitivity)
        self.v_horizontal.set(core.config.recoil_horizontal)
        self.v_vertical.set(core.config.recoil_vertical)
        self.v_smoothing.set(core.config.recoil_smoothing)
        self.v_leading_delay.set(core.config.recoil_leading_delay)
        self.v_duty_cycle.set(core.config.recoil_duty_cycle)

        self.v_sensitivity.trace_add("write", self.v_sensitivity_callback)
        self.v_horizontal.trace_add("write", self.v_horizontal_callback)
        self.v_vertical.trace_add("write", self.v_vertical_callback)
        self.v_smoothing.trace_add("write", self.v_smoothing_callback)
        self.v_leading_delay.trace_add("write", self.v_leading_delay_callback)
        self.v_duty_cycle.trace_add("write", self.v_duty_cycle_callback)

    def v_sensitivity_callback (self, *_):
        core.config.recoil_sensitivity = round(self.v_sensitivity.get(), 2)

    def v_horizontal_callback (self, *_):
        core.config.recoil_horizontal = round(self.v_horizontal.get(), 2)

    def v_vertical_callback (self, *_):
        core.config.recoil_vertical = round(self.v_vertical.get(), 2)

    def v_smoothing_callback (self, *_):
        core.config.recoil_smoothing = self.v_smoothing.get()

    def v_leading_delay_callback (self, *_):
        core.config.recoil_leading_delay = round(self.v_leading_delay.get(), 2)

    def v_duty_cycle_callback (self, *_):
        core.config.recoil_duty_cycle = round(self.v_duty_cycle.get(), 2)
