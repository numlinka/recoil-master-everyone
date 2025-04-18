# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
from typex import once
from ezudesign.taskflow import TaskFlow

# local
from basic import i18n


exit: TaskFlow


@once
def initialize_first() -> None:
    global exit
    exit = TaskFlow(i18n.actions.exit)