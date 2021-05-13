#!/usr/bin/python3
# coding=utf-8

from typing import List
from cmds.roles import EmoteRoleSettings

# level requirements for roles
ROLES_LEVEL = {
    763105108841332766 : 5
}

# roles which will be given by emote
EMOTE_ROLES : List[EmoteRoleSettings]  = [
  EmoteRoleSettings(763374681025150986,"🪃",":boomerang: um Sportler:in zu werden."),
  EmoteRoleSettings(763374893572030464,"🎨",":art: um Künstler:in zu werden."),
  EmoteRoleSettings(763374952304082964,"🎬",":clapper: um Cineast:in zu werden."),
  EmoteRoleSettings(763375031874748449,"📖",":book: wenn Du zum Buchclub gehören möchtest."),
  EmoteRoleSettings(763375132831121409,"🚀",":rocket: wenn Du mit among us spielen möchtest."),
  EmoteRoleSettings(763375172996562945,"🎲",":game_die: wenn Du Tabletop Simulator spielen möchtest."),
  EmoteRoleSettings(763375221201567774,"🎭",":performing_arts: wenn Du Dich für Pen & Paper interessierst.")
]

EMOTE_ROLES_TEST : List[EmoteRoleSettings]  = [
  EmoteRoleSettings(768127008856342560,"🪃","Rolle A für :boomerang:"),
  EmoteRoleSettings(768127041077510234,"🎨","Rolle B für :art:"),
  EmoteRoleSettings(768127053413089330,"🎬", "Rolle C für :clapper:")
]