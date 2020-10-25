from enum import Enum

PREFIXES = ['!']

class ALIASES(Enum):
	RANK = ['rank', 'rang', 'level', 'lvl']
	DICE = ['dice', 'w', 'd']

class STRINGS(Enum):
	DICE_RESULT = "{MENTION} Du hast folgende Zahlen gewürfelt: " #Leave whitespace at end!
	RANK_EMBED_TITLE = "Dein aktuelles Level: {LEVEL}"
	RANK_EMBED_DESCRIPTION = "Aktuelle XP: {EXP}\nVerbleibende XP bis Level {NEXT_LEVEL}: {EXP_LEFT}"
	RANK_IMAGE_GENERATOR_URL = "https://501-legion.de/princesspaperplane/generateLevel.php?user={AUTHOR_ID}&time={TIME}{EXT}"
	QUOTE_MESSAGE = "\"{TEXT}\" - {AUTHOR}"