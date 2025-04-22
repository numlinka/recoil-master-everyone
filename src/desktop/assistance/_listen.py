# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# site
import pynput

# local
import assistance


class Listen (object):
    def __init__(self):
        self.mouse_listen = pynput.mouse.Listener(on_click=self.on_click)
        self.mouse_listen.name = "MouseListen"
        self.mouse_listen.daemon = True
        self.external_conditions = True
        self._need_keep = True
        self._s_left = False
        self._s_x2 = False

    def on_click(self, x: int, y: int, button: pynput.mouse.Button, pressed: bool):
        match button:
            case pynput.mouse.Button.left:
                assistance.recoil.fire.set() if pressed else assistance.recoil.fire.clear()

    def initialize(self):
        ...

    def start(self):
        self.mouse_listen.start()
