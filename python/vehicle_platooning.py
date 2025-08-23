import curses
import random
import time
from fleetmqclass import fleetmqClass
from wcwidth import wcwidth
import secrets
import string
import numpy as np

# Define symbols
HEAD_CAR_SYMBOL = "🚘"
CAR_SYMBOL = "🚖" #🚗
CHARGING_STATION_SYMBOL = "✨"
BLANK = ""
CELL_WIDTH = max(wcwidth(HEAD_CAR_SYMBOL), wcwidth(CAR_SYMBOL), wcwidth(CHARGING_STATION_SYMBOL), 2)

# Game settings
DELAY = 130  # milliseconds between moves

def sparkle_effect(box, car, sh, sw):
    sparkle_positions = [
        [y + dy, x + dx]
        for y, x in car
        for dy in [-1, 0, 1]
        for dx in [-1, 0, 1]
        if 0 < y + dy < sh - 1 and 0 < x + dx < sw - 1
    ]

def generate_secure_code(length=32, prefix="fmq_"):
    charset = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(charset) for _ in range(length))
    return prefix + token

def main(stdscr):
    fleetmq = fleetmqClass()

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(DELAY)

    sh, sw = stdscr.getmaxyx()
    grid_cols = sw // CELL_WIDTH
    grid_rows = sh

    box = curses.newwin(sh, sw, 0, 0)
    box.keypad(1)

    # Initial car body in grid cells
    car = [
        [grid_rows // 2, grid_cols // 2],
        [grid_rows // 2, (grid_cols // 2) - 1],
        [grid_rows // 2, (grid_cols // 2) - 2]
    ]

    # Place first charging station
    charging_station = [
        random.randint(1, grid_rows - 3),
        random.randint(1, grid_cols - 3)
    ]

    # Wait for first direction
    direction = "right"
    while direction is None:
        direction = fleetmq.getAction()

    score = 0

    while True:
        try: 
            box.clear()
            box.border()
            box.addstr(0, 2, f' Score: {score} ')

            # Draw charging station
            try:
                box.addstr(charging_station[0], charging_station[1] * CELL_WIDTH,
                        CHARGING_STATION_SYMBOL)
            except curses.error:
                pass

            # Draw car (head first)
            for idx, (y, x) in enumerate(car):
                try:
                    sym = HEAD_CAR_SYMBOL if idx == 0 else CAR_SYMBOL
                    box.addstr(y, x * CELL_WIDTH, sym)
                except curses.error:
                    pass

            box.refresh()

            new_dir = fleetmq.getAction()
            if new_dir in ("up", "down", "left", "right"):
                # Tentative head if we were to accept new_dir
                ty, tx = car[0]
                if new_dir == "right":
                    tx = (tx + 1) % grid_cols
                elif new_dir == "left":
                    tx = (tx - 1) % grid_cols
                elif new_dir == "up":
                    ty = (ty - 1) % grid_rows
                elif new_dir == "down":
                    ty = (ty + 1) % grid_rows

                # Accept the new direction only if it doesn't hit the body
                if [ty, tx] not in car:
                    direction = new_dir

            y, x = car[0]
            if direction == "right":
                x = (x + 1) 
                if x >= grid_cols:
                    x  = (x+1) % grid_cols
                    y = random.randint(1, grid_rows-2)
            elif direction == "left":
                x = (x - 1) 
                if x <= 0:
                    x  = (x-1) % grid_cols
                    y = random.randint(1, grid_rows-2)
            elif direction == "up":
                y = (y - 1)
                if y <= 0:
                    y  = (y-1) % grid_rows
                    x = random.randint(1, grid_cols-2)
            elif direction == "down":
                y = (y + 1)
                if y >= grid_rows:
                    y  = (y+1) % grid_rows
                    x = random.randint(1, grid_cols-2)
            
            head = [y, x]

            # Self‑collision check (still possible if no safe moves exist)
            # if head in car:
                # msg = "Crashed into self!"
                # break

            # Update car
            car.insert(0, head)

            if head == charging_station:
                score += 1

                charging_station = [
                    random.randint(1, grid_rows - 3),
                    random.randint(1, grid_cols - 3)
                ]
            else:
                car.pop()

            time.sleep(DELAY / 1000)
        except KeyboardInterrupt:
            
            # Game over screen
            stdscr.nodelay(0)
            stdscr.clear()
            stdscr.addstr(sh // 2 + 1, max(0, sw // 2 - 7), f"Final Score: {score}")
            stdscr.addstr(sh // 2 + 3, max(0, sw // 2 - 12), "Press any key to exit...")
            stdscr.refresh()
            stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit