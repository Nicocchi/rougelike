import tcod as libtcodpy


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError(
            'Cannot have a menu with moer than 26 options.')

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
            window, 0, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, text)
        libtcodpy.console_set_char_foreground(window, 0, y, color)
        libtcodpy.console_set_char_foreground(window, 1, y, color)
        libtcodpy.console_set_char_foreground(window, 2, y, color)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcodpy.console_blit(window, 0, 0, width, height, 0, 70, 2, 1.0, 0.7)


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


def main_menu(con, background_image, screen_width, screen_height):
    libtcodpy.image_blit_2x(background_image, 0, 0, 0)

    libtcodpy.console_set_default_foreground(0, libtcodpy.light_yellow)
    libtcodpy.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4,
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER, 'Twilight of the Pixie Goddess')
    libtcodpy.console_print_ex(0, int(screen_width / 2), int(screen_height - 2),
                               libtcodpy.BKGND_NONE, libtcodpy.CENTER, 'By Nicocchi')

    menu(con, '', ['Play a new game', 'Continue last game',
                   'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.strength),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcodpy.console_new(
        character_screen_width, character_screen_height)

    libtcodpy.console_set_default_foreground(window, libtcodpy.white)

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_1, libtcodpy.Color(35, 140, 196), libtcodpy.black)

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_4, libtcodpy.Color(196, 35, 78), libtcodpy.black)

    libtcodpy.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%cCharacter Information%c' % (libtcodpy.COLCTRL_1, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_set_char_foreground(
        window, character_screen_width, character_screen_height, libtcodpy.Color(35, 140, 196))
    libtcodpy.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Level: %c{0}%c'.format(player.level.current_level) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Experience: %c{0}%c'.format(player.level.current_xp) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    'Experience to Level: %c{0}%c'.format(player.level.experience_to_next_level) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Constitution: %c{0}%c'.format(player.fighter.max_hp) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Strength: %c{0}%c'.format(player.fighter.strength) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Endurance: %c{0}%c'.format(player.fighter.defense) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Dexterity: %c{0}%c'.format(player.fighter.dexterity) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Intelligence: %c{0}%c'.format(player.fighter.intelligence) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 0, 11, character_screen_width, character_screen_height,
                                    libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, 'Charisma: %c{0}%c'.format(player.fighter.charisma) % (
                                    libtcodpy.COLCTRL_4, libtcodpy.COLCTRL_STOP))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcodpy.console_blit(window, 0, 0, character_screen_width,
                           character_screen_height, 0, 70, 30, 1.0, 0.7)


def character_equipment_screen(player, char_screen_width, char_screen_height, screen_width, screen_height):
    window = libtcodpy.console_new(char_screen_width, char_screen_height)

    libtcodpy.console_set_default_foreground(window, libtcodpy.white)

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_2, libtcodpy.Color(196, 35, 175), libtcodpy.black)

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
    libtcodpy.console_print_rect_ex(window, 13, 2, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(head) % (libtcodpy.COLCTRL_3, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cRight Hand%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 13, 3, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(right_hand) % (libtcodpy.COLCTRL_3, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cLeft Hand%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 13, 4, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(left_hand) % (libtcodpy.COLCTRL_3, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_print_rect_ex(window, 0, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT, '%cBody%c' % (libtcodpy.COLCTRL_2, libtcodpy.COLCTRL_STOP))
    libtcodpy.console_print_rect_ex(window, 13, 5, char_screen_width, char_screen_height, libtcodpy.BKGND_NONE,
                                    libtcodpy.LEFT,
                                    '%c{0}%c'.format(body) % (libtcodpy.COLCTRL_3, libtcodpy.COLCTRL_STOP))

    libtcodpy.console_blit(window, 0, 0, char_screen_width,
                           char_screen_height, 0, 70, 50, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
