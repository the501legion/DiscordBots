from discord.ext.commands import Bot
from .hltb import HLTB


def setup(bot: Bot):
    bot.add_cog(HLTB(bot))
