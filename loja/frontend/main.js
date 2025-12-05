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
    // Adicionei os relacionamentos específicos
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
        const div = document.createElement('div');
        div.className = 'form-group'; // Classe do seu CSS
        div.innerHTML = `
            <label>${field.label}</label>
            <input type="${field.type}" id="inp-${field.id}" class="form-control" placeholder="${field.label}">
        `;
        container.appendChild(div);
    });

    if (currentAction === 'update') {
        const warning = document.createElement('p');
        warning.style.color = 'orange';
        warning.style.fontSize = '0.9em';
        warning.innerText = '* O primeiro campo será usado para encontrar o registro a ser atualizado.';
        container.prepend(warning);
    }
}

function renderSingleInput(id, placeholder) {
    const container = document.getElementById('dynamic-inputs');
    container.innerHTML = `
        <div class="form-group" style="grid-column: 1 / -1;">
            <label>${placeholder}</label>
            <input type="text" id="inp-${id}" class="form-control" placeholder="Digite aqui...">
        </div>
    `;
}

function handleSpecialActions(action, titleEl, subtitleEl) {
    const container = document.getElementById('dynamic-inputs');
    container.innerHTML = '';

    if (action === 'mass') {
        titleEl.innerText = 'Carga em Massa';
        subtitleEl.innerText = 'Inserir dados fictícios de teste.';
        container.innerHTML = '<p>Clique em executar para popular o banco.</p>';
    } 
    else if (action === 'substring') {
        titleEl.innerText = 'Busca por Nome (Modelo)';
        renderSingleInput('termo', 'Digite parte do nome...');
    }
    else if (action === 'init_db') {
        titleEl.innerText = 'Criar Tabelas';
        subtitleEl.innerText = 'Resetar ou Inicializar o Banco de Dados.';
    }
    else {
        titleEl.innerText = 'Consultas Avançadas';
        subtitleEl.innerText = 'Visualizar relatórios complexos.';
    }
}

// --- 5. COMUNICAÇÃO COM O BACKEND (Fetch) ---

document.getElementById('btn-execute').addEventListener('click', () => {
    const entity = document.getElementById('entity-select').value;
    const outputDiv = document.getElementById('output-content');
    const resultsArea = document.getElementById('results-area');

    // Coleta dados dos inputs (Automático)
    const data = {};
    document.querySelectorAll('[id^="inp-"]').forEach(input => {
        const key = input.id.replace('inp-', '');
        data[key] = input.value;
    });

    // Feedback de Carregamento
    resultsArea.classList.remove('hidden');
    outputDiv.innerHTML = 'Processando...';

    // O Payload segue estritamente o que seu controller.py espera
    const payload = {
        action: currentAction,
        entity: entity,
        data: data
    };

    fetch('/api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(json => {
        // AQUI ESTÁ O SEGREDO DA VISUALIZAÇÃO
        // Se for uma lista, desenha tabela. Se for objeto, mostra texto.
        if (Array.isArray(json)) {
            outputDiv.innerHTML = createTable(json);
        } else if (json.message) {
            outputDiv.innerHTML = `<div style="color: green; font-weight: bold;">${json.message}</div>`;
        } else if (json.error) {
            outputDiv.innerHTML = `<div style="color: red; font-weight: bold;">ERRO: ${json.error}</div>`;
        } else {
            outputDiv.innerText = JSON.stringify(json, null, 2);
        }
    })
    .catch(err => {
        outputDiv.innerHTML = `<div style="color: red;">Erro na requisição: ${err}</div>`;
    });
});

// --- 6. GERADOR DE TABELAS HTML (Visualização) ---
function createTable(data) {
    if (data.length === 0) return '<p>Nenhum dado encontrado.</p>';

    // Pega as chaves do primeiro objeto para fazer o cabeçalho
    const headers = Object.keys(data[0]);
    
    let html = '<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">';
    
    // Cabeçalho
    html += '<thead style="background-color: #2c3e50; color: white;"><tr>';
    headers.forEach(h => {
        html += `<th style="padding: 10px; border: 1px solid #ddd; text-transform: capitalize;">${h}</th>`;
    });
    html += '</tr></thead>';

    // Corpo
    html += '<tbody>';
    data.forEach(row => {
        html += '<tr>';
        headers.forEach(h => {
            html += `<td style="padding: 8px; border: 1px solid #ddd; text-align: center;">${row[h]}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table>';

    return html;
}