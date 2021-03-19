import os
import twitch
from discord.ext.commands import Cog, Bot


class Twitch(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_chat = twitch.Chat(channel=f'#{os.getenv("TWITCH.CHANNEL")}',
                                       nickname="PaperBot",
                                       oauth=f'oauth:{os.getenv("TWITCH.OAUTH")}')


def setup(bot: Bot):
    print("> Loading Twitch integration")
    bot.add_cog(Twitch(bot))
