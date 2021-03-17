from discord.ext.commands import Bot

from ext.quotly.quote import Quote
from ext.quotly.quotly import Quotly


def setup(bot: Bot):
    print("> Loading Quotly")
    bot.add_cog(Quotly(bot))
