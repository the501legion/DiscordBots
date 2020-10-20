#!/usr/bin/python3
# coding=utf-8

from typing import List
from cmds.roles import EmoteRoleSettings

# level requirements for roles
ROLES_LEVEL = {
    763105108841332766 : 5,
    763375085704577034 : 5
}

"""# roles which will be given by emote
ROLES = [ 763374681025150986, 763374893572030464, 763374952304082964, 763375031874748449, 763375085704577034,
 763375132831121409, 763375172996562945, 763375221201567774 ]
EMOTES = [ "🪃", "🎨", "🎬", "📖", "🗣️", "🚀", "🎲", "🎭" ]
TEXT = [ ":boomerang: um Sportler:in zu werden.", ":art: um Künstler:in zu werden.", ":clapper: um Cineast:in zu werden.",
 ":book: wenn Du zum Buchclub gehören möchtest.", ":speaking_head: wenn Du das #kämmerlein sehen möchtest.", ":rocket: wenn Du mit among us spielen möchtest.",
  ":game_die: wenn Du Tabletop Simulator spielen möchtest.", ":performing_arts: wenn Du Dich für Pen & Paper interessierst." ]
ROLES_TEST = [ 763105108841332766, 763105158078922763, 763105190765002783 ]
EMOTES_TEST = [ "🪃", "🎨", "🎬" ]
TEXT_TEST = ["Rolle A für :boomerang:", "Rolle B für :art:", "Rolle C für :clapper:"] """

# roles which will be given by emote
EMOTE_ROLES : List[EmoteRoleSettings]  = [
  EmoteRoleSettings(763374681025150986,"🪃",":boomerang: um Sportler:in zu werden."),
  EmoteRoleSettings(763374893572030464,"🎨",":art: um Künstler:in zu werden."),
  EmoteRoleSettings(763374952304082964,"🎬",":clapper: um Cineast:in zu werden."),
  EmoteRoleSettings(763375031874748449,"📖",":book: wenn Du zum Buchclub gehören möchtest."),
  EmoteRoleSettings(763375085704577034,"🗣️",":speaking_head: wenn Du das #kämmerlein sehen möchtest."),
  EmoteRoleSettings(763375132831121409,"🚀",":rocket: wenn Du mit among us spielen möchtest."),
  EmoteRoleSettings(763375172996562945,"🎲",":game_die: wenn Du Tabletop Simulator spielen möchtest."),
  EmoteRoleSettings(763375221201567774,"🎭",":performing_arts: wenn Du Dich für Pen & Paper interessierst.")
]

EMOTE_ROLES_TEST : List[EmoteRoleSettings]  = [
  EmoteRoleSettings(763105108841332766,"🪃","Rolle A für :boomerang:"),
  EmoteRoleSettings(763105158078922763,"🎨","Rolle B für :art:"),
  EmoteRoleSettings(763105190765002783,"🎬", "Rolle C für :clapper:")
]