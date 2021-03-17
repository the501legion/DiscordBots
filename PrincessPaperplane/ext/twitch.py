import os
import twitch
from discord.ext.commands import Cog, Bot


class Twitch(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_chat = twitch.Chat(channel=f'#{os.getenv("TWITCH.CHANNEL")}',
                                       nickname="PaperBot", oauth=f'oauth:{os.getenv("TWITCH.OAUTH")}')

        # self.twitch_helix = twitch.Helix(client_id=f'{os.getenv("TWITCH.CLIENTID")}', use_cache=True,
        # client_secret=f'{os.getenv("TWITCH.SECRET")}')

        # identifier: str = self.twitch_helix.user("schrottler").id
        # mods = self.twitch_helix.api.get("moderation/moderators", {"broadcaster_id": identifier}).get()

        # print("")


def setup(bot: Bot):
    print("> Loading twitch integration")
    bot.add_cog(Twitch(bot))
