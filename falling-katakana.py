#!/usr/bin/env python3

import random
import curses
import time

def generate_matrix_characters():
    latin_chars = [chr(i) for i in range(ord('/'), ord('z'))]
    katakana = [chr(i) for i in range(0xFF66, 0xFF9D)]
    return latin_chars + katakana

SLEEP_BETWEEN_FRAMES = .05
FALLING_SPEED = 2
MATRIX_CHARACTERS = generate_matrix_characters()

class MatrixRain(object):
    MATRIX_CHARACTERS = generate_matrix_characters()

    def __init__(self, stdscr, column_index):
        self.stdscr = stdscr
        self.column_index = column_index
        self.rain_length = random.randint(curses.LINES//2, curses.LINES)
        self.head = random.randint(-50, -10)

    def _random_char(self):
        return random.choice(MatrixRain.MATRIX_CHARACTERS)

    def animate(self, speed=FALLING_SPEED):
        while True:
            tail = self.head - self.rain_length
            if tail < 0:
                tail = 0
            self._draw(self.head, tail)
            self.head = self.head + speed
            yield
            if tail >= curses.LINES:
                self.head = 0

    def _draw(self, head, tail):
        for i in range(tail, min(head, curses.LINES)):
            self.stdscr.addstr(i, self.column_index, \
                self._random_char(), curses.color_pair(1) | curses.A_BOLD)

def config(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

def main(stdscr):
    config(stdscr)
    rains = [MatrixRain(stdscr, i).animate() for i in range(curses.COLS - 1)]
    while True:
        stdscr.clear()
        for r in rains:
            next(r)

        ch = stdscr.getch()
        if ch != curses.ERR:
            break

        time.sleep(SLEEP_BETWEEN_FRAMES)


if __name__ == "__main__":
    curses.wrapper(main)
