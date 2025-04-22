# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
from typex import once

# internal
from . import _gsi
from . import _weapon


_activitys = [_gsi]

gsi: _gsi.GSI
weapon: _weapon.Weapon


@once
def initialize_first():
    for activity in _activitys:
        objective = getattr(activity, "initialize_first", None)
        objective() if callable(objective) else None


@once
def initialize_setup():
    global gsi, weapon
    gsi = _gsi.GSI()
    weapon = _weapon.Weapon()

    for activity in _activitys:
        objective = getattr(activity, "initialize_setup", None)
        objective() if callable(objective) else None


@once
def initialize_final():
    weapon.load("weapon_ak47")
    print(weapon.mouse_tracks)
    for activity in _activitys:
        objective = getattr(activity, "initialize_final", None)
        objective() if callable(objective) else None
