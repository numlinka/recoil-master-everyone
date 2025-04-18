# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# size
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import constants
import interface
from basic import i18n


class License (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.License)
        self.build()

    @once
    def build(self):
        self.text = ttkbootstrap.Text(self.frame)
        self.text.insert(INSERT, constants.lt.LICENSE)
        self.text.configure(state=DISABLED)
        self.text.pack(fill=BOTH, expand=True)
