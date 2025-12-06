// src/components/Header.jsx
import React from "react";

export default function Header({ title, subtitle }) {
  return (
    <header>
      <h1 id="page-title">{title}</h1>
      <p id="page-subtitle">{subtitle}</p>
    </header>
  );
}
