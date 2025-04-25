# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import tkinter

from dataclasses import dataclass, field

# size
import ttkbootstrap

from typex import Singleton, once
from ttkbootstrap.constants import *

# local
import core
import module
import interface
import constants

from basic import i18n, cwd
from typeins import GameStatePlayerWeapon


@dataclass
class HUDWeapon:
    v_ammo: ttkbootstrap.StringVar = field(default=None)
    v_weapon: ttkbootstrap.StringVar = field(default=None)
    hud_ammo: ttkbootstrap.Label = field(default=None)
    hud_weapon: ttkbootstrap.Label = field(default=None)


class HUD (Singleton):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.hud)
        self.huds: list[HUDWeapon] = []
        self.last_amount = 0
        self.build()
        self.build_hud_window()

    @once
    def build(self):
        self.v_hud_enable = ttkbootstrap.BooleanVar()
        self.v_hud_weapon_sort = ttkbootstrap.BooleanVar()
        self.v_hud_active_first = ttkbootstrap.BooleanVar()
        self.v_hud_active_only = ttkbootstrap.BooleanVar()
        self.v_hud_gun_only = ttkbootstrap.BooleanVar()

        self.checkbutton_enable = ttkbootstrap.Checkbutton(self.frame, text=i18n.UI.hud_enable, variable=self.v_hud_enable, bootstyle=(SQUARE, TOGGLE), cursor="hand2",)
        self.checkbutton_weapon_sort = ttkbootstrap.Checkbutton(self.frame, text=i18n.UI.hud_weapon_sort, variable=self.v_hud_weapon_sort, bootstyle=(SQUARE, TOGGLE), cursor="hand2",)
        self.checkbutton_active_first = ttkbootstrap.Checkbutton(self.frame, text=i18n.UI.hud_active_first, variable=self.v_hud_active_first, bootstyle=(SQUARE, TOGGLE), cursor="hand2",)
        self.checkbutton_active_only = ttkbootstrap.Checkbutton(self.frame, text=i18n.UI.hud_active_only, variable=self.v_hud_active_only, bootstyle=(SQUARE, TOGGLE), cursor="hand2",)
        self.checkbutton_gun_only = ttkbootstrap.Checkbutton(self.frame, text=i18n.UI.hud_gun_only, variable=self.v_hud_gun_only, bootstyle=(SQUARE, TOGGLE), cursor="hand2",)

        self.checkbutton_enable.grid(row=0, column=0, padx=4, pady=(4, 4), sticky=W)
        self.checkbutton_weapon_sort.grid(row=1, column=0, padx=4, pady=(0, 4), sticky=W)
        self.checkbutton_active_first.grid(row=2, column=0, padx=4, pady=(0, 4), sticky=W)
        self.checkbutton_active_only.grid(row=3, column=0, padx=4, pady=(0, 4), sticky=W)
        self.checkbutton_gun_only.grid(row=4, column=0, padx=4, pady=(0, 4), sticky=W)

        self.v_hud_enable.set(core.config.hud_enable)
        self.v_hud_weapon_sort.set(core.config.hud_weapon_sort)
        self.v_hud_active_first.set(core.config.hud_active_first)
        self.v_hud_active_only.set(core.config.hud_active_only)
        self.v_hud_gun_only.set(core.config.hud_gun_only)

        self.v_hud_enable.trace_add("write", self.v_hud_enable_callback)
        self.v_hud_weapon_sort.trace_add("write", self.v_hud_weapon_sort_callback)
        self.v_hud_active_first.trace_add("write", self.v_hud_active_first_callback)
        self.v_hud_active_only.trace_add("write", self.v_hud_active_only_callback)
        self.v_hud_gun_only.trace_add("write", self.v_hud_gun_only_callback)

    @once
    def build_hud_window(self):
        self.hud_window = ttkbootstrap.Toplevel()
        self.hud_window.overrideredirect(True)
        self.hud_window.resizable(width=False, height=False)
        self.hud_window.configure(bg="grey")
        self.hud_window.attributes("-transparentcolor", "grey")
        self.hud_window.attributes("-alpha", 0.5)
        self.hud_window.wm_attributes("-topmost", True)

        interface.methods.center_window_to_screen(self.hud_window, 600, 400, True)

        self.hud_window.grid_columnconfigure(9, weight=1)
        self.hud_window.grid_rowconfigure(9, weight=1)

        core.event.subscribe(constants.event.GSI_UPDATE, self.gsi_update)
        core.event.subscribe(constants.event.CONDITION_UPDATE, self.condition_update)

        for _ in range(10):
            v_ammo = ttkbootstrap.StringVar()
            v_weapon = ttkbootstrap.StringVar()
            hud_ammo = ttkbootstrap.Label(self.hud_window, textvariable=v_ammo)
            hud_weapon = ttkbootstrap.Label(self.hud_window, textvariable=v_weapon, background="White", foreground="Black")
            self.huds.append(HUDWeapon(v_ammo, v_weapon, hud_ammo, hud_weapon))

    def v_hud_enable_callback(self, *_) -> None:
        core.config.hud_enable = self.v_hud_enable.get()

    def v_hud_active_first_callback(self, *_)-> None:
        core.config.hud_active_first = self.v_hud_active_first.get()

    def v_hud_weapon_sort_callback(self, *_) -> None:
        core.config.hud_weapon_sort = self.v_hud_weapon_sort.get()

    def v_hud_gun_only_callback(self, *_) -> None:
        core.config.hud_gun_only = self.v_hud_gun_only.get()

    def v_hud_active_only_callback(self, *_) -> None:
        core.config.hud_active_only = self.v_hud_active_only.get()

    def __weapon_sort__(self, weapon: GameStatePlayerWeapon) -> int:
        match weapon.type:
            case "Rifle":
                return 0
            case "SniperRifle":
                return 0
            case "Submachine Gun":
                return 0
            case "Shotgun":
                return 0
            case "Machine Gun":
                return 0
            case "Pistol":
                return 1
            case "Knife":
                return 2
            case "":
                return 3
            case "Grenade":
                return 4
            case _:
                return 5

    def gsi_update(self) -> None:
        weapons = module.gsi.state.player.weapons
        active_weapon = module.gsi.state.player.active_weapon

        if not core.config.hud_enable:
            now_weapons = []

        elif core.config.hud_active_only:
            now_weapons = [active_weapon]

        else:
            now_weapons = [
                weapon for weapon in weapons.values()
                if not core.config.hud_active_first or weapon.name != active_weapon.name
                if not core.config.hud_gun_only or weapon.ammo_clip_max != 0
            ]

            if core.config.hud_weapon_sort:
                now_weapons.sort(key=self.__weapon_sort__)

            if core.config.hud_active_first:
                now_weapons.insert(0, active_weapon)

        now_amount = len(now_weapons)
        if now_amount > self.last_amount:
            for i in range(self.last_amount, now_amount):
                self.huds[i].hud_ammo.grid(row=20-i, column=10, sticky=E)
                self.huds[i].hud_weapon.grid(row=20-i, column=11, sticky=W, padx=(5, 0))

        elif now_amount < self.last_amount:
            for i in range(now_amount, self.last_amount):
                self.huds[i].hud_ammo.grid_forget()
                self.huds[i].hud_weapon.grid_forget()

        for i, weapon in enumerate(now_weapons[::-1]):
            weapon_name = i18n.ctrl.translation(f"ITEM.{weapon.name}") if weapon.name else "ITEM"
            self.huds[i].v_weapon.set(f" {weapon_name} ")
            self.huds[i].v_ammo.set(f" {weapon.ammo_clip:>3} | {weapon.ammo_reserve:>3} ")

            if weapon.state == constants.gsi.RELOADING:
                self.huds[i].hud_ammo.configure(background="Yellow", foreground="Black")
            elif weapon.ammo_clip == 0 and weapon.ammo_reserve != 0:
                self.huds[i].hud_ammo.configure(background="Chocolate", foreground="White")
            elif weapon.ammo_clip == 0:
                self.huds[i].hud_ammo.configure(background="FireBrick", foreground="White")
            elif weapon.ammo_clip < weapon.ammo_clip_max * 0.25:
                self.huds[i].hud_ammo.configure(background="Yellow", foreground="Black")
            else:
                self.huds[i].hud_ammo.configure(background="White", foreground="Black")

        self.last_amount = now_amount

    def condition_update(self) -> None:
        ...
