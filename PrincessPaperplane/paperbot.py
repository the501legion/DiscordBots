#!/usr/bin/python3
# coding=utf-8

import os
import re  # Regex
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

import configs.cmd_config as cmd_config
import configs.guild_config as guild_config
import configs.roles_config as roles_config
from cmds.dice import Dice
from cmds.quotes import Quotes
from cmds.rank import Rank
from cmds.roles import Roles
from ext import load_extensions
from utility.cogs_enum import Cogs
from utility.db import DB

# import modules

# create bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=cmd_config.PREFIXES, intents=intents)


# Add cogs
def add_cogs():
    bot.add_cog(DB())
    bot.add_cog(Rank(bot))
    bot.add_cog(Dice(bot))
    bot.add_cog(Roles(bot))
    bot.add_cog(Quotes(bot))


add_cogs()

DB: DB = bot.get_cog(Cogs.DB.value)
ROLES: Roles = bot.get_cog(Cogs.ROLES.value)

prefixes_regex = '(' + "|".join(bot.command_prefix) + ')'
DICE_CMD_REGEX = re.compile(r"^({prefix})([w,d]\d)".format(prefix=prefixes_regex))


# start bot
@bot.event
async def on_ready():
    try:
        bot.user.name = "PaperBot"

        DB.log('Bot started')
        print('------')
        print('DB.logged in as')
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
        await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
        # await ROLES.update_reaction_msg(os.getenv("DISCORD.CHANNEL.ROLE.LIVE"), roles_config.EMOTE_ROLES)
    except Exception:
        DB.log("Error: " + traceback.format_exc())


@bot.event
async def on_message(message):
    print("on_message")
    if message.guild.id != guild_config.SERVER:
        pass
        
    await handle_command(message)


async def handle_command(message):
    print("Handle Command")

    # Handle command stuff
    match = DICE_CMD_REGEX.match(message.content)
    if bool(match):
        # Split message content: !w6x8 becomes !w 6x8. Important for command extension, so it can extract parameters
        cmd_length = len(match.group(1)) + len(match.group(2))
        message.content = message.content[:cmd_length] + " " + message.content[cmd_length:]

    await bot.process_commands(message)


def main():
    print("Starting ...")

    # print command line arguments
    for arg in sys.argv[1:]:
        if arg == "-test":
            guild_config.SERVER = guild_config.SERVER_TEST
            guild_config.ROLE_CHANNEL = guild_config.ROLE_CHANNEL_TEST
            roles_config.EMOTE_ROLES = roles_config.EMOTE_ROLES_TEST
            print("Starting on testing environment")

    # REGISTER EXTENSIONS
    print('------')
    print('Loading Extensions')
    load_extensions(bot)

    load_dotenv(find_dotenv())
    API_KEY = os.getenv("DISCORD.API_KEY")

    # RUN BOT
    bot.run(API_KEY)


if __name__ == "__main__":
    main()
