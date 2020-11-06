import random

from discord.ext import commands
from discord.ext.commands import Context, Cog

from ext.quotly import ROLES_WITH_WRITE_ACCESS
from ext.quotly.quote import Quote, EMPTY
from utility.cogs_enum import Cogs


async def post_quote(ctx: Context, quote: Quote):
    return await ctx.channel.send(
        "Quote #{ID}:\r\n \"{TEXT}\" - {AUTHOR}".format(ID=quote.id, TEXT=quote.text, AUTHOR=quote.author))


class Quotly(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = bot.get_cog(Cogs.DB.value)

    def fetch_quote(self) -> Quote:
        database = self.DB.connect()

        try:
            cursor = database.cursor()
            database.autocommit(True)

            cursor.execute("SELECT id, quote, author FROM quotes")
            if cursor.rowcount <= 0:
                return EMPTY

            return Quote(random.choice(cursor.fetchall()))

        except Exception as e:
            database.log(str(e))

        finally:
            database.close()

    def store_quote(self, text: str, author: str) -> Quote:
        database = self.DB.connect()

        try:
            cursor = database.cursor()
            database.autocommit(True)

            cursor.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (text, author,))
            cursor.execute("SELECT id, quote, author FROM quotes WHERE id = (SELECT MAX(id) FROM quotes)")
            data = cursor.fetchone()

            return Quote(data)

        except Exception as e:
            database.log(str(e))

        finally:
            database.close()

    @commands.group(aliases=['quote', 'q'])
    async def cmd_quote(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await self.get_quote(ctx)

    @cmd_quote.command(aliases=['add', 'a'])
    @commands.check_any(commands.has_any_role(ROLES_WITH_WRITE_ACCESS), commands.is_owner())
    async def add_quote(self, ctx: Context, author: str = None, *, text: str = None):
        if author is None:
            return await ctx.channel.send("Author is missing")

        if text is None:
            return await ctx.channel.send("Quote is missing")

        await post_quote(ctx, self.store_quote(text, author))

    @add_quote.error
    async def add_quote_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You are not allowed to use this, {MENTION}'.format(MENTION=ctx.author.mention))

    async def get_quote(self, ctx: Context):
        await post_quote(ctx, self.fetch_quote())
