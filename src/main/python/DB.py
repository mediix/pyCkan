from sqlalchemy import create_engine

def set_connection(user, passwd, host, db, port='3306'):
    """
    user, passwd, host, db; for establishing connection

    return:
        engine
    """
    # MySQL-database connection string
    DB_URI = "mysql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(DB_URI.format(
        user   = user,
        passwd = passwd,
        host   = host,
        port   = port,
        db     = db)
    )

    return engine
