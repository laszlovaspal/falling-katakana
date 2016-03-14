#!/usr/bin/env python3

import random
import curses
import time

SLEEP_BETWEEN_FRAMES = .05

def generate_possible_matrix_characters():
    latin_chars = [chr(i) for i in range(ord('/'), ord('z'))]
    katakana = [chr(i) for i in range(0xFF66, 0xFF9D)]
    return latin_chars + katakana

class MatrixRain(object):
    MATRIX_CHARACTERS = generate_possible_matrix_characters()

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.rain = []
        for i in range(random.randint(2, curses.LINES)):
            self.rain.append(random.choice(MatrixRain.MATRIX_CHARACTERS))
        self.horizontal_position = random.choice(range(curses.COLS - 1))
        self.vertical_position = random.randint(-30, 0) - len(self.rain)
        self.speed = random.randint(1, 2)

    def draw(self):
        for i in range(0, len(self.rain)):
            if self.vertical_position + i < 0:
                continue
            if self.vertical_position + i >= curses.LINES:
                break
            self.stdscr.addstr(self.vertical_position + i, self.horizontal_position, \
                self.rain[i], self._get_color(i))

    def _get_color(self, index):
        color = curses.color_pair(1)
        if index == len(self.rain) - 1:
            color = curses.color_pair(2) | curses.A_BOLD
        elif index > len(self.rain) / 4:
            color = curses.color_pair(1) | curses.A_BOLD
        return color

    def move_down(self):
        self.rain.pop(0)
        self.rain.append(random.choice(MatrixRain.MATRIX_CHARACTERS))
        self.vertical_position += self.speed

    def is_visible(self):
        return self.vertical_position < curses.LINES

def initialize_stdscr(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

def main(stdscr):
    initialize_stdscr(stdscr)
    rains = [MatrixRain(stdscr) for i in range(80)]
    while True:
        stdscr.clear()
        for i in rains[:]:
            i.draw()
            i.move_down()

            if not i.is_visible():
                rains.append(MatrixRain(stdscr))
                rains.remove(i)

        ch = stdscr.getch()
        if ch != curses.ERR:
            break

        time.sleep(SLEEP_BETWEEN_FRAMES)

if __name__ == "__main__":
    curses.wrapper(main)
