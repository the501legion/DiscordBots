from discord.ext import commands
from discord.ext.commands import Greedy, TextChannelConverter
from discord import Embed, TextChannel, Forbidden
from configs.cmd_config import ALIASES
from pathlib import Path
import pandas as pd

class History(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(aliases=ALIASES.HISTORY.value)
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def cmd_history(self, ctx: commands.Context, *args):
        if ctx.subcommand_passed is None:
            await ctx.send("Gibt bitte ein genaueres Command ein!")

    @cmd_history.group(aliases=['xp_count'])
    async def cmd_history_collect(self, ctx: commands.Context, channels : Greedy[TextChannelConverter]):
        if ctx.subcommand_passed is None:
            await self.count_user_messages_in_channels(ctx, ctx.channel)        
        #Collect for this channel only

    async def count_user_messages_in_channels(self, ctx, *channels: TextChannel):
        """Specify channels to parse for user message count
        """
        
        channel_status = dict()
        for c in iter(channels):
            channel_status[c] = "waiting"
        
        embed = self.create_collection_embed(ctx, channel_status)
        status_message = await ctx.channel.send(embed=embed)

        #channels is variable list -> can be iterated
        for channel in iter(channels):
            print(f"COLLECT USER MESSAGE COUNT IN {channel.category.name}-{channel.name} | COLLECTING")

            channel_status[channel] = "collecting"
            embed = self.create_collection_embed(ctx, channel_status)
            await status_message.edit(embed=embed)

            try:
                await self.save_channel_user_message_counts(ctx, channel)
            except (Exception, Forbidden):
                channel_status[channel] = "failed"
            else:
                channel_status[channel] = "finished"

            print(f"COLLECT USER MESSAGE COUNT IN {channel.category.name}-{channel.name} | {channel_status[channel].upper()}")
            print("==============")

        # Final embed
        embed = self.create_collection_embed(ctx, channel_status, True)
        await status_message.edit(embed=embed)

    @cmd_history_collect.command(pass_context=True, aliases=['all', 'a'])
    async def cmd_history_collect_all(self, ctx: commands.Context, *args):
        await self.count_user_messages_in_channels(ctx, *ctx.guild.text_channels)

    @cmd_history_collect.command(pass_context=True, name='allexcept')
    async def count_user_messages_everywhere_except(self, ctx, *exclude_channels: TextChannel):
        """Parses through each channel for user message count, except for those specified
        """
        channels_to_parse = filter(lambda c: not c in exclude_channels, ctx.guild.text_channels)
        await self.count_user_messages_in_channels(ctx, *list(channels_to_parse))


    ### Internal logic
    async def save_channel_user_message_counts(self, ctx, channel : TextChannel):
        """Counts messages per user for channel
        Returns:
            pandas.DataFrame: Dataframe with ['channel_id,' 'count'] and user_id as index label
        """
        df = pd.DataFrame(columns=['channel_id', 'count'], dtype='int64')
        last_time_dict = dict()
        
        # Go through all messages of channel and increment value for each user
        async for message in channel.history(limit = None, oldest_first=True):
            member_id = message.author.id

            if (member_id in df.index):  #Check if exists
                if (message.created_at - last_time_dict[member_id]).total_seconds() <= 60: continue #Difference can't be smaller than 60 seconds
                df.at[member_id, 'count'] = df.at[member_id, 'count'] + 1
                last_time_dict[member_id] = message.created_at

            else: #Insert new entry
                df.loc[member_id] = [channel.id, 1]
                last_time_dict[member_id] = message.created_at

        save_to_folder_path = Path('data') / f'{ctx.guild.id}-{ctx.guild.name}_user_message_counts'

        #Save to file
        if not save_to_folder_path.exists():
            save_to_folder_path.mkdir()
        df.to_csv(save_to_folder_path / f'{channel.id}_{channel.category.name.upper()}-{channel.name}.csv', index=True)

        return df

    def create_collection_embed(self, ctx: commands.Context, channels: dict, isFinished = False):
        """Creates embed that shows progress of collection process

        Args:
            channels (dict): dict of channels with ( TextChannel , str ) pairs. The string encodes the status of the channel (collecting, waiting, failed, finished)

        Returns:
            discord.Embed: Generated embeds
        """
        embed=Embed(title="User message count collection", description="The bot is trying to collect the amount of messages in each channel, by each user")
        embed.set_author(name = ctx.bot.user.name)

        finished_text = ""
        failed_text = ""
        collecting_text = ""
        waiting_text = ""

        for channel, status_string in channels.items():

            if status_string == "finished":
                finished_text += f"{channel.category.name.upper()}.{channel.name} | "
            elif status_string == "failed":
                failed_text += f"{channel.category.name.upper()}.{channel.name} | "
            elif status_string == "collecting":
                collecting_text += f"{channel.category.name.upper()}.{channel.name}"
            elif status_string == "waiting":
                waiting_text += f"{channel.category.name.upper()}.{channel.name} | "

            
        if finished_text is not "": embed.add_field(name='Finished ✅', value=finished_text, inline=False)
        if failed_text is not "": embed.add_field(name='Failed ❌', value=failed_text, inline=False)

        if not isFinished:
            if collecting_text is not "": embed.add_field(name='Collecting 🔍', value=collecting_text, inline=False)
            if waiting_text is not "": embed.add_field(name='WAITING ⌛', value=waiting_text, inline=False)
        else:
            embed.title = "User message count collection COMPLETE"

        #embed.set_footer(text=Parsed x messages)
        return embed

