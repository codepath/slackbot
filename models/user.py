import json
from lib.database import Database

class User:
    TABLE_NAME = 'users'

    @classmethod
    def insert_or_update(cls, info):
        if not info:
            print "Nothing to write..."
            return None

        query = '''
INSERT INTO %(table_name)s
(%(keys)s) VALUES
(%(format)s)
ON CONFLICT (slack_id) DO UPDATE
SET %(update_keys)s
''' % {'table_name' : cls.TABLE_NAME,
       'keys' : ", ".join(info.keys()),
       'format' : ", ".join(['%s']*len(info)),
       'update_keys' : ", ".join(map(lambda x: '%s= excluded.%s' % (x, x), info.keys())) }

        conn = None
        cursor = None
        try:
            conn = Database.connect()
            cursor = conn.cursor()
            cursor.execute(query, info.values())
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
    data = []
    with open('profile_data.json') as data_file:
        data = json.load(data_file)

    print data[0]

    User.insert_or_update(data[0])
