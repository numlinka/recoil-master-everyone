# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
from typex import once
from ezudesign.utils import try_exec, exec_item
from ezudesign.configuration import Configuration, NumericalRange, setting

# local
import core
from basic import cwd


class LocalConfiguration (Configuration):
    localed = setting(str, "")
    log_level = setting(int, 0)
    log_to_std = setting(int, 0, NumericalRange(0, 1))
    log_to_file = setting(int, 0, NumericalRange(0, 1))

    window_width = setting(int, 650)
    window_height = setting(int, 450)
    window_x = setting(int, -1)
    window_y = setting(int, -1)

    gsi_port = setting(int, 25463, NumericalRange(1, 65535))
    gsi_timeout = setting(float, 5.0, NumericalRange(0.1, 60.0))
    gsi_buffer = setting(float, 0.1, NumericalRange(0.1, 10.0))
    gsi_throttle = setting(float, 0.5, NumericalRange(0.1, 10.0))
    gsi_heartbeat = setting(float, 60.0, NumericalRange(0.1, 360.0))

    recoil_mou_sen = setting(float, 1.0, NumericalRange(0.1, 8.0))
    recoil_hor_per = setting(float, 1.0, NumericalRange(0.0, 2.0))
    recoil_ver_per = setting(float, 1.0, NumericalRange(0.0, 2.0))
    recoil_smo_coe = setting(int, 10, NumericalRange(1, 100))


def save(*_):
    try_exec(exec_item(core.config.ctrl.save_json, cwd.configuration, base64=True))


@once
def initialize_final():
    core.action.exit.add_task(save, 8000)
