# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
from dataclasses import dataclass

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import core
import module
import constants
from basic import i18n


class Engine (object):
    def __init__(self, notebook: ttkbootstrap.Notebook):
        self.notebook = notebook
        self.frame = ttkbootstrap.Frame(notebook)
        notebook.add(self.frame, text=i18n.UI.recoil_engine)
        self.available_engines = []
        self.build()

    @once
    def build (self):
        self.v_engine = ttkbootstrap.StringVar()

        self.combobox = ttkbootstrap.Combobox(self.frame, textvariable=self.v_engine, state=READONLY)
        self.label = ttkbootstrap.Label(self.frame, text="...")
        self.frame_options = ttkbootstrap.Frame(self.frame)
        self.button_run = ttkbootstrap.Button(self.frame_options, text=i18n.UI.recoil_run, bootstyle=(SUCCESS, OUTLINE), command=module.assistance.mouse.run)
        self.button_stop = ttkbootstrap.Button(self.frame_options, text=i18n.UI.recoil_stop, bootstyle=(DANGER, OUTLINE), command=module.assistance.mouse.stop)

        self.combobox.pack(side=TOP, fill=X, padx=5, pady=5)
        self.frame_options.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        self.label.pack(side=BOTTOM, fill=X, padx=5)
        self.button_run.pack(side=LEFT)
        self.button_stop.pack(side=LEFT, padx=(5, 0))

        self.v_engine.set(core.config.assistance_mouse)
        self.v_engine.trace_add("write", self.v_engine_callback)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_callback, add=True)
        core.event.subscribe(constants.event.ASSISTANCE_MOUSE_UPDATE, self.on_tab_callback, async_=True)

    def v_engine_callback(self, *_):
        engine_name = self.v_engine.get()
        if engine_name not in self.available_engines:
            self.combobox.config(bootstyle=DANGER)
        else:
            self.combobox.config(bootstyle=NORMAL)
            core.config.assistance_mouse.set(engine_name)

    def on_tab_callback(self, *_):
        self.available_engines.clear()

        if self.notebook.select() == str(self.frame):
            for name in os.listdir(core.cwd.assistance.mouse):
                path = os.path.join(core.cwd.assistance.mouse, name)
                if os.path.isfile(path) and path.endswith(".exe"):
                    self.available_engines.append(name[:-4])

        if module.assistance.mouse.is_alive:
            self.label.config(text=i18n.UI.recoil_service_running, bootstyle=SUCCESS)
        else:
            self.label.config(text=i18n.UI.recoil_service_stop, bootstyle=DANGER)

        self.combobox.config(values=self.available_engines)
        self.v_engine_callback()
