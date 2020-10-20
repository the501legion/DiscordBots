import twitch

from cmds.Quotes import twitch_command_mapping

twitch_chat = twitch.Chat(channel="#<CHANNEL>", nickname="PaperBot", oauth="oauth:<OAUTH>",
                          helix=twitch.Helix(client_id="<CLIENT-ID>", use_cache=True))


Mappings = {
    'QUOTES': [twitch_command_mapping]
}
