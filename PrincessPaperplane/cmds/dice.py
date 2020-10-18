from random import sample, randint
import configs.cmd_config as cmd_config
from discord.ext import commands
from configs.cmd_config import STRINGS, ALIASES
import typing

class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=ALIASES.DICE.value)
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
        content = STRINGS.DICE_RESULT.value.format(MENTION=author.mention)

        for i in range(0, amount):
            if i != 0:
                content = content + ", "
            content = content + str(randint(1, dice))
        await ctx.channel.send(content=content)

    @commands.command(aliases=ALIASES.RANDOM.value)
    async def cmd_random(self, ctx: commands.Context, choice_amount: typing.Optional[int] = 1, *args: str):
        """Wählt zufälliges Element aus

        Args:
            ctx (commands.Context): [description]
        """

        mention : str = ctx.author.mention

        #No values below zero
        if choice_amount <= 0: 
            await ctx.send(STRINGS.RANDOM_INVALID_NUMER.value.format(MENTION=mention))
            return
        # Choices have to be given
        if args is None or args.count <= 0:
            await ctx.send(STRINGS.RANDOM_NO_CHOICES.value.format(MENTION=mention))
            return

        choice_amount = min(choice_amount, len(args)) #Don't go over the amount of possible
        choices = sample(population=args, k=choice_amount)
        await ctx.send(f"{mention}, deine Zufallswahl: {' , '.join(choices)}")
                
