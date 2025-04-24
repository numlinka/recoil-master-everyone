# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import time
import threading
from dataclasses import dataclass

# site
import psutil
import win32gui
import win32process

from  typex import once

# local
import core
import module
import constants
import assistance


class Condition (object):
    def __init__(self):
        self._lock = threading.RLock()
        self._last_condition = False
        self._last_active = ""
        self._effective_weapons = []
        self._invalid_weapons = []
        self._last_taracks = ""

    def __check_active_process_name(self):
        while True:
            try:
                time.sleep(0.5)
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                self.active_update(process.name())

            except Exception as _:
                ...

    def new_condition(self):
        with self._lock:
            # 焦点程序不是 CS2
            if self._last_active != constants.CS2_EXE:
                return False

        # 焦点玩家不是自己
        if module.gsi.state.player.steamid != module.gsi.state.provider.steamid:
            return False

        # 武器不在有效列表中
        if module.gsi.state.player.active_weapon.name not in self._effective_weapons:
            weapon_name = module.gsi.state.player.active_weapon.name
            if module.weapon.load(weapon_name):
                self._effective_weapons.append(weapon_name)

            else:
                return False

        # 武器在装填中
        if module.gsi.state.player.active_weapon.state == constants.gsi.RELOADING:
            return False

        # 武器没子弹
        if module.gsi.state.player.active_weapon.ammo_clip == 0:
            return False

        weapon_name = module.gsi.state.player.active_weapon.name
        module.weapon.load(weapon_name)
        mouse_tracks = module.weapon.mouse_tracks
        if mouse_tracks != self._last_taracks:
            self._last_taracks = mouse_tracks
            assistance.command.tracks(mouse_tracks)

        return True

    def active_update(self, process_name: str):
        with self._lock:
            if process_name != self._last_active:
                self._last_active = process_name
                self.status_update()

            self._last_active = process_name

    def status_update(self):
        condition = self.new_condition()
        if condition != self._last_condition:
            self._last_condition = condition
            assistance.command.condition(condition)

    @once
    def build(self):
        threading.Thread(None, self.__check_active_process_name, "ActiveWindowCheck", daemon=True).start()


@once
def initialize_first():
    ...

@once
def initialize_setup():
    ...

@once
def initialize_final():
    module.condition.build()
    core.event.subscribe(constants.event.GSI_UPDATE, module.condition.status_update)
