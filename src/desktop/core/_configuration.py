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

    theme = setting(str)
    window_width = setting(int, 650)
    window_height = setting(int, 450)
    window_x = setting(int, -1)
    window_y = setting(int, -1)

    gsi_port = setting(int, 25463, NumericalRange(1, 65535))
    gsi_timeout = setting(float, 5.0, NumericalRange(0.1, 60.0, 1))
    gsi_buffer = setting(float, 0.1, NumericalRange(0.1, 10.0, 1))
    gsi_throttle = setting(float, 0.5, NumericalRange(0.1, 10.0, 1))
    gsi_heartbeat = setting(float, 60.0, NumericalRange(0.1, 360.0, 1))

    recoil_enable = setting(int, 0, NumericalRange(0, 1))
    recoil_sensitivity = setting(float, 1.0, NumericalRange(0.1, 8.0, 2))
    recoil_horizontal = setting(float, 1.0, NumericalRange(0.0, 2.0, 2)) 
    recoil_vertical = setting(float, 1.0, NumericalRange(0.0, 2.0, 2))
    recoil_smoothing = setting(int, 10, NumericalRange(1, 100))
    recoil_leading_delay = setting(float, 0.2, NumericalRange(0.0, 0.5, 2))
    recoil_duty_cycle = setting(float, 0.5, NumericalRange(0.0, 1.0, 2))

    effective_weapons = setting(str)

    hud_alpha = setting(int, 50, NumericalRange(0, 100))
    hud_width = setting(int, 600, NumericalRange(200, 16384))
    hud_height = setting(int, 400, NumericalRange(200, 16384))
    hud_enable = setting(int, 1, NumericalRange(0, 1))
    hud_weapon_sort = setting(int, 1, NumericalRange(0, 1))
    hud_active_first = setting(int, 1, NumericalRange(0, 1))
    hud_active_only = setting(int, 0, NumericalRange(0, 1))
    hud_gun_only = setting(int, 1, NumericalRange(0, 1))

    anti_ad_ghosting = setting(int, 0, NumericalRange(0, 1))
    anti_ws_ghosting = setting(int, 0, NumericalRange(0, 1))

    assistance_mouse = setting(str)


def save(*_):
    try_exec(exec_item(core.config.ctrl.save_json, cwd.configuration, base64=True))


@once
def initialize_final():
    core.action.exit.add_task(save, 9000)
