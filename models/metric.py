from lib.database import Database

"""
create table metrics (
 id BIGSERIAL PRIMARY KEY,
 message_id double precision not null,
 text varchar(200) not null,
 room varchar(10) not null,
 match boolean not null,
 user_id varchar(10) references users(slack_id),
 created_at TIMESTAMP default now()
);
"""


class Metric:

    TABLE_NAME = 'metrics'

    @classmethod
    def insert(cls, message, match):
        if not message:
            print "No message to write..."
            return None

        data = {
            'message_id': message.id or -1,
            'text': message.text,
            'room': message.room,
            'user_id': message.user.id,
            'match': 't' if match else 'f'
        }

        query = '''INSERT INTO %(table_name)s (%(keys)s) VALUES (%(format)s)'''\
                % {
                    'table_name': cls.TABLE_NAME,
                    'keys': ", ".join(data.keys()),
                    'format': ", ".join(['%s'] * len(data))
                }

        conn = None
        cursor = None
        try:
            conn = Database.connect()
            cursor = conn.cursor()
            cursor.execute(query, data.values())
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
