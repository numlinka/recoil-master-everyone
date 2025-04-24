# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import multiprocessing
import multiprocessing.connection

from typing import Optional

# site
from typex import once

# local
import core

# internal
from . import command
from . import _recoil
from . import _listen


recoil: _recoil.Recoil
listen: _listen.Listen

master_pipe: Optional[multiprocessing.connection.PipeConnection] = None
assistance: Optional[multiprocessing.Process] = None


def _run_assistance(pipeline: multiprocessing.connection.PipeConnection):
    global recoil, listen
    recoil = _recoil.Recoil()
    listen = _listen.Listen()

    recoil.initialize()
    listen.initialize()

    recoil.start()
    listen.start()

    command._mainloop(pipeline)


def run():
    global master_pipe, assistance
    if isinstance(assistance, multiprocessing.Process) and assistance.is_alive():
        return

    master_pipe, slave_pipe = multiprocessing.Pipe()
    assistance = multiprocessing.Process(None, _run_assistance, "Assistance", (slave_pipe, ), daemon=True)
    assistance.start()


def stop():
    global master_pipe, assistance
    if isinstance(assistance, multiprocessing.Process) and assistance.is_alive():
        assistance.kill()
        assistance.join()
        assistance = None

    if isinstance(master_pipe, multiprocessing.connection.PipeConnection):
        master_pipe.close()
        master_pipe = None


@once
def initialize_final():
    core.action.exit.add_task(stop, 8000)
    run()
