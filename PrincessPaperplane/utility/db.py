import MySQLdb
from discord.ext import commands
import configs.secret as secret
import configs.db_config as db_config
import time

class DB(commands.Cog):
    def __init__(self):
        pass

    def connect(self):
        """Connect to database

        Returns:
            [type]: Connection to database
        """
        return MySQLdb.connect(host=secret.DB_HOST,
        user=secret.DB_USER,
        charset=db_config.DB_CHARSET,
        use_unicode=db_config.DB_UNICODE,
        passwd=secret.DB_PASSWD,
        db=secret.DB_DB)
    
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
            cur.execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (text, time.time(), ))
        except Exception as e:
            self.log("Exception in log: " + str(e))
            pass
