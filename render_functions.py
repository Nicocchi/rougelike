import tcod as libtcodpy

from enum import Enum, auto

from game_states import GameStates

from menus import help_screen, character_equipment_screen, character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcodpy.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcodpy.console_set_default_background(panel, back_color)
    libtcodpy.console_rect(panel, x, y, total_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_background(panel, bar_color)
    if (bar_width > 0):
        libtcodpy.console_rect(panel, x, y, bar_width, 1, False, libtcodpy.BKGND_SCREEN)

    libtcodpy.console_set_default_foreground(panel, libtcodpy.white)
    libtcodpy.console_print_ex(panel, int(x + total_width / 2), y, libtcodpy.BKGND_NONE, libtcodpy.CENTER,
                               '{0}: {1}/{2}'.format(name, value, maximum))


# Draw enties and map
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height,
               panel_y, mouse, colors, game_state):
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcodpy.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcodpy.console_put_char(con, x, y, '#', libtcodpy.BKGND_SET)
                        libtcodpy.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                    else:
                        libtcodpy.console_put_char(con, x, y, '.', libtcodpy.BKGND_SET)
                        libtcodpy.console_set_char_foreground(con, x, y, colors.get('light_ground'))

                    game_map.tiles[x][y].explored = True;
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcodpy.console_put_char(con, x, y, '#', libtcodpy.BKGND_SET)
                        libtcodpy.console_set_char_foreground(con, x, y, colors.get('dark_wall'))
                    else:
                        libtcodpy.console_put_char(con, x, y, '.', libtcodpy.BKGND_SET)
                        libtcodpy.console_set_char_foreground(con, x, y, colors.get('dark_ground'))

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    libtcodpy.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcodpy.console_set_default_background(panel, libtcodpy.black)
    libtcodpy.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcodpy.console_set_default_foreground(panel, message.color)
        libtcodpy.console_print_ex(panel, message_log.x, y, libtcodpy.BKGND_NONE, libtcodpy.LEFT, message.text)
        y += 1

    # Draw health bar
    render_bar(panel, 1, 2, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcodpy.light_red,
               libtcodpy.darker_red)
    libtcodpy.console_print_ex(panel, 1, 4, libtcodpy.BKGND_NONE, libtcodpy.LEFT,
                               'Dungeon Level: {0}'.format(game_map.dungeon_level))

    # Draw names
    libtcodpy.console_set_default_foreground(panel, libtcodpy.light_gray)
    libtcodpy.console_print_ex(panel, 1, 0, libtcodpy.BKGND_NONE, libtcodpy.LEFT,
                               get_names_under_mouse(mouse, entities, fov_map))

    libtcodpy.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    # Draw Inventory
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Inventory'
            color = libtcodpy.Color(107, 107, 107)
        else:
            inventory_title = 'Inventory'
            color = libtcodpy.red

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height, color)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    # elif game_state == GameStates.CHARACTER_SCREEN:
    character_screen(player, 30, 15, screen_width, screen_height)
    character_equipment_screen(player, 30, 10)
    help_screen(30, 15)

    # Draw Inventory on Side
    if game_state not in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        inventory_menu(con, 'Inventory', player, 50, screen_width, screen_height, libtcodpy.white)


# Clears all the entites after drawing to the screen
def clear_all(con, entities, fov_map):
    for entity in entities:
        clear_entity(con, entity, fov_map)


# Draws the entity to the screen
def draw_entity(con, entity, fov_map, game_map):
    if libtcodpy.map_is_in_fov(fov_map, entity.x, entity.y) or (
            entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcodpy.console_set_default_foreground(con, entity.color)
        libtcodpy.console_put_char(con, entity.x, entity.y, entity.char, libtcodpy.BKGND_NONE)


# Clears the entity from the screen so that when the entity moves it doesn't leave a trail behind
def clear_entity(con, entity, fov_map):
    # Erase the character that represents this object
    if libtcodpy.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcodpy.console_put_char(con, entity.x, entity.y, '.', libtcodpy.BKGND_NONE)
