import discord
from discord.ext import commands

from cmds.Quotes import get_random
from configs.cmd_config import STRINGS
from configs.quote_config import WRITE_ACCESS, READ_ACCESS
from utility import Database


async def write_access_granted(ctx: commands.context):
    for role in ctx.author.roles:
        if role.id in WRITE_ACCESS:
            return True

    return False


async def read_access_granted(ctx: commands.context):
    for role in ctx.author.roles:
        if role.id in READ_ACCESS:
            return True

    return False


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['quote', 'q'])
    @commands.check(read_access_granted)
    async def cmd_quote(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.get_quote(ctx)

    @cmd_quote.command(aliases=['add', 'a'])
    @commands.check(write_access_granted)
    async def add_quote(self, ctx: commands.Context, author: discord.Member = None, *, text=None):
        try:
            if author is None:
                return await ctx.channel.send("Author is missing!")

            if text is None:
                return await ctx.channel.send("Quote is missing!")

        except Exception as e:
            Database.log(str(e))

    async def get_quote(self, ctx: commands.Context):
        try:
            quote = get_random()
            return await ctx.channel.send(
                STRINGS.QUOTE_MESSAGE.value.format(TEXT=quote.text, AUTHOR=quote.author))

        except Exception as e:
            self.DB.log(str(e))
