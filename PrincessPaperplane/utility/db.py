import time
import os

import configs.db_config as db_config
import configs.guild_config as guild_config
import configs.secret as secret
import MySQLdb
from discord.ext import commands


class DB(commands.Cog):
    def __init__(self):
        pass

    def connect(self):
        """Connect to database

        Returns:
            [type]: Connection to database
        """
        return MySQLdb.connect(host=secret.DB_HOST,
                               user=os.getenv("DATABASE.USER"),
                               charset=db_config.DB_CHARSET,
                               use_unicode=db_config.DB_UNICODE,
                               passwd=os.getenv("DATABASE.PASSWD"),
                               db=os.getenv("DATABASE.DB"))

    def exist(self, table: str) -> bool:
        db = self.connect()

        try:
            cursor = db.cursor()
            db.autocommit(True)
            cursor.execute("SHOW TABLES LIKE %s", (table,))
            if cursor.rowcount > 0:
                return True

        except Exception as e:
            print(str(e))

        finally:
            db.close()

        return False

    def log(self, text: str):
        """Log text in console and in database

        Args:
            text (string): Text to be logged
        """
        print(text)

        try:
            db = self.connect()
            cur = db.cursor()
            db.autocommit(True)
            if guild_config.SERVER == guild_config.SERVER_TEST:
                cur.execute("INSERT INTO log_info_test (`text`, `time`) VALUES (%s, %s)", (text, time.time(),))
            else:
                cur.execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (text, time.time(),))
        except Exception as e:
            self.log("Exception in log: " + str(e))
            pass
