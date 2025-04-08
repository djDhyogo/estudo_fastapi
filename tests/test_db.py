# tests/test_user.py
from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="Dhyogo",
        email="dhyogo@example",
        password="1234",
    )

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == "dhyogo@example"))

    assert result.email == "dhyogo@example"

    # escreva o assert
    assert user.id == 1
