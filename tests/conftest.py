import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registery
from fast_zero.security import get_passoword_hasd


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client  # type: ignore
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registery.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registery.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = '1234'
    user = User(
        username='Dhyogo',
        email='dhyogo@example.com',
        password=get_passoword_hasd(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    """
    Monkey Patch para armazenar a senha em texto
    claro durante os testes. N o deve ser
    usado em produ o.
    """
    user.clean_password = pwd  # hack para mudar a senha
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
