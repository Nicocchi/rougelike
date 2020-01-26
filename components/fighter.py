import tcod as libtcod

from game_messages import Message

class Fighter:
    def __init__(self, hp, defense, strength, dexterity, intelligence, charisma, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_strength = strength
        self.base_dexterity = dexterity
        self.base_intelligence = intelligence
        self.base_charisma = charisma
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        
        return self.base_max_hp + bonus
    
    @property
    def strength(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.strength_bonus
        else:
            bonus = 0
        
        return self.base_strength + bonus
    
    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        
        return self.base_defense + bonus

    @property
    def dexterity(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dexterity_bonus
        else:
            bonus = 0
        
        return self.base_dexterity + bonus
    
    @property
    def intelligence(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.intelligence_bonus
        else:
            bonus = 0
        
        return self.base_intelligence + bonus
    
    @property
    def charisma(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.charisma_bonus
        else:
            bonus = 0
        
        return self.base_charisma + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if (self.hp <= 0):
            self.hp = 0
            results.append({'dead': self.owner, 'xp': self.xp})
        
        return results
    
    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        # Calculate the damage from the targets defense
        damage = self.strength - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name), libtcod.white)})
        
        return results