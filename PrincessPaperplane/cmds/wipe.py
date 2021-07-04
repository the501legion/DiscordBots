

import configs.guild_config as guild_config
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
        role = ctx.guild.get_role(guild_config.MOD_ROLE)
        channel = ctx.guild.get_channel(guild_config.BOT_CHANNEL)
        chamber = ctx.guild.get_channel(guild_config.CHAMBER_CHANNEL)
        if role not in ctx.author.roles:
            await channel.send(ctx.author.mention + " Finger weg von meinem Besen!")     
            return
        if ctx.channel.id != channel.id and ctx.channel.id != chamber.id:
            await channel.send(ctx.author.mention + " Finger weg von meinem Besen!")     
            return
        await self.purge(ctx.channel)
    
