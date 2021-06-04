#!/usr/bin/python3
# coding=utf-8

import re  # Regex
import sys
import os

# import modules

import traceback
import asyncio
import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

import configs.cmd_config as cmd_config
import configs.guild_config as guild_config
import configs.roles_config as roles_config
from cmds.dice import Dice
from cmds.wipe import Wipe
from cmds.quotes import Quotes
from cmds.rank import Rank
from cmds.roles import Roles
from ext import load_extensions
from utility.cogs_enum import Cogs
from utility.db import DB

# create bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=cmd_config.PREFIXES, intents=intents)


# Add cogs
def add_cogs():
    bot.add_cog(DB())
    bot.add_cog(Rank(bot))
    bot.add_cog(Dice(bot))
    bot.add_cog(Wipe(bot))
    bot.add_cog(Roles(bot))
    bot.add_cog(Quotes(bot))


add_cogs()

DB: DB = bot.get_cog(Cogs.DB.value)
ROLES: Roles = bot.get_cog(Cogs.ROLES.value)

prefixes_regex = '(' + "|".join(bot.command_prefix) + ')'
DICE_CMD_REGEX = re.compile(
    r"^({prefix})([w,d]\d)".format(prefix=prefixes_regex))


# start bot
@bot.event
async def on_ready():
    try:
        bot.user.name = "PaperBot"

        DB.log('Bot started')
        print('------')
        print('logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

        print('Connected to')
        for guild in bot.guilds:
            print("- " + guild.name)

        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(name='twitch.tv/princesspaperplane',
                                                            type=discord.ActivityType.watching))

        print('------')
        bot.loop.create_task(check_time())
        print('Loading Extensions')
        load_extensions(bot)

        print('------')
        if guild_config.SERVER_LIVE in bot.guilds:
            await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
        # await ROLES.update_reaction_msg(os.getenv("DISCORD.CHANNEL.ROLE.LIVE"), roles_config.EMOTE_ROLES)
        
    except Exception:
        DB.log("Error: " + traceback.format_exc())


@bot.event
async def on_message(message):
    print("on_message")
    

    await handle_command(message)


async def handle_command(message):
    print("Handle Command")

    # Handle command stuff
    match = DICE_CMD_REGEX.match(message.content)
    if bool(match):
        # Split message content: !w6x8 becomes !w 6x8. Important for command extension, so it can extract parameters
        cmd_length = len(match.group(1)) + len(match.group(2))
        message.content = message.content[:cmd_length] + \
            " " + message.content[cmd_length:]

    await bot.process_commands(message)


async def check_time():
    channel = bot.get_channel(768126859673731083)
    while True:
        now = datetime.datetime.now()
        print(now.hour, now.minute)
        if now.hour == 3 and now.minute == 0:
            await purge(channel)
        await asyncio.sleep(60)

async def purge(channel):
    await channel.purge()
    await channel.send("Beachten Sie mich nicht, ich putze hier nur.")


def main():
    print("Starting ...")

    # print command line arguments
    for arg in sys.argv[1:]:
        if arg == "-test":
            guild_config.SERVER = guild_config.SERVER_TEST
            guild_config.ROLE_CHANNEL = guild_config.ROLE_CHANNEL_TEST
            roles_config.EMOTE_ROLES = roles_config.EMOTE_ROLES_TEST
            print("Starting on testing environment")

    print(find_dotenv())

    load_dotenv(find_dotenv())
    print(os.getenv("DATABASE.HOST"))
    print(os.getenv("DISCORD.API_KEY"))
    API_KEY = os.getenv("DISCORD.API_KEY")

    # RUN BOT
    print(API_KEY)
    bot.run(API_KEY)


if __name__ == "__main__":
    main()
