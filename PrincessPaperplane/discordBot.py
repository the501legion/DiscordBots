#!/usr/bin/python3
# coding=utf-8

# import modules
import config
import discord
from discord.ext import commands
import MySQLdb
import time
from random import randint

# create bot
bot = commands.Bot(command_prefix='!')

# Discord API key
API_KEY = config.API_KEY

# server ids
LIVE_SERVER = 419549814376759297
TEST_SERVER = 426001973246951424

# channel ids for roles
ROLE_CHANNEL = 609860364309495819
ROLE_CHANNEL_TEST = 763103210155147264

# roles which will be given by emote
ROLES = [ 763105108841332766, 763105158078922763, 763105190765002783 ]
EMOTES = [ "😂", "🏞", "😗" ]

# database connection
DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASSWD = config.DB_PASSWD
DB_DB = config.DB_DB
DB_CHARSET = "utf8mb4"
DB_UNICODE = True

# create new database connection
def dbConnect():
    return MySQLdb.connect(host=DB_HOST,
        user=DB_USER,
        charset=DB_CHARSET,
        use_unicode=DB_UNICODE,
        passwd=DB_PASSWD,
        db=DB_DB)

# log text in console and in database
def log(text):
    print(text)

    try:
        db = dbConnect()
        cur = db.cursor()
        db.autocommit(True)
        cur.execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (text, time.time(), ))
    except Exception as e:
        log("Exception in log: " + str(e))
        pass

# start bot
@bot.event
async def on_ready():
    bot.user.name = "PaperBot"

    log('Bot started')
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    print('Connected to')
    for guild in bot.guilds:
        print("- " + guild.name)
        if guild.id == TEST_SERVER:
            bot.user.name = bot.user.name + " (Test)"

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name='twitch.tv/princesspaperplane', type=discord.ActivityType.watching))
    print('------')

    #await updateReactionMsg(ROLE_CHANNEL)
    await updateReactionMsg(ROLE_CHANNEL_TEST)

# update role message and add reactions
@bot.event
async def updateReactionMsg(roleChannel):
    channel = bot.get_channel(id=roleChannel)
    server = channel.guild
    msg = await channel.history().get(id=channel.last_message_id)

    if msg != None:
        for emote in msg.reactions:
            if emote.me == True:
                await msg.remove_reaction(emote.emoji, bot.user)
    else:
        msg = await channel.send("Hier stehen bald alle Streamer-Rollen, die ihr euch mit dem jeweiligen Emotes als Reaktion geben und wieder nehmen könnt.")

    string = "Hier stehen alle Rollen, die ihr euch mit den jeweiligen Emotes als Reaktion geben und wieder nehmen könnt:\n"
    for x in range(0, len(ROLES)):
        role = server.get_role(role_id=ROLES[x])
        await msg.add_reaction(EMOTES[x])
        string = string + "\n- Rolle " + role.name + " für " + EMOTES[x]

    await msg.edit(content=string)

# handle added reactions
@bot.event
async def on_raw_reaction_add(payload):
    await handleRoleReactions(payload)

# handle removed reactions
@bot.event
async def on_raw_reaction_remove(payload):
    await handleRoleReactions(payload)

# handle role reactions
@bot.event
async def handleRoleReactions(payload):
    if payload.channel_id == ROLE_CHANNEL or payload.channel_id == ROLE_CHANNEL_TEST:
        emoji = payload.emoji
        server = bot.get_guild(id=payload.guild_id)
        user = server.get_member(user_id=payload.user_id)

        if user == bot.user:
            return

        print(emoji.name)
        print(server.id)

        i = -1
        for x in range(0, len(ROLES)):
            if EMOTES[x] == emoji.name:
                i = x
                break

        if i == -1:
            return

        role = server.get_role(role_id=ROLES[i])
        log("Role: " + role.name)
        if role in user.roles:
            log("Role " + role.name + " removed from " + user.name)
            await user.remove_roles(role)
        else:
            log("Role " + role.name + " assigned to " + user.name)
            await user.add_roles(role)

# check new message
@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    server = message.guild

    if author.id == bot.user.id:
        return

    if message.content == "" or len(message.content) == 0:
        return

    string = "[" + server.name + "] " + author.name + " (#" + channel.name + "): " + message.content
    log(string)

    db = dbConnect()
    cur = db.cursor()
    db.autocommit(True)

    # check for banned channels to handle XP and levelup
    cur.execute("SELECT * FROM level_banned_channel WHERE channel = %s", (channel.id,))
    if cur.rowcount == 0:
        if server.id == LIVE_SERVER:
            cur.execute("SELECT exp, expTime, level FROM user_info WHERE id = %s", (author.id,))
        if server.id == TEST_SERVER:
            cur.execute("SELECT exp, expTime, level FROM user_info_test WHERE id = %s", (author.id,))

        if cur.rowcount > 0:
            result = cur.fetchone()
            exp = int(result[0])
            expTime = int(result[1])
            level = int(result[2])

            # skip cooldown on testing
            if server.id == TEST_SERVER:
                expTime = 0

            # has cooldown expired?
            if expTime + 60 <= time.time():
                addedExp = 15 + randint(0, 10)
                exp = exp + addedExp

                levelUp = await getLevelUp(level)

                log("Exp for Level-Up: %d, current XP: %d" % (levelUp, exp))

                # trigger levelup if enough XP gained
                if exp >= levelUp:
                    level = level + 1
                    exp = 0

                    if server.id == LIVE_SERVER:
                        cur.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel = %s", (level,))
                    if server.id == TEST_SERVER:
                        cur.execute("SELECT rewardRole FROM level_reward_test WHERE rewardLevel = %s", (level,))

                    if server.id == TEST_SERVER:
                        await channel.send(author.mention + " Du bist ein Level aufgestiegen! Nun bist du auf Level " + str(level) + "!")

                        if cur.rowcount > 0:
                            role = server.get_role(role_id=int(cur.fetchone()[0]))

                            # give user new role as reward
                            if role not in author.roles:
                                log("Assign " + author.name + " new role " + role.name)
                                await author.add_roles(role)
                            await channel.send(author.mention + " Du erhältst den Rang " + role.name + "!")

                            # remove old reward-roles
                            if server.id == LIVE_SERVER:
                                cur.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel < %s", (level,))
                            if server.id == TEST_SERVER:
                                cur.execute("SELECT rewardRole FROM level_reward_test WHERE rewardLevel < %s", (level,))

                            rows = cur.fetchall()
                            for row in rows:
                                role = server.get_role(role_id=int(row[0]))
                                if role in author.roles:
                                    await author.remove_roles(role)

                # update user in database with new XP (+ level)
                if server.id == LIVE_SERVER:
                    cur.execute("UPDATE user_info SET name = %s, exp = %s, expTime = %s, level = %s, avatar_url = %s WHERE id = %s", (author.name, exp, time.time(), level, author.avatar_url, author.id,))
                if server.id == TEST_SERVER:
                    cur.execute("UPDATE user_info_test SET name = %s, exp = %s, expTime = %s, level = %s, avatar_url = %s WHERE id = %s", (author.name, exp, time.time(), level, author.avatar_url, author.id,))
        # add user to database if missing
        else:
            exp = 15 + randint(0, 10)
            if server.id == LIVE_SERVER:
                cur.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
            if server.id == TEST_SERVER:
                cur.execute("INSERT INTO user_info_test (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url,))

    # commands (starting with !)
    if message.content[0] == "!":

        # handle commands !rank / !rang to print current XP
        if "!rank" in message.content or "!rang" in message.content:
            if server.id == LIVE_SERVER:
                cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
            if server.id == TEST_SERVER:
                cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
            row = cur.fetchone()

            if cur.rowcount == 0:
                if server.id == LIVE_SERVER:
                    cur.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
                    cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
                if server.id == TEST_SERVER:
                    cur.execute("INSERT INTO user_info_test (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url,))
                    cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
                row = cur.fetchone()

            # store current variables
            exp = row[0]
            level = row[1]
            nextLevel = level + 1
            nextLevelUp = await getLevelUp(level)
            expLeft = nextLevelUp - exp

            # print current XP, level and missing XP for next levelup
            description = "Aktuelle XP: %d - Aktuelles Level: %d - Verbleibende XP bis Level %d: %d" % (exp, level, nextLevel, expLeft)
            await channel.send(content=description)

        # handle command !w to roll a dice
        if "w" == message.content[1]:
            # check if !w-command is correct
            try:
                # dice type like W6
                dice = message.content.split('!w')

                # multiple dices
                multiply = dice[1].split('x')

                # if no x after dice type is given, use only one dice
                if len(multiply) == 1:
                    dice = multiply[0]
                    multiply = 1

                # retrieve dice count if x is given
                else:
                    dice = multiply[0]
                    multiply = multiply[1]

                # print rolled dices
                content = author.mention + " Du hast folgende Zahlen gewürfelt: "
                dice = int(dice)
                multiply = int(multiply)

                for i in range(0, multiply):
                    if i != 0:
                        content = content + ", "
                    content = content + str(randint(1, dice))
                log("content2: " + str(content))
                await channel.send(content=content)
            except Exception as e:
                log("Exception in !w: " + str(e))
                pass

# get needed XP to next levelup
@bot.event
async def getLevelUp(currentLevel):
    levelUp = 100
    if currentLevel > 0:
        levelUp = 5 * (currentLevel ** 2) + 50 * currentLevel + 100
    return levelUp

bot.run(API_KEY)