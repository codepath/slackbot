import psycopg2
import sys

class Database:
    @classmethod
    def default_config(cls):
        config = {'dbname' : 'botdb',
                  'user' : 'slackbot',
                  'host' : 'localhost',
                  'password' : 'botpass123'}
        return config

    @classmethod
    def connect(cls, config = None):
        try:
            config = config if config else cls.default_config()
            conn_str = "dbname='%(dbname)s' user='%(user)s' host='%(host)s' password='%(password)s'" % config
            return psycopg2.connect(conn_str)
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    conn = Database.connect()
    cur = conn.cursor()
    cur.execute("""SELECT datname from pg_database""")
    rows = cur.fetchall()
    print "\nShow me the databases:\n"
    for row in rows:
        print "   ", row[0]
