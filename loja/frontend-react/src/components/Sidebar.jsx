import React from "react"

const menuItems = [
  { id: "add", label: "Adicionar dados" },
  { id: "remove", label: "Remover dados" },
  { id: "update", label: "Atualizar dados" },
  { id: "search", label: "Pesquisar por ID" },
  { id: "mass", label: "Manipulação em massa" },
  { id: "substring", label: "Busca por substring" },
  { id: "advanced", label: "Relatório Avançado (JOINs)" },
  { id: "quantifiers", label: "Quantificadores (ANY/ALL)" },
  { id: "grouping", label: "Agrupamento (Vendas)" },
  { id: "init_db", label: "Resetar/Criar Tabelas" },
];

export default function Sidebar({ onSelect }) {
  return (
    <aside className="sidebar">
      <div className="brand" >
        <label className="text-2xl font-black">Concessionária</label>
      </div>0
      <nav className="menu">
        {menuItems.map((m) => (
          <button
            key={m.id}
            className="menu-item"
            onClick={() => onSelect(m.id)}
          >
            {m.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
