# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os

# size
import psutil
import ttkbootstrap

from typex import once
from ezudesign.utils import try_exec, exec_item
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

# local
import core
import module
import constants
import interface
from basic import i18n


class GSI (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.GSI)
        self.build()

    @once
    def build(self):
        self.v_port = ttkbootstrap.IntVar()
        self.v_timeout = ttkbootstrap.DoubleVar()
        self.v_buffer = ttkbootstrap.DoubleVar()
        self.v_throttle = ttkbootstrap.DoubleVar()
        self.v_heartbeat = ttkbootstrap.DoubleVar()

        self.setting = ttkbootstrap.Frame(self.frame)
        self.options = ttkbootstrap.Frame(self.frame)
        self.state = ttkbootstrap.Label(self.frame, text=i18n.UI.GSI_service_stop)

        self.options.pack(side=BOTTOM, fill=BOTH, padx=4, pady=4)
        self.state.pack(side=BOTTOM, fill=BOTH, padx=4, pady=4)
        self.setting.pack(side=TOP, fill=BOTH, padx=4, pady=4)

        self.label_port = ttkbootstrap.Label(self.setting, text=i18n.UI.GSI_port)
        self.label_timeout = ttkbootstrap.Label(self.setting, text=i18n.UI.GSI_timeout)
        self.label_buffer = ttkbootstrap.Label(self.setting, text=i18n.UI.GSI_buffer)
        self.label_throttle = ttkbootstrap.Label(self.setting, text=i18n.UI.GSI_throttle)
        self.label_heartbeat = ttkbootstrap.Label(self.setting, text=i18n.UI.GSI_heartbeat)
        self.spinbox_port = ttkbootstrap.Spinbox(self.setting, from_=1, to=65535, width=8, textvariable=self.v_port, justify=RIGHT)
        self.spinbox_timeout = ttkbootstrap.Spinbox(self.setting, from_=0.1, to=60, width=8, textvariable=self.v_timeout, increment=0.1, justify=RIGHT)
        self.spinbox_buffer = ttkbootstrap.Spinbox(self.setting, from_=0.1, to=60, width=8, textvariable=self.v_buffer, increment=0.1, justify=RIGHT)
        self.spinbox_throttle = ttkbootstrap.Spinbox(self.setting, from_=0.1, to=60, width=8, textvariable=self.v_throttle, increment=0.1, justify=RIGHT)
        self.spinbox_heartbeat = ttkbootstrap.Spinbox(self.setting, from_=0.1, to=60, width=8, textvariable=self.v_heartbeat, increment=0.1, justify=RIGHT)

        self.start_service = ttkbootstrap.Button(self.options, text=i18n.UI.GSI_start_service, bootstyle=OUTLINE, command=self.bin_start_service)
        self.apply_to_game = ttkbootstrap.Button(self.options, text=i18n.UI.GSI_apply_to_game, bootstyle=OUTLINE, command=self.bin_apply_to_game)

        self.label_port.grid(row=0, column=0, padx=4, pady=4, sticky=W)
        self.label_timeout.grid(row=1, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_buffer.grid(row=2, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_throttle.grid(row=3, column=0, padx=4, pady=(0, 4), sticky=W)
        self.label_heartbeat.grid(row=4, column=0, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_port.grid(row=0, column=1, padx=4, pady=4, sticky=W)
        self.spinbox_timeout.grid(row=1, column=1, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_buffer.grid(row=2, column=1, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_throttle.grid(row=3, column=1, padx=4, pady=(0, 4), sticky=W)
        self.spinbox_heartbeat.grid(row=4, column=1, padx=4, pady=(0, 4), sticky=W)

        self.start_service.pack(side=LEFT)
        self.apply_to_game.pack(side=LEFT, padx=(4, 0))

        self.v_port.set(core.config.gsi_port)
        self.v_timeout.set(core.config.gsi_timeout)
        self.v_buffer.set(core.config.gsi_buffer)
        self.v_throttle.set(core.config.gsi_throttle)
        self.v_heartbeat.set(core.config.gsi_heartbeat)
        self.v_port.trace_add("write", self.v_port_callback)

        core.event.subscribe(constants.event.GSI_START, self.state_update, (constants.event.GSI_START, ))
        core.event.subscribe(constants.event.GSI_STOP, self.state_update, (constants.event.GSI_STOP, ))
        core.event.subscribe(constants.event.GSI_ERROR, self.state_update, (constants.event.GSI_ERROR, ))

    def v_port_callback(self, *_):
        value = try_exec(exec_item(self.v_port.get))
        if not isinstance(value, int):
            return

        if value <= 1:
            self.v_port.set(1)

        elif value > 65535:
            self.v_port.set(65535)

    def state_update(self, event: str):
        match event:
            case constants.event.GSI_START:
                self.state.config(text=i18n.UI.GSI_service_running)
                self.state.config(bootstyle=SUCCESS)

            case constants.event.GSI_STOP:
                self.state.config(text=i18n.UI.GSI_service_stop)
                self.state.config(bootstyle=WARNING)

            case constants.event.GSI_ERROR:
                self.state.config(text=i18n.UI.GSI_service_error)
                self.state.config(bootstyle=DANGER)


    def bin_start_service(self, *_):
        value = try_exec(exec_item(self.v_port.get))

        if not isinstance(value, int) or not 1 <= value <= 65535:
            Messagebox.show_error(title=i18n.UI.GSI_port_error, message=i18n.UI.GSI_port_error_desc)
            return

        core.config.gsi_port = value
        core.taskpool.new_task(module.gsi.restart)


    def bin_apply_to_game(self, *_):
        s_port = try_exec(exec_item(self.v_port.get))
        s_timeout = try_exec(exec_item(self.v_timeout.get))
        s_buffer = try_exec(exec_item(self.v_buffer.get))
        s_throttle = try_exec(exec_item(self.v_throttle.get))
        s_heartbeat = try_exec(exec_item(self.v_heartbeat.get))

        if not isinstance(s_port, int) or not 1 <= s_port <= 65535:
            Messagebox.show_error(title=i18n.UI.GSI_port_error, message=i18n.UI.GSI_port_error_desc)
            return

        for value in (s_timeout, s_buffer, s_throttle, s_heartbeat):
            if not isinstance(value, float) or value <= 0:
                Messagebox.show_error(title=i18n.UI.GSI_value_error, message=i18n.UI.GSI_value_error_desc)
                return

        core.config.gsi_port = s_port
        core.config.gsi_timeout = round(s_timeout, 1)
        core.config.gsi_buffer = round(s_buffer, 1)
        core.config.gsi_throttle = round(s_throttle, 1)
        core.config.gsi_heartbeat = round(s_heartbeat, 1)

        for process in psutil.process_iter():
            if process.name() == "cs2.exe":
                break

        else:
            Messagebox.show_error(title=i18n.UI.GSI_game_not_run, message=i18n.UI.GSI_game_not_run_desc)
            return

        game_file_path = process.exe()
        game_cwd = os.path.dirname(game_file_path)
        path = os.path.join(game_cwd, "..", "..", "csgo", "cfg", "gamestate_integration_consolesample.cfg")
        path = os.path.abspath(path)
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                content = constants.lt.CS2_GSI_CFG_TEMPLATE
                content = content.replace("<$PORT>", str(s_port))
                content = content.replace("<$TIMEOUT>", str(core.config.gsi_timeout))
                content = content.replace("<$BUFFER>", str(core.config.gsi_buffer))
                content = content.replace("<$THROTTLE>", str(core.config.gsi_throttle))
                content = content.replace("<$HEARTBEAT>", str(core.config.gsi_heartbeat))
                file.write(content)

        except Exception as _:
            Messagebox.show_error(title=i18n.UI.GSI_game_cfg_error, message=i18n.UI.GSI_game_cfg_error_desc)
            return

        Messagebox.show_info(title=i18n.UI.GSI_game_cfg_success, message=i18n.UI.GSI_game_cfg_success_desc)
