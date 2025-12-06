// src/components/ResultsBox.jsx
import React from "react";

function createTableJSX(data) {
  if (!Array.isArray(data) || data.length === 0) {
    return <p>Nenhum dado encontrado.</p>;
  }
  const headers = Object.keys(data[0]);
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 10 }}>
      <thead style={{ backgroundColor: "#2c3e50", color: "white" }}>
        <tr>
          {headers.map((h) => (
            <th
              key={h}
              style={{
                padding: 10,
                border: "1px solid #ddd",
                textTransform: "capitalize",
              }}
            >
              {h}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {headers.map((h) => (
              <td
                key={h}
                style={{
                  padding: 8,
                  border: "1px solid #ddd",
                  textAlign: "center",
                }}
              >
                {String(row[h] ?? "")}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function ResultsBox({ result, onClose }) {
  if (!result) return null;

  // 🔥 Detecta automaticamente { data: [...] }
  const resultData =
    result?.data && Array.isArray(result.data) ? result.data : null;

  return (
    <div className="card">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 10,
        }}
      >
        <h3>Resultado da Operação</h3>
        <button onClick={onClose} style={{ padding: "5px 10px", cursor: "pointer" }}>
          Fechar
        </button>
      </div>

      <div className="output-box">
        {/* 🔥 Se vier lista → tabela */}
        {resultData && createTableJSX(resultData)}

        {/* Mensagens de sucesso */}
        {result.message && (
          <div style={{ color: "green", fontWeight: "bold", padding: 20 }}>
            {result.message}
          </div>
        )}

        {/* Erros */}
        {result.error && (
          <div style={{ color: "red", fontWeight: "bold", padding: 20 }}>
            {`ERRO: ${result.error}`}
          </div>
        )}

        {/* Caso não seja data, nem erro, nem message */}
        {!resultData && !result.error && !result.message && (
          <pre style={{ padding: 20 }}>{JSON.stringify(result, null, 2)}</pre>
        )}
      </div>
    </div>
  );
}
