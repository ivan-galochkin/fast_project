from fastapi import FastAPI
import fastapi
from item_models import UserItem
from db_session import create_session, global_init
from db_models import User
import sqlalchemy as sa

app = FastAPI()


@app.post("/users")
async def create_user(item: UserItem):
    session = create_session()
    try:
        user = User()
        user.email = item.email
        user.password = item.password
        session.add(user)
        session.commit()
        return fastapi.responses.Response(status_code=200)
    except sa.exc.IntegrityError as exc:
        raise fastapi.exceptions.HTTPException(status_code=409,
                                               detail={'exception': "UniqueError",
                                                       'column': str(exc.orig).split(' ')[-1]})

    finally:
        session.close()


@app.get('/users')
async def get_user(email: str, password: str):
    session = create_session()
    try:
        session.query(User).filter(User.email == email, User.password == password).one()
        return fastapi.responses.Response(status_code=200)
    except sa.orm.exc.NoResultFound as exc:
        raise fastapi.exceptions.HTTPException(status_code=401, detail={'exception': "WrongCredentials"})
    finally:
        session.close()


global_init('users.db')
