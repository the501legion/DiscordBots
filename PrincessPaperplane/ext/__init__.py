HTTP_CODES = {
    200: "All right!",
    401: "You fucked up!",
    418: "I'm a teapot!",
    429: "Too many requests!"
}


def load_extensions(bot):
    bot.load_extension("ext.twitter_crawler")
    bot.load_extension("ext.wool_cmd")
