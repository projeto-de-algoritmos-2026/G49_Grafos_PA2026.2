document.addEventListener('DOMContentLoaded', () => {
    // --- URLs da API Flask ---
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- State ---
    let currentUser = null;
    let popularesData = [];
    let userHistory = [];

    // --- DOM Elements ---
    const loginContainer = document.getElementById('login-container');
    const userInfo = document.getElementById('user-info');
    const userIdInput = document.getElementById('user-id');
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const welcomeMessage = document.getElementById('welcome-message');
    
    const rowPopular = document.getElementById('row-popular');
    
    const sectionConnected = document.getElementById('section-connected');
    const rowConnected = document.getElementById('row-connected');
    const instructionMsg = document.getElementById('instruction-msg');
    
    const searchBar = document.getElementById('searchBar');

    // --- Render Functions ---
    function renderCards(container, data, isLoggedIn = false) {
        container.innerHTML = '';
        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';
            
            const idFilme = item.id_filme || item.id;
            
            const titleSpan = document.createElement('span');
            titleSpan.textContent = item.titulo || item.title;
            card.appendChild(titleSpan);
            
            if (item.palavras_chave) {
                const tagsContainer = document.createElement('div');
                tagsContainer.className = 'tags-container';
                
                const tags = item.palavras_chave.split(';').map(t => t.trim()).filter(t => t.length > 0).slice(0, 3);
                tags.forEach(tagText => {
                    const tag = document.createElement('span');
                    tag.className = 'tag';
                    tag.textContent = tagText;
                    tagsContainer.appendChild(tag);
                });
                card.appendChild(tagsContainer);
            }
            
            if (isLoggedIn) {
                const btn = document.createElement('button');
                btn.className = 'btn-assisti';
                
                if (userHistory.includes(idFilme)) {
                    btn.textContent = '❌ Remover';
                    btn.classList.add('btn-remover');
                } else {
                    btn.textContent = '✔️ Assistir';
                    btn.classList.remove('btn-remover');
                }
                
                btn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    await handleToggle(btn, idFilme);
                });
                card.appendChild(btn);
            }
            
            container.appendChild(card);
        });
    }

    // --- API Calls ---
    async function carregarPopulares() {
        try {
            const response = await fetch(`${API_BASE_URL}/populares`);
            if (!response.ok) throw new Error('Erro ao buscar filmes populares');
            
            const json = await response.json();
            popularesData = json.data;
            
            // Renderiza na tela sem interatividade (pois o utilizador ainda não fez login)
            renderCards(rowPopular, popularesData, false);
        } catch (error) {
            console.error('Falha na API (Populares):', error);
            rowPopular.innerHTML = '<p class="info-msg" style="color: red;">Erro ao carregar os filmes. O servidor Flask está a correr?</p>';
        }
    }

    async function buscarRecomendacoes() {
        if (!currentUser) return;
        
        try {
            // Remove a mensagem de instrução
            instructionMsg.style.display = 'none';
            // Mostra mensagem de carregamento (opcional, mas bom para UX)
            rowConnected.innerHTML = '<p class="info-msg">O Grafo está a calcular as afinidades...</p>';

            const response = await fetch(`${API_BASE_URL}/recomendacoes/${currentUser}`);
            if (!response.ok) throw new Error('Erro ao buscar recomendações do Grafo Bipartido');
            
            const json = await response.json();
            const recomendacoesData = json.data;
            
            if (recomendacoesData.length === 0) {
                // Caso de Cold Start (Utilizador sem arestas no grafo)
                instructionMsg.textContent = "Não encontramos interações suficientes! Clique num filme popular acima para vermos o que os utilizadores com gostos parecidos estão a assistir!";
                instructionMsg.style.display = 'block';
                rowConnected.innerHTML = '';
                rowConnected.appendChild(instructionMsg);
            } else {
                // Renderiza os filmes recomendados com sucesso
                renderCards(rowConnected, recomendacoesData, false);
            }
            
        } catch (error) {
            console.error('Falha na API (Recomendações):', error);
            rowConnected.innerHTML = '<p class="info-msg" style="color: red;">Erro ao contactar o servidor.</p>';
        }
    }

    async function carregarHistorico(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/historico/${userId}`);
            if (response.ok) {
                const json = await response.json();
                userHistory = json.data || [];
            }
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }

    // --- Handlers ---
    async function handleLogin() {
        const userId = userIdInput.value.trim();
        if (userId) {
            currentUser = parseInt(userId);
            
            // Busca o histórico antes de renderizar
            await carregarHistorico(currentUser);
            
            loginContainer.classList.add('hidden');
            welcomeMessage.textContent = `Logado como Utilizador ${currentUser}`;
            userInfo.classList.remove('hidden');
            
            // Mostra a fileira 2 (Conectados)
            sectionConnected.classList.remove('hidden');

            // Torna a fileira 1 interativa (mostra os botões)
            renderCards(rowPopular, popularesData, true);
            
            // Busca as recomendações iniciais se existirem interações
            buscarRecomendacoes();
        }
    }

    function handleLogout() {
        currentUser = null;
        userHistory = [];
        userIdInput.value = '';
        
        userInfo.classList.add('hidden');
        loginContainer.classList.remove('hidden');
        
        // Esconde a fileira 2
        sectionConnected.classList.add('hidden');

        // Volta a mostrar o texto de instrução original
        instructionMsg.textContent = "Clique em algum filme popular acima para vermos o que os usuários com gosto parecido estão assistindo.";
        instructionMsg.style.display = 'block';
        rowConnected.innerHTML = '';
        rowConnected.appendChild(instructionMsg);

        // Tira interatividade da fileira 1
        renderCards(rowPopular, popularesData, false);
    }

    async function handleToggle(btn, idFilme) {
        if (!currentUser) return;

        btn.disabled = true;
        
        try {
            const response = await fetch(`${API_BASE_URL}/toggle_assistido`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id_usuario: currentUser, id_filme: idFilme })
            });
            
            if (response.ok) {
                const json = await response.json();
                
                if (json.status === 'adicionado') {
                    userHistory.push(idFilme);
                    btn.textContent = '❌ Remover';
                    btn.classList.add('btn-remover');
                } else if (json.status === 'removido') {
                    userHistory = userHistory.filter(id => id !== idFilme);
                    btn.textContent = '✔️ Assistir';
                    btn.classList.remove('btn-remover');
                }
                btn.disabled = false;
                
                // Limpar HTML primeiro como pedido e engatilhar recalculo
                rowConnected.innerHTML = '<p class="info-msg">O Grafo está a recalcular as afinidades...</p>';
                buscarRecomendacoes();
            } else {
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Erro ao registar interação:', error);
            btn.disabled = false;
        }
    }

    // --- Init ---
    // Assim que a página carrega, vai buscar os dados ao Heap
    carregarPopulares();

    // Events
    loginBtn.addEventListener('click', handleLogin);
    userIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    logoutBtn.addEventListener('click', handleLogout);
    
    if (searchBar) {
        searchBar.addEventListener('input', async (e) => {
            const termo = e.target.value.trim();
            if (termo.length > 2) {
                try {
                    const response = await fetch(`${API_BASE_URL}/buscar?q=${termo}`);
                    if (response.ok) {
                        const json = await response.json();
                        renderCards(rowPopular, json.data, !!currentUser);
                    }
                } catch (error) {
                    console.error('Erro na busca:', error);
                }
            } else if (termo.length === 0) {
                renderCards(rowPopular, popularesData, !!currentUser);
            }
        });
    }
});
