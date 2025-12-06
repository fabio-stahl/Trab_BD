import React from "react";

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
    <aside className="fixed top-2 left-0 w-full h-18 bg-transparent opacity-80 flex items-center px-6 shadow-md">
      <nav className="flex-1 m-10">
        {menuItems.map((m) => (
          <button
            key={m.id}
            className="px-3 py-2 text-white hover:text-white hover:bg-black rounded transition-all"
            onClick={() => onSelect(m.id)}
          >
            {m.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
