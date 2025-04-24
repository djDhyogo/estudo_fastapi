from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    # Arrange ( organização do teste)
    # client = TestClient(app)

    # act (a ação, aqui e feito a resquisissão )
    response = client.get('/')

    # assert ( comparando a requisissão deu certo se ela retornou ok "200" )
    assert response.status_code == HTTPStatus.OK
    # assert ( para comparar o retorno se o djson e o esperado)
    assert response.json() == {'message': 'Olá Mundo!'}


def test_creat_user(client: TestClient):
    response = client.post(
        '/users',
        json={
            'username': 'teste_nome',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'teste_nome',
        'email': 'user@example.com',
        'id': 1,
    }


def test_create_user_should_return_409_username_exists__exercicio(
    client: TestClient, user: User
):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.json() == ({
        'detail': 'Usuario ja existe no banco de dados'
    })
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_should_return_409_email_exists__exercicio(
    client: TestClient, user: User
):
    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'email': user.email,
            'password': 'string',
        },
    )
    assert response.json() == ({'detail': 'Email ja existe no banco de dados'})
    assert response.status_code == HTTPStatus.CONFLICT


def test_read_users(client: TestClient):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client: TestClient, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_users(client: TestClient, user: User):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_get_users_404(client: TestClient, user: User):
    """
    Teste o endpoint GET /users/{user_id} para um usuario que n existe.

    Verifica se uma solicita o para um usuario inexistente retorna um c digo
    de status 404 e a mensagem de erro apropriada na resposta.
    """

    response = client.get('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_users(client: TestClient, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '1234',
            'username': 'teste_nome2',
            'email': 'user@example.com',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste_nome2',
        'email': 'user@example.com',
        'id': 1,
    }


def test_update_integrity_error(client: TestClient, user: User, token: str):
    response_update = client.post(
        '/users',
        json={
            'username': user.username,
            'email': user.email,
            'password': 'mynewpassword',
        },
    )
    response_update = client.put(
    f'/users/{user.id}',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'username': user.username,  # conflito proposital
        'email': user.email,
        'password': 'mynewpassword',
    },
)

    assert response_update.status_code == HTTPStatus.CONFLICT


def test_update_users_404(client: TestClient, user: User, token):
    response = client.put(
        '/users/666',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste_nome2',
            'email': 'user@example.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# def test_delete_user_404(client: TestClient, user: User, token: str):
#     response = client.delete('/users/666')
#     # assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User Not Found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
