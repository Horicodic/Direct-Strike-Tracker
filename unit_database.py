KEY_TOOLS = {
    "Anti-Air": [
        "Rifleman", "Archer", "Crypt Fiend", "Headhunter",
        "Flying Machine", "Gargoyle", "Dragonhawk Rider", "Siege Engine",
    ],
    "Dispel": [
        "Priest", "Dryad", "Spirit Walker", "Destroyer", "Spellbreaker",
    ],
    "Summoning": ["Necromancer"],
    "Healing": ["Priest", "Witch Doctor", "Obsidian Statue"],
    "Buff": ["Shaman", "Necromancer", "Priest"],
    "Disrupt": ["Banshee", "Sorceress", "Druid of the Talon", "Faerie Dragon"],
    "Detection": ["Flying Machine", "Shade", "Mortar Team", "Witch Doctor"],
    "Air Threat": [
        "Gargoyle", "Dragonhawk Rider", "Destroyer", "Wind Rider",
        "Gryphon Rider", "Frost Wyrm", "Chimaera",
    ],
}


UNIT_DATABASE = {
    # Q
    "Footman": {"slot": "Q", "tier": 1, "attack_type": "Normal", "armor_type": "Heavy", "weight": 2},
    "Huntress": {"slot": "Q", "tier": 1, "attack_type": "Normal", "armor_type": "Unarmored", "weight": 3},
    "Grunt": {"slot": "Q", "tier": 1, "attack_type": "Normal", "armor_type": "Heavy", "weight": 2},
    "Ghoul": {"slot": "Q", "tier": 1, "attack_type": "Normal", "armor_type": "Heavy", "weight": 3},

    # W
    "Rifleman": {"slot": "W", "tier": 1, "attack_type": "Pierce", "armor_type": "Medium", "weight": 2},
    "Archer": {"slot": "W", "tier": 1, "attack_type": "Pierce", "armor_type": "Medium", "weight": 1},
    "Headhunter": {"slot": "W", "tier": 1, "attack_type": "Pierce", "armor_type": "Medium", "weight": 2},
    "Crypt Fiend": {"slot": "W", "tier": 1, "attack_type": "Pierce", "armor_type": "Medium", "weight": 2},

    # E
    "Sorceress": {"slot": "E", "tier": 1, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},
    "Dryad": {"slot": "E", "tier": 1, "attack_type": "Pierce", "armor_type": "Unarmored", "weight": 1},
    "Shaman": {"slot": "E", "tier": 1, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},
    "Banshee": {"slot": "E", "tier": 1, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 1},

    # R
    "Mortar Team": {"slot": "R", "tier": 2, "attack_type": "Siege", "armor_type": "Heavy", "weight": 0},
    "Glaive Thrower": {"slot": "R", "tier": 2, "attack_type": "Siege", "armor_type": "Heavy", "weight": 0},
    "Demolisher": {"slot": "R", "tier": 2, "attack_type": "Siege", "armor_type": "Heavy", "weight": 0},
    "Meat Wagon": {"slot": "R", "tier": 2, "attack_type": "Siege", "armor_type": "Heavy", "weight": 0},

    # A
    "Priest": {"slot": "A", "tier": 2, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},
    "Hippogryph": {"slot": "A", "tier": 2, "attack_type": "Normal", "armor_type": "Unarmored", "weight": 1},
    "Witch Doctor": {"slot": "A", "tier": 2, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 0},
    "Gargoyle": {"slot": "A", "tier": 2, "attack_type": "Pierce", "armor_type": "Unarmored", "weight": 2},

    # S
    "Spellbreaker": {"slot": "S", "tier": 2, "attack_type": "Normal", "armor_type": "Medium", "weight": 3},
    "Druid of the Claw": {"slot": "S", "tier": 2, "attack_type": "Normal", "armor_type": "Heavy", "weight": 3},
    "Spirit Walker": {"slot": "S", "tier": 2, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},
    "Necromancer": {"slot": "S", "tier": 2, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},

    # D
    "Flying Machine": {"slot": "D", "tier": 2, "attack_type": "Pierce", "armor_type": "Heavy", "weight": 0},
    "Druid of the Talon": {"slot": "D", "tier": 2, "attack_type": "Magic", "armor_type": "Unarmored", "weight": 2},
    "Raider": {"slot": "D", "tier": 2, "attack_type": "Siege", "armor_type": "Medium", "weight": 0},
    "Obsidian Statue": {"slot": "D", "tier": 2, "attack_type": "Normal", "armor_type": "Heavy", "weight": 0},

    # F
    "Dragonhawk": {"slot": "F", "tier": 2, "attack_type": "Pierce", "armor_type": "Light", "weight": 1},
    "Faerie Dragon": {"slot": "F", "tier": 2, "attack_type": "Pierce", "armor_type": "Light", "weight": 1},
    "Kodo Beast": {"slot": "F", "tier": 2, "attack_type": "Pierce", "armor_type": "Light", "weight": 0},
    "Shade": {"slot": "F", "tier": 2, "attack_type": "None", "armor_type": "Medium", "weight": 0},

    # Z
    "Knight": {"slot": "Z", "tier": 3, "attack_type": "Normal", "armor_type": "Heavy", "weight": 4},
    "Mountain Giant": {"slot": "Z", "tier": 3, "attack_type": "Normal", "armor_type": "Medium", "weight": 4},
    "Tauren": {"slot": "Z", "tier": 3, "attack_type": "Normal", "armor_type": "Heavy", "weight": 4},
    "Abomination": {"slot": "Z", "tier": 3, "attack_type": "Normal", "armor_type": "Heavy", "weight": 3},

    # X
    "Siege Engine": {"slot": "X", "tier": 3, "attack_type": "Siege", "armor_type": "Fortified", "weight": 2},
    "Hippogryph Riders": {"slot": "X", "tier": 3, "attack_type": "Pierce", "armor_type": "Light", "weight": 1},
    "Batrider": {"slot": "X", "tier": 3, "attack_type": "Siege", "armor_type": "Light", "weight": 0},
    "Destroyer": {"slot": "X", "tier": 3, "attack_type": "Magic", "armor_type": "Light", "weight": 3},

    # C
    "Gryphon Rider": {"slot": "C", "tier": 3, "attack_type": "Magic", "armor_type": "Light", "weight": 2},
    "Chimaera": {"slot": "C", "tier": 3, "attack_type": "Magic", "armor_type": "Light", "weight": 2},
    "Wind Rider": {"slot": "C", "tier": 3, "attack_type": "Pierce", "armor_type": "Light", "weight": 2},
    "Frost Wyrm": {"slot": "C", "tier": 3, "attack_type": "Magic", "armor_type": "Light", "weight": 2},
}


def get_unit_tags(unit_name):
    tags = []

    for tag, units in KEY_TOOLS.items():
        if unit_name in units:
            tags.append(tag)

    return tags


for unit_name, data in UNIT_DATABASE.items():
    data["tags"] = get_unit_tags(unit_name)