import random

import twitch
from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot

from ext.quotly.quote import Quote, EMPTY
from ext.twitch import Twitch
from utility.cogs_enum import Cogs

ROLES_WITH_WRITE_ACCESS = []  # Discord IDs
TWITCH_USER_WITH_ACCESS = []  # Twitch Name


async def post_quote(ctx: Context, quote: Quote):
    return await ctx.channel.send(
        "#{ID}: \"{TEXT}\" - {AUTHOR}".format(ID=quote.id, TEXT=quote.text, AUTHOR=quote.author))


class Quotly(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.DB = bot.get_cog(Cogs.DB.value)

        if not self.DB.exist("quotes"):
            self.setup()

        self.twitch: Twitch = bot.get_cog(Cogs.TWITCH.value)

        if self.twitch is not None:
            self.twitch.twitch_chat.subscribe(self.twitch_command_mapping)

    def setup(self) -> None:
        database = self.DB.connect()

        try:
            cursor = database.cursor()
            database.autocommit(True)

            cursor.execute(
                'CREATE TABLE quotes(id int auto_increment primary key, quote text not null, author text not null);'
            )

            # cursor.execute(
            #     'CREATE TABLE quotly_access(id int auto_increment primary key, token text not null, type bit not null);'
            # )

        except Exception as e:
            self.DB.log(str(e))

        finally:
            database.close()

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

    def twitch_command_mapping(self, message: twitch.chat.Message) -> None:
        if message.text == '!quote':
            q = self.fetch_quote()
            message.chat.send(f'/me "{q.text}" -{q.author}')

        if message.sender in TWITCH_USER_WITH_ACCESS:
            if message.text.startswith('!quote add'):
                tmp = message.text.split('!quote add')[1].strip().split(maxsplit=1)

                if message.text == '!quote add' or len(tmp) < 2:
                    return message.chat.send(f'/me @{message.sender} Missing Parameter!')

                q = self.store_quote(tmp[1], tmp[0])
                return message.chat.send(f'/me @{message.sender} added a new quote from {q.author}.')

            if message.text.startswith('!quote help'):
                return message.chat.send(f'/me Usage: !quote add <author> <quote>')

    @commands.group()
    async def quote(self, ctx: Context):
        """
        Handles the quote commands.
        """

        if ctx.invoked_subcommand is None:
            quote: Quote = self.fetch_quote()

            if quote is EMPTY:
                return await ctx.channel.send("Found no quote. Add one with !quote add <author> <quote>")

            await post_quote(ctx, quote)

    @quote.command(aliases=['add'], name="quote add", help="Adds a new quote.")
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
