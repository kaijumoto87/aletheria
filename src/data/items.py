# Aletheria: Items and values for the game:
# Values are in "talet" currency units. (1 talet = 1/100 of a drachma)

def get_item_value(item_name: str) -> dict:
    """Return item data safely"""
    return ITEMS.get(item_name.lower(), {})

ITEMS = {
    "small health potion": {
        "type": "potion",
        "heal": 8,
        "value": 60,
    },

    "large health potion": {
        "type": "potion",
        "heal": 20,
        "value": 125,
    },

    "small mana potion": {
        "type": "potion",
        "mana": 6,
        "value": 70,
    },

    "large mana potion": {
        "type": "potion",
        "mana": 15,
        "value": 140,
    },

    "rusty sword": {
        "type": "weapon",
        "weapon_bonus": 5,
        "value": 65,
    },

    "wolf pelt": {
        "type": "material",
        "value": 40,
    },

    "sharp fang": {
        "type": "material",
        "value": 35,
    },

    "orcish axe": {
        "type": "weapon",
        "weapon_bonus": 7,
        "value": 100, 
    },

    "healing herb": {
        "type": "material",
        "value": 90,
    },

    "elven bow": {
        "type": "weapon",
        "weapon_bonus": 9,
        "value": 220,
    },

    "magic crystal": {
        "type": "material",
        "value": 160,
    },

# I'm treating the claws of a bloody bear to be like a lesser ivory -- valuable but not exorbitantly so.
    "bear claw": {
        "type": "material",
        "value": 120,
    },

    "thick fur": {
        "type": "material",
        "value": 80,
    },

    "bone sword": {
        "type": "weapon",
        "weapon_bonus": 6,
        "value": 30,
    },

    "shield fragment": {
        "type": "material",
        "value": 55,
    },

# Fenrir materials are considered very valuable due to their rarity and association with the legendary creatures.
    "fenrir fang": {
        "type": "material",
        "value": 200,
    },

    "mythical pelt": {
        "type": "material",
        "value": 420,
    }
}
