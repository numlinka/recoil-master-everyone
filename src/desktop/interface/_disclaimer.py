# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# size
import i18nco
import i18nco.constants
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import constants
import interface
from basic import i18n


class Disclaimer (object):
    def __init__(self):
        self.frame = ttkbootstrap.Frame(interface.notebook)
        interface.notebook.add(self.frame, text=i18n.UI.disclaimer)
        self.build()

    @once
    def build(self):
        i18n.ctrl.set_translation(i18nco.constants.en_US, "disclaimer", constants.lt.DISCLAIMER_EN_US)
        i18n.ctrl.set_translation(i18nco.constants.zh_CN, "disclaimer", constants.lt.DISCLAIMER_ZH_CN)
        self.text = ttkbootstrap.Text(self.frame)
        self.text.insert(1.0, i18n["disclaimer"])
        self.text.configure(state=DISABLED)
        self.text.pack(fill=BOTH, expand=True, padx=5, pady=5)
