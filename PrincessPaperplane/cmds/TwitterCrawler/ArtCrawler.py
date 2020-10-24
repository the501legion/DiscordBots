import os
import sched
import threading
import time
from queue import Queue

from discord import TextChannel, Embed, Emoji, RawReactionActionEvent, Member, Guild
from discord.ext import tasks, commands
from discord.ext.commands import Bot, Cog
from cmds.TwitterCrawler import fetch_tweets


class ArtCrawler(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.queue = Queue()

    async def run(self):
        b_token = os.getenv("TWITTER.BEARER.ART")

        threading.Thread(target=fetch_tweets, args=("ArtCrawler", b_token, self.queue)).start()
        self.tweet_handler.start()

    @tasks.loop(seconds=2.0)
    async def tweet_handler(self):
        channel: TextChannel = self.bot.get_channel(id=int(os.getenv('TWITTER.CHANNEL.CONFIRM')))
        message = self.queue.get()
        embed = Embed(title="TwitterArtCrawler", type="image", description=message)

        posted = await channel.send(message, embed=embed)
        await posted.add_reaction('✔')
        await posted.add_reaction('❌')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        guild: Guild = self.bot.get_guild(id=payload.guild_id)
        user: Member = guild.get_member(user_id=payload.user_id)
        
        if user == self.bot.user:
            return

        if payload.channel_id == int(os.getenv("TWITTER.CHANNEL.CONFIRM")):
            post_channel: TextChannel = self.bot.get_channel(int(os.getenv("TWITTER.CHANNEL.POSTED")))
            channel: TextChannel = self.bot.get_channel(payload.channel_id)
            post = await channel.fetch_message(payload.channel_id)
            emoji: Emoji = payload.emoji

            if emoji == '❌':
                # delete old post
                await post.delete()
                await channel.send("Beitrag abgelehnt!")

            if emoji == '✔':
                await post_channel.send(post.content)

                # delete old post
                await post.delete()
