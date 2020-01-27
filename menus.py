import tcod as libtcodpy

from game_states import GameStates
from input_handlers import handle_keys, handle_main_menu


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError(
            'Cannot have a menu with more than 26 options.')

    # Calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcodpy.console_get_height_rect(
        con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = libtcodpy.console_new(width, height)

    # Print the header, with auto-wrap
    libtcodpy.console_set_default_foreground(window, libtcodpy.white)
    libtcodpy.console_print_rect_ex(
        window, 0, 0, width, height, libtcodpy.BKGND_NONE, libtcodpy.LEFT, header)

    # Print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcodpy.console_print_ex(
            window, 0, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, text)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcodpy.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def side_menu(con, header, options, width, screen_width, screen_height, color=libtcodpy.white):
    header_height = libtcodpy.console_get_height_rect(
        con, 0, 0, width, screen_height, header)

    height = len(options) + header_height
    window = libtcodpy.console_new(width, height)

    # Print the header
    libtcodpy.console_set_default_foreground(window, libtcodpy.white)
    libtcodpy.console_print_rect_ex(window, 0, 0, width, height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, "%cInventory%c" % (libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcodpy.console_print_ex(
            window, 0, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT,
            '%c{0}%c'.format(text) % (libtcodpy.COLCTRL_3, libtcodpy.COLCTRL_STOP))
        libtcodpy.console_set_char_foreground(window, 0, y, color)
        libtcodpy.console_set_char_foreground(window, 1, y, color)
        libtcodpy.console_set_char_foreground(window, 2, y, color)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcodpy.console_blit(window, 0, 0, width, height, 0, screen_width - 30, 2, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height, color):
    # Show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            elif player.equipment.head == item:
                options.append('{0} (on head)'.format(item.name))
            elif player.equipment.body == item:
                options.append('{0} (on body)'.format(item.name))
            else:
                options.append(item.name)

    side_menu(con, header, options, inventory_width,
              screen_width, screen_height, color)


def render_game_menu(con, header, options, width, screen_width, screen_height, game_state, index):
    window = libtcodpy.console_new(width, 30)
    header_height = libtcodpy.console_get_height_rect(
        con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    y = header_height

    letter_index = ord('a')
    for i in range(len(options)):
        # text = '(' + chr(letter_index) + ') ' + option_text
        if i == index:
            libtcodpy.console_print_ex(window, int(width/2), y, libtcodpy.BKGND_SET, libtcodpy.CENTER,
                                       '%c{0}%c'.format(options[i]) % (
                                       libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))
        else:
            libtcodpy.console_print_ex(window, int(width/2), y, libtcodpy.BKGND_SET, libtcodpy.CENTER, '{0}'.format(options[i]))
        y += 2
        letter_index += 1

    libtcodpy.console_blit(window, 0, 0, width, 30, 0, int(screen_width - 80), screen_height - 30, 1.0, 0.7)


def main_menu(con, background_image, screen_width, screen_height, game_state, index):
    libtcodpy.console_clear(con)
    libtcodpy.console_clear(0)
    libtcodpy.image_blit_2x(background_image, 0, 0, 0)

    libtcodpy.console_set_default_foreground(0, libtcodpy.white)
    libtcodpy.console_set_default_background(0, libtcodpy.black)

    libtcodpy.console_print_ex(0, 65, 15,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "  _____          _ _ _       _     _            __   _____ _          ")
    libtcodpy.console_print_ex(0, 65, 16,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               " |_   _|_      _(_) (_) __ _| |__ | |_    ___  / _| |_   _| |__   ___ ")
    libtcodpy.console_print_ex(0, 65, 17,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "   | | \ \ /\ / / | | |/ _` | '_ \| __|  / _ \| |_    | | | '_ \ / _ \ ")
    libtcodpy.console_print_ex(0, 65, 18,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "   | |  \ V  V /| | | | (_| | | | | |_  | (_) |  _|   | | | | | |  __/")
    libtcodpy.console_print_ex(0, 65, 19,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "   |_|   \_/\_/ |_|_|_|\__, |_| |_|\__|  \___/|_|     |_| |_| |_|\___|")
    libtcodpy.console_print_ex(0, 65, 20,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "                       |___/                                          ")
    libtcodpy.console_print_ex(0, 65, 21,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "     ____  _      _         ____           _     _                    ")
    libtcodpy.console_print_ex(0, 65, 22,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "    |  _ \(_)_  _(_) ___   / ___| ___   __| | __| | ___  ___ ___      ")
    libtcodpy.console_print_ex(0, 65, 23,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "    | |_) | \ \/ / |/ _ \ | |  _ / _ \ / _` |/ _` |/ _ \/ __/ __|     ")
    libtcodpy.console_print_ex(0, 65, 24,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "    |  __/| |>  <| |  __/ | |_| | (_) | (_| | (_| |  __/\__ \__ \     ")
    libtcodpy.console_print_ex(0, 65, 25,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "    |_|   |_/_/\_\_|\___|  \____|\___/ \__,_|\__,_|\___||___/___/     ")
    libtcodpy.console_print_ex(0, 65, 26,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               "                                                                      ")

    libtcodpy.console_set_default_foreground(0, libtcodpy.Color(219,251,121))
    libtcodpy.console_print_ex(0, int(screen_width - 10), int(screen_height - 2),
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER, 'Version: 0.0.1')

    render_game_menu(con, '', ['Start game (Normal)', 'Load progress',
                               'Quit'], 30, screen_width, screen_height, game_state, index)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.strength),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcodpy.console_new(
        character_screen_width, character_screen_height)

    libtcodpy.console_set_default_foreground(window, libtcodpy.white)

    libtcodpy.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cCharacter Information%c' % (libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_set_char_foreground(
        window, character_screen_width, character_screen_height, libtcodpy.Color(35, 140, 196))
    libtcodpy.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cLevel%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 2, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.level.current_level) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cExp%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 3, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.level.current_xp) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cExp to Level%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 4, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.level.experience_to_next_level) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cConstitution%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 5, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.max_hp) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cStrength%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 6, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.strength) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cEndurance%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 7, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.defense) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cDexterity%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 8, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.dexterity) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cIntelligence%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 9, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.intelligence) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cCharisma%c' % (
                                        libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 10, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%c{0}%c'.format(player.fighter.charisma) % (
                                        libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcodpy.console_blit(window, 0, 0, character_screen_width,
                           character_screen_height, 0, screen_width - 30, 30, 1.0, 0.7)


def character_equipment_screen(player, char_screen_width, char_screen_height, screen_width):
    window = libtcodpy.console_new(char_screen_width, char_screen_height)

    libtcodpy.console_set_default_foreground(window, libtcodpy.white)

    right_hand = 'Empty'
    left_hand = 'Empty'
    head = 'Empty'
    body = 'Empty'

    if len(player.inventory.items) == 0:
        right_hand = 'Empty'
        left_hand = 'Empty'
        head = 'Empty'
        body = 'Empty'
    else:

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                right_hand = item.name
            elif player.equipment.off_hand == item:
                left_hand = item.name
            elif player.equipment.head == item:
                head = item.name
            elif player.equipment.body == item:
                body = item.name

    libtcodpy.console_print_rect_ex(window, 0, 1, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cCharacter Equipment%c' % (libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 2, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cHead%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 2, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(head) % (
                                    libtcodpy.COLCTRL_4 if head is not 'Empty' else libtcodpy.COLCTRL_3,
                                    libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cRight Hand%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(right_hand) % (
                                    libtcodpy.COLCTRL_4 if right_hand is not 'Empty' else libtcodpy.COLCTRL_3,
                                    libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cLeft Hand%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(left_hand) % (
                                    libtcodpy.COLCTRL_4 if left_hand is not 'Empty' else libtcodpy.COLCTRL_3,
                                    libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cBody%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(body) % (
                                    libtcodpy.COLCTRL_4 if body is not 'Empty' else libtcodpy.COLCTRL_3,
                                    libtcodpy.COLCTRL_STOP))

    libtcodpy.console_blit(window, 0, 0, char_screen_width,
                           char_screen_height, 0, screen_width - 30, 43, 1.0, 0.7)


def help_screen(char_screen_width, char_screen_height, screen_width):
    window = libtcodpy.console_new(char_screen_width, char_screen_height)

    libtcodpy.console_set_default_foreground(window, libtcodpy.white)

    libtcodpy.console_print_rect_ex(window, 0, 1, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cControls%c' % (libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 2, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%ci%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 2, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cInventory%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cd%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cDrop Inventory%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cg%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cPickup%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cz%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cWait%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 6, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%ck j h l%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 6, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cU D L R%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 7, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cu b n z%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 7, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cDiag U D L R%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 8, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cEsc%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 8, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cTitle : Close%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 9, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cEnter%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 9, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cTake Stairs%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 10, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cF11%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 10, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cFullscreen%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 11, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cmouse%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 15, 11, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cTarget%c' % (libtcodpy.COLCTRL_5, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_blit(window, 0, 0, char_screen_width,
                           char_screen_height, 0, screen_width - 30, 50, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
