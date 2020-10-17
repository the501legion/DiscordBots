from enum import Enum

PREFIXES = ['!']

class ALIASES(Enum):
	RANK = ['rank', 'rang', 'level', 'lvl']
	RANK_TRACK = ['track']
	RANK_TRACK_TOGGLE = ['toggle']
	DICE = ['dice', 'w', 'd']
	RANDOM = ['wahl', 'pick', 'choose', 'random']

class STRINGS(Enum):
	DICE_RESULT = "{MENTION} Du hast folgende Zahlen gewürfelt: " #Leave whitespace at end!
	RANK_EMBED_TITLE = "Dein aktuelles Level: {LEVEL}"
	RANK_EMBED_DESCRIPTION = "Aktuelle XP: {EXP}\nVerbleibende XP bis Level {NEXT_LEVEL}: {EXP_LEFT}"
	RANK_IMAGE_GENERATOR_URL = "https://501-legion.de/princesspaperplane/generateLevel.php?user={AUTHOR_ID}&time={TIME}{EXT}"

	RANK_TRACK_TOGGLE_BADARGS = "{MENTION}, du musst einen erkennbaren |wahr| oder |falsch| wert angeben!"
	RANK_TRACK_TOGGLE_TRUE = "{MENTION}, deine XP werden nun getrackt!"
	RANK_TRACK_TOGGLE_FALSE = "{MENTION}, deine XP werden nicht mehr getrackt!"
	
	QUOTE_MESSAGE = "'{TEXT}' -{AUTHOR}"

