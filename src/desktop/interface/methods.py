# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import base64
import tkinter
from io import BytesIO

# site
from PIL import Image, ImageTk

# local
import core
import interface
from basic import cwd


def save_mainwindow_state(*_) -> None:
    core.config.window_width = interface.mainwindow.winfo_width()
    core.config.window_height = interface.mainwindow.winfo_height()
    core.config.window_x = interface.mainwindow.winfo_x()
    core.config.window_y = interface.mainwindow.winfo_y()


def load_mainwindow_state(*_) -> None:
    width = core.config.window_width if core.config.window_width > 0 else 650
    height = core.config.window_height if core.config.window_height > 0 else 450
    interface.mainwindow.geometry(f"{width}x{height}")

    if core.config.window_x < 0 or core.config.window_y < 0:
        center_window_to_screen(interface.mainwindow, width, height)
        return

    interface.mainwindow.geometry(f"+{core.config.window_x}+{core.config.window_y}")


def center_window_to_screen(window: tkinter.Misc, width: int = None, height: int = None, set_size: bool = False) -> None:
    width = width or window.winfo_width()
    height = height or window.winfo_height()
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()

    x = int((screenwidth / 2) - (width / 2))
    y = int((screenheight / 2) - (height / 2))

    if not set_size:
        window.geometry(f"+{x}+{y}")
        return

    window.geometry(f"{width}x{height}+{x}+{y}")


def set_window_icon_from_base64(window: tkinter.Wm, base64_string: str) -> bool:
    try:
        image_data = base64.b64decode(base64_string)
        image_file_like = BytesIO(image_data)
        icon_image = Image.open(image_file_like)
        tk_icon = ImageTk.PhotoImage(icon_image)
        window.iconphoto(False, tk_icon)
        window.iconphoto(True, tk_icon)
        return True

    except Exception as _:
        return False
