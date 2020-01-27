import tcod as libtcodpy

from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = libtcodpy.Color(169,0,32)

    return Message('You died!', libtcodpy.Color(169,0,32)), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcodpy.Color(231,93,16))

    monster.char = '%'
    monster.color = libtcodpy.Color(169,0,32)
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
