# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import time
import json
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

# site
from typex import once

# local
import core
import module
import constants
from typeins import GameState, GameStatePlayerWeapon


class GSI (object):
    def __init__(self):
        self._lock = threading.RLock()
        self.state = GameState()
        self.__service: HTTPServer = None
        self.__thread: threading.Thread = None

    def __run(self):
        try:
            self.__service = HTTPServer(("localhost", core.config.gsi_port), GSIHTTPRequestHandler)
            core.event.emit(constants.event.GSI_START)
            self.__service.serve_forever()

        except Exception as _:
            core.event.emit(constants.event.GSI_ERROR)

        else:
            core.event.emit(constants.event.GSI_STOP)

    def dataclass_update(self, dataclass, data: dict) -> None:
        for key, value in data.items():
            if not hasattr(dataclass, key):
                continue

            elif key == "weapons":
                self.state.player.weapons = {
                    weapon_num: GameStatePlayerWeapon(**weapon_data)
                    for weapon_num, weapon_data in value.items()
                }
                continue

            elif isinstance(value, dict):
                self.dataclass_update(getattr(dataclass, key), value)
                continue

            setattr(dataclass, key, value)

    def update(self, data: dict):
        self.dataclass_update(self.state, data)
        core.event.emit(constants.event.GSI_UPDATE)

    def stop(self) -> None:
        with self._lock:
            if self.__service is None:
                return

            if self.__thread is None or not self.__thread.is_alive():
                return

            self.__service.shutdown()
            self.__service.server_close()
            self.__thread.join()
            self.__service = None
            self.__thread = None

    def start(self) -> None:
        with self._lock:
            if self.__thread is not None and self.__thread.is_alive():
                return

            self.__thread = threading.Thread(None, self.__run, "GSI", (), daemon=True)
            self.__thread.start()

    def restart(self) -> None:
        with self._lock:
            self.stop()
            time.sleep(0.5)
            self.start()


class GSIHTTPRequestHandler (BaseHTTPRequestHandler):
    def callback(self, *_): ...

    def log_message(self, *_): ...

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            module.gsi.update_state(data)

        except Exception:
            ...

        finally:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GSI data received.")


@once
def initialize_final():
    core.event.subscribe(constants.event.ENTER_MAINLOOP, module.gsi.start, async_=True)
