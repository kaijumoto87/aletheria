# Coinage system for Aletheria RPG:

def add_money(total_talet: int, amount_talet: int) -> int:
    """Return new total after adding new amount (both in talet)."""
    return total_talet + amount_talet

def can_afford(total_talet: int, cost_talet: int) -> bool:
    return total_talet >= cost_talet

def spend_money(total_talet: int, cost_talet: int) -> int:
    """Return new total after spending cost"""
    if cost_talet > total_talet:
        return total_talet
    return total_talet - cost_talet

def break_coins(total: int) -> dict:
    """Convert total talet into drachma/shille/talet."""
    drachma = total // 100
    remainder = total % 100

    shille = remainder // 10
    talet = remainder % 10

    return {
        "drachma": drachma,
        "shille": shille,
        "talet": talet,
    }
def format_coins(total: int) -> str:
    coins = break_coins(total)

    parts = []
    if coins["drachma"]:
        parts.append(f"{coins['drachma']} drachma")
    if coins["shille"]:
        parts.append(f"{coins['shille']} shille")
    if coins["talet"] or not parts:
        parts.append(f"{coins['talet']} talet")

    return ", ".join(parts)
"""
Example usage:
0        → "0 talet"
7        → "7 talet"
23       → "2 shille, 3 talet"
145      → "1 drachma, 4 shille, 5 talet"
1200     → "12 drachma"
"""