# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import threading
import subprocess

from typing import Optional

# site
from typex import once, Singleton

# local
import core
import constants
from basic import cwd


class AssistanceMouse (object):
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._popen: Optional[subprocess.Popen] = None

    @property
    def is_alive(self) -> bool:
        with self._lock:
            return isinstance(self._popen, subprocess.Popen) and self._popen.poll() is None

    def run(self) -> bool:
        with self._lock:
            if self.is_alive:
                return False

            path = os.path.join(cwd.assistance.mouse, f"{core.config.assistance_mouse}.exe")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._popen = subprocess.Popen(
                [path, "recoil-master-everyone:assistance"], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                startupinfo=startupinfo,
            )

            core.event.emit(constants.event.ASSISTANCE_MOUSE_UPDATE)
            return True

    def stop(self) -> bool:
        with self._lock:
            if not self.is_alive:
                return False

            self._popen.stdin.write("exit\n")
            self._popen.stdin.flush()

            try:
                self._popen.wait(3)

            except subprocess.TimeoutExpired:
                self._popen.kill()
                self._popen.wait()

            self._popen = None
            core.event.emit(constants.event.ASSISTANCE_MOUSE_UPDATE)
            return True

    def exit(self) -> None:
        self.stop()

    def tracks(self, mouse_tracks: str) -> bool:
        with self._lock:
            if not self.is_alive:
                return False

            self._popen.stdin.write(f"tracks {mouse_tracks}\n")
            self._popen.stdin.flush()
            return True

    def condition(self, value: bool) -> bool:
        with self._lock:
            if not self.is_alive:
                return False

            self._popen.stdin.write(f"condition {int(value)}\n")
            self._popen.stdin.flush()
            return True


class Assistance (Singleton):
    def __init__ (self) -> None:
        self.mouse = AssistanceMouse()


@once
def initialize_final() -> None:
    assistance = Assistance()
    core.event.subscribe(constants.event.ENTER_MAINLOOP, assistance.mouse.run, async_=True)
    core.action.exit.add_task(assistance.mouse.stop, 8000)
