# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.
# win32api-mouse

__assistance_name__ = "win32api-mouse"
__author__ = "numlinka"
__version_info__ = (0, 1)
__version__ = ".".join(map(str, __version_info__))

# std
import sys
from typing import NoReturn

# site
from typex import Static

# local
import _recoil
import _listen


class Status (Static):
    recoil: _recoil.Recoil
    listen: _listen.Listen


def _execute(action: str, value: str = ..., *_):
    match action:
        case "exit":
            sys.exit(0)

        case "version":
            sys.stdout.write(f"[INFO] Version: {__version__}\n")
            sys.stdout.flush()

        case "tracks":
            Status.recoil.set_tracks(value)

        case "condition":
            Status.recoil.condition.set() if (int(value)) else Status.recoil.condition.clear()

        case _:
            sys.stderr.write(f"[ERROR] Unknown action.\n")
            sys.stderr.flush()


def mainloop() -> NoReturn:
    sys.stdout.write(f"[INFO] {__assistance_name__} Ready.\n")
    sys.stdout.flush()

    while True:
        try:
            message = sys.stdin.readline().strip().split(" ", 1)
            _execute(*message)

        except Exception as _:
            pass


def main() -> None:
    if sys.argv[-1] != "recoil-master-everyone:assistance":
        raise SystemExit("This module is not intended to be run directly.")

    Status.recoil = _recoil.Recoil()
    Status.listen = _listen.Listen(Status.recoil)
    Status.recoil.start()
    Status.listen.start()
    mainloop()


if __name__ == "__main__":
    main()
