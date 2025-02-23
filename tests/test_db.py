# tests/test_user.py
from fast_zero.models import User


def test_create_user():
    user = User(
        username='Dhyogo',
        email='dhyogo@example',
        password='1234',
    )

    # escreva o assert
    assert user.username == 'Dhyogo'
