# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.


ENTER_MAINLOOP = "rme.enter-mainloop"

GSI_UPDATE = "rme.gsi-update"
GSI_START = "rme.gsi-start"
GSI_ERROR = "rme.gsi-error"
GSI_STOP = "rme.gsi-stop"

CONDITION_UPDATE = "rme.condition-update"

ASSISTANCE_MOUSE_UPDATE = "rme.assistance-mouse-update"


__all__ = [x for x in dir() if not x.startswith("_")]
__all_events__ = [v for x, v in globals().items() if not x.startswith("_")]
