

import configs.guild_config as guild_config
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
    async def cmd_wipe(self, ctx: commands.Context, args = None):
        modRole = ctx.guild.get_role(guild_config.MOD_ROLE)
        princessRole = ctx.guild.get_role(guild_config.PRINCESS_ROLE)
        channel = ctx.guild.get_channel(guild_config.BOT_CHANNEL)

        if modRole not in ctx.author.roles and princessRole not in ctx.author.roles:
            await channel.send(ctx.author.mention + " Finger weg von meinem Besen!")
            return

        try:
            msgs = int(args) + 1
        except ValueError:
            await channel.send(ctx.author.mention + " Ich kann so nicht arbeiten! Nur mit !wipe [Ganzzahl]")
            return
        except:
            msgs = 0
        await self.purge(ctx.channel, msgs)
    
