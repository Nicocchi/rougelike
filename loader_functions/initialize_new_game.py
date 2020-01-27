import tcod as libtcodpy

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from components.level import Level

from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from item_functions import heal
from map_objects.game_map import GameMap
from render_functions import RenderOrder


def get_constants():
    window_title = 'Twilight of the Pixie Goddess'

    # Screen
    screen_width = 130
    screen_height = 80

    # Healthbar
    bar_width = 20

    # Bottom Panel
    panel_height = 8
    panel_y = screen_height - panel_height

    side_panel_width = 40
    side_panel_x = screen_width + 2

    # Message box
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Map
    map_width = screen_width - 35
    map_height = screen_height - 8

    room_max_size = 14
    room_min_size = 6
    max_rooms = 120

    # Field of View
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # Entities
    max_monsters_per_room = 3
    max_items_per_room = 2

    colors = {
        'dark_wall': libtcodpy.Color(17,65,89),
        'dark_ground': libtcodpy.Color(42,138,138),
        'light_wall': libtcodpy.Color(32,121,0),
        'light_ground': libtcodpy.Color(89,219,85)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'side_panel_width': side_panel_width,
        'side_panel_x': side_panel_x,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_1, libtcodpy.Color(47, 121, 251), libtcodpy.black) # Sky blue

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_2, libtcodpy.Color(246, 89, 154), libtcodpy.black) # Pink

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_3, libtcodpy.Color(121, 121, 121), libtcodpy.black)  # Grey

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_4, libtcodpy.Color(231, 0, 89), libtcodpy.black) # Redish Pink

    libtcodpy.console_set_color_control(
        libtcodpy.COLCTRL_5, libtcodpy.Color(89,219,85), libtcodpy.black) # Light green

    return constants


def get_game_variables(constants):
    # Entities
    fighter_component = Fighter(hp=10000, defense=1, strength=200, dexterity=0, intelligence=0, charisma=0)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcodpy.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    for itm in range(0, 25):
        item_component = Item(use_function=heal, amount=40)
        item = Entity(0, 0, '!', libtcodpy.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                      item=item_component)
        player.inventory.add_item(item)

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, strength_bonus=2)
    dagger = Entity(0, 0, '-', libtcodpy.sky, 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    # Game Map
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    # Message
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
