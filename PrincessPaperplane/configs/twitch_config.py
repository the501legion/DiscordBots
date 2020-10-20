import twitch

from cmds.Quotes import twitch_command_mapping

twitch_chat = twitch.Chat(channel="#schrottler", nickname="Horst", oauth="oauth:d6xtl0ycqlx62io7qfr4o8mvf4dube",
                          helix=twitch.Helix(client_id="krc3jjqwjuktzcx8xfavgr2v8o2owi", use_cache=True))


Mappings = {
    'QUOTES': [twitch_command_mapping]
}
