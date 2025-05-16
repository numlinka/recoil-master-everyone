# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import interface
from basic import i18n

# internal
from . import _engine
from . import _recoil
from . import _weapon

_activitys = [_weapon]


class Recoil (object):
    def __init__ (self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.recoil)
        self.build()

    def build (self):
        self.notebook = ttkbootstrap.Notebook(self.frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.engine = _engine.Engine(self.notebook)
        self.recoil = _recoil.Recoil(self.notebook)
        self.weapon = _weapon.Weapon(self.notebook)


@once
def initialize_first():
    for activity in _activitys:
        objective = getattr(activity, "initialize_first", None)
        objective() if callable(objective) else None


@once
def initialize_setup():
    for activity in _activitys:
        objective = getattr(activity, "initialize_setup", None)
        objective() if callable(objective) else None


@once
def initialize_final():
    for activity in _activitys:
        objective = getattr(activity, "initialize_final", None)
        objective() if callable(objective) else None
