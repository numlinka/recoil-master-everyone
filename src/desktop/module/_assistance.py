# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import os
import subprocess

from typing import Optional

# site
from typex import once, Singleton

# local
import core
from basic import cwd


class Assistance (Singleton):
    def __init__ (self) -> None:
        self.assistance: Optional[subprocess.Popen] = None
        self.command: Optional[Command] = None

    def run(self) -> None:
        if isinstance(self.assistance, subprocess.Popen) and self.assistance.is_alive():
            return

        path = os.path.join(cwd.assistance, "win32api-mouse.exe")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.assistance = subprocess.Popen([path, "recoil-master-everyone:assistance"], 
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           text=True,
                                           bufsize=1,
                                           universal_newlines=True,
                                           startupinfo=startupinfo,
                                           )
        self.command = Command(self.assistance)

    def stop(self) -> None:
        self.command.exit()
        self.assistance.wait()
        self.assistance = None


class Command (object):
    def __init__ (self, assistance: subprocess.Popen) -> None:
        self.assistance = assistance

    def exit(self) -> None:
        self.assistance.stdin.write("exit\n")
        self.assistance.stdin.flush()

    def tracks(self, name: str) -> None:
        self.assistance.stdin.write(f"tracks {name}\n")
        self.assistance.stdin.flush()

    def condition(self, value: bool) -> None:
        self.assistance.stdin.write(f"condition {int(value)}\n")
        self.assistance.stdin.flush()


@once
def initialize_final() -> None:
    assistance = Assistance()
    assistance.run()
    core.action.exit.add_task(assistance.stop, 8000)
