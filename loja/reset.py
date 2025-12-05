import sqlite3
from pathlib import Path

# Caminho do arquivo ao lado do reset.py
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"

print(f"📌 Usando banco em: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("🔍 Tabelas antes de limpar:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print("\n🧹 Limpando banco de dados...")

cursor.execute("PRAGMA foreign_keys = OFF;")

tabelas = [
    "Negociacao",
    "Telefone",
    "Gerente",
    "Vendedor",
    "Funcionario",
    "Carro",
    "Cliente",
]

for tabela in tabelas:
    print(f" - DROP TABLE IF EXISTS {tabela}")
    cursor.execute(f"DROP TABLE IF EXISTS {tabela};")

cursor.execute("PRAGMA foreign_keys = ON;")

conn.commit()

print("\n🔍 Tabelas depois de limpar:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()

print("\n✅ Banco resetado com sucesso.")
