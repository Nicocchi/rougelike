import tcod as libtcod

from enum import Enum, auto

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu

class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
                if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if (bar_width > 0):
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

# Draw enties and map
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, 
                panel_y, mouse, colors, game_state):
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                    else:
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, colors.get('light_ground'))
                    
                    game_map.tiles[x][y].explored = True;
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, colors.get('dark_wall'))
                    else:
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, colors.get('dark_ground'))

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)
    
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    # Draw health bar
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon Level: {0}'.format(game_map.dungeon_level))

    # Draw names
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
    
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    # Draw Inventory
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Inventory'
            color = libtcod.Color(107, 107, 107)
        else:
            inventory_title = 'Inventory'
            color = libtcod.red
            
        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height, color)
    
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)
    
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    # Draw Inventory on Side
    if game_state not in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        inventory_menu(con, 'Inventory', player, 50, screen_width, screen_height, libtcod.white)

# Clears all the entites after drawing to the screen
def clear_all(con, entities, fov_map):
    for entity in entities:
        clear_entity(con, entity, fov_map)

# Draws the entity to the screen
def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# Clears the entity from the screen so that when the entity moves it doesn't leave a trail behind
def clear_entity(con, entity, fov_map):
    # Erase the character that represents this object
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_put_char(con, entity.x, entity.y, '.', libtcod.BKGND_NONE)
