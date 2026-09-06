# 🏛️ Arquitetura do Sistema: GrafoFlix

Bem-vindo à documentação técnica do MVP do nosso Sistema de Recomendação. Este documento foi elaborado para fornecer à banca universitária da disciplina de **Estruturas de Dados 2** uma visão aprofundada de como o sistema funciona por baixo dos panos, demonstrando o uso avançado de Estruturas de Dados puras sem a utilização de bibliotecas prontas como `networkx` ou `heapq`.

---

## 1. O Fluxo de Dados (Pipeline ETL)

O nosso sistema não se baseia em dados aleatórios simples. Simulámos um cenário real da indústria de *Data Science*:

*   **A Origem:** Começámos com um *dataset* massivo e real de filmes extraído do Kaggle (`dataset_bruto.csv`).
*   **Limpeza (Pandas):** Utilizamos a biblioteca `pandas` num script isolado (`gerador_dados.py`) para filtrar as colunas de Título, Sinopse e Popularidade, e limpámos os valores nulos (NaN). Extraímos uma amostra reproduzível de 1000 filmes.
*   **NLP e IA:** Para cada filme, lemos a sua Sinopse original em inglês e utilizamos Processamento de Linguagem Natural com o algoritmo **Rake-NLTK** para extrair as 5 palavras-chave mais relevantes. 
*   **Arestas e Interações:** Para dar vida ao grafo, gerámos 50 usuários mockados e desenvolvemos um algoritmo que sorteia aleatoriamente entre 10 e 30 interações de visualização (`assistiu=1`) por usuário com os filmes da base, exportando tudo para 3 ficheiros `CSV` na pasta `/data/`.

---

## 2. Estruturas de Dados Clássicas Implementadas do Zero

Para este trabalho académico, o coração do back-end reside em duas estruturas implementadas inteiramente na mão:

### A. Estrutura 1: O Max-Heap (`meu_heap.py`)
*   **Objetivo:** Obter eficientemente a lista dos Filmes Mais Populares da plataforma no topo da página.
*   **Implementação:** Baseada numa Lista Padrão do Python (Array).
*   **Lógica:** O campo chave para a ordenação dos nós da árvore binária virtual é a coluna `popularidade`. 
*   **Complexidade:**
    *   A inserção de um novo filme na árvore demora **$O(\log n)$** devido ao algoritmo de `_subir()` (*heapify-up*).
    *   A remoção da raiz (o filme mais popular de todos) também leva **$O(\log n)$** devido à reorganização do último folha e chamadas recursivas ao `_descer()` (*heapify-down*).

### B. Estrutura 2: Grafo Bipartido (`meu_grafo.py`)
*   **Objetivo:** Obter a recomendação personalizada e inteligente de conteúdos baseados no gosto do Utilizador atual (Filtragem Colaborativa).
*   **Implementação:** Lista de Adjacência em Memória RAM utilizando Dicionários e Conjuntos (Sets) em Python. Esta estrutura divide logicamente os Vértices em dois grupos estanques: *Usuários (U)* e *Filmes (V)*, sendo que as arestas só podem conectar um nó de U a um de V (uma interação).
*   **Filtragem Colaborativa (O Método de Recomendação):**
    Quando queremos recomendar algo para o Usuário 1:
    1. O algoritmo olha para a lista de filmes que o Usuário 1 já viu (Arestas de $U_{usuario1}$).
    2. Através desses filmes, ele viaja pelo grafo e descobre **quem mais** assistiu aos mesmos filmes (Vizinhança partilhada).
    3. Ele analisa as arestas que saem dessa "vizinhança" para encontrar filmes que esses usuários viram, mas que o Usuário 1 ainda não viu.
    4. Ele acumula a pontuação por frequência de ocorrência e ordena o resultado final, gerando sugestões altamente precisas baseadas na projeção do grafo bipartite original.

---

## 3. A Camada de Comunicação e a Persistência (Back-end Flask)

Para que o Front-end consiga visualizar as Estruturas de Dados sem tocar nelas diretamente, utilizamos o **Flask** (`api.py`) como motor da nossa API REST:

1.  **Carga O(V+E):** Quando o `api.py` é inicializado, ele lê todo o CSV e monta as instâncias do Max-Heap e do Grafo Bipartido integralmente na memória RAM do servidor para velocidade ultra-rápida.
2.  **Consulta (`GET`):** O JS Vanilla (`app.js`) envia requisições assíncronas para `/api/populares` (onde extraímos do Heap e devolvemos via JSON) e para `/api/recomendacoes/<id>` (onde consultamos o Grafo).
3.  **Persistência (`POST`):** Quando o usuário clica em "✔️ Já Assisti" no browser:
    *   O Front-end envia um `POST /api/assistir` para o Flask.
    *   O Flask adiciona uma nova aresta no GrafoBipartido na RAM quase instantaneamente (em **$O(1)$** porque usamos sets).
    *   **Efeito Duradouro:** O Flask faz um `append` ('a') na última linha física do ficheiro `/data/interacoes.csv`. Isto garante a durabilidade dos dados, de forma que ao desligar o computador e religar amanhã, as interações do painel Front-end permanecerão registadas no Grafo!

---
*MVP finalizado com sucesso. Preparado para a apresentação.*
