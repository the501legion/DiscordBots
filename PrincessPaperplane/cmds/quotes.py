import random
from typing import List

import discord
from discord.ext import commands

from configs.cmd_config import STRINGS
from configs.quote_config import WRITE_ACCESS, READ_ACCESS
from utility.cogs_enum import Cogs


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
        self.DB = bot.get_cog(Cogs.DB.value)

    @commands.group(aliases=['quote', 'q'])
    @commands.check(read_access_granted)
    async def cmd_quote(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.get_quote(ctx)

    @cmd_quote.command(aliases=['add', 'a'])
    @commands.check(write_access_granted)
    async def add_quote(self, ctx: commands.Context, member: discord.Member = None, *, quote=None):
        db = self.DB.connect()

        try:
            cur = db.cursor()
            db.autocommit(True)

            if member is None:
                return await ctx.channel.send("Author is missing!")

            if quote is None:
                return await ctx.channel.send("Quote is missing!")

            # add new quote
            cur.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote, member.display_name,))
        except Exception as e:
            self.DB.log(str(e))

        finally:
            db.close()

    async def get_quote(self, ctx: commands.Context):
        db = self.DB.connect()

        try:
            cur = db.cursor()
            db.autocommit(True)
            cur.execute("SELECT quote, author FROM quotes")

            if cur.rowcount <= 0:
                return await ctx.channel.send("No quotes found!")

            qs: List = cur.fetchall()
            q = random.choice(qs)

            return await ctx.channel.send(
                STRINGS.QUOTE_MESSAGE.value.format(TEXT=q[0], AUTHOR=q[1]))

        except Exception as e:
            self.DB.log(str(e))

        finally:
            db.close()
