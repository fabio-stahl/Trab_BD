// Estado da Aplicação
let currentSection = '';

// Elementos DOM
const titleEl = document.getElementById('page-title');
const subtitleEl = document.getElementById('page-subtitle');
const entityGroup = document.getElementById('entity-selector-group');
const dynamicInputs = document.getElementById('dynamic-inputs');
const actionArea = document.getElementById('action-area');
const resultsArea = document.getElementById('results-area');
const outputContent = document.getElementById('output-content');
const btnExecute = document.getElementById('btn-execute');

// Mapeamento de Configurações por Seção
const sections = {
    'add': { title: 'Adicionar Dados', subtitle: 'Insira novos registros no banco.', showEntity: true },
    'remove': { title: 'Remover Dados', subtitle: 'Exclua registros por ID ou Chave.', showEntity: true },
    'update': { title: 'Atualizar Dados', subtitle: 'Modifique registros existentes.', showEntity: true },
    'search': { title: 'Pesquisar Dados', subtitle: 'Busque registros específicos.', showEntity: true },
    'mass': { title: 'Manipulação em Massa', subtitle: 'Inserção de múltiplos dados (Dummy Data).', showEntity: false },
    'substring': { title: 'Busca por Substring', subtitle: 'Encontre carros por parte do nome.', showEntity: false },
    'advanced': { title: 'Consultas Avançadas', subtitle: 'Joins e Agrupamentos complexos.', showEntity: false },
    'quantifiers': { title: 'Cálculo Relacional', subtitle: 'Consultas com ANY / ALL.', showEntity: false },
    'grouping': { title: 'Relatórios Gerenciais', subtitle: 'Agrupamento, Ordenação e Recursão.', showEntity: false },
    'triggers': { title: 'Gatilhos (Triggers)', subtitle: 'Inicializar validações de banco.', showEntity: false },
};

// 1. Função chamada ao clicar no Menu Lateral
function showSection(sectionKey) {
    currentSection = sectionKey;
    const config = sections[sectionKey];

    // Atualiza Textos
    titleEl.innerText = config.title;
    subtitleEl.innerText = config.subtitle;

    // Reseta Interface
    resultsArea.classList.add('hidden');
    outputContent.innerText = '';
    
    // Mostra/Esconde Seletor de Entidade
    if (config.showEntity) {
        entityGroup.classList.remove('hidden');
        updateFormFields(); // Gera os inputs baseados na entidade padrão
    } else {
        entityGroup.classList.add('hidden');
        renderSpecificInputs(sectionKey);
    }

    actionArea.classList.remove('hidden');
}

// 2. Renderiza inputs para casos de CRUD (Entidades)
function updateFormFields() {
    const entity = document.getElementById('entity-select').value;
    let html = '';

    if (currentSection === 'add') {
        if (entity === 'cliente') {
            html += `<input id="inp-cpf" placeholder="CPF (Numérico)">`;
            html += `<input id="inp-nome" placeholder="Nome Completo">`;
            html += `<input id="inp-end" placeholder="Endereço">`;
        } else if (entity === 'carro') {
            html += `<input id="inp-chassi" placeholder="Chassi">`;
            html += `<input id="inp-modelo" placeholder="Modelo">`;
            html += `<input id="inp-cor" placeholder="Cor (Padrão: Preto)">`;
        } else if (entity === 'negociacao') {
            html += `<input id="inp-mat" placeholder="Matrícula Func.">`;
            html += `<input id="inp-chassi" placeholder="Chassi Carro">`;
            html += `<input id="inp-cpf" placeholder="CPF Cliente">`;
            html += `<input id="inp-val" placeholder="Valor Total">`;
            html += `<input id="inp-data" type="date">`;
        }
    } 
    else if (currentSection === 'remove' || currentSection === 'search') {
        html += `<input id="inp-id" placeholder="ID Chave Primária (CPF, Chassi ou ID)">`;
    }

    dynamicInputs.innerHTML = html;
}

// 3. Renderiza inputs para casos Específicos (Não-CRUD)
function renderSpecificInputs(key) {
    let html = '';
    
    if (key === 'substring') {
        html += `<input id="inp-termo" placeholder="Digite parte do nome do Modelo...">`;
    } else if (key === 'mass') {
        html += `<p>Esta ação irá inserir 5 Carros e 5 Clientes de teste automaticamente.</p>`;
    } else {
        html += `<p>Clique em executar para rodar a consulta SQL definida no backend.</p>`;
    }

    dynamicInputs.innerHTML = html;
}

// 4. Lógica de Envio para o Django
btnExecute.addEventListener('click', () => {
    // Coleta dados possíveis
    const payload = {
        action: currentSection,
        entity: document.getElementById('entity-select').value,
        data: {}
    };

    // Coleta valores dos inputs se existirem
    const inputs = dynamicInputs.querySelectorAll('input');
    inputs.forEach(input => {
        const key = input.id.replace('inp-', ''); // ex: inp-nome vira 'nome'
        payload.data[key] = input.value;
    });

    // Feedback visual
    outputContent.innerText = "Processando...";
    resultsArea.classList.remove('hidden');

    // Fetch API
    fetch('/api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        // Formata o JSON bonito
        outputContent.innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
        outputContent.innerText = "Erro na requisição: " + err;
    });
});