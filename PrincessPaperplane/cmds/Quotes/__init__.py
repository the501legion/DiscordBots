import random
from typing import List

import twitch
from cmds.Quotes.Quote import Quote
from utility import Database


def twitch_command_mapping(message: twitch.chat.Message) -> None:
    if message.text == '!quote':
        q = get_random()
        message.chat.send(f'/me "{q.text}" -{q.author}')

    if message.text.startswith('!quote add'):
        tmp = message.text.removeprefix('!quote add').strip().split(maxsplit=1)

        if message.text == '!quote add' or len(tmp) < 2:
            return message.chat.send(f'/me @{message.sender} Missing Parameter!')

        q = store(Quote(tmp))
        return message.chat.send(f'/me @{message.sender} added a new quote from {q.author}.')


def get_random() -> Quote:
    db = Database.connect()

    try:
        cur = db.cursor()
        db.autocommit(True)

        cur.execute("SELECT author, quote FROM quotes")

        if cur.rowcount <= 0:
            raise Exception("No quotes found!")

        qs: List = cur.fetchall()
        return Quote(random.choice(qs))

    except Exception as e:
        Database.log(str(e))

    finally:
        db.close()


def store(quote: Quote) -> Quote:
    db = Database.connect()

    try:
        cur = db.cursor()
        db.autocommit(True)

        # add new quote
        cur.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote.text, quote.author,))
        return quote

    except Exception as e:
        Database.log(e)

    finally:
        db.close()
