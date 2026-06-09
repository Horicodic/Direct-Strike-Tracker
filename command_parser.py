import re

UNIT_ALIASES = {
    "foot": "Footman",
    "footman": "Footman",
    "grunt": "Grunt",
    "ghoul": "Ghoul",
    "hunt": "Huntress",
    "huntress": "Huntress",

    "rifle": "Rifleman",
    "rifleman": "Rifleman",
    "arch": "Archer",
    "archer": "Archer",
    "crypt": "Crypt Fiend",
    "fiend": "Crypt Fiend",
    "cryptfiend": "Crypt Fiend",
    "headhunter": "Headhunter",
    "hh": "Headhunter",

    "sham": "Shaman",
    "shaman": "Shaman",
    "dryad": "Dryad",
    "banshee": "Banshee",
    "sorc": "Sorceress",
    "sorceress": "Sorceress",

    "mortar": "Mortar Team",
    "mortarteam": "Mortar Team",
    "glaive": "Glaive Thrower",
    "glaivethrower": "Glaive Thrower",
    "demo": "Demolisher",
    "demolisher": "Demolisher",
    "meat": "Meat Wagon",
    "meatwagon": "Meat Wagon",
    "wagon": "Meat Wagon",

    "priest": "Priest",
    "hippogryph": "Hippogryph",
    "witch": "Witch Doctor",
    "witchdoctor": "Witch Doctor",
    "gargoyle": "Gargoyle",

    "spellbreaker": "Spellbreaker",
    "claw": "Druid of the Claw",
    "druidoftheclaw": "Druid of the Claw",
    "dotc": "Druid of the Claw",
    "spirit": "Spirit Walker",
    "spiritwalker": "Spirit Walker",
    "sw": "Spirit Walker",
    "necro": "Necromancer",
    "necromancer": "Necromancer",

    "fm": "Flying Machine",
    "flyingmachine": "Flying Machine",
    "talon": "Druid of the Talon",
    "druidofthetalon": "Druid of the Talon",
    "raider": "Raider",
    "obsidian": "Obsidian Statue",
    "statue": "Obsidian Statue",
    "obsidianstatue": "Obsidian Statue",

    "dragonhawk": "Dragonhawk",
    "hawk": "Dragonhawk",
    "faerie": "Faerie Dragon",
    "faeriedragon": "Faerie Dragon",
    "kodo": "Kodo Beast",
    "kodobeast": "Kodo Beast",
    "shade": "Shade",

    "knight": "Knight",
    "giant": "Mountain Giant",
    "mountaingiant": "Mountain Giant",
    "mountain": "Mountain Giant",
    "mg": "Mountain Giant",
    "tauren": "Tauren",
    "abom": "Abomination",
    "abomination": "Abomination",

    "tank": "Siege Engine",
    "siegeengine": "Siege Engine",
    "engine": "Siege Engine",
    "hippogryphriders": "Hippogryph Riders",
    "gryph": "Hippogryph Riders",
    "rider": "Hippogryph Riders",
    "batrider": "Batrider",
    "bat": "Batrider",
    "destroyer": "Destroyer",

    "gryphon": "Gryphon Rider",
    "gryphonrider": "Gryphon Rider",
    "chimaera": "Chimaera",
    "chim": "Chimaera",
    "wind": "Wind Rider",
    "windrider": "Wind Rider",
    "frost": "Frost Wyrm",
    "frostwyrm": "Frost Wyrm",
    "wyrm": "Frost Wyrm",
}


def parse_command(text):

    text = text.lower().strip()

    pattern = r"^([123])\s+([a-z ]+)$"

    match = re.match(pattern, text)

    if not match:
        return None

    enemy = int(match.group(1))
    alias = match.group(2).replace(" ", "")

    unit = UNIT_ALIASES.get(alias)

    if unit is None:
        return None

    return {
        "enemy": enemy,
        "unit": unit
    }