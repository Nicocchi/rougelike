import tcod as libtcod

from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():
    # Define screen size
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    # Define player position -> center screen
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    # Tell libtcod which font to use
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Create the screen
    libtcod.console_init_root(screen_width, screen_height, 'Rougelike', False)

    # Define new console
    con = libtcod.console_new(screen_width, screen_height)

    # Define the game map
    game_map = GameMap(map_width, map_height)

    # Hold the mouse and keyboard input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():
        # Captures new "events", user input. Updates the key and mouse vars with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Print the player and set the background to none -> (console, x, y, what to draw, background)
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        # Present everything to the screen
        libtcod.console_flush()

        # Clear all entities
        clear_all(con, entities)

        # Capture the return value from handle_keys
        action = handle_keys(key)

        # Set the variables from the dictionary action
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # Move the player
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
        
        # Exit the game
        if exit:
            return True
        
        # Fullscreen the game
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()