# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
import pynput
from typex import once

# local
import core


class Anti:
    def __init__(self):
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.daemon = True
        self.w = pynput.keyboard.KeyCode.from_char("w")
        self.a = pynput.keyboard.KeyCode.from_char("a")
        self.s = pynput.keyboard.KeyCode.from_char("s")
        self.d = pynput.keyboard.KeyCode.from_char("d")

    def on_press(self, key):
        match key:
            case self.a: self.keyboard.release(self.d) if core.config.anti_ad_ghosting else None
            case self.d: self.keyboard.release(self.a) if core.config.anti_ad_ghosting else None
            case self.w: self.keyboard.release(self.s) if core.config.anti_ws_ghosting else None
            case self.s: self.keyboard.release(self.w) if core.config.anti_ws_ghosting else None


@once
def initialize_final():
    anti = Anti()
    anti.keyboard_listener.start()
