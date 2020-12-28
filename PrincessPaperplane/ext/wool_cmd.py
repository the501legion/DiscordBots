from discord.ext import commands
from discord.ext.commands import Bot, Context
from typing import List

# configs
ALIASES: List[str] = ['wool', 'wolle', 'wa']
USER: int = 168781680864133120
MESSAGE: str = "***Achtung!** {MENTION} will wieder Wolle kaufen!*"


# command group
@commands.command(name="WoolAlert", aliases=ALIASES)
async def wool_cmd(ctx: Context):
    await ctx.channel.send(MESSAGE.format(MENTION=ctx.bot.get_user(USER).mention))


def setup(bot: Bot):
    print("> Loading WoolAlert")
    bot.add_command(wool_cmd)


def teardown(bot: Bot):
    print("> Unloading WoolAlert")
    bot.remove_command(wool_cmd)
