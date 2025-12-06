// src/components/DynamicForm.jsx
import React, { useState, useEffect } from "react";
import { entities } from "../data/entities";

export default function DynamicForm({
  action,
  entity,
  onEntityChange,
  onExecute,
}) {
  const [selectedEntity, setSelectedEntity] = useState(entity || "cliente");
  const [values, setValues] = useState({});

  // Estado para Manipulação em Massa (Lista de itens a inserir)
  const [massQueue, setMassQueue] = useState([]);

  // Estado para mensagens de erro de validação
  const [error, setError] = useState("");

  // Atualiza campos quando a entidade muda
  const fields = entities[selectedEntity] || [];

  // Resetar estados ao mudar de ação ou entidade
  useEffect(() => {
    setValues({});
    setMassQueue([]);
    setError("");
  }, [action, selectedEntity]);

  function handleInputChange(e) {
    const { name, value } = e.target;
    setValues((s) => ({ ...s, [name]: value }));
    // limpamos o erro assim que o usuário começar a digitar
    setError("");
  }

  function handleEntitySelect(e) {
    const newEntity = e.target.value;
    setSelectedEntity(newEntity);
    setValues({});
    setMassQueue([]); // Limpa a fila se trocar a tabela
    setError("");
    if (onEntityChange) onEntityChange(newEntity);
  }

  // --- helper para validar se todos os campos estão preenchidos ---
  const isAddOrUpdate = ["add", "update"].includes(action);
  const isFormValid =
    !isAddOrUpdate ||
    fields.length === 0 ||
    fields.every((f) => {
      const v = values[f.id];
      return v !== undefined && String(v).trim() !== "";
    });

  // --- Lógica para Adicionar à Fila (Massa) ---
  function addToQueue(e) {
    e.preventDefault();
    setError("");

    // Para carga em massa: também podemos exigir todos os campos preenchidos
    const hasEmpty = fields.some((f) => {
      const v = values[f.id];
      return v === undefined || String(v).trim() === "";
    });

    if (hasEmpty) {
      setError("Preencha todos os campos antes de adicionar à fila.");
      return;
    }

    // Transforma o objeto {cpf: 1, nome: "A"} em array [1, "A"] na ordem correta
    const rowAsArray = fields.map((field) => values[field.id] || "");

    setMassQueue([...massQueue, rowAsArray]);
    setValues({}); // Limpa o formulário para o próximo
  }

  // --- Lógica de Envio (Submit) ---
  function submitForm(e) {
    e && e.preventDefault();
    setError("");

    const payloadData = {};

    // ✅ Validação para ADD / UPDATE: não deixa enviar se tiver campo vazio
    if (["add", "update"].includes(action)) {
      const missingFields = fields.filter((f) => {
        const v = values[f.id];
        return v === undefined || String(v).trim() === "";
      });

      if (missingFields.length > 0) {
        setError("Preencha todos os campos antes de executar a operação.");
        return; // trava o envio
      }

      fields.forEach((f) => {
        payloadData[f.id] = values[f.id];
      });
    } else if (["remove", "search"].includes(action)) {
      payloadData.id = values.id || "";
    } else if (action === "substring") {
      payloadData.termo = values.termo || "";
    } else if (action === "mass") {
      // O Controller espera chaves no plural (clientes, carros...)
      const pluralMap = {
        cliente: "clientes",
        carro: "carros",
        funcionario: "funcionarios",
        negociacao: "negociacoes",
      };

      if (!massQueue.length) {
        setError("Adicione pelo menos um item à fila antes de executar.");
        return;
      }

      const key = pluralMap[selectedEntity] || selectedEntity + "s";
      payloadData[key] = massQueue;
    } else {
      Object.assign(payloadData, values);
    }

    if (onExecute) {
      onExecute({
        action,
        entity: selectedEntity,
        data: payloadData,
      });
    }
  }

  // --- RENDERIZAÇÃO: Select de Tabela (Comum a Add, Update, Mass) ---
  const renderEntitySelect = () => (
    <div className="form-group" style={{ marginBottom: 16 }}>
      <label className="text-gray-700 font-bold mb-2">Tabela Alvo:</label>
      <select
        value={selectedEntity}
        onChange={handleEntitySelect}
        className="form-control"
      >
        <option value="cliente">Cliente</option>
        <option value="carro">Carro</option>
        <option value="funcionario">Funcionário</option>
        <option value="negociacao">Negociação</option>
        {/* Vendedor/Gerente/Telefone geralmente não tem mass load no seu controller, mas mantivemos aqui */}
        {action !== "mass" && <option value="vendedor">Vendedor</option>}
        {action !== "mass" && <option value="gerente">Gerente</option>}
        {action !== "mass" && <option value="telefone">Telefone</option>}
      </select>
    </div>
  );

  // --- 1. VIEW: ADD / UPDATE ---
  if (["add", "update"].includes(action)) {
    return (
      <form onSubmit={submitForm}>
        {renderEntitySelect()}

        <div className="input-grid">
          {fields.map((f) => (
            <div className="form-group" key={f.id}>
              <label>{f.label}</label>
              <input
                name={f.id}
                type={f.type}
                className="form-control"
                placeholder={f.label}
                value={values[f.id] || ""}
                onChange={handleInputChange}
              />
            </div>
          ))}
        </div>

        {error && (
          <p className="text-red-600 mt-2">
            {error}
          </p>
        )}

        <div style={{ marginTop: 20 }}>
          <button
            className="btn-primary"
            type="submit"
            disabled={!isFormValid}
          >
            {action === "add" ? "Adicionar" : "Atualizar"}
          </button>
        </div>
      </form>
    );
  }

  // --- 2. VIEW: MASS LOAD ---
  if (action === "mass") {
    return (
      <div>
        {renderEntitySelect()}

        <div className="bg-gray-50 p-4 rounded border border-gray-200 mb-4">
          <h4 className="mb-2 font-bold text-gray-700">1. Preencha uma amostra:</h4>
          <div className="input-grid">
            {fields.map((f) => (
              <div className="form-group" key={f.id}>
                <label>{f.label}</label>
                <input
                  name={f.id}
                  type={f.type}
                  className="form-control"
                  placeholder={f.label}
                  value={values[f.id] || ""}
                  onChange={handleInputChange}
                />
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={addToQueue}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
          >
            + Adicionar à Fila
          </button>
        </div>

        {error && (
          <p className="text-red-600 mb-3">
            {error}
          </p>
        )}

        {/* Preview da Fila */}
        {massQueue.length > 0 && (
          <div className="mb-6">
            <h4 className="mb-2 font-bold text-gray-700">
              2. Itens na Fila ({massQueue.length}):
            </h4>
            <div className="overflow-x-auto border rounded">
              <table className="w-full text-sm text-left">
                <thead className="bg-gray-200 text-gray-700">
                  <tr>
                    {fields.map((f) => (
                      <th key={f.id} className="p-2">
                        {f.label}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {massQueue.map((row, idx) => (
                    <tr key={idx} className="border-b">
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} className="p-2">
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {massQueue.length > 0 && (
          <button className="btn-primary w-full" onClick={submitForm}>
            Executar Carga em Massa ({massQueue.length} itens)
          </button>
        )}
      </div>
    );
  }

  // --- 3. VIEW: REMOVE / SEARCH ---
  if (["remove", "search"].includes(action)) {
    return (
      <form onSubmit={submitForm}>
        {renderEntitySelect()}
        <div className="form-group" style={{ gridColumn: "1 / -1" }}>
          <label>Identificador (CPF, Chassi, Matrícula ou ID)</label>
          <input
            name="id"
            className="form-control"
            placeholder="Digite o ID..."
            value={values.id || ""}
            onChange={handleInputChange}
          />
        </div>
        <div style={{ marginTop: 20 }}>
          <button className="btn-primary" type="submit">
            Executar
          </button>
        </div>
      </form>
    );
  }

  // --- 4. VIEW: SUBSTRING ---
  if (action === "substring") {
    return (
      <form onSubmit={submitForm}>
        {renderEntitySelect()}
        <div className="form-group" style={{ gridColumn: "1 / -1" }}>
          <label>Termo de Busca</label>
          <input
            name="termo"
            className="form-control"
            placeholder="Digite parte do nome/modelo..."
            value={values.termo || ""}
            onChange={handleInputChange}
          />
        </div>
        <div style={{ marginTop: 20 }}>
          <button className="btn-primary" type="submit">
            Pesquisar
          </button>
        </div>
      </form>
    );
  }

  // --- 5. VIEW: AÇÕES SIMPLES (INIT, REPORTS) ---
  return (
    <div>
      <p className="mb-4 text-gray-600">
        Esta ação não requer parâmetros de entrada. Clique para processar.
      </p>
      <button
        className="btn-primary"
        onClick={() => onExecute({ action, entity: selectedEntity, data: {} })}
      >
        Executar {action}
      </button>
    </div>
  );
}
