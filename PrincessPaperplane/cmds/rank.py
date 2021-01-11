import asyncio
import time
import traceback
from random import randint
from typing import Optional

from configs.cmd_config import STRINGS, ALIASES
import configs.guild_config as guild_config
import configs.xp_config as xp_config
from discord import Member, TextChannel, Guild, Message, Role, Embed
from discord.ext import commands
from utility.checks import Checks
from utility.cogs_enum import Cogs
from utility.db import DB


class Rank(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.DB : DB = bot.get_cog(Cogs.DB.value)
        self.base_xp = xp_config.BASE
        self.random_xp_range = xp_config.RANDOM_RANGE

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.handle_user_message_xp(message)

    async def handle_user_message_xp(self, message: Message) -> None:
        author : Member = message.author
        channel : TextChannel = message.channel
        guild : Guild = message.guild

        print("Guildname: ", guild.name)

        if author.id in guild_config.IGNORE_LIST:
            return

        level_channel : TextChannel
        level_channel = self.bot.get_channel(id=guild_config.LEVEL_CHANNEL)

        if author.id == self.bot.user.id:
            return

        if message.content == "" or len(message.content) == 0:
            return

        db = self.DB.connect()
        cur = db.cursor()
        db.autocommit(True)

        # check for banned channels to handle XP and levelup
        cur.execute("SELECT * FROM level_banned_channel WHERE channel = %s", (channel.id,))
        if cur.rowcount == 0:
            if guild.id == guild_config.SERVER_LIVE:
                cur.execute("SELECT exp, expTime, level FROM user_info WHERE id = %s", (author.id,))
            if guild.id == guild_config.SERVER_TEST:
                cur.execute("SELECT exp, expTime, level FROM user_info_test WHERE id = %s", (author.id,))

            if cur.rowcount > 0:
                result = cur.fetchone()
                exp = int(result[0])
                expTime = int(result[1])
                level = int(result[2])

                # skip cooldown on testing
                if guild.id == guild_config.SERVER_TEST:
                    expTime = 0

                # has cooldown (60s) expired?
                if expTime + 60 <= time.time():
                    addedExp = self.calc_xp_reward()
                    exp = exp + addedExp

                    levelUp = self.get_levelup_threshold(level)

                    self.DB.log("Exp for Level-Up: %d, current XP: %d" % (levelUp, exp))

                    # trigger levelup if enough XP gained
                    if exp >= levelUp:
                        level = level + 1
                        exp = 0

                        if guild.id == guild_config.SERVER_LIVE:
                            cur.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel = %s", (level,))
                        if guild.id == guild_config.SERVER_TEST:
                            cur.execute("SELECT rewardRole FROM level_reward_test WHERE rewardLevel = %s", (level,))

                        if cur.rowcount > 0:
                            roleId = int(cur.fetchone()[0])
                            role = guild.get_role(role_id=roleId)

                            # give user new role as reward
                            if role not in author.roles:
                                self.DB.log("Assign " + author.name + " new role " + role.name)
                                await author.add_roles(role)

                            # remove old reward-roles
                            if guild.id == guild_config.SERVER_LIVE:
                                await level_channel.send(author.mention + " Du hast eine neue Stufe erreicht und erhältst den neuen Rang " + role.name + "!")
                                cur.execute("SELECT rewardRole FROM level_reward WHERE rewardLevel < %s AND rewardLevel > 1", (level,))
                            if guild.id == guild_config.SERVER_TEST:
                                cur.execute("SELECT rewardRole FROM level_reward_test WHERE rewardLevel < %s AND rewardLevel > 1", (level,))

                            rows = cur.fetchall()
                            for row in rows:
                                role = guild.get_role(role_id=int(row[0]))
                                if role in author.roles:
                                    self.DB.log("Remove " + author.name + " old role " + role.name)
                                    await author.remove_roles(role)

                    # update user in database with new XP (+ level)
                    if guild.id == guild_config.SERVER_LIVE:
                        cur.execute("UPDATE user_info SET name = %s, exp = %s, expTime = %s, level = %s, avatar_url = %s WHERE id = %s", (author.name, exp, time.time(), level, author.avatar_url, author.id,))
                    if guild.id == guild_config.SERVER_TEST:
                        cur.execute("UPDATE user_info_test SET name = %s, exp = %s, expTime = %s, level = %s, avatar_url = %s WHERE id = %s", (author.name, exp, time.time(), level, author.avatar_url, author.id,))

            # add user to database if missing
            else:
                self.add_user_to_db(cur, guild, author)

    def add_user_to_db(self, cur, guild : Guild, author: Member) -> None:
        exp = self.calc_xp_reward()
        if guild.id == guild_config.SERVER_LIVE:
            cur.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
        if guild.id == guild_config.SERVER_TEST:
            cur.execute("INSERT INTO user_info_test (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url,))
    
    def get_levelup_threshold(self, currentLevel : int) -> int:
        levelUp = 100
        if currentLevel > 0:
            levelUp = 5 * (currentLevel ** 2) + 50 * currentLevel + 100
        return levelUp

    def calc_xp_reward(self) -> int:
        return self.base_xp + randint(*self.random_xp_range)

    ### Commands

    @commands.command(aliases=ALIASES.RANK.value)
    @Checks.is_channel(760861542735806485)
    async def cmd_rank(self, ctx: commands.Context, member: Optional[Member]) -> None:
        """Handles rank command

        Args:
            ctx (commands.Context): [description]
            member (typing.Optional[discord.Member]): Member argument
        """
        channel : TextChannel = ctx.channel
        guild : Guild = ctx.guild
        author : Member = ctx.author
        
        db = self.DB.connect()
        cur = db.cursor()
        db.autocommit(True)

        if guild.id == guild_config.SERVER_LIVE:
            cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
        if guild.id == guild_config.SERVER_TEST:
            cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
        row = cur.fetchone()

        if cur.rowcount == 0:
            exp = 0
            if guild.id == guild_config.SERVER_LIVE:
                cur.execute("INSERT INTO user_info (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
                cur.execute("SELECT exp, level, name FROM user_info WHERE id = %s", (author.id,))
            if guild.id == guild_config.SERVER_TEST:
                cur.execute("INSERT INTO user_info_test (`id`, `name`, `exp`, `expTime`, `avatar_url`) VALUES (%s, %s, %s, %s, %s)", (author.id, author.name, exp, time.time(), author.avatar_url, ))
                cur.execute("SELECT exp, level, name FROM user_info_test WHERE id = %s", (author.id,))
            row = cur.fetchone()

        # store current variables
        exp = row[0]
        level = row[1]

        embed = self.create_rank_display_embed(guild, author, level, exp)
        await channel.send(embed=embed)

    def create_rank_display_embed(self, guild : Guild, author: Member, level : int, exp: int) -> Embed:
        # generate image with stats
        ext = ""
        if guild.id == guild_config.SERVER_TEST:
            ext = "&test"
        url = STRINGS.RANK_IMAGE_GENERATOR_URL.value.format(AUTHOR_ID=author.id, TIME=time.time(), EXT=ext)

        next_level = level + 1
        nextLevelUp = self.get_levelup_threshold(level)
        exp_left = nextLevelUp - exp

        # embed current XP, level and missing XP for next levelup
        title = STRINGS.RANK_EMBED_TITLE.value.format(LEVEL=level)
        description = STRINGS.RANK_EMBED_DESCRIPTION.value.format(EXP=exp, NEXT_LEVEL=next_level, EXP_LEFT=exp_left)
        colour = author.top_role.colour

        embed = Embed(title=title, description=description, colour=colour)
        embed.set_author(name=author.name, icon_url=author.avatar_url_as(format="png"))
        embed.set_image(url=url)
        print(url)

        return embed