from meu_heap import MaxHeapArestas


def test_extrai_em_ordem_decrescente_de_peso():
    heap = MaxHeapArestas()
    heap.inserir({'peso': 3, 'de': 1, 'para': 2})
    heap.inserir({'peso': 7, 'de': 1, 'para': 3})
    heap.inserir({'peso': 5, 'de': 2, 'para': 3})

    assert heap.extrair_max()['peso'] == 7
    assert heap.extrair_max()['peso'] == 5
    assert heap.extrair_max()['peso'] == 3


def test_tamanho_reflete_insercoes_e_remocoes():
    heap = MaxHeapArestas()
    assert heap.tamanho() == 0

    heap.inserir({'peso': 1, 'de': 1, 'para': 2})
    heap.inserir({'peso': 2, 'de': 1, 'para': 3})
    assert heap.tamanho() == 2

    heap.extrair_max()
    assert heap.tamanho() == 1


def test_extrair_max_em_heap_vazio_retorna_none():
    heap = MaxHeapArestas()
    assert heap.extrair_max() is None


def test_mantem_a_propriedade_de_heap_com_muitas_insercoes():
    heap = MaxHeapArestas()
    pesos = [4, 8, 1, 9, 2, 7, 3, 6, 5]
    for indice, peso in enumerate(pesos):
        heap.inserir({'peso': peso, 'de': 0, 'para': indice + 1})

    extraidos = [heap.extrair_max()['peso'] for _ in pesos]
    assert extraidos == sorted(pesos, reverse=True)
