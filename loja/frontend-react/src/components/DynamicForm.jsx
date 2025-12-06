// src/components/DynamicForm.jsx
import React, { useState } from "react";
import { entities } from "../data/entities";

/**
 * props:
 * - action: currentAction (add, update, remove, search, ...)
 * - entity: selected entity (cliente, carro...)
 * - onExecute(payload) => executes request
 * - onEntityChange(entity) optional
 */
export default function DynamicForm({
  action,
  entity,
  onEntityChange,
  onExecute,
}) {
  const [selectedEntity, setSelectedEntity] = useState(entity || "cliente");
  const [values, setValues] = useState({});
  const fields = entities[selectedEntity] || [];

  function handleInputChange(e) {
    const { name, value } = e.target;
    setValues((s) => ({ ...s, [name]: value }));
  }

  function handleEntitySelect(e) {
    setSelectedEntity(e.target.value);
    setValues({});
    if (onEntityChange) onEntityChange(e.target.value);
  }

  function submitForm(e) {
    e && e.preventDefault();
    // If action is remove/search, use special key "id"
    const payloadData = {};
    if (["remove", "search"].includes(action)) {
      payloadData.id = values.id || "";
    } else if (["add", "update"].includes(action)) {
      // collect all fields for the selected entity
      fields.forEach((f) => {
        payloadData[f.id] = values[f.id] || "";
      });
    } else if (action === "substring") {
      payloadData.termo = values.termo || "";
    } else {
      // other actions might not need data
      Object.assign(payloadData, values);
    }

    onExecute &&
      onExecute({ action, entity: selectedEntity, data: payloadData });
  }

  // Render helpers
  if (["add", "update"].includes(action)) {
    return (
      <form onSubmit={submitForm}>
        <div className="form-group" style={{ marginBottom: 16 }}>
          <label>Tabela Alvo:</label>
          <select value={selectedEntity} onChange={handleEntitySelect}>
            <option value="cliente">Cliente</option>
            <option value="carro">Carro</option>
            <option value="vendedor">Vendedor</option>
            <option value="gerente">Gerente</option>
          </select>
        </div>

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

        <div style={{ marginTop: 20 }}>
          <button className="btn-primary" type="submit">
            Executar
          </button>
        </div>
      </form>
    );
  }

  if (["remove", "search"].includes(action)) {
    return (
      <form onSubmit={submitForm}>
        <div className="form-group" style={{ gridColumn: "1 / -1" }}>
          <label>Identificador (PK)</label>
          <input
            name="id"
            className="form-control"
            placeholder="Digite aqui..."
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

  if (action === "substring") {
    return (
      <form onSubmit={submitForm}>
        <div className="form-group" style={{ gridColumn: "1 / -1" }}>
          <label>Busca por substring</label>
          <input
            name="termo"
            className="form-control"
            placeholder="Digite parte do nome..."
            value={values.termo || ""}
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

  if (action === "mass") {
    return (
      <div>
        <p>Clique em executar para popular o banco.</p>
        <div style={{ marginTop: 20 }}>
          <button
            className="btn-primary"
            onClick={() =>
              onExecute({ action, entity: selectedEntity, data: {} })
            }
          >
            Executar
          </button>
        </div>
      </div>
    );
  }

  if (action === "init_db") {
    return (
      <div>
        <p>Resetar ou inicializar o banco de dados.</p>
        <div style={{ marginTop: 20 }}>
          <button
            className="btn-primary"
            onClick={() =>
              onExecute({ action, entity: selectedEntity, data: {} })
            }
          >
            Executar
          </button>
        </div>
      </div>
    );
  }

  // default fallback
  return (
    <div>
      <p>Selecione uma ação no menu lateral.</p>
    </div>
  );
}
