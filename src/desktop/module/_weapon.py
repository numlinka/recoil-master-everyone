# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import json

from typing import Iterable

# local
import core

from basic import cwd
from typeins import WeaponOffsets


class Weapon (object):
    def __init__ (self) -> None:
        self._rpm = 0  # repeat per minute
        self._foe = 0  # fires once every
        self._original_offsets: Iterable[Iterable[int, int]] = []
        self._offsets: Iterable[tuple[int, int]] = []

    def load(self, weapon_name: str) -> bool:
        if not weapon_name:
            return False

        file_path = os.path.join(cwd.assets.weapons, f"{weapon_name}.json")

        if not os.path.isfile(file_path):
            return False

        with open(file_path, "r", encoding="utf-8") as file:
            data: WeaponOffsets = json.load(file)

        self._rpm = data["RPM"]
        self._foe = data["FOE"]
        self._original_offsets = data["offsets"]

        self.calculate_offsets()
        return True

    def calculate_offsets(self) -> None:
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

    def calculate_mouse_tracks(self) -> Iterable[tuple[int, int]]:
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
