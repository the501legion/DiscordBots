from typing import Optional

from discord.ext import commands


def is_in_channel(channel_id : int, check_on_server_id : Optional[int] = 0):
    """Used as decorator that checks if bot can post in this channel"""
    #Define predicate to be checked
    async def predicate(ctx):
        if ctx.guild.id == check_on_server_id and ctx.channel.id != channel_id: # only allow !rank / !rang in #bod_spam
            return False
        else:
            return True

    # Return as check, use with decorator
    return commands.check(predicate)
