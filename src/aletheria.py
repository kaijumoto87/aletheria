"""
Notes & Plans:
- Make coinage system and assign values to items.
- Add more item types (armor, potions, etc).
- Add biome variety (caves, swamps, etc).
- Seperate monsters into different biomes.
- Make potions usable in combat and exploration.
- Add spells and magic system with level locks and mana costs.
Note: First spell could be something like "Air Blast" that does 7 damage costing 5 mana and with a casting warm up of 2 turns that unlocks at level 2 if manna is 12 or higher.
- Make spell scrolls that can be found in loot and used to learn new spells.
- Refactor loot drops to have drop chances and multiple items.
- Make a player info save file system.
- Incorperate mana into leveling system and add mana potions to loot.
- Give an optional npc encounter at the start of game that gives the player some base for lore and the potential for a small potion or basic weapon (that gives a small boost but isn't strictly necessary) to help them survive the early game.
- Add a "rest" action in the exploration loop that allows the player to recover some health but with a chance of being ambushed by a monster.
- Add a "search" action in the exploration loop that allows the player to find hidden items or clues in certain areas, but also with a chance of triggering a trap or monster encounter.
- Make seperate files for different modules (player, monsters, combat, exploration, etc) and import them into the main game file to keep things organized as the codebase grows. 😭
- Run a mental (renice +6 -p coding.py) and sleep at some point 💀
- Add a "save and quit" option that writes the player's current state to a file, and a "load game" option at the start that allows them to continue from where they left off.
- Add a simple text-based map system that tracks the player's location in the world and allows them to navigate between different areas (village, forest, cave, etc) with unique encounters and loot in each.
- Make more areas to explore beyond the Dark Forest, each with their own unique monsters, loot, and challenges. For example, a dark cave system with bats and giant spiders, or a haunted swamp with ghosts and poisonous plants.
Note: When a task is completed, add a note in the code like this: " ----- IGNORE ----- " so that I can easily see what has been done and what still needs work when I review the code later.
"""
# Note for next time: -----> swap all instances of "Gold" with coinage used in currency.py


print("Welcome to Aletheria!")
print()
print("You have now entered a world of magic and lies...")
print("Seek the truth, adventurer. Survive if you can...")
print()
print()

try:
    name = input("What is your name adventurer? ")
except (EOFError, KeyboardInterrupt):
    print("\nGoodbye, adventurer.")
    raise SystemExit
print(f"Welcome, {name}!")
print()

# PLAYER STATS
import random

def create_player() -> dict:
    """Create and return a new player state dict."""
    return {
        "name": name,
        "level": 1,
        "exp": 0,
        "exp_to_next": 10,
        "health": random.randint(18, 24),
        "strength": random.randint(4, 7),
        "courage": random.randint(20, 35),
        "mana": random.randint(10, 15),
        "inventory": [],
        "equipped_weapon": "fists",
        "weapon_bonus": 0,
        "coins": 0,
    }

from data.currency import add_money, spend_money, format_coins

def show_player_stats(p: dict) -> None:
    print("\nYour stats:")
    print(f"Level: {p['level']}")
    print(f"EXP: {p['exp']}/{p['exp_to_next']}")
    print(f"Health: {p['health']}")
    print(f"Strength: {p['strength']}")
    print(f"Courage: {p['courage']}")
    print(f"Mana: {p['mana']}\n")


def get_crit_chance(courage):
    """
    Turn courage into a critical-hit chance.
    Returns a number between 0.0 and 0.20 (0%-20%).
    """
    base = 0.001  # 0.1% at courage = 1
    # choose a slope so that around courage 35 you reach ~20%
    scale = (0.20 - base) / 34

    chance = base + scale * (courage - 1)

    # clamp between 0 and 20%
    if chance < 0:
        chance = 0
    if chance > 0.20:
        chance = 0.20

    return chance

# weapon types:
weapon_stats = {
    "fists": 0,
    "bronze dagger": 3,
    "rusty sword": 5,
    "orcish axe": 8,
    "elven bow": 6,
}

MONSTERS = [
    {
        "name": "Goblin",
        "health_range": (10, 15),
        "loot_table": ["small health potion", "gold coin", "rusty sword"],
        "exp_reward": 10,
    },
    {
        "name": "Wolf",
        "health_range": (12, 18),
        "loot_table": ["wolf pelt", "sharp fang", "gold coin"],
        "exp_reward": 12,
    },
    {
        "name": "Orc",
        "health_range": (15, 22),
        "loot_table": ["orcish axe", "gold coin", "health potion"],
        "exp_reward": 15,
    },
    {
        "name": "Dark Elf",
        "health_range": (18, 25),
        "mana_range": (5, 10),
        "loot_table": ["elven bow", "magic crystal", "mana potion"],
        "exp_reward": 20,
    },
    {
        "name": "Bloody Bear",
        "health_range": (20, 30),
        "loot_table": ["bear claw", "thick fur", "large health potion"],
        "exp_reward": 25,
    },
    {
        "name": "Skeleton Warrior",
        "health_range": (15, 20),
        "loot_table": ["bone sword", "shield fragment", "gold coin"],
        "exp_reward": 18,
    },
    {
        "name": "Fenrir Wolf",
        "health_range": (40, 65),
        "loot_table": ["fenrir fang", "mythical pelt", "large health potion"],
        "exp_reward": 80,
    },
]

def level_up_check(player: dict) -> None:
    """Increase player level when they have enough EXP."""
    leveled = False
    while player["exp"] >= player["exp_to_next"]:
        player["exp"] -= player["exp_to_next"]
        player["level"] += 1
        health_gain = random.randint(1, 3)
        player["health"] += health_gain
        player["strength"] += 1
        player["exp_to_next"] += random.randint(5, 10)
        leveled = True
        print()
        print(f"*** You leveled up! You are now Level {player['level']}! ***")
        print(f"Health increased by {health_gain} to: {player['health']}")
        print(f"Strength increased to: {player['strength']}")
        print(f"Next level at: {player['exp_to_next']} EXP")
    if not leveled:
        return

def canonicalize_item(item_name: str) -> str:
    """Return canonical (internal) form for an item name."""
    return item_name.strip().lower()

def human_item(item_name: str) -> str:
    """Return human-friendly form of an item."""
    return item_name.title()

def spawn_monster() -> dict:
    """Pick a monster template and return a monster instance dict."""
    template = random.choice(MONSTERS)
    min_hp, max_hp = template["health_range"]
    hp = random.randint(min_hp, max_hp)
    return {
        "name": template["name"],
        "max_health": hp,
        "health": hp,
        "loot_table": [canonicalize_item(x) for x in template.get("loot_table", [])],
        "exp_reward": template.get("exp_reward", 0),
        # attack potential: scale roughly with health
        "attack_range": (1, min(8, max(3, hp // 4))),
    }

def list_weapons_in_inventory(player: dict) -> list:
    """Return a list of weapon item names (canonical) the player can equip."""
    return [item for item in player["inventory"] if item in weapon_stats and item != "fists"]

def equip_weapon(player: dict) -> None:
    """Prompt the player to equip a weapon from inventory."""
    weapon_options = list_weapons_in_inventory(player)
    if not weapon_options:
        print("You have no other weapons you can equip.")
        print(f"Current weapon: {human_item(player['equipped_weapon'])} (+{player['weapon_bonus']})\n")
        return

    print("\nWeapons you can equip:")
    for w in weapon_options:
        print(f"- {human_item(w)} (+{weapon_stats[w]})")
    print()
    try:
        choice = input("Type the name of the weapon that you want to equip: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nEquip cancelled.")
        return

    if choice in weapon_options:
        player["equipped_weapon"] = choice
        player["weapon_bonus"] = weapon_stats[choice]
        print(f"You equip the {human_item(player['equipped_weapon'])}.")
        print(f"New weapon bonus: +{player['weapon_bonus']} attack\n")
    else:
        print("\nYou fumble with your gear and fail to equip anything.\n")

def roll_player_attack(player: dict):
    """Return (damage, is_crit)."""
    crit = random.random() < get_crit_chance(player["courage"])
    base = random.randint(1, max(1, player["strength"] + player["weapon_bonus"]))
    dmg = base * (2 if crit else 1)
    return dmg, crit

def try_escape(player: dict, monster: dict) -> bool:
    """Return True if escape succeeded, False if failed (and player may be attacked)."""
    escape_chance = 60 + (player["courage"] - 20) // 2  # courage affects chance
    escape_chance = max(10, min(90, escape_chance))
    roll = random.randint(1, 100)
    if roll <= escape_chance:
        player["courage"] = max(0, player["courage"] - 1)
        print("\nYou turn and flee! You manage to escape the monster!")
        print(f"courage: {player['courage']}")
        return True
    else:
        print("\nYou try to run, but the monster blocks your path!")
        m_dmg = random.randint(*monster["attack_range"])
        player["health"] -= m_dmg
        print(f"The monster strikes you for {m_dmg} damage as you flee!")
        print(f"Your health: {player['health']}")
        return False

def combat_encounter(player: dict, monster: dict) -> bool:
    """Run combat. Return True if player survived, False if died."""
    print(f"A {monster['name']} leaps out! (HP: {monster['health']})")

    while monster["health"] > 0 and player["health"] > 0:
        try:
            action = input("Choose action (attack, run, inv, stats, equip, help): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting combat.")
            return False

        if action in ("attack", "a"):
            dmg, crit = roll_player_attack(player)
            monster["health"] -= dmg
            print(f"You deal {dmg} damage{' (CRITICAL!)' if crit else ''}.")
            if monster["health"] <= 0:
                break
            # monster attacks back
            m_dmg = random.randint(*monster["attack_range"])
            player["health"] -= m_dmg
            print(f"The {monster['name']} hits you for {m_dmg} damage!")
            print(f"Your health: {player['health']}")
            print(f"Monster health: {monster['health']}")
        elif action in ("run", "r"):
            if try_escape(player, monster):
                return True
        elif action in ("inv", "inventory", "i"):
            print("\nYour Inventory:")
            if player["inventory"]:
                for item in player["inventory"]:
                    print(f"- {human_item(item)}")
            else:
                print("(Empty)")
            print()
            continue
        elif action in ("stats", "s"):
            show_player_stats(player)
            print(f"Strength: {player['strength']}")
            print(f"Courage: {player['courage']}\n")
            continue
        elif action in ("equip", "e"):
            equip_weapon(player)
            continue
        elif action in ("help", "h", "?"):
            print("Available actions: attack, run, inv (inventory), stats, equip, help")
            continue
        else:
            print("You hesitate and do nothing...")

    if player["health"] <= 0:
        print("You collapse... The darkness takes you.")
        return False

    # Victory
    print()
    print("You defeated the monster! Victory is yours!")
    loot = random.choice(monster["loot_table"]) if monster["loot_table"] else None
    if loot:
        player["inventory"].append(loot)
        print(f"The monster dropped: {human_item(loot)}!")
        # auto-equip specific weapons if wanted
        if loot in weapon_stats and player.get("equipped_weapon") == "fists":
            player["equipped_weapon"] = loot
            player["weapon_bonus"] = weapon_stats[loot]
            print(f"You equip the {human_item(loot)}")
            print(f"Weapon bonus: +{player['weapon_bonus']} attack")
        else:
            print("You can type 'equip' later to change weapons.")
    else:
        print("The monster dropped nothing.")

    # EXP reward
    gained_exp = monster.get("exp_reward", 0)
    player["exp"] += gained_exp
    print(f"You gained {gained_exp} EXP!")
    print(f"Total EXP: {player['exp']}/{player['exp_to_next']}")

    level_up_check(player)

    return True

def forest_exploration(player: dict) -> bool:
    """
    Loop exploration in the Dark Forest. Return True if player leaves alive,
    False if player dies in the forest.
    """
    print("You continue into the Dark Forest. Stay alert.")
    while player["health"] > 0:
        try:
            choice = input("What do you do? (explore, leave, inv, stats, equip, help): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nYou quietly leave the area.")
            return True

        if choice in ("explore", "e", "investigate", "i"):
            encounter_chance = random.randint(1, 100)
            if encounter_chance <= 75:  # 75% chance to meet a monster
                monster = spawn_monster()
                survived = combat_encounter(player, monster)
                if not survived:
                    print("You were slain in the forest.")
                    return False
                # loop continues automatically after victory
            else:
                print("You press on and find nothing... a sense of unease follows you.")
            continue
        elif choice in ("leave", "l", "retreat"):
            print("You leave the Dark Forest and return to the village.")
            return True
        elif choice in ("inv", "inventory"):
            print("\nYour Inventory:")
            if player["inventory"]:
                for item in player["inventory"]:
                    print(f"- {human_item(item)}")
            else:
                print("(Empty)")
            print()
            continue
        elif choice in ("stats", "s"):
            show_player_stats(player)
            continue
        elif choice in ("equip", "eq", "e"):
            equip_weapon(player)
            continue
        elif choice in ("help", "h", "?"):
            print("Options: explore (chance to encounter), leave, inv, stats, equip, help")
            continue
        else:
            print("Unrecognized command. Type 'help' for options.")
            continue
    # fell out of loop because health <= 0
    print("You collapse... The darkness takes you.")
    return False

# Initialize player
player = create_player()

print(f"Your starting stats:")
show_player_stats(player)

print()  

try:
    choice = input("Do you want to enter the Dark Forest? (yes/no) ").strip().lower()
except (EOFError, KeyboardInterrupt):
    print("\nGoodbye, adventurer.")
    raise SystemExit

if choice == "yes" or choice.startswith("y"):
    print("You step into the forest. The trees seem to whisper your name...")

    # SECOND CHOICE (glowing chest) - do this once and do NOT loop it
    print()
    try:
        forest_choice = input("You see a strange glow on the path. Do you follow it or ignore it? (follow/ignore) ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nYou decide to leave the forest.")
        raise SystemExit

    if forest_choice in ("follow", "f"):
        print("You follow a small chest pulsing with light.")
        print("You open it and find a bronze dagger inside!")
        player['inventory'].append(canonicalize_item("Bronze dagger"))
        player['equipped_weapon'] = canonicalize_item("bronze dagger")
        player['weapon_bonus'] = weapon_stats["bronze dagger"]

        print("You equip the Bronze dagger")
        print(f"Weapon bonus: +{player['weapon_bonus']} attack")
        print("You can type 'equip' later to change weapons.")
        print()
        print("Armed with your new weapon, you return to the main path.")

    elif forest_choice in ("ignore", "i"):
        print("You stay on the main path, feeling a chill, but staying safe... for now.")
    else:
        print("You hesitate too long, the glow fades into the darkness.")
    print("You continue along the path...")
    print()

    # Investigate initial rustling once -- if choose to investigate, start the ongoing exploration loop afterwards.
    try:
        investigate_choice = input("You hear a rustling noise in the bushes nearby! Do you run away or investigate? (run/investigate) ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nYou quietly leave the area.")
        raise SystemExit

    if investigate_choice in ("investigate", "inv", "i"):
        encounter_chance = random.randint(1, 100)
        if encounter_chance <= 100:  # 100% chance for testing
            monster = spawn_monster()
            survived = combat_encounter(player, monster)
            if not survived:
                print("You fall. The light fades from your eyes as the forest claims another victim...")
            else:
                # Start loop after the initial encounter
                left_safely = forest_exploration(player)
                if not left_safely:
                    print("Game Over.")
        else:
            print("You discover nothing... you continue on.")
            left_safely = forest_exploration(player)
            if not left_safely:
                print("Game Over.")
    elif investigate_choice in ("run", "r"):
        print("You run away from the noise and decide to head back to the village for now.")
    else:
        print("You stand frozen, the noise fades, and you continue on cautiously.")
        left_safely = forest_exploration(player)
        if not left_safely:
            print("Game Over.")

else:
    print("You decide to stay in the village another day.")
