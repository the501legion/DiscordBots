from discord.ext import commands
from discord.ext.commands import Bot

from utility.cogs_enum import Cogs


class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = bot.get_cog(Cogs.DB.value)

    def store_request(self, request_type: str, request: str):
        db = self.DB.connect()

        try:
            cur = db.cursor()
            db.autocommit(True)

            cur.execute("INSERT INTO requests (type, text) VALUES(%s, %s)", (request_type, request))
        except Exception as e:
            self.DB.log(str(e))

        finally:
            db.close()

    @commands.command()
    async def bug(self, ctx: commands.Context, *, bug_report: str = None):
        if bug_report is None:
            return await ctx.channel.send("Missing bug report")

        self.store_request("bug", bug_report)

    @commands.command()
    async def feature(self, ctx: commands.Context, *, feature_request: str = None):
        if feature_request is None:
            return await ctx.channel.send("Missing feature request")

        self.store_request("feature", feature_request)


def setup(bot: Bot):
    print("> Loading Requests")

    bot.add_cog(Requests(bot))
