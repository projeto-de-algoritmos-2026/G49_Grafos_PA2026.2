# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO:
# 1. Certifique-se de que o ambiente virtual está ativado
# 2. Execute: pip install flask flask-cors pandas
# ==============================================================================

import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importa as estruturas de dados criadas manualmente
from meu_heap import MaxHeap
from meu_grafo import GrafoBipartido, GrafoSimilaridadeTextual

app = Flask(__name__)
# Habilita o CORS para permitir requisições do front-end local (index.html)
CORS(app)

# Instancia as estruturas globais
heap_populares = MaxHeap()
grafo_recomendacao = GrafoBipartido()
meta_keywords = {} # Cache global para NLP e Frontend

def carregar_dados():
    """
    Função chamada ao iniciar o servidor para ler os CSVs
    e popular as estruturas de dados na memória RAM.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(base_dir, 'data')
    
    print("Iniciando a carga de dados na memória...")

    # 1. LER E POPULAR FILMES NO HEAP E NOS GRAFOS
    caminho_filmes = os.path.join(data_dir, 'filmes.csv')
    if os.path.exists(caminho_filmes):
        df_filmes = pd.read_csv(caminho_filmes)
        
        dict_keywords = {}
        for _, row in df_filmes.iterrows():
            id_filme = int(row['id_filme'])
            titulo = row['titulo']
            # Trata N/A ou NaN lidos pelo pandas transformando em string
            palavras_chave = str(row.get('palavras_chave', ''))
            
            # Adiciona o nó do filme no Grafo (Conjunto V)
            grafo_recomendacao.adicionar_filme(id_filme, titulo)
            dict_keywords[id_filme] = palavras_chave
            meta_keywords[id_filme] = palavras_chave

        print("-> Construindo Grafo de Similaridade Textual (NLP)...")
        grafo_nlp = GrafoSimilaridadeTextual()
        grafo_nlp.construir_grafo(dict_keywords)
        centralidade = grafo_nlp.calcular_centralidade()
            
        for _, row in df_filmes.iterrows():
            id_filme = int(row['id_filme'])
            titulo = row['titulo']
            peso_nlp = centralidade.get(id_filme, 0)
            
            # Insere no Max-Heap (a chave de ordenação no código do meu_heap.py é 'popularidade')
            # Agora estamos substituindo pela centralidade do NLP!
            heap_populares.inserir({
                'id': id_filme,
                'titulo': titulo,
                'popularidade': peso_nlp
            })
        print(f"-> {len(df_filmes)} Filmes carregados no Heap e nos Grafos.")

    # 2. LER E POPULAR UTILIZADORES NO GRAFO
    caminho_utilizadores = os.path.join(data_dir, 'usuarios.csv')
    if os.path.exists(caminho_utilizadores):
        df_users = pd.read_csv(caminho_utilizadores)
        for _, row in df_users.iterrows():
            id_user = int(row['id_usuario'])
            nome = row['nome']
            
            # Adiciona o nó do utilizador no Grafo (Conjunto U)
            grafo_recomendacao.adicionar_utilizador(id_user, nome)
        print(f"-> {len(df_users)} Utilizadores carregados no Grafo.")

    # 3. LER E POPULAR INTERAÇÕES (ARESTAS) NO GRAFO
    caminho_interacoes = os.path.join(data_dir, 'interacoes.csv')
    if os.path.exists(caminho_interacoes):
        df_interacoes = pd.read_csv(caminho_interacoes)
        for _, row in df_interacoes.iterrows():
            id_user = int(row['id_usuario'])
            id_filme = int(row['id_filme'])
            
            # Cria a aresta não direcionada entre Utilizador e Filme
            grafo_recomendacao.adicionar_aresta(id_user, id_filme)
        print(f"-> {len(df_interacoes)} Interações (Arestas) carregadas no Grafo.")

    print("Carga de dados concluída com sucesso!\n")


@app.route('/api/populares', methods=['GET'])
def get_populares():
    """
    Retorna os top 5 filmes mais populares utilizando a nossa implementação de Max-Heap.
    """
    top_5 = []
    
    # Extrai (remove) os maiores da raiz um por um
    for _ in range(15):
        if heap_populares.tamanho() > 0:
            filme = heap_populares.extrair_max()
            if filme:
                # Criamos um copy raso para nao poluir o heap com palavras_chave
                filme_resposta = filme.copy()
                filme_resposta['palavras_chave'] = meta_keywords.get(filme['id'], '')
                top_5.append(filme_resposta)
                
    # Como extrair_max REMOVE os itens da árvore, precisamos reinseri-los
    # usando os objetos originais do heap (sem as palavras_chave injetadas)
    for filme in top_5:
        original = {'id': filme['id'], 'titulo': filme['titulo'], 'popularidade': filme['popularidade']}
        heap_populares.inserir(original)
        
    # Retorna o JSON para o frontend
    return jsonify({
        "status": "success",
        "data": top_5
    })

@app.route('/api/recomendacoes/<int:id_usuario>', methods=['GET'])
def get_recomendacoes(id_usuario):
    """
    Dada a identificação do utilizador, projeta o Grafo Bipartido
    para sugerir filmes baseados em filtragem colaborativa.
    """
    recomendacoes_tuplas = grafo_recomendacao.recomendar_para_utilizador(id_usuario)
    
    # Prepara a formatação da resposta esperada pelo app.js
    recomendacoes_formatadas = []
    for f_id, titulo in recomendacoes_tuplas:
        recomendacoes_formatadas.append({
            "id": f_id,
            "title": titulo,
            "palavras_chave": meta_keywords.get(f_id, '')
        })
        
    return jsonify({
        "status": "success",
        "data": recomendacoes_formatadas
    })

@app.route('/api/historico/<int:id_usuario>', methods=['GET'])
def get_historico(id_usuario):
    """
    Retorna a lista de IDs de filmes que o utilizador já assistiu.
    """
    # adj_utilizadores é um dicionário: chave = ID do utilizador, valor = set() com IDs dos filmes
    filmes_assistidos = grafo_recomendacao.adj_utilizadores.get(id_usuario, set())
    return jsonify({
        "status": "success",
        "data": list(filmes_assistidos)
    })

@app.route('/api/toggle_assistido', methods=['POST'])
def post_toggle_assistido():
    """
    Regista ou remove que um utilizador assistiu a um filme.
    Atualiza o Grafo na memória e persiste no ficheiro interacoes.csv.
    """
    dados = request.get_json()
    if not dados or 'id_usuario' not in dados or 'id_filme' not in dados:
        return jsonify({"status": "error", "message": "Dados inválidos. Requer id_usuario e id_filme."}), 400
        
    id_usuario = int(dados['id_usuario'])
    id_filme = int(dados['id_filme'])
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    caminho_interacoes = os.path.join(base_dir, 'data', 'interacoes.csv')
    
    filmes_do_usuario = grafo_recomendacao.adj_utilizadores.get(id_usuario, set())
    
    try:
        if id_filme in filmes_do_usuario:
            # 1. Remover do Grafo
            grafo_recomendacao.remover_aresta(id_usuario, id_filme)
            
            # 2. Remover do CSV
            df = pd.read_csv(caminho_interacoes)
            # Filtra removendo a linha exata
            df = df[~((df['id_usuario'] == id_usuario) & (df['id_filme'] == id_filme))]
            df.to_csv(caminho_interacoes, index=False)
            
            return jsonify({"status": "removido", "message": "Aresta removida com sucesso!"})
        else:
            # 1. Adicionar no Grafo
            grafo_recomendacao.adicionar_aresta(id_usuario, id_filme)
            
            # 2. Adicionar no CSV (append para ser mais rápido)
            with open(caminho_interacoes, 'a', encoding='utf-8') as f:
                f.write(f"{id_usuario},{id_filme},1\n")
                
            return jsonify({"status": "adicionado", "message": "Aresta adicionada com sucesso!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao processar: {str(e)}"}), 500

@app.route('/api/buscar', methods=['GET'])
def get_buscar():
    """
    Busca filmes pelo termo contido no título.
    Retorna no máximo 10 resultados.
    """
    termo = request.args.get('q', '').lower().strip()
    if not termo:
        return jsonify({"status": "success", "data": []})
        
    resultados = []
    # Itera no dicionário meta_filmes na RAM O(N)
    for id_filme, titulo in grafo_recomendacao.meta_filmes.items():
        if termo in str(titulo).lower():
            resultados.append({
                "id": id_filme, 
                "titulo": titulo,
                "palavras_chave": meta_keywords.get(id_filme, '')
            })
            if len(resultados) == 10:
                break
                
    return jsonify({
        "status": "success",
        "data": resultados
    })


if __name__ == '__main__':
    # Antes de subir o servidor web, dispara a carga pesada dos CSVs para a memória RAM
    carregar_dados()
    
    # Sobe o servidor na porta padrão do Flask
    app.run(debug=True, port=5000)
