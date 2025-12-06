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
  const [type, selectType] = useState("");
  const [massQueue, setMassQueue] = useState([]);
  const [error, setError] = useState("");

  // Atualiza selectedEntity se a prop `entity` mudar externamente
  useEffect(() => {
    if (entity && entity !== selectedEntity) {
      setSelectedEntity(entity);
      setValues({});
      setMassQueue([]);
      setError("");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entity]);

  // Resetar estados ao mudar de ação ou entidade selecionada
  useEffect(() => {
    setValues({});
    setMassQueue([]);
    setError("");
  }, [action, selectedEntity]);

  // Campos da entidade selecionada (fallback para array vazio)
  const fields = entities[selectedEntity] || [];

  function handleInputChange(e) {
    const { name, value } = e.target;
    setValues((s) => ({ ...s, [name]: value }));
    setError("");
  }

  function handleEntitySelect(e) {
    const newEntity = e.target.value;
    setSelectedEntity(newEntity);
    setValues({});
    setMassQueue([]);
    setError("");
    if (onEntityChange) onEntityChange(newEntity);
  }

  // Validação geral do formulário para add/update
  const isAddOrUpdate = ["add", "update"].includes(action);
  const isFormValid =
    !isAddOrUpdate ||
    fields.length === 0 ||
    fields.every((f) => {
      const v = values[f.id];
      return v !== undefined && String(v).trim() !== "";
    });

  // Adicionar à fila (massa) — torna seguro caso e seja undefined
  function addToQueue(e) {
    if (e && e.preventDefault) e.preventDefault();
    setError("");

    const hasEmpty = fields.some((f) => {
      const v = values[f.id];
      return v === undefined || String(v).trim() === "";
    });

    if (hasEmpty) {
      setError("Preencha todos os campos antes de adicionar à fila.");
      return;
    }

    // Formata linha na ordem correta (usar string vazia como fallback)
    const rowAsArray = fields.map((field) =>
      values[field.id] !== undefined ? values[field.id] : ""
    );

    setMassQueue((q) => [...q, rowAsArray]);
    setValues({});
  }

  // Envio do formulário (submit)
  function submitForm(e) {
    if (e && e.preventDefault) e.preventDefault();
    setError("");

    const payloadData = {};

    if (["add", "update"].includes(action)) {
      const missingFields = fields.filter((f) => {
        const v = values[f.id];
        return v === undefined || String(v).trim() === "";
      });

      if (missingFields.length > 0) {
        setError("Preencha todos os campos antes de executar a operação.");
        return;
      }

      fields.forEach((f) => {
        payloadData[f.id] = values[f.id];
      });
    } else if (["remove", "search"].includes(action)) {
      payloadData.id = values.id || "";
    } else if (action === "substring") {
      payloadData.termo = values.termo || "";
    } else if (action === "mass") {
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

  // Render do select de entidade (reaproveitável)
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
        {action !== "mass" && <option value="vendedor">Vendedor</option>}
        {action !== "mass" && <option value="gerente">Gerente</option>}
        {action !== "mass" && <option value="telefone">Telefone</option>}
      </select>
    </div>
  );

  // 1) ADD / UPDATE
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

        {error && <p className="text-red-600 mt-2">{error}</p>}

        <div style={{ marginTop: 20 }}>
          <button className="btn-primary" type="submit" disabled={!isFormValid}>
            {action === "add" ? "Adicionar" : "Atualizar"}
          </button>
        </div>
      </form>
    );
  }

  // 2) MASS LOAD
  if (action === "mass") {
    return (
      <div>
        {renderEntitySelect()}

        <div className="bg-gray-50 p-4 rounded border border-gray-200 mb-4">
          <h4 className="mb-2 font-bold text-gray-700">
            1. Preencha uma amostra:
          </h4>
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

        {error && <p className="text-red-600 mb-3">{error}</p>}

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

  // 3) REMOVE / SEARCH
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

  // 4) SUBSTRING
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

  if (action === "quantifiers") {
    return (
      <div className="flex flex-col gap-4">
        {/* Tipo de Quantificador */}
        <div className="flex flex-col">
          <label>Tipo de Quantificador</label>
          <select
            className="input"
            onChange={(e) =>
              setValues({ ...values, type: e.target.value.toLowerCase() })
            }
          >
            <option value="ANY">ANY</option>
            <option value="ALL">ALL</option>
          </select>
        </div>

        {/* Botão */}
        <button
          className="btn-primary"
          onClick={() =>
           onExecute({
              action:  "quantifier",
              entity,
              data: {}
            })
          }
        >
          Executar
        </button>
      </div>
    );
  }

  // 5) AÇÕES SIMPLES (INIT, REPORTS etc.)
  return (
    <div>
      <p className="mb-4 text-gray-600">
        Esta ação não requer parâmetros de entrada. Clique para processar.
      </p>
      <button
        className="btn-primary"
        onClick={() =>
          onExecute && onExecute({ action, entity: selectedEntity, data: {} })
        }
      >
        Executar {action}
      </button>
    </div>
  );
}
