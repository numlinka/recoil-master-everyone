# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
from dataclasses import dataclass

# size
import i18nco
import i18nco.constants
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import core
import interface
from basic import i18n


@dataclass
class ComboboxWidget:
    variable: ttkbootstrap.StringVar
    label: ttkbootstrap.Label
    combobox: ttkbootstrap.Combobox


class Setting (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.settings)
        self.combobox_settings: dict[str, ComboboxWidget] = {}
        self.localed_options: dict[str, str] = {}
        self.localed_options_reverse: dict[str, str] = {}
        self.build()

    @once
    def build (self):
        unknown_count = 0
        for local_code in i18n.ctrl.available_locales:
            local_name = i18nco.constants.LANGUAGE_TABLE.get(local_code, None)
            if local_name is None:
                local_name = i18n.ctrl.translation("language", local_code)
                if local_name == "language":
                    local_name = f"Unknown - {unknown_count}"
                    unknown_count += 1
            self.localed_options[local_name] = local_code
            self.localed_options_reverse[local_code] = local_name

        combobox_settings = [
            core.config.localed.name,
            core.config.theme.name
        ]

        for index, name in enumerate(combobox_settings):
            variable = ttkbootstrap.StringVar()
            label = ttkbootstrap.Label(self.frame, text=i18n.UI[f"settings_{name}"])
            combobox = ttkbootstrap.Combobox(self.frame, textvariable=variable, state=READONLY)
            label.grid(row=index, column=0, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            combobox.grid(row=index, column=1, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            self.combobox_settings[name] = ComboboxWidget(variable, label, combobox)

            if name == core.config.localed.name:
                combobox.config(values=list(self.localed_options.keys()))
                variable.set(self.localed_options_reverse.get(core.config.localed, "Unknown") if core.config.localed else "")

            elif name == core.config.theme.name:
                combobox.config(values=interface.style.theme_names())
                variable.set(core.config.theme)

            variable.trace_add("write", self.combobox_settings_callback)

    def combobox_settings_callback(self, variable_id, *_):
        for name, widget in self.combobox_settings.items():
            if variable_id == str(widget.variable):
                break

        else:
            return

        if name == core.config.localed.name:
            local_name = widget.variable.get()
            if local_name not in self.localed_options:
                return

            local_code = self.localed_options[local_name]
            i18n.ctrl.set_locale(local_code)
            core.config.localed.set(local_code)

        elif name == core.config.theme.name:
            theme_name = widget.variable.get()
            if theme_name not in interface.style.theme_names():
                return
            interface.set_theme(theme_name)
            core.config.theme.set(theme_name)
