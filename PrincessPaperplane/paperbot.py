#!/usr/bin/python3
# coding=utf-8

import re  # Regex

# import modules
import configs.secret as secret
import configs.guild_config as guild_config
import configs.roles_config as roles_config
import discord
import MySQLdb
from discord.ext import commands

import utility.db
from cmds.dice import Dice
from cmds.rank import Rank
from cmds.roles import Roles
from utility.checks import is_in_channel
from utility.cogs_enum import Cogs

# create bot
bot = commands.Bot(command_prefix='!')

# Add cogs
def add_cogs():
    bot.add_cog(DB())
    bot.add_cog(Rank(bot))
    bot.add_cog(Dice(bot))
    bot.add_cog(Roles(bot))
add_cogs()

DB = bot.get_cog(Cogs.DB)
ROLES = bot.get_cog(Cogs.ROLES)

# Discord API key
API_KEY = secret.API_KEY

prefixes_regex = '(' + "|".join(bot.command_prefix) + ')'
DICE_CMD_REGEX = re.compile(r"^({prefix})([w,d])".format(prefix=prefixes_regex))

# start bot
@bot.event
async def on_ready():
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
        if guild.id == guild_config.TEST_SERVER:
            bot.user.name = bot.user.name + " (Test)"

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name='twitch.tv/princesspaperplane', type=discord.ActivityType.watching))
    print('------')

    await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.ROLES, roles_config.EMOTES, roles_config.TEXT)
    await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL_TEST, roles_config.ROLES_TEST, roles_config.EMOTES_TEST, roles_config.TEXT_TEST)

@bot.event
async def on_message(message):
    await handle_command(message)

async def handle_command(message):
        # Handle command stuff
    match = DICE_CMD_REGEX.match(message.content)
    if bool(match):
        #Split message content: !w6x8 becomes !w 6x8. Important for command extension, so it can extract parameters
        cmd_length = len(match.group(1)) + len(match.group(2))
        message.content = message.content[:cmd_length] + " " + message.content[cmd_length:]
    await bot.process_commands(message)

bot.run(API_KEY)
