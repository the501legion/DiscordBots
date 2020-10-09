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
ROLE_CHANNEL = 425748476379529227
ROLE_CHANNEL_TEST = 763491543163731980

# channel ids for level ups
LEVEL_CHANNEL = 760861542735806485
LEVEL_CHANNEL_TEST = 763491543163731980

# user ids which will be ignored by level + commands
IGNORE_LIST = [ 392783651248799754 ]

# level requirements for roles
ROLES_LEVEL = {
    763105108841332766: 5,
    763375085704577034 : 5
}

# roles which will be given by emote
ROLES = [ 763374681025150986, 763374893572030464, 763374952304082964, 763375031874748449, 763375085704577034,
 763375132831121409, 763375172996562945, 763375221201567774 ]
EMOTES = [ "🪃", "🎨", "🎬", "📖", "🗣️", "🚀", "🎲", "🎭" ]
TEXT = [ ":boomerang: um Sportler:in zu werden.", ":art: um Künstler:in zu werden.", ":clapper: um Cineast:in zu werden.",
 ":book: wenn Du zum Buchclub gehören möchtest.", ":speaking_head: wenn Du das #kämmerlein sehen möchtest.", ":rocket: wenn Du mit among us spielen möchtest.",
  ":game_die: wenn Du Tabletop Simulator spielen möchtest.", ":performing_arts: wenn Du Dich für Pen & Paper interessierst." ]
ROLES_TEST = [ 763105108841332766, 763105158078922763, 763105190765002783 ]
EMOTES_TEST = [ "🪃", "🎨", "🎬" ]
TEXT_TEST = [ "Rolle A für :boomerang:", "Rolle B für :art:", "Rolle C für :clapper:" ]

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

    await updateReactionMsg(ROLE_CHANNEL, ROLES, EMOTES, TEXT)
    await updateReactionMsg(ROLE_CHANNEL_TEST, ROLES_TEST, EMOTES_TEST, TEXT_TEST)

# update role message and add reactions
@bot.event
async def updateReactionMsg(roleChannel, roles, emotes, text):
    channel = bot.get_channel(id=roleChannel)
    server = channel.guild
    msg = None

    async for message in channel.history(limit=200):
        if message.author == bot.user:
            msg = message

    if msg != None:
        for emote in msg.reactions:
            if emote.me == True:
                await msg.remove_reaction(emote.emoji, bot.user)
    else:
        msg = await channel.send("Hier stehen bald alle Streamer-Rollen, die ihr euch mit dem jeweiligen Emotes als Reaktion geben und wieder nehmen könnt. :boomerang:")

    string = "Hier stehen alle Rollen, die ihr euch mit den jeweiligen Emotes als Reaktion geben und wieder nehmen könnt:\n"
    for x in range(0, len(roles)):
        role = server.get_role(role_id=roles[x])

        str = 'Rolle %s, %s' % (roles[x], emotes[x])
        await msg.add_reaction(emotes[x])

        string = string + "\n" + text[x]
        if roles[x] in ROLES_LEVEL:
            string = "%s (mindestens Level %d)" % (string, ROLES_LEVEL.get(roles[x]))

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
        roles = []
        emotes = []
        level = 0

        if user == bot.user:
            return

        db = dbConnect()
        cur = db.cursor()
        db.autocommit(True)

        if payload.channel_id == ROLE_CHANNEL:
            roles = ROLES
            emotes = EMOTES
            cur.execute("SELECT level FROM user_info WHERE id = %s", (user.id,))
        elif payload.channel_id == ROLE_CHANNEL_TEST:
            roles = ROLES_TEST
            emotes = EMOTES_TEST
            cur.execute("SELECT level FROM user_info_test WHERE id = %s", (user.id,))
        if cur.rowcount > 0:
            level = cur.fetchone()[0]
        db.close()

        i = -1
        for x in range(0, len(roles)):
            if emotes[x] == emoji.name:
                i = x
                break

        if i == -1:
            log("No emote found")
            return

        role = server.get_role(role_id=roles[i])
        log("Role %s request from %s (Level %d)" % (role.name, user.name, level))

        if role in user.roles:
            log("Role " + role.name + " removed from " + user.name)
            await user.remove_roles(role)
        else:
            if roles[i] in ROLES_LEVEL:
                if level >= ROLES_LEVEL.get(roles[i]):
                    log("Role " + role.name + " with min-level " + level + " assigned to " + user.name)
                    await user.add_roles(role)
            else:
                log("Role " + role.name + " assigned to " + user.name)
                await user.add_roles(role)

# check new message
@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    server = message.guild

    if author.id in IGNORE_LIST:
        return

    if server.id == LIVE_SERVER:
        levelChannel = bot.get_channel(id=LEVEL_CHANNEL)
    if server.id == TEST_SERVER:
        levelChannel = bot.get_channel(id=LEVEL_CHANNEL_TEST)

    if author.id == bot.user.id:
        return

    if message.content == "" or len(message.content) == 0:
        return

    string = "[" + server.name + "] " + author.name + " (#" + channel.name + "): " + message.content

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

            # has cooldown (60s) expired?
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


                    await levelChannel.send(author.mention + " Du bist ein Level aufgestiegen! Nun bist du auf Level " + str(level) + "!")

                    if cur.rowcount > 0:
                        role = server.get_role(role_id=int(cur.fetchone()[0]))

                        # give user new role as reward
                        if role not in author.roles:
                            log("Assign " + author.name + " new role " + role.name)
                            await author.add_roles(role)
                        await levelChannel.send(author.mention + " Du erhältst den Rang " + role.name + "!")

                        # remove old reward-roles
                        if server.id == LIVE_SERVER:
                            cur.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel < %s AND rewardLevel > 1", (level,))
                        if server.id == TEST_SERVER:
                            cur.execute("SELECT rewardRole FROM level_reward_test WHERE rewardLevel < %s AND rewardLevel > 1", (level,))

                        rows = cur.fetchall()
                        for row in rows:
                            role = server.get_role(role_id=int(row[0]))
                            if role in author.roles:
                                log("Remove " + author.name + " old role " + role.name)
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
                # only allow !rank / !rang in #bod_spam
                if channel.id != 760861542735806485:
                    return

                cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
            if server.id == TEST_SERVER:
                cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
            row = cur.fetchone()

            if cur.rowcount == 0:
                exp = 0
                if server.id == LIVE_SERVER:
                    cur.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
                    cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
                if server.id == TEST_SERVER:
                    cur.execute("INSERT INTO user_info_test (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
                    cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
                row = cur.fetchone()

            # store current variables
            exp = row[0]
            level = row[1]
            nextLevel = level + 1
            nextLevelUp = await getLevelUp(level)
            expLeft = nextLevelUp - exp

            # generate image with stats
            ext = ""
            if server.id == TEST_SERVER:
                ext = "&test"
            url = "https://501-legion.de/princesspaperplane/generateLevel.php?user=%s&time=%s%s" % (author.id, time.time(), ext)

            # embed current XP, level and missing XP for next levelup
            title = "Dein aktuelles Level: %d" % (level)
            description = "Aktuelle XP: %d\nVerbleibende XP bis Level %d: %d" % (exp, nextLevel, expLeft)
            colour = author.top_role.colour

            embed = discord.Embed(title=title, description=description, colour=colour)
            embed.set_author(name=author.name, icon_url=author.avatar_url_as(format="png"))
            embed.set_image(url=url)

            await channel.send(embed=embed)

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
