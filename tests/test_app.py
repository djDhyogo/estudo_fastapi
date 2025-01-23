from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Arrange ( organização do teste)
    # client = TestClient(app)

    # act (a ação, aqui e feito a resquisissão )
    response = client.get('/')

    # assert ( comparando a requisissão deu certo se ela retornou ok "200" )
    assert response.status_code == HTTPStatus.OK
    # assert ( para comparar o retorno se o djson e o esperado)
    assert response.json() == {'message': 'Ola mundo'}


def test_creat_user(client):
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


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'user@example.com',
                'id': 1,
                'username': 'teste_nome',
            },
        ]
    }
