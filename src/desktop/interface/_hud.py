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

    @once
    def build(self):
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
            case _:
                return 2

    def gsi_update(self) -> None:
        weapons = module.gsi.state.player.weapons
        active_weapon = module.gsi.state.player.active_weapon
        now_weapons = [weapon for weapon in weapons.values() if weapon.name != active_weapon.name if weapon.ammo_clip_max != 0]
        now_weapons.sort(key=self.__weapon_sort__)
        now_weapons.insert(0, active_weapon)
        now_amount = len(now_weapons)
        if now_amount > self.last_amount:
            for i in range(self.last_amount, now_amount):
                self.huds[i].hud_ammo.grid(row=i+10, column=10, sticky=E)
                self.huds[i].hud_weapon.grid(row=i+10, column=11, sticky=W, padx=(5, 0))

        elif now_amount < self.last_amount:
            for i in range(now_amount, self.last_amount):
                self.huds[i].hud_ammo.grid_forget()
                self.huds[i].hud_weapon.grid_forget()

        for i, weapon in enumerate(now_weapons):
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
