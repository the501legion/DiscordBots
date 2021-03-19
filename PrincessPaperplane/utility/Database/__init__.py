import MySQLdb

from configs import secret, db_config


def connect() -> MySQLdb.connection:
    return MySQLdb.connect(host=secret.DB_HOST,
                           user=secret.DB_USER,
                           charset=db_config.DB_CHARSET,
                           use_unicode=db_config.DB_UNICODE,
                           passwd=secret.DB_PASSWD,
                           db=secret.DB_DB)


def log(message) -> None:
    db = connect()

    try:
        cur = db.cursor()
        db.autocommit(True)
        cur.execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (text, time.time(),))
    except Exception as e:
        print(str(e))

    finally:
        print(message)
        db.close()
