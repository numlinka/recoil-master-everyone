# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
from i18nco.constants import en_US
from ezudesign.configuration import Configuration, NumericalRange, setting


class LocalConfiguration (Configuration):
    localed = setting(str, "")
    log_level = setting(int, 0)
    log_to_std = setting(int, 0, NumericalRange(0, 1))
    log_to_file = setting(int, 0, NumericalRange(0, 1))

    window_width = setting(int, 650)
    window_height = setting(int, 450)

    gsi_port = setting(int, 25463)
    gsi_timeout = setting(float, 5.0)
    gsi_buffer = setting(float, 0.1)
    gsi_throttle = setting(float, 0.5)
    gsi_heartbeat = setting(float, 60.0)
