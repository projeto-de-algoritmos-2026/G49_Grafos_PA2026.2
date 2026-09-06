import os
import pandas as pd
import numpy as np
import random
from rake_nltk import Rake

# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO:
# 1. pip install rake-nltk pandas
# 2. python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
# ==============================================================================

def gerar_dados_reais():
    # Caminhos
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(base_dir, 'data')
    
    dataset_bruto_path = os.path.join(data_dir, 'dataset_bruto.csv')
    filmes_csv_path = os.path.join(data_dir, 'filmes.csv')
    usuarios_csv_path = os.path.join(data_dir, 'usuarios.csv')
    interacoes_csv_path = os.path.join(data_dir, 'interacoes.csv')
    
    print(f"Lendo base bruta: {dataset_bruto_path}")
    
    # 1. PROCESSAMENTO DOS FILMES
    # Tenta ler o CSV, usando on_bad_lines para pular possiveis erros de formatação do Kaggle
    df_bruto = pd.read_csv(dataset_bruto_path, on_bad_lines='skip')
    
    # Mapear as colunas baseadas no padrão encontrado (id, title, overview, popularity)
    colunas_necessarias = ['id', 'title', 'overview', 'popularity']
    
    # Verifica se as colunas existem
    for col in colunas_necessarias:
        if col not in df_bruto.columns:
            print(f"Erro: Coluna '{col}' não encontrada no dataset bruto.")
            return

    # Filtra colunas
    df_filmes = df_bruto[colunas_necessarias].copy()
    
    # Trata valores nulos (NaN)
    df_filmes.dropna(subset=['id', 'title', 'overview'], inplace=True)
    
    # Pega uma amostra de 1000 filmes (para não pesar o processamento do Rake)
    # Se tiver menos de 1000, pega todos. O random_state garante que sempre pegaremos os mesmos 1000
    n_amostra = min(1000, len(df_filmes))
    df_filmes = df_filmes.sample(n=n_amostra, random_state=42).reset_index(drop=True)
    
    print(f"Iniciando PLN em {n_amostra} filmes...")
    
    # Configura o Rake para o idioma da base (inglês)
    r = Rake(language='english')
    
    palavras_chave_lista = []
    
    for idx, row in df_filmes.iterrows():
        sinopse = str(row['overview'])
        r.extract_keywords_from_text(sinopse)
        top_keywords = r.get_ranked_phrases()[:5]
        palavras_chave_lista.append("; ".join(top_keywords))
        
        # Apenas para mostrar progresso
        if (idx + 1) % 200 == 0:
            print(f"Processado: {idx + 1}/{n_amostra}")
            
    df_filmes['palavras_chave'] = palavras_chave_lista
    
    # Renomeia para o padrão do projeto
    df_filmes.rename(columns={
        'id': 'id_filme', 
        'title': 'titulo', 
        'popularity': 'popularidade'
    }, inplace=True)
    
    # Ajusta o tipo do ID
    df_filmes['id_filme'] = df_filmes['id_filme'].astype(int)
    
    # Salva filmes.csv apenas com as colunas finais
    df_filmes_final = df_filmes[['id_filme', 'titulo', 'palavras_chave', 'popularidade']]
    df_filmes_final.to_csv(filmes_csv_path, index=False, encoding='utf-8')
    print(f"Salvo: {filmes_csv_path}")

    # 2. GERAÇÃO DE USUÁRIOS
    num_usuarios = 50
    print(f"Gerando {num_usuarios} usuários mockados...")
    
    df_usuarios = pd.DataFrame({
        'id_usuario': range(1, num_usuarios + 1),
        'nome': [f"Usuário {i}" for i in range(1, num_usuarios + 1)]
    })
    df_usuarios.to_csv(usuarios_csv_path, index=False, encoding='utf-8')
    print(f"Salvo: {usuarios_csv_path}")

    # 3. GERAÇÃO DE INTERAÇÕES (ARESTAS)
    print("Gerando arestas do Grafo (Interações)...")
    
    lista_ids_filmes = df_filmes_final['id_filme'].tolist()
    interacoes = []
    
    # Seed para garantir a reprodutibilidade das interações
    random.seed(42)
    
    for user_id in df_usuarios['id_usuario']:
        # Sorteia quantos filmes o usuário assistiu (entre 10 e 30)
        num_filmes_assistidos = random.randint(10, 30)
        
        # Sorteia QUAIS filmes da amostra de 1000 ele assistiu, sem repetição
        filmes_assistidos = random.sample(lista_ids_filmes, num_filmes_assistidos)
        
        for filme_id in filmes_assistidos:
            interacoes.append({
                'id_usuario': user_id,
                'id_filme': filme_id,
                'assistiu': 1
            })
            
    df_interacoes = pd.DataFrame(interacoes)
    df_interacoes.to_csv(interacoes_csv_path, index=False, encoding='utf-8')
    print(f"Geradas {len(df_interacoes)} interações.")
    print(f"Salvo: {interacoes_csv_path}")
    
    print("\nETL Finalizado com Sucesso! Os 3 CSVs do Grafo estão prontos.")

if __name__ == "__main__":
    gerar_dados_reais()
