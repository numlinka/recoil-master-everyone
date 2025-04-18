# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.


LICENSE = """
recoil-master-everyone
GNU General Public License v3.0
Copyright (C) 2024 numlinka
https://github.com/numlinka/recoil-master-everyone


cpython
GNU General Public License
Copyright (c) 2001 Python Software Foundation
https://github.com/python/cpython


ezudesign
GNU Lesser General Public License v3.0
Copyright (C) 2023 numlinka
https://github.com/numlinka/pyezudesign


i18nco
MIT License
Copyright (C) 2023 numlinka
https://github.com/numlinka/pyi18nco


logop
MIT License
Copyright (C) 2023 numlinka
https://github.com/numlinka/pylogop


pillow
MIT-CMU License
Copyright © 1997-2011 by Secret Labs AB
Copyright © 1995-2011 by Fredrik Lundh and contributors
https://github.com/python-pillow/Pillow


psutil
BSD 3-Clause License
Copyright (c) 2009, Jay Loden, Dave Daeschler, Giampaolo Rodola
https://github.com/giampaolo/psutil


pynput
GNU Lesser General Public License v3.0
Copyright (c) moses-palmer
https://github.com/moses-palmer/pynput


six
MIT License
Copyright (c) 2010-2024 Benjamin Peterson
https://github.com/benjaminp/six


ttkbootstrap
MIT License
Copyright (c) 2021 Israel Dryer
https://github.com/israel-dryer/ttkbootstrap


typex
MIT License
Copyright (C) 2022 numlinka
https://github.com/numlinka/pytypex
"""



CS2_GSI_CFG_TEMPLATE = """
"Console Sample v.1"
{
  "uri" "http://127.0.0.1:<$PORT>"
  "timeout" "<$TIMEOUT>"
  "buffer"  "<$BUFFER>"
  "throttle" "<$THROTTLE>"
  "heartbeat" "<$HEARTBEAT>"
  "auth"
  {
    "token" "recoil-master-everyone"
  }
  "output"
  {
    "precision_time" "3"
    "precision_position" "1"
    "precision_vector" "3"
  }
    "data"
  {
    "provider"            "1"    // general info about client being listened to: game name, appid, client steamid, etc.
    "map"                 "1"    // map, gamemode, and current match phase ('warmup', 'intermission', 'gameover', 'live') and current score
    "round"               "1"    // round phase ('freezetime', 'over', 'live'), bomb state ('planted', 'exploded', 'defused'), and round winner (if any)
    "player_id"           "1"    // player name, clan tag, observer slot (ie key to press to observe this player) and team
    "player_state"        "1"    // player state for this current round such as health, armor, kills this round, etc.
    "player_weapons"      "1"    // output equipped weapons.
    "player_match_stats"  "1"    // player stats this match such as kill, assists, score, deaths and MVPs
  }
}
""".strip()