# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
from tkinter import TclError
from dataclasses import dataclass

# size
import psutil
import ttkbootstrap

from typex import once
from ezudesign.utils import try_exec, exec_item
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ezudesign.configuration import ConfigurationBaseException

# local
import core
import module
import constants
import interface
from basic import i18n


@dataclass
class NumberWidget:
    variable: ttkbootstrap.IntVar
    label: ttkbootstrap.Label
    spinbox: ttkbootstrap.Spinbox


class GSI (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.gsi)
        self.number_settings: dict[str, NumberWidget] = {}
        self.build()

    @once
    def build(self):
        self.setting = ttkbootstrap.Frame(self.frame)
        self.options = ttkbootstrap.Frame(self.frame)
        self.state = ttkbootstrap.Label(self.frame, text=i18n.UI.gsi_service_stop)

        self.options.pack(side=BOTTOM, fill=BOTH, padx=4, pady=4)
        self.state.pack(side=BOTTOM, fill=BOTH, padx=4, pady=4)
        self.setting.pack(side=TOP, fill=BOTH, padx=4, pady=4)

        number_settings = [
            core.config.gsi_port.name,
            core.config.gsi_timeout.name,
            core.config.gsi_buffer.name,
            core.config.gsi_throttle.name,
            core.config.gsi_heartbeat.name
        ]

        for index, name in enumerate(number_settings):
            variable = ttkbootstrap.IntVar() if core.config[name].types is int else ttkbootstrap.DoubleVar()
            label = ttkbootstrap.Label(self.setting, text=i18n.UI[name])
            increment = 1 / (10 ** core.config[name].ranges.round)
            spinbox = ttkbootstrap.Spinbox(
                self.setting,
                from_=core.config[name].ranges.min,
                to=core.config[name].ranges.max,
                textvariable=variable,
                increment=increment,
                width=8,
                justify=RIGHT
            )
            self.number_settings[name] = NumberWidget(variable, label, spinbox)
            label.grid(row=index, column=0, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            spinbox.grid(row=index, column=1, padx=5, pady=(0 if index != 0 else 5, 5), sticky=W)
            variable.set(core.config[name])
            variable.trace_add("write", self.number_settings_update)

        self.start_service = ttkbootstrap.Button(self.options, text=i18n.UI.gsi_start_service, bootstyle=OUTLINE, command=self.bin_start_service)
        self.apply_to_game = ttkbootstrap.Button(self.options, text=i18n.UI.gsi_apply_to_game, bootstyle=OUTLINE, command=self.bin_apply_to_game)

        self.start_service.pack(side=LEFT)
        self.apply_to_game.pack(side=LEFT, padx=(4, 0))

        core.event.subscribe(constants.event.GSI_START, self.state_update, (constants.event.GSI_START, ))
        core.event.subscribe(constants.event.GSI_STOP, self.state_update, (constants.event.GSI_STOP, ))
        core.event.subscribe(constants.event.GSI_ERROR, self.state_update, (constants.event.GSI_ERROR, ))

    def state_update(self, event: str):
        match event:
            case constants.event.GSI_START:
                self.state.config(text=i18n.UI.gsi_service_running)
                self.state.config(bootstyle=SUCCESS)

            case constants.event.GSI_STOP:
                self.state.config(text=i18n.UI.gsi_service_stop)
                self.state.config(bootstyle=WARNING)

            case constants.event.GSI_ERROR:
                self.state.config(text=i18n.UI.gsi_service_error)
                self.state.config(bootstyle=DANGER)

    def number_settings_update(self, *_, value_error: bool = False) -> bool:
        for name, widget in self.number_settings.items():
            try:
                core.config[name] = widget.variable.get()
            except (ConfigurationBaseException, TclError) as _:
                widget.spinbox.configure(bootstyle=DANGER)
                if value_error:
                    if name == core.config.gsi_port.name:
                        Messagebox.show_error(title=i18n.UI.gsi_port_error, message=i18n.UI.gsi_port_error_desc)
                        return True

                    else:
                        Messagebox.show_error(title=i18n.UI.gsi_value_error, message=i18n.UI.gsi_value_error_desc)
                        return True

            else:
                widget.spinbox.configure(bootstyle=NORMAL)

        return False

    def bin_start_service(self, *_):
        if self.number_settings_update(value_error=True):
            return

        core.taskpool.new_task(module.gsi.restart)

    def bin_apply_to_game(self, *_):
        if self.number_settings_update(value_error=True):
            return

        s_port = core.config.gsi_port
        s_timeout = core.config.gsi_timeout
        s_buffer = core.config.gsi_buffer
        s_throttle = core.config.gsi_throttle
        s_heartbeat = core.config.gsi_heartbeat

        core.config.gsi_port = s_port
        core.config.gsi_timeout = round(s_timeout, 1)
        core.config.gsi_buffer = round(s_buffer, 1)
        core.config.gsi_throttle = round(s_throttle, 1)
        core.config.gsi_heartbeat = round(s_heartbeat, 1)

        for process in psutil.process_iter():
            if process.name() == constants.CS2_EXE:
                break

        else:
            Messagebox.show_error(title=i18n.UI.gsi_game_not_run, message=i18n.UI.gsi_game_not_run_desc)
            return

        game_file_path = process.exe()
        game_cwd = os.path.dirname(game_file_path)
        path = os.path.join(game_cwd, "..", "..", "csgo", "cfg", "gamestate_integration_consolesample.cfg")
        path = os.path.abspath(path)
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                content = constants.lt.CS2_gsi_CFG_TEMPLATE
                content = content.replace("<$PORT>", str(s_port))
                content = content.replace("<$TIMEOUT>", str(core.config.gsi_timeout))
                content = content.replace("<$BUFFER>", str(core.config.gsi_buffer))
                content = content.replace("<$THROTTLE>", str(core.config.gsi_throttle))
                content = content.replace("<$HEARTBEAT>", str(core.config.gsi_heartbeat))
                file.write(content)

        except Exception as _:
            Messagebox.show_error(title=i18n.UI.gsi_game_cfg_error, message=i18n.UI.gsi_game_cfg_error_desc)
            return

        Messagebox.show_info(title=i18n.UI.gsi_game_cfg_success, message=i18n.UI.gsi_game_cfg_success_desc)
