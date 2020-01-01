import sys
import os
from typing import Tuple


def _length_of_terminal() -> int:
    pass


def _rows_of_terminal() -> int:
    pass


def get_getters() -> Tuple[_length_of_terminal, _rows_of_terminal]:
    length_of_terminal, rows_of_terminal = None, None
    if sys.version[0:3] < "3.0":
        import fcntl
        import termios
        import struct

        def length_of_terminal() -> int:
            _, columns, _, _ = struct.unpack('HHHH',
                                             fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                         struct.pack('HHHH', 0, 0, 0, 0)))
            return columns

        def rows_of_terminal() -> int:
            rows, _, _, _ = struct.unpack('HHHH',
                                          fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                      struct.pack('HHHH', 0, 0, 0, 0)))
            return rows
    else:

        def length_of_terminal() -> int:
            return os.get_terminal_size().columns

        def rows_of_terminal() -> int:
            return os.get_terminal_size().lines

    return length_of_terminal, rows_of_terminal


length_of_terminal, rows_of_terminal = get_getters()


def console_write(string: str) -> None:
    sys.stdout.write(string)
    sys.stdout.flush()


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_line() -> None:
    console_write("\r" + " " * (length_of_terminal()) + "\r")


def up() -> None:
    console_write('\x1b[1A')


def down() -> None:
    console_write('\n')


def clear_n_lines(n: int) -> None:
    for i in range(n):
        clear_line()
        down()
    clear_line()
    for i in range(n):
        up()
