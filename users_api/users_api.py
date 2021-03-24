from fastapi import FastAPI
import fastapi
from models import UserItem
from db_session import create_session, global_init
from schemas import User
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8081",
    "https://localhost:8081",
    "localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
