# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import tkinter

# size
import ttkbootstrap

from typex import Singleton, once
from ttkbootstrap.constants import *

# local
import core
import interface
from basic import i18n, cwd


class Weapon (Singleton):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.weapon)
        self.weapon_variable: dict[str, ttkbootstrap.BooleanVar] = {}
        self.weapon_checkbutton: dict[str, ttkbootstrap.Checkbutton] = {}
        self.build()

    @once
    def build(self):
        ...

    def initial_weapons(self):
        effective_weapons_name = core.config.effective_weapons.split(";")
        weapon_list = []
        for filename in os.listdir(cwd.assets.weapons):
            if not os.path.isfile(os.path.join(cwd.assets.weapons, filename)):
                continue

            if not filename.endswith(".json"):
                continue

            name = filename[:-5]
            weapon_list.append(name)

        for name in weapon_list:
            if name in self.weapon_variable:
                pass

            self.weapon_variable[name] = ttkbootstrap.BooleanVar()
            self.weapon_variable[name].trace_add("write", self.bin_weapon_update)

            if name in effective_weapons_name:
                self.weapon_variable[name].set(True)

        for checkbutton in self.weapon_checkbutton.values():
            checkbutton.destroy()

        self.weapon_checkbutton.clear()

        for index, name in enumerate(weapon_list):
            self.weapon_checkbutton[name] = ttkbootstrap.Checkbutton(
                self.frame,
                text=i18n.ctrl.translation(f"ITEM.{name}"),
                cursor="hand2",
                variable=self.weapon_variable[name],
                onvalue=True,
                offvalue=False,
                bootstyle=(SQUARE, TOGGLE)
            )
            self.weapon_checkbutton[name].grid(row=index//3, column=index%3, sticky=W, padx=(5, 20), pady=5)

    def bin_weapon_update(self, *_):
        effective_weapons_name = []
        for name, variable in self.weapon_variable.items():
            if variable.get():
                effective_weapons_name.append(name)

        core.config.effective_weapons.set(";".join(effective_weapons_name))
        ... # TODO


def initialize_final():
    weapon = Weapon()
    weapon.initial_weapons()
