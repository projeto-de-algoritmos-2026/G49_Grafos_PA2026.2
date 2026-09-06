# 🎬 GrafoFlix: Sistema Híbrido de Recomendação de Filmes e Séries

Este projeto consiste num *Motor de Recomendação* desenvolvido como trabalho final para a disciplina de *Projeto de Algoritmos*, do professor *Mauricio Serrano*.

O sistema utiliza uma abordagem *híbrida, combinando **Processamento de Linguagem Natural (PLN)* e *Teoria dos Grafos* para sugerir conteúdos de forma *semântica e colaborativa*.

---

## 🎯 Domínio Escolhido

*Área de Aplicação:*
Cinema e Televisão (Base de dados real de 1000 filmes do Kaggle).

### Objetivos Principais

### 1. Resolver o problema do Cold Start (Início Frio)

Sugerir filmes relevantes para novos utilizadores através da análise de similaridade textual das sinopses.

### 2. Filtragem Colaborativa

Sugerir conteúdos com base nos padrões de visualização e gostos similares da comunidade de utilizadores.

---

## 🧠 Tecnologias e Estruturas de Dados

### Linguagem e Stack

* *Back-end:* Python + Flask
* *Front-end:* Vanilla JavaScript, HTML e CSS

### Processamento de Linguagem Natural (PLN)

Extração de palavras-chave de sinopses reais utilizando o algoritmo *RAKE (Rapid Automatic Keyword Extraction)* com apoio da biblioteca *NLTK*.

### Estruturas de Dados Implementadas

#### Estrutura 1 — Grafo Ponderado de Similaridade Textual (Implementação Própria)

Liga filmes entre si.

O peso das arestas representa a intersecção de palavras-chave identificadas nas sinopses.

#### Estrutura 2 — Grafo Bipartido (Implementação Própria)

Modela as interações (*arestas) entre o conjunto de **Utilizadores* e o conjunto de *Filmes*.

#### Estrutura 3 — Max-Heap / Fila de Prioridade (Implementação Própria)

Ordena os filmes pelo seu grau de centralidade no *Grafo Ponderado* em tempo *O(log n), alimentando a vitrine de **Destaques* de forma eficiente.

#### Estrutura 4 — Árvore Geradora via Algoritmo de Prim (Futura Estrutura)

Adição planejada para o trabalho de *Projeto de Algoritmos*: uma Árvore Geradora, construída com o Algoritmo de Prim, sobre o próprio Grafo Ponderado de Similaridade (Estrutura 1). Ela conecta todos os filmes pelas ligações de maior similaridade textual entre si, sem ciclos, formando trilhas de descoberta de conteúdos parecidos.

---

## 👥 Integrantes do Grupo

| Integrante                       | GitHub                                         | Contribuição |
| -------------------------------- | ---------------------------------------------- | ------------ |
| Samuel Rodrigues Viana Lobo      | [@Samuelvlobo](https://github.com/Samuelvlobo) | Participação na definição e construção da estrutura do projeto, organização da arquitetura da solução e apoio na elaboração da documentação técnica.          |
| Gabriel Sampaio Fae              | [@Faehzin](https://github.com/Faehzin)         | Adaptação do projeto para a disciplina de Projeto de Algoritmos e desenvolvimento da Estrutura 4 (Árvore Geradora via Algoritmo de Prim).          |

---

## 📌 Resumo da Solução

O *GrafoFlix* combina *recomendação baseada em conteúdo* e *filtragem colaborativa* utilizando estruturas de grafos implementadas manualmente, permitindo gerar recomendações relevantes tanto para *novos utilizadores* quanto para utilizadores com histórico de interação.

## ⚙️ Como executar o projeto localmente

Para testar este MVP na sua máquina, siga os passos exatos abaixo:

1. **Ativar o ambiente virtual**:
   - No **Linux/Mac**:
   ```bash
   python -m venv venv/bin/activate
   ```
   - No **Windows**:
   ```bash
   venv\Scripts\activate
   ```

2. **Instalar dependências**:
   Com o ambiente ativado, instale os pacotes (Flask, Pandas, Rake-NLTK):
   ```bash
   pip install -r requirements.txt
   ```
   *Nota 1: talvez seja necessário fazer um override do pip, porque pode ser que o gerenciador de pacotes exija a instalação dos requisitos por ele ao invés do gerenciador pip. Basta executar: `pip install -r requirements.txt --break-system-packages`*
   *Nota 2: O NLTK precisa dos pacotes básicos de PLN. Se for a primeira vez, execute: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')" `*

3. **Iniciar o servidor (Back-end)**:
   Inicie a nossa API REST em Flask que vai carregar o Grafo e o Heap para a memória RAM:
   ```bash
   python src/back/api.py
   ```
   *Deixe este terminal aberto.*

4. **Abrir a Interface (Front-end)**:
   Como não usamos frameworks de Front-end, não precisamos de NPM. Basta abrir o ficheiro diretamente no seu navegador padrão (ou usar uma extensão como o Live Server):
   ```bash
   # No Linux, basta rodar noutro terminal:
   xdg-open src/front/index.html
   ```
5. **Criar um usuário**
   Para adicionar um usuário ao sistema, basta designar um número de ID ao usuário e escolher os filmes que o usuário já assistiu. Desta forma, os filmes mais similares ao gosto do usuário aparecerão primeiro. Assim, os tipo de usuário que podem ser adicionado são dois:
   Usuário com gosto pré-definido: para adicioná-lo, designe um ID de número menor ou igual a 50. Pois os usuários de 0 a 50 já tem gostos definidos.
   Usuário sem gosto pré-definido: para adicioná-lo, designe um ID de número maior que 50. 
