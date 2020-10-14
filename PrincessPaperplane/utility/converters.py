from discord.ext import commands
from typing import List, Union

class BoolParser(commands.Converter):
    """Converts a string to boolean value, based on content of string, not existance
    """
    def __init__(self, true_strings: List[str], false_strings: List[str]):
        """[summary]

        Args:
            true_strings (List[str]): Strings that resolve to a True value
            false_strings (List[str]): Strings that resolve to a False value
        """
        # Convert all to lower case, just in case
        self.true_strings = [true_string.lower() for true_string in true_strings]
        self.false_strings = [false_string.lower() for false_string in false_strings]

    async def convert(self, ctx, argument) -> Union[bool , None]:
        lowered = argument.lower()
        if lowered in self.true_strings:
            return True
        elif lowered in self.false_strings:
            return False
        else:
            return None #None of both was catched