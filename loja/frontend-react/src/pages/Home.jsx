// src/pages/Home.jsx

import React, { useState } from "react";
import BgImage from "../assets/image_car.jpeg";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import DynamicForm from "../components/DynamicForm";
import ResultsBox from "../components/ResultsBox";
import "../styles/index.css";
import { PageHome } from "../components/PageHome";

const API_ENDPOINT = "http://localhost:8000/api/handler/";

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
      const payload = {
        action: act || action,
        entity: ent || entity,
        data: data || {},
      };

      const res = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        let errorDetails;
        try {
          const errText = await res.text();
          const errJson = JSON.parse(errText);
          errorDetails = errJson.error || JSON.stringify(errJson);
        } catch {
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

  const getTitle = () => {
    switch (action) {
      case "add":
        return "Adicionar Registro";
      case "remove":
        return "Remover Dados";
      case "update":
        return "Atualizar Registro";
      case "search":
        return "Pesquisar por ID";
      case "mass":
        return "Manipulação em Massa";
      case "substring":
        return "Busca por Substring";
      case "advanced":
        return "Relatório Avançado (JOINs)";
      case "quantifiers":
        return "Quantificadores (ANY/ALL)";
      case "grouping":
        return "Agrupamento e Ordenação";
      case "init_db":
        return "Configuração do Banco";
      default:
        return action;
    }
  };

  return (
    <div className="app-container">
      <Sidebar onSelect={handleMenuClick} />

      <main
        className="content-area"
        style={{
          backgroundImage: `url(${BgImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Header
          title={action ? getTitle() : <PageHome />}
          subtitle={action ? "" : ""}
        />

        <section
          id="interface-container"
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
}
