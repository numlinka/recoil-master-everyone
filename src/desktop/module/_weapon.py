# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import json
import threading

from typing import Iterable
from dataclasses import dataclass

# local
import core

from basic import cwd
from typeins import WeaponOffsets



@dataclass
class LastConfig (object):
    recoil_sensitivity: float = 0.0
    recoil_horizontal: float = 0.0
    recoil_vertical: float = 0.0
    recoil_leading_delay: float = 0.0
    recoil_duty_cycle: float = 0.0


class Weapon (object):
    def __init__ (self) -> None:
        self._lock = threading.RLock()
        self._rpm = 0  # repeat per minute
        self._foe = 0  # fires once every
        self._original_offsets: Iterable[Iterable[int, int]] = []
        self._original_offsets_changed = False
        self._offsets: Iterable[tuple[int, int]] = []
        self._offsets_changed = False
        self._tracks: Iterable[tuple[int, int]] = []
        self._last = LastConfig()

    def load(self, weapon_name: str) -> bool:
        if not weapon_name:
            return False

        file_path = os.path.join(cwd.assets.weapons, f"{weapon_name}.json")

        if not os.path.isfile(file_path):
            return False

        with open(file_path, "r", encoding="utf-8") as file:
            data: WeaponOffsets = json.load(file)

        with self._lock:
            if (self._rpm, self._foe, self._original_offsets) == (data["RPM"], data["FOE"], data["offsets"]):
                return True

            self._rpm = data["RPM"]
            self._foe = data["FOE"]
            self._original_offsets = data["offsets"]
            self._original_offsets_changed = True

        self.calculate_offsets()
        return True

    def calculate_offsets(self) -> None:
        with self._lock:
            if (not self._original_offsets_changed and
                (core.config.recoil_sensitivity, core.config.recoil_horizontal, core.config.recoil_vertical) ==
                (self._last.recoil_sensitivity, self._last.recoil_horizontal, self._last.recoil_vertical)):
                return

            rel_x = [i[0] for i in self._original_offsets]
            rel_y = [i[1] for i in self._original_offsets]

            abs_x = [sum(rel_x[:i + 1]) for i in range(len(rel_x))]
            abs_y = [sum(rel_y[:i + 1]) for i in range(len(rel_y))]

            xp = 2 / core.config.recoil_sensitivity * core.config.recoil_horizontal
            yp = 2 / core.config.recoil_sensitivity * core.config.recoil_vertical

            co_abs_x = [round(x * xp) for x in abs_x]
            co_abs_y = [round(y * yp) for y in abs_y]

            co_rel_x = [x if i == 0 else co_abs_x[i] - co_abs_x[i-1] for i, x in enumerate(co_abs_x)]
            co_rel_y = [y if i == 0 else co_abs_y[i] - co_abs_y[i-1] for i, y in enumerate(co_abs_y)]

            self._offsets = list(zip(co_rel_x, co_rel_y))
            self._offsets_changed = True
            self._original_offsets_changed = False
            self._last.recoil_sensitivity = core.config.recoil_sensitivity
            self._last.recoil_horizontal = core.config.recoil_horizontal
            self._last.recoil_vertical = core.config.recoil_vertical

    def calculate_mouse_tracks(self) -> Iterable[tuple[int, int]]:
        with self._lock:
            if (not self._offsets_changed and
                (core.config.recoil_leading_delay, core.config.recoil_duty_cycle) ==
                (self._last.recoil_leading_delay, self._last.recoil_duty_cycle)):
                return self._tracks

            ticks_cycle = round(self._foe / 5)
            lead_tick = round(core.config.recoil_leading_delay * self._foe / 5)
            duty_tick = round(core.config.recoil_duty_cycle * self._foe / 5)
            idle_tick = ticks_cycle - duty_tick

            tracks = []
            tracks.extend([(0, 0)] * lead_tick)

            for index, offset in enumerate(self._offsets):
                if index != 0:
                    tracks.extend([(0, 0)] * idle_tick)

                tracks.extend(zip(distribute(offset[0], duty_tick), distribute(offset[1], duty_tick)))

            self._tracks = tracks
            self._offsets_changed = False
            self._last.recoil_leading_delay = core.config.recoil_leading_delay
            self._last.recoil_duty_cycle = core.config.recoil_duty_cycle

        return tracks

    @property
    def mouse_tracks (self) -> str:
        tracks = self.calculate_mouse_tracks()
        return ",".join([f"{x},{y}" for x, y in tracks])


def distribute(original: int, length: int) -> list[int]:
    average, residue = divmod(abs(original), length)

    if original >= 0:
        return [average + 1] * residue + [average] * (length - residue)

    return [-(average + 1)] * residue + [-average] * (length - residue)
