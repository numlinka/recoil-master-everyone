# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# recoil-master-everyone Copyright (C) 2024 numlinka.

# std
import time
import threading

from typing import NoReturn, Iterable

# site
import win32api
import win32con


class Recoil (object):
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._tracks: Iterable[tuple[int, int]] = []
        self._length = 0
        self.fire = threading.Event()
        self.condition = threading.Event()

        self.thread = threading.Thread(None, self.mainloop, "Recoil", daemon=True)

    def mainloop(self) -> NoReturn:
        step = 0

        start_time = time.perf_counter()
        count = 0

        while True:
            count += 1
            next_time = start_time + 0.005 * count
            difference = next_time - time.perf_counter()
            if difference > 0:
                time.sleep(difference)

            if not self.fire.is_set():
                step = 0
                continue

            if not self.condition.is_set():
                self.fire.clear()
                step = 0
                continue

            step += 1

            if step >= self._length:
                step = 0
                self.fire.clear()
                continue

            with self._lock:
                mh, mv = self._tracks[step]
                if mh == 0 and mv == 0: continue
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, mh, mv)


    def set_tracks(self, msg: str) -> None:
        data = [int(x) for x in msg.split(",")]
        if len(data) % 2 != 0: data = data[:-1]
        oxl = [x for x in data[0::2]]
        oxr = [x for x in data[1::2]]
        tracks = list(zip(oxl, oxr))
        length = len(tracks)

        with self._lock:
            self._tracks = tracks
            self._length = length

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        self.thread.start()
