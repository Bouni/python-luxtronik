import os
import shutil
import sys

if sys.platform == "win32":
    import msvcrt
else:
    import select
    import termios
    import tty





class UpdateScreen:

    if sys.platform == "win32":

        def init_key(self):
            pass

        def get_key(self):
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\xe0': # special key
                        key2 = msvcrt.getch()
                        if key2 == b'H':
                            key = "up"
                        elif key2 == b'P':
                            key = "down"
                    else:
                        key = key.decode()
                    return key
            except Exception:
                pass
            return None

        def finalize_key(self):
            pass

    else:

        def init_key(self):
            self._fd = sys.stdin.fileno()
            self._old_settings = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)

        def get_key(self):
            try:
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if key == "\x1b[A":
                        key = "up"
                    elif key == "\x1b[B":
                        key = "down"
                    return key
            except Exception:
                pass
            return None

        def finalize_key(self):
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)


    NUM_STATUS_LINES = 1

    def __init__(self, buffer_size):
        self._buffer_size = buffer_size
        self._buffer = [""] * self._buffer_size
        self._offset = 0
        self._index = 0
        self._counter = 0
        self.init_key()

    def __del__(self):
        self.finalize_key()

    def _safe_up(self, n):
        _, rows = shutil.get_terminal_size()
        rows -= 1 # one for half lines
        n = min(n, rows)
        sys.stdout.write(f"\033[{n}A")
        sys.stdout.flush()

    def clear(self):
        self._buffer = [""] * self._buffer_size
        self._offset = 0
        self._index = 0
        self._counter = 0
        os.system("cls" if os.name == "nt" else "clear")

    def write(self, text):
        if self._index < self._buffer_size:
            self._buffer[self._index] = text
            self._index += 1

    def get_visible_size(self):
        cols, rows = shutil.get_terminal_size()
        rows -= 1 # one for half lines
        visible_rows = rows - self.NUM_STATUS_LINES
        return cols, visible_rows

    def update(self):
        cols, rows = self.get_visible_size()
        visible = self._buffer[self._offset : self._offset + rows]
        for line in visible:
            print(line[:cols] + "\033[0K") # clear residual line
        print(f"[Update: {self._counter}, Offset: {self._offset}]  up/down to scroll, q to quit" + "\033[0K")
        self._counter += 1

    def reset(self):
        # "clear" screen
        self._index = 0
        self._safe_up(self._buffer_size)

    def on_key_press(self, key):
        _, rows = self.get_visible_size()
        if key == "q":
            return True
        elif key == "down":
            self._offset = min(self._offset + self.NUM_STATUS_LINES, self._buffer_size - rows)
        elif key == "up":
            self._offset = max(self._offset - self.NUM_STATUS_LINES, 0)
        return False

    def process_keys(self, count):
        do_exit = False
        # Repeat query user-input for smaller latency
        for i in range(count):
            key = self.get_key()
            if self.on_key_press(key):
                do_exit = True
                break
        return do_exit