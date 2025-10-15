import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    areas = [
        ('Linguagens, Códigos e suas Tecnologias', 'Língua Portuguesa, Literatura, Línguas Estrangeiras, Artes, Educação Física e Tecnologias da Comunicação'),
        ('Matemática e suas Tecnologias', 'Conhecimentos matemáticos, raciocínio lógico, resolução de problemas'),
        ('Ciências Humanas e suas Tecnologias', 'História, Geografia, Filosofia, Sociologia'),
        ('Ciências da Natureza e suas Tecnologias', 'Química, Física, Biologia')
    ]
    
    cur.executemany('INSERT INTO areas (name, description) VALUES (?,?)', areas)
    conn.commit()
    
    cur.execute('SELECT id, name FROM areas')
    area_map = {name: id for (id, name) in cur.fetchall()}
    
    temas = {
        'Linguagens, Códigos e suas Tecnologias': [
            'Interpretação de Textos', 'Gêneros Textuais', 'Funções da Linguagem', 'Figuras de Linguagem',
            'Literatura Brasileira - Barroco', 'Literatura Brasileira - Arcadismo', 'Literatura Brasileira - Romantismo',
            'Literatura Brasileira - Realismo', 'Literatura Brasileira - Modernismo', 'Gramática - Classes de Palavras',
            'Gramática - Sintaxe', 'Gramática - Concordância', 'Gramática - Regência', 'Semântica e Coesão',
            'Variação Linguística', 'Inglês - Reading Comprehension', 'Inglês - Vocabulary', 'Espanhol - Compreensión Lectora',
            'Artes Visuais', 'Arte Contemporânea', 'Música e Contexto Histórico', 'Teatro e Performance',
            'Cinema e Audiovisual', 'Cultura Digital', 'Tecnologias da Comunicação'
        ],
        'Matemática e suas Tecnologias': [
            'Razão e Proporção', 'Porcentagem', 'Regra de Três', 'Matemática Financeira', 'Análise Combinatória',
            'Probabilidade', 'Estatística Básica', 'Funções do 1º Grau', 'Funções do 2º Grau', 'Função Exponencial',
            'Função Logarítmica', 'Trigonometria - Razões', 'Trigonometria - Círculo', 'Geometria Plana - Áreas',
            'Geometria Plana - Perímetros', 'Geometria Espacial - Volumes', 'Geometria Espacial - Áreas',
            'Geometria Analítica', 'Matrizes', 'Determinantes', 'Sistemas Lineares', 'Progressões Aritméticas',
            'Progressões Geométricas', 'Números Complexos', 'Polinômios'
        ],
        'Ciências Humanas e suas Tecnologias': [
            'Brasil Colônia', 'Brasil Imperial', 'República Velha', 'Era Vargas', 'Ditadura Militar',
            'Nova República', 'Idade Média', 'Renascimento', 'Iluminismo', 'Revoluções Industriais',
            'Primeira Guerra Mundial', 'Segunda Guerra Mundial', 'Guerra Fria', 'Globalização',
            'Geografia Física - Clima', 'Geografia Física - Relevo', 'Geografia Física - Hidrografia',
            'Geografia Humana - Demografia', 'Geografia Humana - Urbanização', 'Geopolítica',
            'Filosofia Antiga', 'Filosofia Moderna', 'Filosofia Contemporânea', 'Sociologia - Teorias Clássicas',
            'Sociologia - Movimentos Sociais'
        ],
        'Ciências da Natureza e suas Tecnologias': [
            'Química - Tabela Periódica', 'Química - Ligações Químicas', 'Química - Funções Inorgânicas',
            'Química - Funções Orgânicas', 'Química - Reações Químicas', 'Química - Estequiometria',
            'Química - Soluções', 'Química - Termoquímica', 'Química - Eletroquímica', 'Química Ambiental',
            'Física - Cinemática', 'Física - Dinâmica', 'Física - Energia', 'Física - Gravitação',
            'Física - Hidrostática', 'Física - Termologia', 'Física - Óptica', 'Física - Ondulatória',
            'Física - Eletricidade', 'Física - Magnetismo', 'Biologia - Citologia', 'Biologia - Genética',
            'Biologia - Evolução', 'Biologia - Ecologia', 'Biologia - Fisiologia Humana'
        ]
    }
    
    count = 0
    for area_name, area_id in area_map.items():
        temas_area = temas.get(area_name, [])
        repeticoes = max(1, 125 // len(temas_area)) if temas_area else 1
        
        for tema in temas_area:
            for i in range(repeticoes):
                if count >= 500:
                    break
                    
                variacao = '' if i == 0 else f' - Parte {i+1}'
                title = f'{tema}{variacao}'
                
                summary = f'Resumo direto ao ponto sobre {tema}. Este conteúdo aborda os conceitos fundamentais que frequentemente aparecem no ENEM, com foco em aplicação prática e resolução de questões.'
                
                if 'Literatura' in tema:
                    bullets = 'Características do movimento|Principais autores e obras|Contexto histórico'
                elif 'Gramática' in tema:
                    bullets = 'Regras essenciais|Casos especiais|Aplicação em questões'
                elif 'Matemática' in tema or 'Geometria' in tema or 'Função' in tema:
                    bullets = 'Fórmulas principais|Passo a passo da resolução|Pegadinhas comuns'
                elif 'Química' in tema:
                    bullets = 'Conceitos fundamentais|Cálculos importantes|Aplicações práticas'
                elif 'Física' in tema:
                    bullets = 'Leis e princípios|Fórmulas essenciais|Problemas típicos'
                elif 'Biologia' in tema:
                    bullets = 'Processos biológicos|Relações ecológicas|Aspectos evolutivos'
                elif 'História' in area_name or any(x in tema for x in ['Brasil', 'Guerra', 'Revolução']):
                    bullets = 'Causas do evento|Principais acontecimentos|Consequências históricas'
                elif 'Geografia' in tema:
                    bullets = 'Características geográficas|Distribuição espacial|Impactos ambientais'
                elif 'Filosofia' in tema or 'Sociologia' in tema:
                    bullets = 'Conceitos centrais|Pensadores importantes|Aplicação contemporânea'
                else:
                    bullets = 'Ponto-chave 1|Ponto-chave 2|Ponto-chave 3'
                
                quick_tip = 'Revise em 20 minutos e faça exercícios práticos para fixação.'
                
                cur.execute('INSERT INTO topics (area_id, title, content) VALUES (?,?,?)', 
                           (area_id, title, f'Conteúdo detalhado sobre {tema}. Este material foi elaborado seguindo a matriz de referência do ENEM.'))
                topic_id = cur.lastrowid
                
                cur.execute('INSERT INTO resumos (topic_id, title, summary, bullets, quick_tip) VALUES (?,?,?,?,?)',
                           (topic_id, title, summary, bullets, quick_tip))
                count += 1
        
        if count >= 500:
            break
    
    conn.commit()
    print(f'✅ {count} resumos criados com sucesso!')
    conn.close()

if __name__ == '__main__':
    seed_database()
