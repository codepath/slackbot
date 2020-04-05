from dataclasses import dataclass

import psycopg2


@dataclass
class Config:
    dbname: str
    user: str
    host: str
    password: str


class Database:
    @classmethod
    def default_config(cls):
        return Config(
            dbname="botdb", user="slackbot", host="localhost", password="botpass123",
        )

    @classmethod
    def connect(cls, config=None):
        try:
            config = config if config else cls.default_config()
            conn_str = (
                f"dbname='{config.dbname}' "
                f"user='{config.user}' "
                f"host='{config.host}' "
                f"password='{config.password}'"
            )

            return psycopg2.connect(conn_str)
        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    conn = Database.connect()
    cur = conn.cursor()
    cur.execute("""SELECT datname from pg_database""")
    rows = cur.fetchall()
    print("\nShow me the databases:\n")
    for row in rows:
        print("   ", row[0])
