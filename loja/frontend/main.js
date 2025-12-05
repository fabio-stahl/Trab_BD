// --- 1. CONFIGURAÇÃO (O Cérebro da Interface) ---
// Mapeia quais campos cada entidade precisa. 
// Isso evita aquele monte de if/else com HTML misturado.
const entityFields = {
    'cliente': [
        { id: 'cpf', label: 'CPF (Somente Números)', type: 'number' },
        { id: 'nome', label: 'Nome Completo', type: 'text' },
        { id: 'endereco', label: 'Endereço', type: 'text' }
    ],
    'carro': [
        { id: 'chassi', label: 'Chassi', type: 'text' },
        { id: 'modelo', label: 'Modelo', type: 'text' },
        { id: 'cor', label: 'Cor (Opcional)', type: 'text' }
    ],
    'funcionario': [
        { id: 'matricula', label: 'Matrícula', type: 'number' },
        { id: 'nome', label: 'Nome', type: 'text' },
        { id: 'salario', label: 'Salário', type: 'number' }
    ],
    'gerente': [
        { id: 'matricula', label: 'Matrícula (Já existente)', type: 'number' },
        { id: 'vale_alimentacao', label: 'Vale Alimentação', type: 'number' }
    ],
    'vendedor': [
        { id: 'matricula', label: 'Matrícula (Já existente)', type: 'number' },
        { id: 'vale_transporte', label: 'Vale Transporte', type: 'number' }
    ],
    'telefone': [
        { id: 'numero', label: 'Número do Telefone', type: 'number' },
        { id: 'cpf', label: 'CPF do Dono', type: 'number' }
    ],
    'negociacao': [
        { id: 'matricula', label: 'Matrícula Vendedor', type: 'number' },
        { id: 'chassi', label: 'Chassi Carro', type: 'text' },
        { id: 'cpf', label: 'CPF Cliente', type: 'number' },
        { id: 'valor', label: 'Valor Total', type: 'number' },
        { id: 'data', label: 'Data (AAAA-MM-DD)', type: 'date' }
    ]
};

// --- 2. ESTADO GLOBAL ---
let currentAction = '';

// --- 3. LÓGICA DE NAVEGAÇÃO (Menu Lateral) ---
// Função chamada pelo onclick no HTML
function showSection(action) {
    currentAction = action;
    
    // Elementos da DOM
    const titleEl = document.getElementById('page-title');
    const subtitleEl = document.getElementById('page-subtitle');
    const entityGroup = document.getElementById('entity-selector-group');
    const interfaceContainer = document.getElementById('interface-container');
    const resultsArea = document.getElementById('results-area');
    
    // Reset visual
    interfaceContainer.classList.remove('hidden');
    resultsArea.classList.add('hidden');
    document.getElementById('output-content').innerHTML = '';

    // Lógica do Título e Inputs
    if (['add', 'update'].includes(action)) {
        titleEl.innerText = action === 'add' ? 'Adicionar Registro' : 'Atualizar Registro';
        subtitleEl.innerText = 'Selecione a tabela e preencha os dados.';
        entityGroup.classList.remove('hidden');
        renderEntityInputs(); // Desenha os inputs da entidade selecionada
    } 
    else if (['remove', 'search'].includes(action)) {
        titleEl.innerText = action === 'remove' ? 'Remover Registro' : 'Pesquisar Registro';
        subtitleEl.innerText = 'Informe o identificador (ID, CPF, Chassi ou Matrícula).';
        entityGroup.classList.remove('hidden');
        renderSingleInput('id', 'Identificador (PK)');
    }
    else {
        // Ações Especiais (Mass, Substring, Relatórios)
        entityGroup.classList.add('hidden');
        handleSpecialActions(action, titleEl, subtitleEl);
    }
}

// --- 4. RENDERIZAÇÃO DE INPUTS (Dinâmico) ---

// Chamado quando muda o <select> ou clica em Add/Update
function updateFormFields() {
    if (['add', 'update'].includes(currentAction)) {
        renderEntityInputs();
    }
}

function renderEntityInputs() {
    const entity = document.getElementById('entity-select').value;
    const container = document.getElementById('dynamic-inputs');
    container.innerHTML = ''; // Limpa inputs antigos

    const fields = entityFields[entity] || [];
    
    if (fields.length === 0) {
        container.innerHTML = '<p>Selecione uma entidade válida.</p>';
        return;
    }

    fields.forEach(field => {
        const input = document.createElement('input');
        input.id = field.id;
        input.type = field.type;
        input.placeholder = field.label;
        input.required = true; // Ensure the field is required

        // Add input validation for numbers
        if (field.type === 'number') {
            input.addEventListener('input', function() {
                if (this.value < 0) {
                    this.setCustomValidity('O valor não pode ser negativo.');
                } else {
                    this.setCustomValidity('');
                }
            });
        }

        container.appendChild(input);
    });
}

/* Compatibilidade com index.html (wrappers) */
function handleMenuClick(action) { showSection(action); }
function renderInputs() { renderEntityInputs(); }

/* Renderiza um único input (para search/remove por ID) */
function renderSingleInput(id, label) {
    const container = document.getElementById('dynamic-inputs');
    container.innerHTML = '';
    const input = document.createElement('input');
    input.id = id;
    input.type = 'text';
    input.placeholder = label;
    input.required = true;
    container.appendChild(input);
}

/* Trata ações especiais (mass, substring, advanced, quantifiers, grouping) */
function handleSpecialActions(action, titleEl, subtitleEl) {
    document.getElementById('dynamic-inputs').innerHTML = '';
    const subtitleMap = {
        'mass': 'Executa carga em massa de dados dummy.',
        'substring': 'Digite o termo para buscar (substring).',
        'advanced': 'Executa relatório avançado (JOINs).',
        'quantifiers': 'Executa consulta com quantificadores.',
        'grouping': 'Relatório de vendas por vendedor.'
    };
    titleEl.innerText = {
        'mass': 'Carga em Massa',
        'substring': 'Busca por Substring',
        'advanced': 'Relatório Avançado',
        'quantifiers': 'Consultas com Quantificadores',
        'grouping': 'Agrupamento e Relatórios'
    }[action] || 'Operação';
    subtitleEl.innerText = subtitleMap[action] || '';

    // Se for substring, adiciona um input de termo
    if (action === 'substring') {
        const container = document.getElementById('dynamic-inputs');
        const input = document.createElement('input');
        input.id = 'termo';
        input.type = 'text';
        input.placeholder = 'Termo de busca';
        input.required = true;
        container.appendChild(input);
    }

    // Mostra a área de interface e botão executar
    document.getElementById('interface-container').classList.remove('hidden');
}

/* Ajuste seguro do escapeHtml */
function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return '';
    const s = String(unsafe);
    return s
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/* Melhor tratamento de fetch: sempre retorna objeto (ou lança um erro claro) */
async function fetchData(url, method, data) {
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json().catch(() => ({ error: 'Resposta JSON inválida' }));

        if (!response.ok) {
            // inclui mensagem do servidor quando disponível
            const msg = result && result.error ? result.error : `${response.status} ${response.statusText}`;
            return { error: msg };
        }
        return result;
    } catch (error) {
        console.error('Erro ao enviar dados:', error);
        return { error: String(error) };
    }
}

/* Executa a ação atual: monta payload e chama /handler/ */
async function executeAction() {
    const entityGroupVisible = !document.getElementById('entity-selector-group').classList.contains('hidden');
    const entity = entityGroupVisible ? document.getElementById('entity-select').value : null;
    const data = {};

    // coleta inputs dinamicamente
    document.querySelectorAll('#dynamic-inputs input').forEach(inp => {
        data[inp.id] = inp.value;
    });

    const payload = { action: currentAction, entity: entity, data: data };
    const res = await fetchData('/handler/', 'POST', payload);

    if (!res) {
        displayOutput({ error: 'Sem resposta do servidor' });
        return;
    }
    displayOutput(res);
}

/* Renderiza a saída (objeto, mensagem ou lista) */
function displayOutput(response) {
    const resultsArea = document.getElementById('results-area');
    const output = document.getElementById('output-content');
    output.innerHTML = '';

    if (response === null) {
        output.innerText = 'Resposta vazia';
    } else if (Array.isArray(response) && response.length > 0) {
        // cria tabela quando array de objetos
        createTable(response);
        resultsArea.classList.remove('hidden');
    } else if (Array.isArray(response) && response.length === 0) {
        output.innerText = 'Nenhum resultado.';
        resultsArea.classList.remove('hidden');
    } else if (typeof response === 'object') {
        if (response.error) {
            output.innerHTML = `<div class="error">Erro: ${escapeHtml(response.error)}</div>`;
        } else if (response.message) {
            output.innerHTML = `<div class="message">${escapeHtml(response.message)}</div>`;
        } else {
            // exibe objeto formatado
            const pre = document.createElement('pre');
            pre.innerText = JSON.stringify(response, null, 2);
            output.appendChild(pre);
        }
        resultsArea.classList.remove('hidden');
    } else {
        output.innerText = String(response);
        resultsArea.classList.remove('hidden');
    }
}

/* Hook inicial para botões e execução */
document.addEventListener('DOMContentLoaded', () => {
    // botao executar
    const btn = document.getElementById('btn-execute');
    if (btn) btn.addEventListener('click', executeAction);

    // Inicialmente esconder interface
    document.getElementById('interface-container').classList.add('hidden');
    document.getElementById('results-area').classList.add('hidden');
});