import os
import threading
from pathlib import Path
from queue import Queue

from discord import TextChannel, Embed
from discord.ext import tasks
from discord.ext.commands import Bot, Cog

from cmds.TwitterCrawler import fetch_tweets


class ArtCrawler(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.queue = Queue()

    async def run(self):
        b_token = os.getenv("TWITTER.BEARER.ART")

        # fetch tweets in separate thread
        threading.Thread(target=fetch_tweets, args=("ArtCrawler", b_token, self.queue)).start()
        self.tweet_handler.start()

    @tasks.loop(seconds=60.0)
    async def tweet_handler(self):
        channel: TextChannel = self.bot.get_channel(id=int(os.getenv('TWITTER.CHANNEL.CONFIRM')))
        tweet = self.queue.get()

        author = tweet['includes']['users'][0]
        embed = Embed(title="PaperBot",
                      type="image",
                      description=tweet['data']['text'],
                      url=f"https://twitter.com/{author['username']}/status/{tweet['data']['id']}")

        media_url = tweet['includes']['media'][0]['url']
        embed.set_thumbnail(url=media_url)
        embed.set_image(url=Path('../../res/img') / 'Twitter_Social_Icon_Circle_Color.png')

        embed.set_author(name=author['name'],
                         icon_url=author['profile_image_url'],
                         url=f"https://twitter.com/{author['username']}")

        await channel.send(embed=embed)
