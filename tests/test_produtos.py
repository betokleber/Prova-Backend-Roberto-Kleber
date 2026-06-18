import pytest

def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

def test_criar_produto_sucesso(client):
    payload = {"nome": "SSD M.2 NVMe", "preco": 450.00, "estoque": 5, "ativo": True}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    dados = response.json()
    assert dados["id"] is not None
    assert dados["nome"] == payload["nome"]

def test_produto_aparece_na_listagem(client):
    payload = {"nome": "Memória RAM 16GB", "preco": 320.00}
    client.post("/produtos", json=payload)
    response = client.get("/produtos")
    assert len(response.json()) == 1

def test_buscar_produto_por_id_sucesso(client, produto_existente):
    prod_id = produto_existente["id"]
    response = client.get(f"/produtos/{prod_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Base"

def test_buscar_produto_id_inexistente(client):
    response = client.get("/produtos/8888")
    assert response.status_code == 404

def test_deletar_produto_sucesso(client, produto_existente):
    prod_id = produto_existente["id"]
    response = client.delete(f"/produtos/{prod_id}")
    assert response.status_code == 204

def test_deletar_e_confirmar_remocao(client, produto_existente):
    prod_id = produto_existente["id"]
    client.delete(f"/produtos/{prod_id}")
    res_get = client.get(f"/produtos/{prod_id}")
    assert res_get.status_code == 404

def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/8888")
    assert response.status_code == 404

@pytest.mark.parametrize(
    "payload, desc",
    [
        ({"nome": "", "preco": 10.0}, "Nome vazio"),
        ({"nome": "Fone", "preco": -1.0}, "Preço negativo"),
        ({"nome": "Fone", "preco": 0.0}, "Preço zero"),
        ({"preco": 10.0}, "Falta nome"),
        ({"nome": "Fone"}, "Falta preço"),
    ]
)
def test_validacoes_esquema(client, payload, desc):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422

def test_isolamento_estado_um(client):
    client.post("/produtos", json={"nome": "Item Unico", "preco": 5.0})
    res = client.get("/produtos")
    assert len(res.json()) == 1

def test_isolamento_estado_dois(client):
    res = client.get("/produtos")
    assert len(res.json()) == 0