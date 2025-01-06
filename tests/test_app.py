from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    # Arrange ( organização do teste)
    client = TestClient(app)

    # act (a ação, aqui e feito a resquisissão )
    response = client.get('/')

    # assert ( comparando a requisissão deu certo se ela retornou ok "200" )
    assert response.status_code == HTTPStatus.OK
    # assert ( para comparar o retorno se o djson e o esperado)
    assert response.json() == {'mensagem': 'Ola mundo'}
