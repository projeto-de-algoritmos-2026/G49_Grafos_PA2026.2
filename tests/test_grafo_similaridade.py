import math

from meu_grafo import GrafoSimilaridadeTextual

def test_aresta_simetrica_com_peso_correto():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({
        1: "amor guerra espada",
        2: "amor traicao espada",
    })

    assert grafo.adjacencia[1][2] == 2
    assert grafo.adjacencia[2][1] == 2


def test_sem_intersecao_nao_cria_aresta():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({
        1: "amor guerra espada",
        2: "robo espacial futuro",
    })

    assert 2 not in grafo.adjacencia[1]
    assert 1 not in grafo.adjacencia[2]


def test_filme_sem_palavras_chave_fica_isolado_mas_continua_vertice():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({
        1: "amor guerra espada",
        2: "",
    })

    assert 2 in grafo.adjacencia
    assert grafo.adjacencia[2] == {}


def test_valor_nao_string_e_tratado_como_sem_palavras_chave():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({
        1: "amor guerra espada",
        2: math.nan,
        3: None,
    })

    assert grafo.adjacencia[2] == {}
    assert grafo.adjacencia[3] == {}


def test_nenhum_auto_laco():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({
        1: "amor guerra espada",
        2: "amor guerra espada",
    })

    assert 1 not in grafo.adjacencia[1]
    assert 2 not in grafo.adjacencia[2]


def test_grafo_vazio_nao_quebra():
    grafo = GrafoSimilaridadeTextual()
    grafo.construir_grafo({})

    assert grafo.adjacencia == {}
