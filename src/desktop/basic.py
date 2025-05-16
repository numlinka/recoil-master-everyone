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
        weapons = "weapons"
        favicon = "favicon.ico"

    assistance = "assistance"
    logs = "logs"
    configuration = FilePath("configuration")


class _LocalI18n (i18nco.Internationalization):
    slogan: str

    class actions (object):
        exit: str

    class UI (object):
        gsi: str
        gsi_depict: str
        gsi_port: str
        gsi_timeout: str
        gsi_buffer: str
        gsi_throttle: str
        gsi_heartbeat: str
        gsi_start_service: str
        gsi_apply_to_game: str
        gsi_port_error: str
        gsi_port_error_desc: str
        gsi_value_error: str
        gsi_value_error_desc: str
        gsi_service_running: str
        gsi_service_stop: str
        gsi_service_error: str
        gsi_game_not_run: str
        gsi_game_not_run_desc: str
        gsi_game_cfg_error: str
        gsi_game_cfg_error_desc: str
        gsi_game_cfg_success: str
        gsi_game_cfg_success_desc: str

        hud: str
        hud_alpha: str
        hud_width: str
        hud_height: str
        hud_enable: str
        hud_weapon_sort: str
        hud_active_first: str
        hud_active_only: str
        hud_gun_only: str

        recoil: str
        recoil_track: str
        recoil_sensitivity: str
        recoil_horizontal: str
        recoil_vertical: str
        recoil_smoothing: str
        recoil_leading_delay: str
        recoil_duty_cycle: str

        weapon: str

        anti: str
        anti_ad_ghosting: str
        anti_ws_ghosting: str

        licenses: str

    class ITEM (object):
        weapon_glock: str
        weapon_hkp2000: str
        weapon_usp_silencer: str
        weapon_p250: str
        weapon_tec9: str
        weapon_fiveseven: str
        weapon_cz75a: str
        weapon_deagle: str
        weapon_revolver: str
        weapon_dualberettas: str
        weapon_nova: str
        weapon_xm1014: str
        weapon_sawedoff: str
        weapon_mag7: str
        weapon_m249: str
        weapon_negev: str
        weapon_mp9: str
        weapon_mac10: str
        weapon_mp7: str
        weapon_mp5sd: str
        weapon_ump45: str
        weapon_p90: str
        weapon_bizon: str
        weapon_famas: str
        weapon_galilar: str
        weapon_m4a4: str
        weapon_m4a1: str
        weapon_m4a1_silencer: str
        weapon_ak47: str
        weapon_sg556: str
        weapon_aug: str
        weapon_ssg08: str
        weapon_awp: str
        weapon_g3sg1: str
        weapon_scar20: str
        weapon_knife: str
        weapon_knife_t: str
        weapon_flashbang: str
        weapon_hegrenade: str
        weapon_smokegrenade: str
        weapon_molotov: str
        weapon_incgrenade: str
        weapon_decoy: str
        weapon_taser: str
        weapon_c4: str
        item_defuser: str
        item_kevlar: str
        item_assaultsuit: str


abscwd = _CWD()
_CWD._include_ = False
cwd = _CWD()

log = logop.Logging(stdout=False)
log.pause()

i18n = _LocalI18n()
