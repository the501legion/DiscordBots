from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, Bot
from howlongtobeatpy import HowLongToBeat, HowLongToBeatEntry


class HLTB(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='hltb', aliases=['hl', 'howlong', 'howlongtobeat'], help="Lookup estimated playtime for a game")
    async def hltb(self, ctx: commands.Context, *, game: str):
        result_list = await HowLongToBeat(0.0).async_search(game, similarity_case_sensitive=False)
        if result_list is not None and len(result_list) > 0:
            g: HowLongToBeatEntry = max(result_list, key=lambda element: element.similarity)

            embed = Embed(title=g.game_name)
            embed.set_author(name="How Long To Beat", url="https://howlongtobeat.com/")
            embed.add_field(name="Main Story", value=f"{g.gameplay_main} {g.gameplay_main_unit}")
            embed.add_field(name="Story + Extras", value=f"{g.gameplay_main_extra} {g.gameplay_main_extra_unit}")
            embed.add_field(name="Completionist", value=f"{g.gameplay_completionist} {g.gameplay_completionist_unit}")

            embed.add_field(name="Link", value=g.game_web_link)
            embed.set_thumbnail(url=f"https://howlongtobeat.com{g.game_image_url}")

            return await ctx.channel.send(embed=embed)

        return await ctx.channel.send(f"No results for {game} :(")
