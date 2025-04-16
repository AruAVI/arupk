#!/usr/bin/env python3

import curses
import os

def show_home(stdscr):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    welcome = "PyVim - Python Vim"
    usage = "Press ENTER to open a file to edit"
    quit_usage = "Press 'q' to quit"
    credit = "Created by Aru using Python and curses"

    for y in range(max_y - 1):
        stdscr.addstr(y, 0, "~", curses.A_DIM)

    stdscr.addstr(max_y // 2 - 2, (max_x - len(welcome)) // 2, welcome)
    stdscr.addstr(max_y // 2,     (max_x - len(usage)) // 2, usage)
    stdscr.addstr(max_y // 2 + 1, (max_x - len(quit_usage)) // 2, quit_usage)
    stdscr.addstr(max_y // 2 + 3, (max_x - len(credit)) // 2, credit)

    stdscr.refresh()

    while True:
        key = stdscr.get_wch()
        if key == "\n" or key == curses.KEY_ENTER:
            break
        elif key == "q":
            return "quit"

def get_filename(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter filename to edit: ")
    curses.echo()
    filename = stdscr.getstr(0, 24).decode()
    curses.noecho()
    return filename

def main(stdscr):
    curses.curs_set(1)
    curses.use_default_colors()

    action = show_home(stdscr)
    if action == "quit":
        return

    filename = get_filename(stdscr)

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
    else:
        lines = [""]

    cursor_y = 0
    cursor_x = 0
    mode = 'NORMAL'

    while True:
        stdscr.clear()
        max_display_lines = curses.LINES - 2

        for idx in range(max_display_lines):
            if idx < len(lines):
                stdscr.addstr(idx, 0, lines[idx])
            else:
                stdscr.addstr(idx, 0, "~", curses.A_DIM)

        # Bottom line shows mode
        stdscr.addstr(curses.LINES - 1, 0, "-- {} --".format(mode))
        stdscr.move(cursor_y, cursor_x)
        key = stdscr.get_wch()

        if mode == 'INSERT':
            if key == '\x1b':  # ESC
                mode = 'NORMAL'
            elif key == curses.KEY_UP:
                cursor_y = max(0, cursor_y - 1)
            elif key == curses.KEY_DOWN:
                cursor_y = min(len(lines) - 1, cursor_y + 1)
            elif key == curses.KEY_LEFT:
                cursor_x = max(0, cursor_x - 1)
            elif key == curses.KEY_RIGHT:
                cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
            elif key in ("\n", curses.KEY_ENTER):
                current_line = lines[cursor_y]
                new_line = current_line[cursor_x:]
                lines[cursor_y] = current_line[:cursor_x]
                lines.insert(cursor_y + 1, new_line)
                cursor_y += 1
                cursor_x = 0
            elif key in ("\b", "\x7f", curses.KEY_BACKSPACE):
                if cursor_x > 0:
                    lines[cursor_y] = lines[cursor_y][:cursor_x-1] + lines[cursor_y][cursor_x:]
                    cursor_x -= 1
                elif cursor_y > 0:
                    prev_line_len = len(lines[cursor_y - 1])
                    lines[cursor_y - 1] += lines[cursor_y]
                    del lines[cursor_y]
                    cursor_y -= 1
                    cursor_x = prev_line_len
            elif isinstance(key, str):
                line = lines[cursor_y]
                lines[cursor_y] = line[:cursor_x] + key + line[cursor_x:]
                cursor_x += 1

        else:  # NORMAL mode
            if key == 'i':
                mode = 'INSERT'
            elif key == 'q':
                break
            elif key == curses.KEY_UP:
                cursor_y = max(0, cursor_y - 1)
            elif key == curses.KEY_DOWN:
                cursor_y = min(len(lines) - 1, cursor_y + 1)
            elif key == curses.KEY_LEFT:
                cursor_x = max(0, cursor_x - 1)
            elif key == curses.KEY_RIGHT:
                cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
            elif key == ':':
                # Enter command-line mode
                stdscr.addstr(curses.LINES - 1, 0, ":")
                stdscr.clrtoeol()
                curses.echo()
                command = stdscr.getstr(curses.LINES - 1, 1).decode()
                curses.noecho()

                if command == 'q':
                    break
                elif command == 'w':
                    with open(filename, 'w') as f:
                        f.write("\n".join(lines))
                elif command == 'wq':
                    with open(filename, 'w') as f:
                        f.write("\n".join(lines))
                    break
                else:
                    stdscr.addstr(curses.LINES - 1, 0, "-- Unknown command: {} --".format(command))
                    stdscr.clrtoeol()
                    stdscr.getch()

        # Clamp cursor
        cursor_y = max(0, min(cursor_y, len(lines) - 1))
        cursor_x = max(0, min(cursor_x, len(lines[cursor_y])))

    with open(filename, 'w') as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    curses.wrapper(main)
