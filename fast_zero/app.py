from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import (
    Message,
    UserDB,
    UserPublic,
    UserSchema,
    UsersListe,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def creat_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    # breakpoint()
    # print(user_with_id)

    return user_with_id


@app.get('/users', status_code=HTTPStatus.OK, response_model=UsersListe)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_class=UserPublic)
def update_user(usar_id: int, user: UserSchema):
    pass
