import sqlalchemy as sa

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
    sa.Column('date_joined ', sa.Date, nullable=False),
    sa.Column('room_id', sa.INTEGER, nullable=True),

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

# async def get_message(conn, message_id):
#     result = await conn.execute(
#         message.select()
#         .where(message.c.id == message_id))
#     message_record = await result.first()
#     if not message_record:
#         msg = "Question with id: {} does not exists"
#         raise RecordNotFound(msg.format(message_id))
#     result = await conn.execute(
#         message.select()
#         .where(message.c.message_id == message_id)
#         .order_by(message.c.id))
#     message_records = await result.fetchall()
#     return message_record, message_records


# async def vote(conn, question_id, choice_id):
#     result = await conn.execute(
#         choice.update()
#         .returning(*choice.c)
#         .where(choice.c.question_id == question_id)
#         .where(choice.c.id == choice_id)
#         .values(votes=choice.c.votes+1))
#     record = await result.fetchone()
#     if not record:
#         msg = "Question with id: {} or choice id: {} does not exists"
#         raise RecordNotFound(msg.format(question_id, choice_id))
