import json

from lib.database import Database


class User:
    TABLE_NAME = "users"

    @classmethod
    def insert_or_update(cls, info):
        if not info:
            print("Nothing to write...")
            return None

        table_name = cls.TABLE_NAME
        keys = ", ".join(info.keys())
        values = ", ".join(["%s"] * len(info))
        update_keys = ", ".join(map(lambda x: f"{x}= excluded.{x}", info.keys()))

        conn = None
        cursor = None
        query = (
            f"INSERT INTO {table_name} ({keys}) VALUES ({values}) "
            f"ON CONFLICT (slack_id) DO UPDATE "
            f"SET {update_keys}"
        )

        try:
            conn = Database.connect()
            cursor = conn.cursor()
            cursor.execute(query, list(info.values()))
        except Exception as e:
            # TODO: Change print to logger
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.commit()
                conn.close()


if __name__ == "__main__":
    with open("profile_data.json") as data_file:
        data = json.load(data_file)

    print(data[0])

    User.insert_or_update(data[0])
