import json
import os
import threading
from queue import Queue

import requests
from discord import TextChannel
from discord.ext import tasks

from ext import HTTP_CODES


def fetch_tweets(queue: Queue):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=attachments.media_keys,author_id&media.fields"
        "=preview_image_url,url&user.fields=id,profile_image_url,username",
        headers={"Authorization": "Bearer {}".format(os.getenv("TWITTER.BEARER.ART"))}, stream=True
    )

    status_code = response.status_code
    print(f"> Twitter Crawler Status: {HTTP_CODES.get(status_code, 'Something went wrong')} ({status_code})")
    if status_code == 200:
        for raw_tweet in response.iter_lines():
            if raw_tweet:
                queue.put(json.loads(str(raw_tweet, 'utf-8')))


@tasks.loop(seconds=int(os.getenv('TWITTER.TIMER', 60)))
async def tweet_handler(bot, queue: Queue):
    if os.getenv('TWITTER.CHANNEL.CONFIRM') == "":
        return
        
    channel: TextChannel = bot.get_channel(id=int(os.getenv('TWITTER.CHANNEL.CONFIRM')))
    if queue.qsize() > 0:
        tweet = queue.get(False)
        # tweet_id = tweet['matching_rules'][0]['id']
        author = tweet['includes']['users'][0]
        # embed = Embed(title="PaperBot",
        #              type="image",
        #              description=tweet['data']['text'],
        #              url=f"https://twitter.com/{author['username']}/status/{tweet['data']['id']}")

        # media_url = tweet['includes']['media'][0]['url']
        # embed.set_image(url=media_url)
        # embed.set_image(url=Path('../../res/img') / 'Twitter_Social_Icon_Circle_Color.png')

        # embed.set_author(name=author['name'],
        #                 icon_url=author['profile_image_url'],
        #                 url=f"https://twitter.com/{author['username']}")

        # await channel.send(embed=embed)
        await channel.send(f"https://twitter.com/{author['username']}/status/{tweet['data']['id']}")


def setup(bot):
    print("> Loading twitter crawler")
    q = Queue()

    threading.Thread(target=fetch_tweets, args=(q,)).start()
    tweet_handler.start(bot, q)
