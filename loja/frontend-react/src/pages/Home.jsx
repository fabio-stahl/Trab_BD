// src/pages/Home.jsx

import React, { useState } from "react";
import BgImage from "../assets/image_car.jpeg";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import DynamicForm from "../components/DynamicForm";
import ResultsBox from "../components/ResultsBox";
import "../styles/index.css";
import { PageHome } from "../components/PageHome";

// O ENDPOINT CORRETO CONFIGURADO NO DJANGO É /handler/
const API_ENDPOINT = "http://localhost:8000/api/handler/";

export default function Home() {
  const [action, setAction] = useState("");
  const [entity, setEntity] = useState("cliente");
  const [result, setResult] = useState(null);
  const [showInterface, setShowInterface] = useState(false);
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
      const payload = {
  async function executeHandler({ action: act, entity: ent, data }) {
    setResult({ message: "Processando..." });

    try {
      const payload = {
        action: act || action,
        entity: ent || entity,
        data: data || {},
      };

      // --- ALTERAÇÃO AQUI: DE "/" PARA O ENDPOINT CORRETO ---
      const res = await fetch(API_ENDPOINT, {
        // --------------------------------------------------------
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      // Tratamento de erro HTTP
      if (!res.ok) {
        let errorDetails;
        try {
          // Tenta ler o JSON de erro do Django
          const errText = await res.text();
          const errJson = JSON.parse(errText);
          errorDetails = errJson.error || JSON.stringify(errJson);
        } catch (e) {
          // Fallback se não for JSON
          errorDetails = `Erro HTTP: ${res.status} (${res.statusText})`;
        }
        throw new Error(errorDetails);
      }

      const json = await res.json();
      setResult(json);
    } catch (err) {
      setResult({ error: String(err.message || err) });
    }
  }

  // Função auxiliar para definir o título baseado na ação selecionada
  const getTitle = () => {
    switch (action) {
      case "add": return "Adicionar Registro";
      case "remove": return "Remover Dados";
      case "update": return "Atualizar Registro";
      case "search": return "Pesquisar por ID";
      case "mass": return "Manipulação em Massa";
      case "substring": return "Busca por Substring";
      case "advanced": return "Relatório Avançado (JOINs)";
      case "quantifiers": return "Quantificadores (ANY/ALL)";
      case "grouping": return "Agrupamento e Ordenação";
      case "init_db": return "Configuração do Banco";
      default: return action; // Fallback
    }
  };

  return (
    <div className="app-container">

      <Sidebar onSelect={handleMenuClick} />
      <main
        className="content-area"
        style={{
          // CORREÇÃO: Adicionadas crases (backticks) para template string
          backgroundImage: `url(${BgImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Header
          // Lógica simplificada usando a função getTitle
          title={action ? getTitle() : <PageHome />}
          subtitle={action ? `Operação: ${entity.toUpperCase()}` : ""}
        />

        <section
          id="interface-container"
          // CORREÇÃO: Adicionadas crases (backticks) para template string
          className={`card ${!showInterface ? "hidden" : ""}`}
        >
          <div id="dynamic-inputs" className="input-grid">
            <DynamicForm
              action={action}
              entity={entity}
              onEntityChange={(e) => setEntity(e)}
              onExecute={executeHandler}
            />
          </div>
        </section>

        <section
          id="results-area"
          className={`card ${!result ? "hidden" : ""}`}
        >
          <ResultsBox result={result} onClose={() => setResult(null)} />
        </section>
      </main>
    </div>
  );
        <section
          id="results-area"
          // CORREÇÃO: Adicionadas crases (backticks) para template string
          className={`card ${!result ? "hidden" : ""}`}
        >
          <ResultsBox result={result} onClose={() => setResult(null)} />
        </section>
      </main>
    </div>
  );
}
