# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
from dataclasses import dataclass, field

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import core
import interface
from basic import i18n


@dataclass
class SwitchWidget:
    variable: ttkbootstrap.BooleanVar = field(default=None)
    checkbutton: ttkbootstrap.Checkbutton = field(default=None)


class Anti (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.anti)
        self.switch_settings: dict[str, SwitchWidget] = {}
        self.build()

    @once
    def build(self):
        switch_settings = [
            core.config.anti_ad_ghosting.name,
            core.config.anti_ws_ghosting.name
        ]

        for index, name in enumerate(switch_settings):
            variable = ttkbootstrap.BooleanVar()
            checkbutton = ttkbootstrap.Checkbutton(
                self.frame,
                text=i18n.UI[name],
                variable=variable,
                bootstyle=(SQUARE, TOGGLE),
                cursor="hand2"
            )
            self.switch_settings[name] = SwitchWidget(variable, checkbutton)
            checkbutton.grid(row=index, column=0, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W, columnspan=2)
            variable.set(core.config[name])
            variable.trace_add("write", self.switch_settings_update)

    def switch_settings_update(self, *_):
        for name, widget in self.switch_settings.items():
            core.config[name] = widget.variable.get()
