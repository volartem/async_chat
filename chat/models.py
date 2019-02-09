import sqlalchemy as sa
from datetime import datetime
from .security import generate_password_hash

meta = sa.MetaData()

rooms = sa.Table(
    'room', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('name', sa.String(150), nullable=False, unique=True),
    sa.Column('created', sa.Date, nullable=False),

    sa.PrimaryKeyConstraint('id', name='room_id__pk'),
)

users = sa.Table(
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
messages = sa.Table(
    'message', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('message', sa.Text, nullable=False),
    sa.Column('created', sa.Date, nullable=False),
    sa.Column('author_id', sa.Integer, nullable=False),
    sa.Column('room_id', sa.INTEGER, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='message_id_pkey'),
    sa.ForeignKeyConstraint(['author_id'], [users.c.id],
                            name='chat_author_id_fkey',
                            ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room_id'], [rooms.c.id],
                            name='message__room_fk',
                            ondelete='CASCADE')
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def get_message_by_id(conn, message_id):
    result = await conn.execute(
        messages.select()
        .where(messages.c.id == message_id))
    message_record = await result.first()
    if not message_record:
        msg = "Message with id: {} does not exists".format(message_id)
        raise RecordNotFound(msg.format(message_id))
    return instance_as_dict(message_record)


async def get_message_by_room_id(conn, room_id):
    cursor = await conn.execute(
        messages.select().where(messages.c.room_id == room_id).order_by(messages.c.created)
    )
    records = await cursor.fetchall()
    return [instance_as_dict(row) for row in records if records]


async def get_messages_with_users_by_room_id(conn, room_id):
    join = sa.join(messages, users, users.c.id == messages.c.author_id)
    query = sa.select([messages, users], use_labels=True).select_from(join)\
        .where(messages.c.room_id == room_id).order_by(messages.c.created)
    records = await conn.execute(query)
    messages_dict = [instance_as_dict(m) for m in records]
    return messages_dict


async def get_all_rooms(conn):
    cursor_room = await conn.execute(rooms.select())
    records_room = await cursor_room.fetchall()
    rooms_dict = [instance_as_dict(r) for r in records_room]
    return rooms_dict


async def get_user_by_username(conn, username):
    cursor = await conn.execute(users.select().where(users.c.username == username))
    result = await cursor.first()
    return result


async def get_room_by_id(conn, id):
    cursor = await conn.execute(rooms.select().where(rooms.c.id == id))
    result = await cursor.first()
    return result


async def create_message(conn, text, user_id, room_id):
    message_insert = messages.insert().returning(*messages.c).values(message=text, author_id=user_id, room_id=room_id,
                                                                     created=datetime.now())
    result = await conn.execute(message_insert)
    message = await result.first()
    return instance_as_dict(message)


async def create_user(conn, form):
    password = generate_password_hash(form['password'])
    user_insert = users.insert().returning(*users.c).values(username=form['username'], password=password,
                                                            email=form['email'],
                                                            is_superuser=False,
                                                            date_joined=datetime.now(), last_login=datetime.now())
    result = await conn.execute(user_insert)
    return await result.first()


def instance_as_dict(obj):
    return {row: obj[row] if not isinstance(obj[row], datetime) else obj[row].strftime("%Y/%m/%d %H:%M:%S")
            for row in obj}
