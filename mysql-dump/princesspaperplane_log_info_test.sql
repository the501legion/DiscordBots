create table log_info_test
(
    id   int auto_increment
        primary key,
    text varchar(2056) null,
    time int default 0 null
)
    charset = latin1;

INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6920, 'Bot started', 1610201386);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6921, 'Error: Traceback (most recent call last):
  File "PrincessPaperplane/paperbot.py", line 77, in on_ready
    await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
  File "/bot/PrincessPaperplane/cmds/roles.py", line 36, in update_reaction_msg
    guild : Guild = channel.guild
AttributeError: ''NoneType'' object has no attribute ''guild''
', 1610201386);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6922, 'Bot started', 1610201407);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6923, 'Error: Traceback (most recent call last):
  File "PrincessPaperplane/paperbot.py", line 77, in on_ready
    await ROLES.update_reaction_msg(guild_config.ROLE_CHANNEL, roles_config.EMOTE_ROLES)
  File "/bot/PrincessPaperplane/cmds/roles.py", line 36, in update_reaction_msg
    guild : Guild = channel.guild
AttributeError: ''NoneType'' object has no attribute ''guild''
', 1610201407);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6924, 'Bot started', 1610201583);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6925, 'Error: Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 606, in _load_from_module_spec
    spec.loader.exec_module(lib)
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/bot/PrincessPaperplane/ext/twitter_crawler.py", line 28, in <module>
    @tasks.loop(seconds=int(os.getenv(''TWITTER.TIMER'', 60)))
ValueError: invalid literal for int() with base 10: ''''

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "PrincessPaperplane/paperbot.py", line 74, in on_ready
    load_extensions(bot)
  File "/bot/PrincessPaperplane/ext/__init__.py", line 10, in load_extensions
    bot.load_extension("ext.twitter_crawler")
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 663, in load_extension
    self._load_from_module_spec(spec, name)
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 609, in _load_from_module_spec
    raise errors.ExtensionFailed(key, e) from e
discord.ext.commands.errors.ExtensionFailed: Extension ''ext.twitter_crawler'' raised an error: ValueError: invalid literal for int() with base 10: ''''
', 1610201583);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6926, 'Bot started', 1610212109);
INSERT INTO princesspaperplane.log_info_test (id, text, time) VALUES (6927, 'Error: Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 606, in _load_from_module_spec
    spec.loader.exec_module(lib)
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/bot/PrincessPaperplane/ext/twitter_crawler.py", line 28, in <module>
    @tasks.loop(seconds=int(os.getenv(''TWITTER.TIMER'', 60)))
ValueError: invalid literal for int() with base 10: ''''

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "PrincessPaperplane/paperbot.py", line 74, in on_ready
    load_extensions(bot)
  File "/bot/PrincessPaperplane/ext/__init__.py", line 10, in load_extensions
    bot.load_extension("ext.twitter_crawler")
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 663, in load_extension
    self._load_from_module_spec(spec, name)
  File "/usr/local/lib/python3.7/site-packages/discord/ext/commands/bot.py", line 609, in _load_from_module_spec
    raise errors.ExtensionFailed(key, e) from e
discord.ext.commands.errors.ExtensionFailed: Extension ''ext.twitter_crawler'' raised an error: ValueError: invalid literal for int() with base 10: ''''
', 1610212109);