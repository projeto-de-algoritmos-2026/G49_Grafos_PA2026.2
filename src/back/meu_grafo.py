"""
Módulo Didático: Implementação de Grafo Bipartido
Criado para fins educacionais - Disciplina de Estruturas de Dados 2

Este grafo separa logicamente utilizadores e filmes e é armazenado
por meio de Lista de Adjacência utilizando dicionários do Python.
"""

from meu_heap import MaxHeapArestas


class GrafoBipartido:
    def __init__(self):
        # Listas de adjacência separadas para clareza didática.
        # adj_utilizadores[id_user] = set(id_filmes_assistidos)
        self.adj_utilizadores = {}
        
        # adj_filmes[id_filme] = set(id_users_que_assistiram)
        self.adj_filmes = {}
        
        # Armazenamento de metadados para facilitar buscas nominais (O(1))
        self.meta_utilizadores = {}
        self.meta_filmes = {}

    def adicionar_utilizador(self, id_utilizador, nome):
        """Adiciona um nó no conjunto U (Utilizadores). Complexidade: O(1)."""
        if id_utilizador not in self.adj_utilizadores:
            self.adj_utilizadores[id_utilizador] = set()
            self.meta_utilizadores[id_utilizador] = nome

    def adicionar_filme(self, id_filme, titulo):
        """Adiciona um nó no conjunto V (Filmes). Complexidade: O(1)."""
        if id_filme not in self.adj_filmes:
            self.adj_filmes[id_filme] = set()
            self.meta_filmes[id_filme] = titulo

    def adicionar_aresta(self, id_utilizador, id_filme):
        """
        Cria uma ligação não-direcionada entre Utilizador e Filme.
        Como é implementado com Sets, a inserção não duplica arestas.
        Complexidade: O(1) médio.
        """
        # Garante que os nós existam no grafo antes de criar a aresta
        if id_utilizador not in self.adj_utilizadores:
            self.adicionar_utilizador(id_utilizador, f"Utilizador {id_utilizador}")
        if id_filme not in self.adj_filmes:
            self.adicionar_filme(id_filme, f"Filme {id_filme}")

        self.adj_utilizadores[id_utilizador].add(id_filme)
        self.adj_filmes[id_filme].add(id_utilizador)

    def remover_aresta(self, id_utilizador, id_filme):
        """
        Remove a ligação não-direcionada entre Utilizador e Filme,
        usando .discard() para ser O(1) e não dar erro se não existir.
        """
        if id_utilizador in self.adj_utilizadores:
            self.adj_utilizadores[id_utilizador].discard(id_filme)
        if id_filme in self.adj_filmes:
            self.adj_filmes[id_filme].discard(id_utilizador)

    def recomendar_para_utilizador(self, id_utilizador):
        """
        Projeção de Grafo Bipartido (Filtragem Colaborativa).
        Descobre utilizadores com gostos similares para inferir filmes.
        
        Complexidade: O(F * U * f), onde:
        F = filmes assistidos pelo alvo
        U = utilizadores que também assistiram F
        f = filmes que esses utilizadores U assistiram
        """
        if id_utilizador not in self.adj_utilizadores:
            return [] # Utilizador inexistente

        filmes_assistidos_pelo_alvo = self.adj_utilizadores[id_utilizador]
        
        if not filmes_assistidos_pelo_alvo:
            # Caso de "Cold Start": O utilizador ainda não interagiu com o sistema
            return []

        # Dicionário para contar a frequência de recomendações (Grau da aresta virtual na projeção)
        frequencia_recomendacao = {}

        # 1. Para cada filme que o alvo assistiu
        for id_filme_assistido in filmes_assistidos_pelo_alvo:
            
            # 2. Descobre quem mais assistiu a esse mesmo filme (Nós adjacentes no grafo)
            vizinhos_similares = self.adj_filmes[id_filme_assistido]
            
            for id_vizinho in vizinhos_similares:
                # Evita que o algoritmo se auto-recomende
                if id_vizinho == id_utilizador:
                    continue
                
                # 3. Para cada vizinho similar, analisa quais filmes ELE assistiu
                filmes_do_vizinho = self.adj_utilizadores[id_vizinho]
                
                for filme_sugestao in filmes_do_vizinho:
                    # Só recomenda filmes que o alvo AINDA NÃO ASSISTIU
                    if filme_sugestao not in filmes_assistidos_pelo_alvo:
                        if filme_sugestao in frequencia_recomendacao:
                            frequencia_recomendacao[filme_sugestao] += 1
                        else:
                            frequencia_recomendacao[filme_sugestao] = 1

        # Transforma o dicionário num formato de lista de tuplas para poder ordenar
        # formato: [(id_filme, score_frequencia), ...]
        sugestoes_ordenadas = sorted(
            frequencia_recomendacao.items(), 
            key=lambda x: x[1], # Ordena pelo valor da contagem (score)
            reverse=True        # Ordem decrescente (mais recomendados primeiro)
        )

        # Seleciona os Top 15 melhores IDs de filmes
        top_15_ids = [sugestao[0] for sugestao in sugestoes_ordenadas[:15]]
        
        # Converte os IDs num formato (ID, Título) para a API processar
        top_15_tuplas = [(f_id, self.meta_filmes.get(f_id, f"Desconhecido ({f_id})")) for f_id in top_15_ids]

        return top_15_tuplas

class GrafoSimilaridadeTextual:
    def __init__(self):
        # adjacencia[id_u] = {id_v: peso_intersecao}
        self.adjacencia = {}

    def construir_grafo(self, dicionario_filmes):
        """
        Recebe um dicionário {id_filme: "palavra1; palavra2"}
        Constrói arestas baseadas na intersecção de palavras-chave.
        """
        filmes_sets = {}
        for id_filme, texto_palavras in dicionario_filmes.items():
            if isinstance(texto_palavras, str):
                # Usando split e limpeza básica para pegar palavras relevantes
                palavras = set([p.strip().lower() for p in texto_palavras.replace(';', ' ').split() if len(p.strip()) > 2])
                filmes_sets[id_filme] = palavras
            else:
                filmes_sets[id_filme] = set()

        ids = list(filmes_sets.keys())
        
        # Complexidade O(V^2), razoável para a carga inicial
        for i in range(len(ids)):
            id_u = ids[i]
            if id_u not in self.adjacencia:
                self.adjacencia[id_u] = {}
                
            for j in range(i + 1, len(ids)):
                id_v = ids[j]
                intersecao = filmes_sets[id_u].intersection(filmes_sets[id_v])
                peso = len(intersecao)
                
                if peso > 0:
                    self.adjacencia[id_u][id_v] = peso
                    if id_v not in self.adjacencia:
                        self.adjacencia[id_v] = {}
                    self.adjacencia[id_v][id_u] = peso

    def calcular_centralidade(self):
        """
        Retorna {id_filme: soma_dos_pesos_das_arestas}
        """
        pesos = {}
        for id_filme, vizinhos in self.adjacencia.items():
            pesos[id_filme] = sum(vizinhos.values())
        return pesos

    def gerar_arvore_geradora(self, origem=None):
        """
        Algoritmo de Prim (variante Árvore Geradora MÁXIMA).

        Constrói uma árvore que conecta todos os filmes alcançáveis a
        partir de 'origem', escolhendo a cada passo a aresta de MAIOR
        peso (maior similaridade) que liga a árvore já construída a um
        filme ainda fora dela. O resultado não tem ciclos e representa
        a espinha dorsal de maior similaridade textual entre os filmes.

        Retorna uma lista de tuplas (id_de, id_para, peso), na ordem em
        que cada filme entrou na árvore. Se o grafo for desconexo, cobre
        apenas o componente alcançável a partir de 'origem'.

        Complexidade: O(E log E), pois cada aresta pode ser inserida na
        fila de prioridade a partir de cada uma das suas duas pontas.
        """
        if not self.adjacencia:
            return []

        vertices = list(self.adjacencia.keys())
        if origem is None or origem not in self.adjacencia:
            origem = vertices[0]

        visitados = {origem}
        arvore = []
        borda = MaxHeapArestas()

        for vizinho, peso in self.adjacencia[origem].items():
            borda.inserir({'peso': peso, 'de': origem, 'para': vizinho})

        while borda.tamanho() > 0 and len(visitados) < len(vertices):
            aresta = borda.extrair_max()

            if aresta['para'] in visitados:
                continue  # aresta obsoleta: a outra ponta já entrou na árvore por outro caminho

            visitados.add(aresta['para'])
            arvore.append((aresta['de'], aresta['para'], aresta['peso']))

            for vizinho, peso in self.adjacencia[aresta['para']].items():
                if vizinho not in visitados:
                    borda.inserir({'peso': peso, 'de': aresta['para'], 'para': vizinho})

        return arvore
