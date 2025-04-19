# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import tkinter

# size
import psutil
import ttkbootstrap

from typex import once
from ezudesign.utils import try_exec, exec_item
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

# local
import core
import module
import constants
import interface
from basic import i18n


class Recoil (object):
    def __init__ (self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.recoil)
        self.build()

    @once
    def build (self):
        self.v_mou_sen = tkinter.DoubleVar()
        self.v_hor_per = tkinter.DoubleVar()
        self.v_ver_per = tkinter.DoubleVar()
        self.v_smo_coe = tkinter.IntVar()

        self.label_mou_sen = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_mou_sen)
        self.label_hor_per = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_hor_per)
        self.label_ver_per = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_ver_per)
        self.label_smo_coe = ttkbootstrap.Label(self.frame, text=i18n.UI.recoil_smo_coe)

        self.scale_mou_sen = tkinter.Scale(self.frame, from_=core.config.recoil_mou_sen.ranges.min, to=core.config.recoil_mou_sen.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_mou_sen)
        self.scale_hor_per = tkinter.Scale(self.frame, from_=core.config.recoil_hor_per.ranges.min, to=core.config.recoil_hor_per.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_hor_per)
        self.scale_ver_per = tkinter.Scale(self.frame, from_=core.config.recoil_ver_per.ranges.min, to=core.config.recoil_ver_per.ranges.max, resolution=0.01, orient=HORIZONTAL, variable=self.v_ver_per)
        self.scale_smo_coe = tkinter.Scale(self.frame, from_=core.config.recoil_smo_coe.ranges.min, to=core.config.recoil_smo_coe.ranges.max, resolution=1, orient=HORIZONTAL, variable=self.v_smo_coe)

        self.spinbox_mou_sen = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_mou_sen.ranges.min, to=core.config.recoil_mou_sen.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_mou_sen)
        self.spinbox_hor_per = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_hor_per.ranges.min, to=core.config.recoil_hor_per.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_hor_per)
        self.spinbox_ver_per = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_ver_per.ranges.min, to=core.config.recoil_ver_per.ranges.max, width=8, increment=0.01, justify=RIGHT, textvariable=self.v_ver_per)
        self.spinbox_smo_coe = ttkbootstrap.Spinbox(self.frame, from_=core.config.recoil_smo_coe.ranges.min, to=core.config.recoil_smo_coe.ranges.max, width=8, increment=1, justify=RIGHT, textvariable=self.v_smo_coe)

        self.label_mou_sen.grid(row=0, column=0, padx=4, pady=(4, 4), sticky=W)
        self.label_hor_per.grid(row=1, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_ver_per.grid(row=2, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_smo_coe.grid(row=3, column=0, padx=4, pady=(0, 4), sticky=W)

        self.scale_mou_sen.grid(row=0, column=1, padx=4, pady=(4, 4), sticky=EW)
        self.scale_hor_per.grid(row=1, column=1, padx=4, pady=(0, 4), sticky=EW)
        self.scale_ver_per.grid(row=2, column=1, padx=4, pady=(0, 4), sticky=EW)
        self.scale_smo_coe.grid(row=3, column=1, padx=4, pady=(0, 4), sticky=EW)

        self.spinbox_mou_sen.grid(row=0, column=2, padx=4, pady=(4, 4), sticky=W)
        self.spinbox_hor_per.grid(row=1, column=2, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_ver_per.grid(row=2, column=2, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_smo_coe.grid(row=3, column=2, padx=4, pady=(0, 4), sticky=W)

        self.frame.grid_columnconfigure(1, weight=1)
        self.v_mou_sen.set(core.config.recoil_mou_sen)
        self.v_hor_per.set(core.config.recoil_hor_per)
        self.v_ver_per.set(core.config.recoil_ver_per)
        self.v_smo_coe.set(core.config.recoil_smo_coe)

        self.v_mou_sen.trace_add("write", self.v_mou_sen_callback)
        self.v_hor_per.trace_add("write", self.v_hor_per_callback)
        self.v_ver_per.trace_add("write", self.v_ver_per_callback)
        self.v_smo_coe.trace_add("write", self.v_smo_coe_callback)

    def v_mou_sen_callback (self, *_):
        core.config.recoil_mou_sen = round(self.v_mou_sen.get(), 2)

    def v_hor_per_callback (self, *_):
        core.config.recoil_hor_per = round(self.v_hor_per.get(), 2)

    def v_ver_per_callback (self, *_):
        core.config.recoil_ver_per = round(self.v_ver_per.get(), 2)

    def v_smo_coe_callback (self, *_):
        core.config.recoil_smo_coe = self.v_smo_coe.get()
