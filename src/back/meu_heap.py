"""
Módulo Didático: Implementação de Max-Heap
Criado para fins educacionais - Disciplina de Estruturas de Dados 2

A Fila de Prioridade (Heap) é implementada "do zero" utilizando um array (lista do Python).
Cada nó representa um dicionário de um filme e a chave de ordenação é a "popularidade".
"""

class MaxHeap:
    def __init__(self):
        # A árvore binária completa é armazenada de forma contígua na lista
        self.heap = []

    def _pai(self, indice):
        """Retorna o índice do nó pai."""
        return (indice - 1) // 2

    def _filho_esquerdo(self, indice):
        """Retorna o índice do filho esquerdo."""
        return 2 * indice + 1

    def _filho_direito(self, indice):
        """Retorna o índice do filho direito."""
        return 2 * indice + 2

    def _swap(self, i, j):
        """Troca dois elementos de posição no array. Operação O(1)."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _subir(self, indice):
        """
        Heapify-Up: Restaura a propriedade do Max-Heap subindo o elemento.
        Complexidade: O(log n), pois no pior dos casos sobe a altura da árvore.
        """
        # Enquanto não for a raiz e for maior que o seu pai
        while indice > 0 and self.heap[indice]['popularidade'] > self.heap[self._pai(indice)]['popularidade']:
            pai_idx = self._pai(indice)
            self._swap(indice, pai_idx)
            indice = pai_idx

    def _descer(self, indice):
        """
        Heapify-Down: Restaura a propriedade do Max-Heap descendo o elemento raiz.
        Complexidade: O(log n), pois no pior dos casos desce a altura da árvore.
        """
        maior = indice
        esq = self._filho_esquerdo(indice)
        dir_ = self._filho_direito(indice)
        tamanho = len(self.heap)

        # Verifica se o filho esquerdo existe e é maior que o nó atual
        if esq < tamanho and self.heap[esq]['popularidade'] > self.heap[maior]['popularidade']:
            maior = esq

        # Verifica se o filho direito existe e é maior que o maior atual
        if dir_ < tamanho and self.heap[dir_]['popularidade'] > self.heap[maior]['popularidade']:
            maior = dir_

        # Se o maior não for o nó raiz (atual), fazemos a troca e continuamos a descer
        if maior != indice:
            self._swap(indice, maior)
            self._descer(maior)

    def inserir(self, elemento):
        """
        Insere um novo filme no final do heap e faz o bubble-up (_subir).
        Complexidade: O(log n).
        """
        self.heap.append(elemento)
        self._subir(len(self.heap) - 1)

    def extrair_max(self):
        """
        Remove e retorna o filme com a maior popularidade (raiz).
        Complexidade: O(log n).
        """
        if not self.heap:
            return None
            
        if len(self.heap) == 1:
            return self.heap.pop()
            
        # Guarda o valor máximo (raiz)
        maximo = self.heap[0]
        # Pega o último elemento da árvore e coloca na raiz
        self.heap[0] = self.heap.pop()
        # Faz o heapify-down (_descer) para restaurar as propriedades
        self._descer(0)
        
        return maximo

    def tamanho(self):
        """Complexidade O(1)"""
        return len(self.heap)
