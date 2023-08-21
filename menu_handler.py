import json
import curses
import actions

def load_menu(file_name, menu_name):
    with open(file_name, 'r') as file:
        menu_data = json.load(file)
    return menu_data.get(menu_name, [])

def handle_selected_item(selected_item, stdscr, menu_stack):
    if selected_item["type"] == "action":
        if selected_item["action"] == "back":
            return "back"
        elif selected_item["action"] == "exit_program":
            return "exit_program"
        else:
            func = getattr(actions, selected_item["action"], None)
            if func:
                func(stdscr)
            return None
    elif selected_item["type"] == "menu":
        menu_stack.append(selected_item["action"])
        return "menu"

def display_menu(stdscr, menu_items, menu_stack):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.bkgd(curses.color_pair(1))

        for idx, item in enumerate(menu_items):
            paddingLeft = 10
            paddingTop = idx + 10

            if idx == current_row:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(paddingTop, paddingLeft, item["name"])
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(paddingTop, paddingLeft, item["name"])

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10]: 
            selected_item = menu_items[current_row]
            action = handle_selected_item(selected_item, stdscr, menu_stack)
            if action == "back":
                if len(menu_stack) > 1:
                    menu_stack.pop()
                return "back"
            elif action == "exit_program":
                return "exit_program"
            elif action == "menu":
                return
