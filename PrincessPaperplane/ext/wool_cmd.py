from typing import List

from discord.ext import commands
from discord.ext.commands import Bot, Context

# configs
ALIASES: List[str] = ['wool', 'wolle', 'wa']
MESSAGE: str = "***Achtung!** {MENTION} will wieder Wolle kaufen!*"

USER: int = 168781680864133120
USER_STAGE: int = 762982903789125682
USER_LOCAL: int = 255003995871903745


# command group
@commands.command(name="WoolAlert", aliases=ALIASES)
async def wool_cmd(ctx: Context):
    user = ctx.bot.get_user(USER)
    user = ctx.bot.get_user(USER_STAGE) if user is None else user
    user = ctx.bot.get_user(USER_LOCAL) if user is None else user

    await ctx.channel.send(MESSAGE.format(MENTION=user.mention))


def setup(bot: Bot):
    print("> Loading WoolAlert")
    bot.add_command(wool_cmd)


def teardown(bot: Bot):
    print("> Unloading WoolAlert")
    bot.remove_command(wool_cmd)
