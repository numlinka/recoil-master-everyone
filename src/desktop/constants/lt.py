# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.


DISCLAIMER_EN_US = """Disclaimer
1. Software Nature
This software (hereinafter referred to as the "Tool") provides recoil control and counter-strafing assistance solely for personal practice and simplified gameplay. Users must acknowledge that:

This Tool is not an official Valve product and has no affiliation with *Counter-Strike 2 (CS2)* or its developers.

2. Usage Risks
Users are fully aware of the following risks:

Game developers (Valve) may detect this Tool through anti-cheat systems (e.g., VAC) and classify it as unauthorized third-party software, resulting in account bans or other penalties.

Using this Tool in online matches may violate CS2’s Terms of Service (e.g., Steam Subscriber Agreement Section 6 "You agree not to…"), and the user assumes all responsibility.

This Tool does not guarantee 100% compatibility with all game versions. Users bear all risks related to account issues, data loss, or malfunctions due to updates or compatibility problems.

3. User Responsibility
Before using this Tool, users must confirm that they:

Understand local laws regarding game-assist software.

Will only use it in offline mode or private servers (if risk mitigation is desired).

Voluntarily accept all consequences, including but not limited to account bans, stat resets, or community bans.

4. Limitation of Liability
The developer/provider is not responsible for:

Direct or indirect damages caused by the use of this Tool.

Tool malfunctions or increased risks due to changes in game policies.

Penalties or legal repercussions resulting from violations of game rules.

5. Copyright & Termination
This Tool is intended for educational and technical research purposes only. Commercial use is prohibited. The developer reserves the right to discontinue distribution if required by Valve or legal authorities.


Last Updated: 5 17, 2025
"""



DISCLAIMER_ZH_CN = """免责声明

1. 软件性质说明

　本软件（以下简称“工具”）提供的压枪辅助、急停辅助等功能仅为用户个人练习及简化操作流程而设计，属于本地化的人机交互优化工具。用户需明确知晓：该工具并非 Valve 官方产品，与《Counter-Strike 2》（CS2）游戏开发商及运营商无任何关联。

2. 使用风险警示

　用户应知悉以下风险：
　- 游戏开发商（Valve）可能通过反作弊系统（如 VAC）检测并判定该工具为违规第三方软件，导致游戏账号受到封禁或其他处罚；
　- 使用本工具参与在线对战可能违反 CS2 用户协议（如《Steam 订阅协议》第 6 节“您同意不…”条款），责任由用户自行承担；
　- 本工具不保证 100% 兼容所有游戏版本，因更新或兼容性问题导致的账号异常、数据丢失等风险由用户自负。

3. 用户责任与义务

　用户在使用本工具前须确认：
　- 已充分了解所在地区关于游戏辅助工具的法律法规；
　- 仅在离线模式或私人服务器中使用（如需规避风险）；
　- 自愿承担因使用本工具导致的一切后果，包括但不限于账号封禁、战绩重置、社区禁令等。

4. 免责条款

　开发者/提供者不对以下情况负责：
　- 因用户使用本工具导致的直接或间接损失；
　- 游戏政策变动导致的工具失效或风险变化；
　- 用户违反游戏规则导致的处罚及连带责任。

5. 版权与终止声明

　本工具仅供学习技术原理交流，禁止用于商业用途。如 Valve 官方或法律要求，开发者保留随时终止分发的权利。


最后更新日期：2025年5月17日
"""



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