# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import ctypes
from tkinter import TclError
from dataclasses import dataclass, field

# size
import ttkbootstrap

from typex import Singleton, once
from ttkbootstrap.constants import *
from ezudesign.configuration import ConfigurationBaseException

# local
import core
import module
import interface
import constants

from basic import i18n
from typeins import GameStatePlayerWeapon


@dataclass
class HUDWeapon:
    v_ammo: ttkbootstrap.StringVar = field(default=None)
    v_weapon: ttkbootstrap.StringVar = field(default=None)
    hud_ammo: ttkbootstrap.Label = field(default=None)
    hud_weapon: ttkbootstrap.Label = field(default=None)


@dataclass
class NumberWidget:
    variable: ttkbootstrap.IntVar = field(default=None)
    label: ttkbootstrap.Label = field(default=None)
    spinbox: ttkbootstrap.Spinbox = field(default=None)


@dataclass
class SwitchWidget:
    variable: ttkbootstrap.BooleanVar = field(default=None)
    checkbutton: ttkbootstrap.Checkbutton = field(default=None)


class HUD (Singleton):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.hud)
        self.huds: list[HUDWeapon] = []
        self.number_settings: dict[str, NumberWidget] = {}
        self.switch_settings: dict[str, SwitchWidget] = {}
        self.last_amount = 0
        self.build()
        self.build_hud_window()
        self.number_settings_update()

    @once
    def build(self):
        number_settings = [
            core.config.hud_alpha.name,
            core.config.hud_width.name,
            core.config.hud_height.name
        ]

        for index, name in enumerate(number_settings):
            variable = ttkbootstrap.IntVar()
            label = ttkbootstrap.Label(self.frame, text=i18n.UI[name])
            spinbox = ttkbootstrap.Spinbox(
                self.frame,
                from_=core.config[name].ranges.min,
                to=core.config[name].ranges.max,
                textvariable=variable,
                width=8,
                justify=RIGHT
            )
            self.number_settings[name] = NumberWidget(variable, label, spinbox)
            label.grid(row=index, column=0, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            spinbox.grid(row=index, column=1, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            variable.set(core.config[name])
            variable.trace_add("write", self.number_settings_update)

        row_plus = index + 1

        switch_settings = [
            core.config.hud_enable.name,
            core.config.hud_weapon_sort.name,
            core.config.hud_active_first.name,
            core.config.hud_active_only.name,
            core.config.hud_gun_only.name
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
            checkbutton.grid(row=row_plus+index, column=0, padx=5, pady=(5, 5), sticky=W, columnspan=2)
            variable.set(core.config[name])
            variable.trace_add("write", self.switch_settings_update)

    @once
    def build_hud_window(self):
        self.hud_window = ttkbootstrap.Toplevel()
        self.hud_window.overrideredirect(True)
        self.hud_window.resizable(width=False, height=False)
        self.hud_window.configure(bg="grey")
        self.hud_window.attributes("-transparentcolor", "grey")
        self.hud_window.attributes("-alpha", core.config.hud_alpha / 100)
        self.hud_window.wm_attributes("-topmost", True)

        # interface.methods.center_window_to_screen(self.hud_window, 600, 400, True)

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

    @once
    def set_click_through(self) -> None:
        user32 = ctypes.WinDLL("user32")
        # self.hud_window.update_idletasks()  # ? This line is not needed, as the window is already created.
        hwnd = user32.GetParent(self.hud_window.winfo_id())
        style = user32.GetWindowLongPtrW(hwnd, -20)
        user32.SetWindowLongPtrW(hwnd, -20, style | 0x00000020 | 0x00080000)

    def number_settings_update(self, *_) -> None:
        for name, numberwidget in self.number_settings.items():
            try:
                core.config[name] = numberwidget.variable.get()
            except (ConfigurationBaseException, TclError) as _:
                numberwidget.spinbox.configure(bootstyle=DANGER)
            else:
                numberwidget.spinbox.configure(bootstyle=NORMAL)

        interface.methods.center_window_to_screen(self.hud_window, core.config.hud_width, core.config.hud_height, True)
        self.hud_window.attributes("-alpha", core.config.hud_alpha / 100)

    def switch_settings_update(self, *_) -> None:
        for name, switchwidget in self.switch_settings.items():
            core.config[name] = switchwidget.variable.get()

    def _weapon_sort_key(self, weapon: GameStatePlayerWeapon) -> int:
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
                now_weapons.sort(key=self._weapon_sort_key)

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
            weapon_name = i18n.ITEM[weapon.name] if weapon.name else "ITEM"
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


def initialize_final() -> None:
    core.event.subscribe(constants.event.ENTER_MAINLOOP, HUD().set_click_through)
