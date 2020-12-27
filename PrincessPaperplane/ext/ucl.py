from discord.ext import commands


@commands.command(aliases=['wolle'])
async def wool(ctx: commands.Context):
    await ctx.channel.send("Achtung! Natascha will wieder Wolle kaufen!")


def setup(bot):
    print("> Loading utility command library")
    bot.add_command(wool)
