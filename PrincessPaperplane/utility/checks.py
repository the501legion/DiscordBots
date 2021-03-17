from typing import Optional

from discord.ext import commands


class Checks:

    @staticmethod
    def is_channel(channel_id: int, check_on_server_id: Optional[int] = -1):
        """Checks if bot can accept commands in channel

        Args:
            channel_id (int): Allowed channel
            check_on_server_id (Optional[int], optional): Server ID on which to check for channel. Defaults to 0.

        Returns:
            [type]: Predicate
        """

        # Define predicate to be checked
        async def predicate(ctx):
            if ctx.guild.id == check_on_server_id and ctx.channel.id != channel_id:  # only allow !rank / !rang in #bod_spam
                return False
            else:
                return True

        # Return as check, use with decorator
        return commands.check(predicate)
