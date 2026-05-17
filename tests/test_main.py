from unittest.mock import patch
from codigo.main import adicionar_medicamento, buscar_endereco_cep


def test_adicionar_medicamento_sucesso():
    lista = []
    sucesso, msg = adicionar_medicamento(lista, "Dipirona", "08:00", "1 comp")
    assert sucesso is True
    assert len(lista) == 1


def test_adicionar_medicamento_incompleto():
    lista = []
    sucesso, msg = adicionar_medicamento(lista, "", "08:00", "1 comp")
    assert sucesso is False


@patch('requests.get')
def test_buscar_cep_sucesso(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }

    sucesso, resultado = buscar_endereco_cep("01001-000")
    assert sucesso is True
    assert "Praça da Sé" in resultado


@patch('requests.get')
def test_buscar_cep_inexistente(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"erro": True}

    sucesso, resultado = buscar_endereco_cep("99999999")
    assert sucesso is False
    assert resultado == "CEP não encontrado."