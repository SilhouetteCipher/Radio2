import curses
from menu_handler import load_menu, display_menu

def main(stdscr):
    curses.curs_set(0)
    menu_stack = ["main_menu"]

    while True:
        current_menu_name = menu_stack[-1]
        current_menu = load_menu('menu.json', current_menu_name)
        action = display_menu(stdscr, current_menu, menu_stack)
        
        if action == "exit_program":
            break

curses.wrapper(main)
