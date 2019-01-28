import sqlalchemy as sa
from datetime import datetime
import aiopg.sa

__all__ = ['user', 'message', 'room']

meta = sa.MetaData()

room = sa.Table(
    'room', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('name', sa.String(150), nullable=False, unique=True),
    sa.Column('created', sa.Date, nullable=False),

    sa.PrimaryKeyConstraint('id', name='room_id__pk'),
)

user = sa.Table(
    'auth_user', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('password', sa.String(128), nullable=False),
    sa.Column('username', sa.String(150), nullable=False),
    sa.Column('email', sa.String(254), nullable=False),
    sa.Column('is_superuser', sa.Boolean, default=False),
    sa.Column('last_login', sa.Date, nullable=True),
    sa.Column('date_joined', sa.Date, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='auth_user_id__pk'),
)
message = sa.Table(
    'message', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('message', sa.Text, nullable=False),
    sa.Column('created', sa.Date, nullable=False),
    sa.Column('author_id', sa.Integer, nullable=False),
    sa.Column('room_id', sa.INTEGER, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='message_id_pkey'),
    sa.ForeignKeyConstraint(['author_id'], [user.c.id],
                            name='chat_author_id_fkey',
                            ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room_id'], [room.c.id],
                            name='message__room_fk',
                            ondelete='CASCADE')
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['models'] = engine


async def close_pg(app):
    app['models'].close()
    await app['models'].wait_closed()


async def get_message_by_id(conn, message_id):
    result = await conn.execute(
        message.select()
        .where(message.c.id == message_id))
    message_record = await result.first()
    if not message_record:
        msg = "Message with id: {} does not exists".format(message_id)
        raise RecordNotFound(msg.format(message_id))
    return instance_as_dict(message_record)


async def get_message_by_room_id(conn, room_id):
    cursor = await conn.execute(
        message.select().where(message.c.room_id == room_id).order_by(message.c.created)
    )
    records = await cursor.fetchall()
    return [instance_as_dict(row) for row in records if records]


async def get_messages_with_users(conn):
    join = sa.join(message, user, user.c.id == message.c.author_id)
    query = (sa.select([message, user], use_labels=True).select_from(join))
    result = await conn.execute(query)
    return result


async def get_all_rooms_and_messages(conn):
    records = await get_messages_with_users(conn)
    messages = [instance_as_dict(m) for m in records]
    cursor_room = await conn.execute(room.select())
    records_room = await cursor_room.fetchall()
    rooms = [instance_as_dict(r) for r in records_room]
    return messages, rooms


def instance_as_dict(obj):
    return {row: obj[row] if not isinstance(obj[row], datetime) else obj[row].strftime("%Y/%m/%d %H:%M:%S")
            for row in obj}
