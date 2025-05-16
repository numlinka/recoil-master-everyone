# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
from typing import TypedDict
from dataclasses import dataclass, field

# local
from constants import *


@dataclass
class GameStateAuth (object):
    token: str = ""


@dataclass
class GameStateMapTeam (object):  # 
    consecutive_round_losses: int = 0  # 连败次数
    matches_won_this_series: int = 0
    score: int = 0  # 分数
    timeouts_remaining: int = 1  # 剩余超时次数


@dataclass
class GameStateMap (object):
    mode: str = ""  # 模式
    name: str = ""  # 地图名
    num_matches_to_win_series: int = 0
    phase: str = ""  # 比赛阶段  Literal[LIVE]
    team_ct: GameStateMapTeam = field(default_factory=GameStateMapTeam)
    team_t: GameStateMapTeam = field(default_factory=GameStateMapTeam)


@dataclass
class GameStatePlayerMatch (object):
    assists: int = 0  # 助攻
    deaths: int = 0  # 死亡
    kills: int = 0  # 击杀
    mvps: int = 0  # MVP
    score: int = 0  # 分数


@dataclass
class GameStatePlayerState (object):
    health: int = 0  # 生命
    armor: int = 0  # 护甲
    helmet: bool = False  # 拥有头盔
    defusekit: bool = False  # 拥有防具
    money: int = 0  # 经济
    equip_value: int = 0  # 装备价值
    round_killhs: int = 0  # 回合爆头数
    round_kills: int = 0  # 回合击杀数
    flashed: int = 0  # 被闪
    smoked: int = 0  # 被烟
    burning: int = 0  # 被燃烧


@dataclass
class GameStatePlayerWeapon (object):
    ammo_clip: int = 0  # 当前弹药
    ammo_clip_max: int = 0  # 最大弹药
    ammo_reserve: int = 0  # 剩余弹药
    name: str = ""  # 武器名
    paintkit: str = ""  # 皮肤
    state: str = ""  # 武器状态  Literal[ACTIVE, HOLSTERED, RELOADING]
    type: str = ""  # 武器类型  Literal[KNIFE, PISTOL, RIFLE]


@dataclass
class GameStatePlayer (object):
    activity: str = ""  # 状态  Literal[PLAYING]
    name: str = ""  # 玩家名
    observer_slot: int = 0  # 观察者数量
    steamid: str = ""
    team: str = ""  # 队伍  Literal[T, CT]
    state: GameStatePlayerState = field(default_factory=GameStatePlayerState)
    match_stats: GameStatePlayerMatch = field(default_factory=GameStatePlayerMatch)
    weapons: dict[str, GameStatePlayerWeapon] = field(default_factory=dict)
    active_weapon: GameStatePlayerWeapon = field(default_factory=GameStatePlayerWeapon)


@dataclass
class GameStateProvider (object):
    appid: int = 0  # 游戏 ID
    name: str = ""  # 游戏名
    steamid: str = ""
    timestamp: int = 0  # 时间戳
    version: int = 0  # 版本


@dataclass
class GameStateRound (object):
    phase: str = ""  # 回合阶段  Literal[OVER]
    win_team: str = ""  # 胜利队伍


@dataclass
class GameState (object):
    auth: GameStateAuth = field(default_factory=GameStateAuth)
    map: GameStateMap = field(default_factory=GameStateMap)
    player: GameStatePlayer = field(default_factory=GameStatePlayer)
    provider: GameStateProvider = field(default_factory=GameStateProvider)
    round: GameStateRound = field(default_factory=GameStateRound)


class WeaponOffsets (TypedDict):
    RPM: int
    FOE: int
    offsets: list[list[int, int]]
