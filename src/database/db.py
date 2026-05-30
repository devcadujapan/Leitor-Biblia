"""
Módulo de banco de dados - SQLite
Gerencia livros, capítulos, versículos e progresso de leitura.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "biblia.db")

# ─── Dados dos 66 livros ────────────────────────────────────────────────────

BOOKS = [
    # Antigo Testamento
    ("Gênesis",        "AT", 50), ("Êxodo",          "AT", 40), ("Levítico",       "AT", 27),
    ("Números",        "AT", 36), ("Deuteronômio",   "AT", 34), ("Josué",          "AT", 24),
    ("Juízes",         "AT", 21), ("Rute",           "AT",  4), ("1 Samuel",       "AT", 31),
    ("2 Samuel",       "AT", 24), ("1 Reis",         "AT", 22), ("2 Reis",         "AT", 25),
    ("1 Crônicas",     "AT", 29), ("2 Crônicas",     "AT", 36), ("Esdras",         "AT", 10),
    ("Neemias",        "AT", 13), ("Ester",          "AT", 10), ("Jó",             "AT", 42),
    ("Salmos",         "AT",150), ("Provérbios",     "AT", 31), ("Eclesiastes",    "AT", 12),
    ("Cantares",       "AT",  8), ("Isaías",         "AT", 66), ("Jeremias",       "AT", 52),
    ("Lamentações",    "AT",  5), ("Ezequiel",       "AT", 48), ("Daniel",         "AT", 12),
    ("Oséias",         "AT", 14), ("Joel",           "AT",  3), ("Amós",           "AT",  9),
    ("Obadias",        "AT",  1), ("Jonas",          "AT",  4), ("Miquéias",       "AT",  7),
    ("Naum",           "AT",  3), ("Habacuque",      "AT",  3), ("Sofonias",       "AT",  3),
    ("Ageu",           "AT",  2), ("Zacarias",       "AT", 14), ("Malaquias",      "AT",  4),
    # Novo Testamento
    ("Mateus",         "NT", 28), ("Marcos",         "NT", 16), ("Lucas",          "NT", 24),
    ("João",           "NT", 21), ("Atos",           "NT", 28), ("Romanos",        "NT", 16),
    ("1 Coríntios",    "NT", 16), ("2 Coríntios",    "NT", 13), ("Gálatas",        "NT",  6),
    ("Efésios",        "NT",  6), ("Filipenses",     "NT",  4), ("Colossenses",    "NT",  4),
    ("1 Tessalonicenses","NT", 5),("2 Tessalonicenses","NT", 3),("1 Timóteo",      "NT",  6),
    ("2 Timóteo",      "NT",  4), ("Tito",           "NT",  3), ("Filemom",        "NT",  1),
    ("Hebreus",        "NT", 13), ("Tiago",          "NT",  5), ("1 Pedro",        "NT",  5),
    ("2 Pedro",        "NT",  3), ("1 João",         "NT",  5), ("2 João",         "NT",  1),
    ("3 João",         "NT",  1), ("Judas",          "NT",  1), ("Apocalipse",     "NT", 22),
]

# Versículos por capítulo (amostra real - simplificado para demo)
# Em produção, substituir pela Bíblia ACF completa em JSON
SAMPLE_VERSES = {
    "Gênesis": {
        1: [
            "No princípio criou Deus os céus e a terra.",
            "E a terra era sem forma e vazia; e havia trevas sobre a face do abismo; e o Espírito de Deus se movia sobre a face das águas.",
            "E disse Deus: Haja luz; e houve luz.",
            "E viu Deus que a luz era boa; e fez Deus separação entre a luz e as trevas.",
            "E Deus chamou à luz Dia; e às trevas chamou Noite. E foi a tarde e a manhã, o dia primeiro.",
        ],
        2: [
            "Assim os céus e a terra foram acabados, e todo o seu exército.",
            "E havendo Deus acabado no dia sétimo a obra que fizera, descansou no dia sétimo de toda a sua obra que tinha feito.",
        ],
    },
    "João": {
        1: [
            "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.",
            "Este estava no princípio com Deus.",
            "Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.",
            "Nele estava a vida, e a vida era a luz dos homens.",
            "E a luz resplandece nas trevas, e as trevas não a compreenderam.",
        ],
    },
}


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    """Cria tabelas e popula livros na primeira execução."""
    con = get_connection()
    cur = con.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            testament TEXT NOT NULL,
            chapters INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reading_progress (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name   TEXT NOT NULL,
            chapter     INTEGER NOT NULL,
            read        INTEGER DEFAULT 0,
            UNIQUE(book_name, chapter)
        );

        CREATE TABLE IF NOT EXISTS user_profile (
            id      INTEGER PRIMARY KEY CHECK (id = 1),
            name    TEXT DEFAULT 'Carlos',
            theme   TEXT DEFAULT 'dark'
        );

        INSERT OR IGNORE INTO user_profile (id, name, theme) VALUES (1, 'Carlos', 'dark');
    """)

    # Popula livros se ainda não existem
    cur.execute("SELECT COUNT(*) FROM books")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO books (name, testament, chapters) VALUES (?, ?, ?)",
            BOOKS
        )

    con.commit()
    con.close()


# ─── Livros ─────────────────────────────────────────────────────────────────

def get_books():
    con = get_connection()
    rows = con.execute("SELECT id, name, testament, chapters FROM books ORDER BY id").fetchall()
    con.close()
    return rows  # list of (id, name, testament, chapters)


# ─── Versículos ─────────────────────────────────────────────────────────────

def get_verses(book_name: str, chapter: int) -> list[str]:
    """Retorna lista de versículos. Usa amostra se não houver JSON externo."""
    # Tenta carregar de arquivo JSON (biblia_acf.json) se disponível
    json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "biblia_acf.json")
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8-sig") as f:
            data = json.load(f)
        try:
            return data[book_name][str(chapter)]
        except KeyError:
            pass

    # Fallback: amostra embutida
    return SAMPLE_VERSES.get(book_name, {}).get(chapter, [
        f"[Versículos de {book_name} cap. {chapter} não carregados.]",
        "Adicione o arquivo data/biblia_acf.json para o texto completo.",
        "Veja o README para instruções de download.",
    ])


# ─── Progresso de leitura ────────────────────────────────────────────────────

def mark_chapter_read(book_name: str, chapter: int, read: bool = True):
    con = get_connection()
    con.execute("""
        INSERT INTO reading_progress (book_name, chapter, read)
        VALUES (?, ?, ?)
        ON CONFLICT(book_name, chapter) DO UPDATE SET read = excluded.read
    """, (book_name, chapter, 1 if read else 0))
    con.commit()
    con.close()


def is_chapter_read(book_name: str, chapter: int) -> bool:
    con = get_connection()
    row = con.execute(
        "SELECT read FROM reading_progress WHERE book_name=? AND chapter=?",
        (book_name, chapter)
    ).fetchone()
    con.close()
    return bool(row and row[0])


def get_progress_stats() -> dict:
    """Retorna estatísticas globais de leitura."""
    con = get_connection()
    total_chapters = con.execute("SELECT SUM(chapters) FROM books").fetchone()[0] or 1
    read_chapters  = con.execute("SELECT COUNT(*) FROM reading_progress WHERE read=1").fetchone()[0]
    con.close()
    return {
        "total": total_chapters,
        "read": read_chapters,
        "percent": round(read_chapters / total_chapters * 100, 1),
    }


def get_book_progress(book_name: str, total_chapters: int) -> dict:
    con = get_connection()
    read = con.execute(
        "SELECT COUNT(*) FROM reading_progress WHERE book_name=? AND read=1",
        (book_name,)
    ).fetchone()[0]
    con.close()
    return {"read": read, "total": total_chapters}


# ─── Perfil ──────────────────────────────────────────────────────────────────

def get_profile() -> dict:
    con = get_connection()
    row = con.execute("SELECT name, theme FROM user_profile WHERE id=1").fetchone()
    con.close()
    return {"name": row[0], "theme": row[1]} if row else {"name": "Carlos", "theme": "dark"}


def save_profile(name: str, theme: str):
    con = get_connection()
    con.execute("UPDATE user_profile SET name=?, theme=? WHERE id=1", (name, theme))
    con.commit()
    con.close()