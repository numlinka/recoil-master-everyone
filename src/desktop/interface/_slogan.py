# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import ttkbootstrap

from ttkbootstrap.constants import *
from typex import once

# local
import env
import interface
from basic import i18n


class Slogan (object):
    def __init__(self):
        self.parent = interface.mainwindow
        self.build()

    @once
    def build(self):
        self.frame = ttkbootstrap.Frame(self.parent)
        self.slogan = ttkbootstrap.Label(self.frame, text=i18n.slogan, cursor="hand2", bootstyle=INFO)

        self.frame.pack(side=BOTTOM, fill=X, padx=5, pady=(0, 5))
        self.slogan.pack(side=LEFT)

        self.slogan.bind("<Button-1>", self.bin_open_url)

    def bin_open_url(self, *_):
        import webbrowser
        webbrowser.open(env.GITHUB)
