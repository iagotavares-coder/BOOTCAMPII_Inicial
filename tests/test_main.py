from codigo.main import adicionar_medicamento, listar_medicamentos

def test_adicionar_medicamento_sucesso():
    lista = []
    sucesso, msg = adicionar_medicamento(lista, "Dipirona", "08:00", "1 gota")
    assert sucesso is True
    assert len(lista) == 1

def test_adicionar_medicamento_invalido():
    lista = []
    sucesso, msg = adicionar_medicamento(lista, "", "", "") 
    assert sucesso is False
    assert "obrigatórios" in msg

def test_listar_vazio():
    lista = []
    resultado = listar_medicamentos(lista)
    assert "Nenhum medicamento" in resultado