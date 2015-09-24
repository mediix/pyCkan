from sqlalchemy import create_engine

def set_connection(user, passwd, host, db, port='3306'):
    """
    MySQL-database connection string
    """
    DB_URI = "mysql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(DB_URI.format(
        user   = user,
        passwd = passwd,
        host   = host,
        port   = port,
        db     = db)
    )

    return engine
    # conn = MySQLdb.connect(
    #             user    = user,
    #             passwd  = passwd,
    #             host    = host,
    #             db      = db,
    #             charset = "utf8",
    #             use_unicode=True)

    # return conn


def table_exists(table_name=None, con=None):
    """
    table_name:
    con:

    return:
    """
    cur = con.cursor()
    try:
      cur.execute("SHOW TABLES;")
    except MySQLdb.Error as e:
      print "ERROR FROM => table_exists %d: %s" % (e.args[0], e.args[1])
    finally:
      cur.close()

    table_names = cur.fetchall()
    table_names = [x[0].encode('utf-8') for x in table_names]
    exists = True if table_name in table_names else False
    return exists

def check_id(table_name=None, con=None, *args):
    """
    table_name:
    con:
    *args:
    """
    # print args, type(args), len(args)
    col = [ elem.keys() for elem in args ][0]
    val = [ tuple(elem.values()) for elem in args ]

    col = ', '.join('%s=%s AND' % c for c in col)

    # print "COLUMNS: %s" % col
    # print "VALUES: %s" % val

    sql = """SELECT id FROM %(table_name)s
             WHERE %(col_val)s;""" % {'table_name':table_name, 'col_val':col_val}
    try:
      cur = con.cursor()
      cur.execute(sql)
      db_response = cur.fetchone()
    except MySQLdb.Error as e:
      print "ERROR FROM => check_id %d: %s" % (e.args[0], e.args[1])

