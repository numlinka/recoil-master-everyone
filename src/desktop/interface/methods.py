# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

import tkinter

import core
import interface


def save_mainwindow_state(*_):
    core.config.window_width = interface.mainwindow.winfo_width()
    core.config.window_height = interface.mainwindow.winfo_height()
    core.config.window_x = interface.mainwindow.winfo_x()
    core.config.window_y = interface.mainwindow.winfo_y()


def load_mainwindow_state(*_):
    width = core.config.window_width if core.config.window_width <= 0 else 650
    height = core.config.window_height if core.config.window_height <= 0 else 450
    interface.mainwindow.geometry(f"{width}x{height}")

    if core.config.window_x < 0 or core.config.window_y < 0:
        center_window_to_screen(interface.mainwindow, width, height)
        return

    interface.mainwindow.geometry(f"+{core.config.window_x}+{core.config.window_y}")


def center_window_to_screen(window: tkinter.Misc, width: int = None, height: int = None, set_size: bool = False):
    width = width or window.winfo_width()
    height = height or window.winfo_height()
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()

    x = int((screenwidth / 2) - (width / 2))
    y = int((screenheight / 2) - (height / 2))

    window.geometry(f"+{x}+{y}")
