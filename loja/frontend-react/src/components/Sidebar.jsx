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

export default function Sidebar({ onSelect, active }) {
  return (
    <aside
      className="
        fixed top-4 left-1/2 -translate-x-1/2
        w-[95%] max-w-6xl
        backdrop-blur-xl
        py-3 px-6 rounded-2xl
        flex justify-center
      "
    >
      <nav className="flex gap-4">
        {menuItems.map((m) => (
          <button
            key={m.id}
            onClick={() => onSelect(m.id)}
            className={`
              text-white text-sm font-medium
              px-4 py-2 rounded-4xl
              w-full
              transition-all duration-200 whitespace-nowrap
              ${active === m.id 
                ? " backdrop-blur-sm shadow-sm scale-105" 
                : " hover:scale-110 hover:shadow-2xl"
              }
            `}
          >
            {m.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
