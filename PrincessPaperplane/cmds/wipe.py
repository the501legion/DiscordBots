

import configs.cmd_config as cmd_config
from discord.ext import commands
from configs.cmd_config import STRINGS, ALIASES


class Wipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    async def purge(self, channel):
            await channel.purge()
            await channel.send("Beachten Sie mich nicht, ich putze hier nur.")
    @commands.command(aliases=ALIASES.WIPE.value)
    async def cmd_wipe(self, ctx: commands.Context):

        await self.purge(ctx.channel)
    
