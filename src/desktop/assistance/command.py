# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

import sys
import multiprocessing.connection
from typing import NoReturn

import assistance

def _execute(action: str, value: str = ..., *_):
    match action:
        case "exit":
            sys.exit(0)

        case "tracks":
            assistance.recoil.set_tracks(value)

        case "condition":
            assistance.recoil.condition.set() if (int(value)) else assistance.recoil.condition.clear()

def _mainloop(pipeline: multiprocessing.connection.PipeConnection) -> NoReturn:
    while True:
        try:
            message = pipeline.recv().strip().split(" ", 1)
            _execute(*message)

        except Exception as _:
            ...

def exit():
    assistance.master_pipe.send("exit")

def tracks(name: str):
    assistance.master_pipe.send(f"tracks {name}")

def condition(value: bool):
    assistance.master_pipe.send(f"condition {int(value)}")
