from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, head=None, body=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.head = head
        self.body = body

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.max_hp_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.max_hp_bonus

        return bonus

    @property
    def strength_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.strength_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.strength_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.strength_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.strength_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.defense_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.defense_bonus

        return bonus

    @property
    def dexterity_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.dexterity_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.dexterity_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.dexterity_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.dexterity_bonus

        return bonus

    @property
    def intelligence_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.intelligence_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.intelligence_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.intelligence_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.intelligence_bonus

        return bonus

    @property
    def charisma_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.charisma_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.charisma_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.charisma_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.charisma_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'dequipped': self.head})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.BODY:
            if self.body == equippable_entity:
                self.body = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.body:
                    results.append({'dequipped': self.body})

                self.body = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
