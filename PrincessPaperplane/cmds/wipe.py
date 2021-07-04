

import configs.cmd_config as cmd_config
from discord.ext import commands
from configs.cmd_config import STRINGS, ALIASES


class Wipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def purge(self, channel, msgs=0):
        if msgs == 0:
            await channel.purge()
        else:
            await channel.purge(limit=msgs)

    @commands.command(aliases=ALIASES.WIPE.value)
    async def cmd_wipe(self, ctx: commands.Context, args):
        try:
            msgs = int(args) + 1
        except:
            msgs = 0
        await self.purge(ctx.channel, msgs)
    
