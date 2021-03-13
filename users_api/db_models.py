import sqlalchemy as sa
from db_session import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)
    email = sa.Column(sa.String(64), unique=True, nullable=False)
    password = sa.Column(sa.String(512), nullable=False)
