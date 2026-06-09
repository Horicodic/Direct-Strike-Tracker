# Direct-Strike-Tracker
A tracker for the WC3 custom game Direct Strike - Made by Horiciculic and Nemo
Built from source with PyInstaller.
Source code available for review.

# How to use
    1. Run .exe
    2. Place DST on second monitor (works best as second monitor app, can be of course used also with one monitor)
    3. Click/ type in units as enemy sends them
        a. To use Text to DST press "Right Shift" while in game -> A small textbox will appear.
            * The texbox will understand [number] [text] (a list of text that it understands can be found below) any other input will be ignored
            * example: "1 foot" --> Enemy 1 (top enemy) has footmen
            * example: "3 tank" --> Enemy 3 (bottom enemy) has Siege Engines
            * Textbox is used to not have to alt-tab/ move your mouse to the second monitor to select a unit, from testionmg this is much faster than manually pressing the units
    4. Check the DST UI as it will give you valueable info about your enemies unit composition, armor and attack types.
    



# Bash Build command
python -m PyInstaller --clean --onefile --noconsole --icon=icons/logo.ico --add-data "UnitPortraits;UnitPortraits" --add-data "icons;icons" --name DST main.py

# Hotkey for Textbox inside game is "Right Shift" - can be changed in main.py

# TO DO
    Damage and Armor recommendations are still very basic, will be iterated on in the future
    Unit weights might have to be reworked
    More QOL for inputting units if ideas appear
    App design overhaul
    Info on what enemy lacks: dispell antiair buffs

# Text Parser - this is what the Textbox can read

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
