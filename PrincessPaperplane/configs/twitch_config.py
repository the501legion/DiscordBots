import os

import twitch

from cmds.Quotes import twitch_command_mapping

twitch_chat = twitch.Chat(channel=f'#{os.getenv("TWITCH.CHANNEL")}',
                          nickname="PaperBot", oauth=f'oauth:{os.getenv("TWITCH.OAUTH")}',
                          helix=twitch.Helix(client_id=os.getenv("TWITCH.CLIENTID"), use_cache=True))


Mappings = {
    'QUOTES': [twitch_command_mapping]
}
