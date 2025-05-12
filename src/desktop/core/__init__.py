# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import sys

# site
import i18nco
import ezudesign

from typex import once
from ezudesign.utils import try_exec, exec_item

# local
import module
import constants
import interface
import assistance

from basic import log, cwd, i18n

# internal
from . import action
from . import _convert
from . import _configuration


_activitys = [_configuration, _convert, action, module, interface, assistance]

config: _configuration.LocalConfiguration
event: ezudesign.eventhub.EventHub
taskpool: ezudesign.taskpool.TaskPool
tasksequence: ezudesign.tasksequence.TaskSequence


@once
def initialize_first() -> None:
    global config, event, taskpool, tasksequence
    config = _configuration.LocalConfiguration()
    event = ezudesign.eventhub.EventHub(constants.event.__all_events__)
    taskpool = ezudesign.taskpool.TaskPool()
    tasksequence = ezudesign.tasksequence.TaskSequence()

    try_exec(exec_item(config.ctrl.load_json, cwd.configuration, base64=True))
    try_exec(exec_item(i18n.ctrl.auto_load, cwd.assets.i18n))
    try_exec(exec_item(log.set_level, config.log_level))

    i18n.ctrl.set_locale(config.localed or i18nco.utils.get_locale_code())

    for activity in _activitys:
        objective = getattr(activity, "initialize_first", None)
        objective() if callable(objective) else None


@once
def initialize_setup() -> None:
    for activity in _activitys:
        objective = getattr(activity, "initialize_setup", None)
        objective() if callable(objective) else None


@once
def initialize_final() -> None:
    tasksequence.start()

    action.exit.add_task(lambda *_: sys.exit(0), 10000)

    for activity in _activitys:
        objective = getattr(activity, "initialize_final", None)
        objective() if callable(objective) else None


@once
def initialize() -> None:
    initialize_first()
    initialize_setup()
    initialize_final()


@once
def run() -> None:
    log.info("recoil-master-everyone")
    log.unpause()
    initialize()
    interface.mainwindow.after(0, lambda *_: event.emit(constants.event.ENTER_MAINLOOP))
    interface.mainwindow.mainloop()
    raise SystemExit("The main thread exits normally.")
