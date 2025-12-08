export const entities = {
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
        { id: 'data', label: 'Data (AAAA-MM-DD)', type: 'date' },
        { id: 'valor', label: 'Valor Total', type: 'number' }        
    ]
};
