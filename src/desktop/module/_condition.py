# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import time
import threading
from typing import NoReturn

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
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._last_condition = False
        self._active_window = ""
        self._effective_weapons = []
        self._invalid_weapons = []
        self._last_taracks = ""

    def __check_active_process_name(self) -> NoReturn:
        while True:
            try:
                time.sleep(0.5)
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                self.active_update(process.name())

            except Exception as _:
                ...

    def set_effective_weapons(self, weapons: list[str]) -> None:
        with self._lock:
            self._effective_weapons = weapons

    def new_condition(self) -> bool:
        state = module.gsi.state

        with self._lock:
            if self._active_window != constants.CS2_EXE:
                return False

            if state.player.active_weapon.name not in self._effective_weapons:
                return False

            if state.player.active_weapon.name in self._invalid_weapons:
                return False

        if state.player.steamid != state.provider.steamid:
            return False

        if state.player.active_weapon.state == constants.gsi.RELOADING:
            return False

        if state.player.active_weapon.ammo_clip == 0:
            return False

        weapon_name = state.player.active_weapon.name
        module.weapon.load(weapon_name)
        mouse_tracks = module.weapon.mouse_tracks

        with self._lock:
            if mouse_tracks == self._last_taracks:
                return True

            self._last_taracks = mouse_tracks

        assistance.command.tracks(mouse_tracks)
        return True

    def active_update(self, process_name: str) -> None:
        with self._lock:
            if process_name != self._active_window:
                self._active_window = process_name
                self.status_update()

            self._active_window = process_name

    def status_update(self) -> None:
        condition = self.new_condition()
        if condition == self._last_condition:
            return

        self._last_condition = condition
        assistance.command.condition(condition)

    @once
    def build(self):
        threading.Thread(None, self.__check_active_process_name, "ActiveWindowCheck", daemon=True).start()


@once
def initialize_final():
    module.condition.build()
    core.event.subscribe(constants.event.GSI_UPDATE, module.condition.status_update)
