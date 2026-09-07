from meu_grafo import GrafoSimilaridadeTextual


def _grafo_a_partir_de_arestas(arestas):
    grafo = GrafoSimilaridadeTextual()
    for de, para, peso in arestas:
        grafo.adjacencia.setdefault(de, {})[para] = peso
        grafo.adjacencia.setdefault(para, {})[de] = peso
    return grafo


def test_triangulo_escolhe_as_duas_arestas_de_maior_peso():
    grafo = _grafo_a_partir_de_arestas([
        (1, 2, 5),
        (2, 3, 1),
        (1, 3, 3),
    ])

    assert grafo.gerar_arvore_geradora(origem=1) == [(1, 2, 5), (1, 3, 3)]


def test_grafo_que_ja_e_uma_arvore_retorna_as_mesmas_arestas():
    grafo = _grafo_a_partir_de_arestas([
        (1, 2, 2),
        (2, 3, 6),
        (3, 4, 4),
    ])

    assert grafo.gerar_arvore_geradora(origem=1) == [(1, 2, 2), (2, 3, 6), (3, 4, 4)]


def test_arvore_cobre_todos_os_vertices_de_um_grafo_conexo():
    grafo = _grafo_a_partir_de_arestas([
        (1, 2, 5),
        (2, 3, 1),
        (1, 3, 3),
        (3, 4, 7),
    ])

    arvore = grafo.gerar_arvore_geradora(origem=1)

    assert len(arvore) == 3
    vertices_cobertos = {1}
    for de, para, _peso in arvore:
        vertices_cobertos.add(de)
        vertices_cobertos.add(para)
    assert vertices_cobertos == {1, 2, 3, 4}


def test_grafo_desconexo_cobre_apenas_o_componente_da_origem():
    grafo = _grafo_a_partir_de_arestas([
        (1, 2, 5),
        (3, 4, 2),
    ])

    assert grafo.gerar_arvore_geradora(origem=1) == [(1, 2, 5)]


def test_lida_com_empate_de_peso_sem_quebrar():
    grafo = _grafo_a_partir_de_arestas([
        (1, 2, 4),
        (2, 3, 4),
        (1, 3, 4),
    ])

    arvore = grafo.gerar_arvore_geradora(origem=1)

    assert len(arvore) == 2
    assert sum(peso for _, _, peso in arvore) == 8
    vertices_cobertos = {1}
    for de, para, _peso in arvore:
        vertices_cobertos.add(de)
        vertices_cobertos.add(para)
    assert vertices_cobertos == {1, 2, 3}


def test_grafo_com_um_unico_vertice_nao_gera_arestas():
    grafo = GrafoSimilaridadeTextual()
    grafo.adjacencia = {1: {}}

    assert grafo.gerar_arvore_geradora(origem=1) == []


def test_grafo_vazio_nao_gera_arestas():
    grafo = GrafoSimilaridadeTextual()

    assert grafo.gerar_arvore_geradora() == []


def test_origem_invalida_cai_para_o_primeiro_vertice():
    grafo = _grafo_a_partir_de_arestas([(1, 2, 5), (2, 3, 1)])

    assert grafo.gerar_arvore_geradora(origem=999) == grafo.gerar_arvore_geradora()
