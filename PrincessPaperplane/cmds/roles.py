from discord.ext import commands
import configs.roles_config as roles_config
import configs.guild_config as guild_config
from utility.cogs_enum import Cogs

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.DB = bot.get_cog(Cogs.DB)

        # handle added reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_role_reactions(payload)

    # handle removed reactions
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_role_reactions(payload)
    
    # update role message and add reactions
    async def update_reaction_msg(self, roleChannel, roles, emotes, text):
        channel = self.bot.get_channel(id=roleChannel)
        server = channel.guild
        msg = None

        async for message in channel.history(limit=200):
            if message.author == self.bot.user:
                msg = message

        if msg != None:
            for emote in msg.reactions:
                if emote.me == True:
                    await msg.remove_reaction(emote.emoji, self.bot.user)
        else:
            msg = await channel.send("Hier stehen bald alle Streamer-Rollen, die ihr euch mit dem jeweiligen Emotes als Reaktion geben und wieder nehmen könnt. :boomerang:")

        string = "Hier stehen alle Rollen, die ihr euch mit den jeweiligen Emotes als Reaktion geben und wieder nehmen könnt:\n"
        for x in range(0, len(roles)):
            role = server.get_role(role_id=roles[x])

            string_role = 'Rolle %s, %s' % (roles[x], emotes[x])
            await msg.add_reaction(emotes[x])

            string = string + "\n" + text[x]
            if roles[x] in roles_config.ROLES_LEVEL:
                string = "%s (mindestens Level %d)" % (string, roles_config.ROLES_LEVEL.get(roles[x]))

        await msg.edit(content=string)

    # handle role reactions
    async def handle_role_reactions(self, payload):
        if payload.channel_id == guild_config.ROLE_CHANNEL or payload.channel_id == guild_config.ROLE_CHANNEL_TEST:
            emoji = payload.emoji
            server = self.bot.get_guild(id=payload.guild_id)
            user = server.get_member(user_id=payload.user_id)
            roles = []
            emotes = []
            level = 0

            if user == self.bot.user:
                return

            db = self.DB.dbConnect()
            cur = db.cursor()
            db.autocommit(True)

            if payload.channel_id == guild_config.ROLE_CHANNEL:
                roles = roles_config.ROLES
                emotes = roles_config.EMOTES
                cur.execute("SELECT level FROM user_info WHERE id = %s", (user.id,))
                levelChannel = self.bot.get_channel(id=guild_config.LEVEL_CHANNEL)
            elif payload.channel_id == guild_config.ROLE_CHANNEL_TEST:
                roles = roles_config.ROLES_TEST
                emotes = roles_config.EMOTES_TEST
                cur.execute("SELECT level FROM user_info_test WHERE id = %s", (user.id,))
                levelChannel = self.bot.get_channel(id=guild_config.LEVEL_CHANNEL_TEST)
            if cur.rowcount > 0:
                level = cur.fetchone()[0]
            db.close()

            i = -1
            for x in range(0, len(roles)):
                if emotes[x] == emoji.name:
                    i = x
                    break

            if i == -1:
                self.DB.log("No emote found")
                return

            role = server.get_role(role_id=roles[i])
            self.DB.log("Role %s request from %s (Level %d)" % (role.name, user.name, level))

            if role in user.roles:
                self.DB.log("Role " + role.name + " removed from " + user.name)
                await user.remove_roles(role)
            else:
                if roles[i] in roles_config.ROLES_LEVEL:
                    if level >= roles_config.ROLES_LEVEL.get(roles[i]):
                        self.DB.log("Role " + role.name + " with min-level " + str(roles_config.ROLES_LEVEL.get(roles[i])) + " assigned to " + user.name)
                        await user.add_roles(role)
                    else:
                        await levelChannel.send(user.mention + " Du erfüllst das notwendige Level (" + str(level) + " statt " + str(roles_config.ROLES_LEVEL.get(roles[i])) + ") für die Rolle " + role.name + " nicht!")
                else:
                    self.DB.log("Role " + role.name + " assigned to " + user.name)
                    await user.add_roles(role)