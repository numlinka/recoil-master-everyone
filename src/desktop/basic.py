# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

__all__ = ["abscwd", "cwd", "log", "i18n"]

# site
from typex import Directory, FilePath
import logop
import i18nco


class _CWD (Directory):
    class assets (Directory):
        i18n = "i18n"

    logs = "logs"
    configuration = FilePath("configuration")


class _LocalI18n (i18nco.Internationalization):
    slogan: str

    class UI (object):
        GSI: str
        GSI_depict: str
        GSI_port: str
        GSI_timeout: str
        GSI_buffer: str
        GSI_throttle: str
        GSI_heartbeat: str
        GSI_start_service: str
        GSI_apply_to_game: str
        GSI_port_error: str
        GSI_port_error_desc: str
        GSI_value_error: str
        GSI_value_error_desc: str
        GSI_service_running: str
        GSI_service_stop: str
        GSI_service_error: str
        GSI_game_not_run: str
        GSI_game_not_run_desc: str
        GSI_game_cfg_error: str
        GSI_game_cfg_error_desc: str
        GSI_game_cfg_success: str
        GSI_game_cfg_success_desc: str

        License: str


abscwd = _CWD()
_CWD._include_ = False
cwd = _CWD()

log = logop.Logging(stdout=False, asynchronous=True)
log.pause()

i18n = _LocalI18n()
