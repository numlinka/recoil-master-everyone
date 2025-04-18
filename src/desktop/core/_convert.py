# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
from typing import Any, Iterable, Mapping

# site
from ezudesign.eventhub import EventHubDefaultAction, EventItem
from ezudesign.taskflow import TaskFlowDefaultAction, TaskFlow, TaskItem

# local
import core


def event_exec_async_task(event_item: EventItem) -> None:
    core.taskpool.new_task(event_item.callback, event_item.args, event_item.kwargs)


def flow_exec_async_task(self: TaskFlow, taskunit: TaskItem, args: Iterable[Any], kwargs: Mapping[str, Any]) -> None:
    core.taskpool.new_task(taskunit.task, args, kwargs)


def initialize_first():
    EventHubDefaultAction.exec_async_task = event_exec_async_task
    TaskFlowDefaultAction.exec_async_task
