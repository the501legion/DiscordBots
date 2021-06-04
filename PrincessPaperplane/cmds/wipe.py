

import configs.cmd_config as cmd_config
from discord.ext import commands
from configs.cmd_config import STRINGS, ALIASES


class Wipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases = ALIASES.WIPE.value)
    async def cmd_wipe(self, ctx: commands.Context, args):
        
        await purge(ctx.channel)
