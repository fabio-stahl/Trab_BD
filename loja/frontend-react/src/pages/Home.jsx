// src/pages/Home.jsx
import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import DynamicForm from "../components/DynamicForm";
import ResultsBox from "../components/ResultsBox";
import "../styles/index.css"; 


export default function Home() {
  const [action, setAction] = useState("");
  const [entity, setEntity] = useState("cliente");
  const [result, setResult] = useState(null);
  const [showInterface, setShowInterface] = useState(false);

  function handleMenuClick(selectedAction) {
    setAction(selectedAction);
    setShowInterface(true);
    setResult(null);
  }

  async function executeHandler({ action: act, entity: ent, data }) {
    setResult({ message: "Processando..." });
    try {
      const payload = { action: act || action, entity: ent || entity, data: data || {} };
      const res = await fetch("/api/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      setResult(json);
    } catch (err) {
      setResult({ error: String(err) });
    }
  }

  return (
    <div className="app-container">
      <Sidebar onSelect={handleMenuClick} />

      <main className="content-area">
        <Header title={ action ? (action === "add" ? "Adicionar Registro" : action === "update" ? "Atualizar Registro" : action ) : "Bem-vindo" }
                subtitle={ action ? "" : "Selecione uma operação no menu lateral." } />

        <section id="interface-container" className={`card ${!showInterface ? "hidden" : ""}`}>
          <div id="entity-selector-group" className={`form-group ${!["add","update","remove","search"].includes(action) ? "hidden" : ""}`}>
            <label>Tabela Alvo:</label>
            <select id="entity-select" value={entity} onChange={(e) => setEntity(e.target.value)}>
              <option value="cliente">Cliente</option>
              <option value="carro">Carro</option>
              <option value="negociacao">Negociação</option>
              <option value="funcionario">Funcionário</option>
            </select>
          </div>

          <div id="dynamic-inputs" className="input-grid">
            <DynamicForm
              action={action}
              entity={entity}
              onEntityChange={(e) => setEntity(e)}
              onExecute={executeHandler}
            />
          </div>
        </section>

        <section id="results-area" className={`card ${!result ? "hidden" : ""}`}>
          <ResultsBox result={result} onClose={() => setResult(null)} />
        </section>
      </main>
    </div>
  );
}
