# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import tkinter

from tkinter import TclError
from dataclasses import dataclass

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *
from ezudesign.configuration import ConfigurationBaseException

# local
import core
from basic import i18n


@dataclass
class ScaleSetWidget:
    variable: ttkbootstrap.DoubleVar
    label: ttkbootstrap.Label
    scale: ttkbootstrap.Scale
    spinbox: ttkbootstrap.Spinbox


class Recoil (object):
    def __init__(self, notebook: ttkbootstrap.Notebook):
        self.frame = ttkbootstrap.Frame(notebook)
        notebook.add(self.frame, text=i18n.UI.recoil_track)
        self.settings: dict[str, ScaleSetWidget] = {}
        self.build()

    @once
    def build (self):
        recoil_settings = [
            core.config.recoil_sensitivity.name,
            core.config.recoil_horizontal.name,
            core.config.recoil_vertical.name,
            core.config.recoil_leading_delay.name,
            core.config.recoil_duty_cycle.name
        ]

        for index, name in enumerate(recoil_settings):
            variable = ttkbootstrap.DoubleVar()
            label = ttkbootstrap.Label(self.frame, text=i18n.UI[name])
            min_value = core.config[name].ranges.min
            max_value = core.config[name].ranges.max
            increment = 1 / (10 ** core.config[name].ranges.round)
            scale = tkinter.Scale(self.frame, from_=min_value, to=max_value, resolution=increment, orient=HORIZONTAL, variable=variable)
            spinbox = ttkbootstrap.Spinbox(
                self.frame,
                from_=min_value,
                to=max_value,
                width=8,
                increment=increment,
                justify=RIGHT,
                textvariable=variable
            )

            variable.set(core.config[name])
            self.settings[name] = ScaleSetWidget(variable, label, scale, spinbox)
            variable.trace_add("write", self.setting_callback)
            self.frame.grid_columnconfigure(1, weight=1)
            label.grid(row=index, column=0, padx=4, pady=(4, 4), sticky=W)
            scale.grid(row=index, column=1, padx=4, pady=(0, 4), sticky=EW)
            spinbox.grid(row=index, column=2, padx=4, pady=(0, 4), sticky=W)

    def setting_callback(self, *_):
        for name, widget in self.settings.items():
            try:
                core.config[name] = widget.variable.get()
            except (ConfigurationBaseException, TclError) as _:
                widget.spinbox.configure(bootstyle=DANGER)
            else:
                widget.spinbox.configure(bootstyle=NORMAL)
