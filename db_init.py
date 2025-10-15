import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

schema = '''
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    FOREIGN KEY(area_id) REFERENCES areas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resumos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    bullets TEXT,
    quick_tip TEXT,
    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS essays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    prompt TEXT,
    essay_text TEXT,
    score INTEGER,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    topic_id INTEGER,
    completed INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    pergunta TEXT NOT NULL,
    opcao_a TEXT NOT NULL,
    opcao_b TEXT NOT NULL,
    opcao_c TEXT NOT NULL,
    opcao_d TEXT NOT NULL,
    opcao_e TEXT NOT NULL,
    resposta_correta TEXT NOT NULL,
    explicacao TEXT NOT NULL,
    dificuldade TEXT DEFAULT 'Média',
    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS explicacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    titulo TEXT NOT NULL,
    conteudo_detalhado TEXT NOT NULL,
    exemplos TEXT,
    dicas TEXT,
    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
);
'''

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print(f'✅ Database created at {DB_PATH}')
