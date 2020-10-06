#!/usr/bin/python3
# coding=utf-8

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    global VOICE_CREATE
    VOICE_CREATE = bot.get_channel(id=0) # ID des Channels

@bot.event
async def on_voice_state_update(member, before, after):
    global VOICE_CREATE

    if after.channel != None:
        # Joined creation channel
        if after.channel.id == VOICE_CREATE.id:
            channelname = member.name + "'s Sprachchannel"
            voice = await VOICE_CREATE.category.create_voice_channel(channelname, overwrites=None, reason="Created by user")
            await voice.set_permissions(member, read_messages=True, send_messages=False)
            await member.move_to(voice)

    if before.channel != None:
        # Delete if channel is empty
        if before.channel.category == VOICE_CREATE.category and before.channel.id != VOICE_CREATE.id:
            if len(before.channel.members) == 0:
                await before.channel.delete(reason="Empty user channel")

@bot.event
async def on_message(message):
    global VOICE_CREATE

    if message.channel.type == discord.ChannelType.private:
        for voice in VOICE_CREATE.category.voice_channels:
            for user in voice.members:
                if message.author.id == user.id and voice.id != VOICE_CREATE.id:
                    if user.name in voice.name:
                        await voice.edit(name=message.content + " - by " + user.name)

bot.run("") # API-Key des Bots
