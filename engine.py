import tcod as libtcod

from input_handlers import handle_keys

def main():
    # Define screen size
    screen_width = 80
    screen_height = 50

    # Define player position -> center screen
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # Tell libtcod which font to use
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Create the screen
    libtcod.console_init_root(screen_width, screen_height, 'Rougelike', False)

    # Define new console
    con = libtcod.console_new(screen_width, screen_height)

    # Hold the mouse and keyboard input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():
        # Captures new "events", user input. Updates the key and mouse vars with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Tell libtcod to set the color for the player -> @
        libtcod.console_set_default_foreground(con, libtcod.white)

        # Print the player and set the background to none -> (console, x, y, what to draw, background)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        # Present everything to the screen
        libtcod.console_flush()

        # Reprint the player on the screen
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        # Capture the return value from handle_keys
        action = handle_keys(key)

        # Set the variables from the dictionary action
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # Move the player
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy
        
        # Exit the game
        if exit:
            return True
        
        # Fullscreen the game
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()