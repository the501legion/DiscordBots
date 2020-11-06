from discord.ext.commands import Bot

from ext.quotly.quotly import Quotly

ROLES_WITH_WRITE_ACCESS = []

# def twitch_command_mapping(message: twitch.chat.Message) -> None:
#     if message.text == '!quote':
#         q = get_random()
#         message.chat.send(f'/me "{q.text}" -{q.author}')
#
#     if message.text.startswith('!quote add'):
#         tmp = message.text.removeprefix('!quote add').strip().split(maxsplit=1)
#
#         if message.text == '!quote add' or len(tmp) < 2:
#             return message.chat.send(f'/me @{message.sender} Missing Parameter!')
#
#         q = store(Quote(tmp))
#         return message.chat.send(f'/me @{message.sender} added a new quote from {q.author}.')


def setup(bot: Bot):
    print("> Loading Quotly")

    bot.add_cog(Quotly(bot))
