// src/pages/Home.jsx

import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import DynamicForm from "../components/DynamicForm";
import ResultsBox from "../components/ResultsBox";
import "../styles/index.css"; 

// O ENDPOINT CORRETO CONFIGURADO NO DJANGO É /handler/
const API_ENDPOINT = "/api/handler/";

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
            
            // --- ALTERAÇÃO AQUI: DE "/" PARA O ENDPOINT CORRETO ---
            const res = await fetch(API_ENDPOINT, { 
            // --------------------------------------------------------
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            // Adicionado tratamento de erro HTTP
            if (!res.ok) {
                // Tenta ler o JSON de erro do Django, se disponível
                let errorDetails = await res.text();
                try {
                    errorDetails = JSON.parse(errorDetails);
                    errorDetails = errorDetails.error || JSON.stringify(errorDetails);
                } catch (e) {
                    // Se não for JSON, usa o status
                    errorDetails = `Erro HTTP: ${res.status} (${res.statusText})`;
                }
                throw new Error(errorDetails);
            }
            
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
                <Header title={ action ? (action === "add" ? "Adicionar Registro" : action === "update" ? "Atualizar Registro" : action == "remove" ? "Remover Dados" : action) : ""}
                        subtitle={ action ? "" : "" } />

                <section id="interface-container" className={`card ${!showInterface ? "hidden" : ""}`}>
                
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