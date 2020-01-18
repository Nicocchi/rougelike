import tcod as libtcod

from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():
    # Define screen size
    screen_width = 80
    screen_height = 50

    # Size of the map
    map_width = 80
    map_height = 45

    # Some variables for the room sin the map
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Field of view
    fov_algorithm = 0 # Default algorithm libtcod uses
    fov_light_walls = True # Whether or not to light up the walls
    fov_radius = 10 # How far player can see

    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Define player position -> center screen
    # player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True)
    # npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [player]

    # Tell libtcod which font to use
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Create the screen
    libtcod.console_init_root(screen_width, screen_height, 'Rougelike', False)

    # Define new console
    con = libtcod.console_new(screen_width, screen_height)

    # Define the game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    # Hold the mouse and keyboard input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # Main game loop
    while not libtcod.console_is_window_closed():
        # Captures new "events", user input. Updates the key and mouse vars with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Recompute field of view
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Print the player and set the background to none -> (console, x, y, what to draw, background)
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

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
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN
        
        # Exit the game
        if exit:
            return True
        
        # Fullscreen the game
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()