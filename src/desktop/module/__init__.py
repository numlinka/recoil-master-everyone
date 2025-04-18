# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
from typex import once

# internal
from . import _gsi


_activitys = [_gsi]

gsi: _gsi.GSI


@once
def initialize_first():
    for activity in _activitys:
        objective = getattr(activity, "initialize_first", None)
        objective() if callable(objective) else None


@once
def initialize_setup():
    global gsi
    gsi = _gsi.GSI()

    for activity in _activitys:
        objective = getattr(activity, "initialize_setup", None)
        objective() if callable(objective) else None


@once
def initialize_final():
    for activity in _activitys:
        objective = getattr(activity, "initialize_final", None)
        objective() if callable(objective) else None
