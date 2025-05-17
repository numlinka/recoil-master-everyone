# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import tkinter

# site
import ttkbootstrap

from typex import once
from ezudesign.utils import try_exec, exec_item
from ttkbootstrap.constants import *

# local
import env
import core
import constants

# internal
from . import _slogan
from . import _disclaimer
from . import _gsi
from . import _hud
from . import _recoil
from . import _anti
from . import _setting
from . import _license
from . import methods

_activitys = [ _hud, _recoil]

mainwindow: ttkbootstrap.Window
style: ttkbootstrap.Style
notebook: ttkbootstrap.Notebook
slogan: _slogan.Slogan
disclaimer: _disclaimer.Disclaimer
gsi: _gsi.GSI
hud: _hud.HUD
recoil: _recoil.Recoil
# anti: _anti.Anti
setting: _setting.Setting
licenses: _license.License


def set_theme(theme_name: str) -> None:
    try_exec(exec_item(style.theme_use, theme_name))
    try_exec(exec_item("hud.hud_window.configure", bg="grey"))


@once
def initialize_first():
    global mainwindow, style, notebook

    mainwindow = ttkbootstrap.Window()
    style = ttkbootstrap.Style()
    set_theme(core.config.theme)
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
    global slogan, disclaimer, gsi, hud, recoil, setting, licenses
    slogan = _slogan.Slogan()
    disclaimer = _disclaimer.Disclaimer()
    gsi = _gsi.GSI()
    hud = _hud.HUD()
    recoil = _recoil.Recoil()
    # anti = _anti.Anti()
    setting = _setting.Setting()
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
