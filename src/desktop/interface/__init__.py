# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import env
import core
import constants

# internal
from . import _slogan
from . import _gsi
from . import _hud
from . import _recoil
from . import _anti
from . import _license
from . import methods

_activitys = [ _hud, _recoil]

mainwindow: ttkbootstrap.Window
style: ttkbootstrap.Style
notebook: ttkbootstrap.Notebook
slogan: _slogan.Slogan
gsi: _gsi.GSI
hud: _hud.HUD
recoil: _recoil.Recoil
anti: _anti.Anti
licenses: _license.License


@once
def initialize_first():
    global mainwindow, style, notebook

    mainwindow = ttkbootstrap.Window()
    style = ttkbootstrap.Style()
    style.theme_use("darkly")
    mainwindow.title(env.MAIN_TITLE)
    methods.load_mainwindow_state()
    methods.set_window_icon_from_base64(mainwindow, constants.media.favicon)

    notebook = ttkbootstrap.Notebook(mainwindow)
    notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

    for activity in _activitys:
        objective = getattr(activity, "initialize_first", None)
        objective() if callable(objective) else None


@once
def initialize_setup():
    global slogan, gsi, hud, recoil, anti, licenses
    slogan = _slogan.Slogan()
    gsi = _gsi.GSI()
    hud = _hud.HUD()
    recoil = _recoil.Recoil()
    anti = _anti.Anti()
    licenses = _license.License()

    for activity in _activitys:
        objective = getattr(activity, "initialize_setup", None)
        objective() if callable(objective) else None


@once
def initialize_final():
    mainwindow.protocol("WM_DELETE_WINDOW", core.action.exit)
    core.action.exit.add_task(methods.save_mainwindow_state, 4800)
    core.action.exit.add_task(mainwindow.destroy, 5000)

    for activity in _activitys:
        objective = getattr(activity, "initialize_final", None)
        objective() if callable(objective) else None
