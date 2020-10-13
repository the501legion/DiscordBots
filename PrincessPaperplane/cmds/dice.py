
from random import randint

import configs.cmd_config as cmd_config
from discord.ext import commands

class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=cmd_config.ALIASES["dice"])
    async def cmd_dice(self, ctx: commands.Context, args):
        author = ctx.author

        if 'x' in args:
            dice = int(args.split('x')[0])
            amount = int(args.split('x')[1])
        else:
            dice = int(args)
            amount = 1

        if dice < 1 or amount < 1:
            return

        # print rolled dices
        content = author.mention + " Du hast folgende Zahlen gewürfelt: "

        for i in range(0, amount):
            if i != 0:
                content = content + ", "
            content = content + str(randint(1, dice))
        await ctx.channel.send(content=content)
