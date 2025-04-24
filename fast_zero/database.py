# criando uma conexão com o banco de dados
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engene = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engene) as session:
        yield session
