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
        return fastapi.responses.HTMLResponse(200)
    except sa.exc.IntegrityError as exc:
        raise fastapi.exceptions.HTTPException(status_code=403,
                                               detail={'exception': "UniqueError",
                                                       'column': str(exc.orig).split(' ')[-1]})

    finally:
        session.close()


global_init('users.db')
