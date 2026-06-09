from collections import Counter
from unit_database import UNIT_DATABASE


ARMOR_COUNTERS = {
    "Heavy": ["Magic"],
    "Medium": ["Normal"],
    "Light": ["Pierce", "Magic"],
    "Unarmored": ["Pierce", "Siege"],
    "Fortified": ["Siege"],
}

ATTACK_COUNTERS = {
    "Normal": ["Anythign except Medium Armor"],
    "Pierce": ["Medium/ Fortified"],
    "Magic": ["Medium/ Unarmored/ Fortified"],
    "Siege": ["Medium Armor"],
}


def get_selected_units(group_selected):
    return [
        unit for unit in group_selected.values()
        if unit is not None
    ]

# Armor analyzer
def analyze_armor_profile(group_selected):
    selected_units = get_selected_units(group_selected)

    armor_counts = Counter()

    for unit in selected_units:
        data = UNIT_DATABASE.get(unit)

        if not data:
            print(f"[WARN] Missing unit in UNIT_DATABASE: {unit}")
            continue

        armor_type = data.get("armor_type")
        weight = data.get("weight", 1)

        if armor_type and weight > 0:
            armor_counts[armor_type] += weight

    if not armor_counts:
        return {
            "status": "unknown",
            "message": "No armor profile yet",
            "armor_counts": {},
            "recommended_damage": [],
        }

    dominant_armor, count = armor_counts.most_common(1)[0]
    total_weight = sum(armor_counts.values())
    percentage = round((count / total_weight) * 100)

    recommended_damage = ARMOR_COUNTERS.get(dominant_armor, [])

    if percentage >= 60 and count >= 4:
        status = "strong"
        message = f"{dominant_armor} armor core"
    elif percentage >= 45:
        status = "medium"
        message = f"{dominant_armor} armor leaning"
    else:
        status = "mixed"
        message = "Mixed armor profile"

    return {
        "status": status,
        "message": message,
        "armor_counts": dict(armor_counts),
        "dominant_armor": dominant_armor,
        "dominant_percentage": percentage,
        "recommended_damage": recommended_damage,
    }

#Attack analyzer
def analyze_attack_profile(group_selected):
    selected_units = get_selected_units(group_selected)

    attack_counts = Counter()

    for unit in selected_units:
        data = UNIT_DATABASE.get(unit)

        if not data:
            print(f"[WARN] Missing unit in UNIT_DATABASE: {unit}")
            continue

        attack_type = data.get("attack_type")
        weight = data.get("weight", 1)

        if attack_type and attack_type != "None" and weight > 0:
            attack_counts[attack_type] += weight

    if not attack_counts:
        return {
            "status": "unknown",
            "message": "No attack profile yet",
            "attack_counts": {},
            "dominant_attack": None,
            "dominant_percentage": 0,
        }

    dominant_attack, count = attack_counts.most_common(1)[0]
    total_weight = sum(attack_counts.values())
    percentage = round((count / total_weight) * 100)

    recommended_armor = ATTACK_COUNTERS.get(dominant_attack,[])

    if percentage >= 60 and count >= 4:
        status = "strong"
        message = f"{dominant_attack} damage core"
    elif percentage >= 45:
        status = "medium"
        message = f"{dominant_attack} damage leaning"
    else:
        status = "mixed"
        message = "Mixed damage profile"

    return {
        "status": status,
        "message": message,
        "attack_counts": dict(attack_counts),
        "dominant_attack": dominant_attack,
        "dominant_percentage": percentage,
        "recommended_armor": recommended_armor,
    }