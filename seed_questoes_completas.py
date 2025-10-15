import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

def adicionar_questoes_para_todos_topicos():
    """Adiciona questões de múltipla escolha para TODOS os 500 tópicos"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Buscar todos os tópicos
    cur.execute('''
        SELECT t.id, t.title, a.name as area_name
        FROM topics t
        JOIN areas a ON t.area_id = a.id
        ORDER BY a.id, t.id
    ''')
    
    topicos = cur.fetchall()
    total = len(topicos)
    
    # Verificar quantas questões já existem
    cur.execute('SELECT COUNT(*) FROM questoes')
    questoes_existentes = cur.fetchone()[0]
    
    print(f'📝 Adicionando questões para {total} tópicos...')
    print(f'   Questões existentes: {questoes_existentes}\n')
    
    count = 0
    questoes_adicionadas = 0
    
    for topic_id, title, area_name in topicos:
        # Verificar se já existem questões para este tópico
        cur.execute('SELECT COUNT(*) FROM questoes WHERE topic_id = ?', (topic_id,))
        tem_questoes = cur.fetchone()[0] > 0
        
        if tem_questoes:
            count += 1
            continue
        
        # Gerar 3 questões por tópico
        questoes = gerar_questoes_para_topico(title, area_name)
        
        for questao in questoes:
            cur.execute('''
                INSERT INTO questoes 
                (topic_id, pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, 
                 resposta_correta, explicacao, dificuldade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (topic_id, questao['pergunta'], questao['a'], questao['b'], 
                  questao['c'], questao['d'], questao['e'], questao['correta'],
                  questao['explicacao'], questao['dificuldade']))
            questoes_adicionadas += 1
        
        count += 1
        if count % 50 == 0:
            print(f'✅ {count}/{total} tópicos processados... ({questoes_adicionadas} questões adicionadas)')
    
    conn.commit()
    conn.close()
    
    print(f'\n✅ CONCLUÍDO! {questoes_adicionadas} questões adicionadas ao banco!')
    print(f'📊 Total de questões no banco: {questoes_existentes + questoes_adicionadas}')

def gerar_questoes_para_topico(titulo, area):
    """Gera 3 questões de múltipla escolha para o tópico"""
    
    if 'Linguagens' in area:
        return gerar_questoes_linguagens(titulo)
    elif 'Matemática' in area:
        return gerar_questoes_matematica(titulo)
    elif 'Humanas' in area:
        return gerar_questoes_humanas(titulo)
    elif 'Natureza' in area:
        return gerar_questoes_natureza(titulo)
    else:
        return gerar_questoes_genericas(titulo)

def gerar_questoes_linguagens(titulo):
    """Questões para Linguagens, Códigos e suas Tecnologias"""
    
    if 'Interpretação' in titulo:
        return [
            {
                'pergunta': 'Leia o texto: "Apesar dos avanços tecnológicos recentes, a desigualdade digital persiste no Brasil, especialmente nas regiões mais afastadas dos grandes centros urbanos."\n\nQual é a principal crítica apresentada no texto?',
                'a': 'Os avanços tecnológicos são insuficientes no Brasil',
                'b': 'A tecnologia não chega às regiões urbanas',
                'c': 'Há desigualdade no acesso à tecnologia apesar do progresso',
                'd': 'Os centros urbanos concentram toda a tecnologia',
                'e': 'A tecnologia digital é mal distribuída nas cidades',
                'correta': 'C',
                'explicacao': 'A palavra "apesar" indica concessão: mesmo havendo avanços, o problema da desigualdade continua. A crítica é sobre a persistência da desigualdade digital.',
                'dificuldade': 'Média'
            },
            {
                'pergunta': 'Ao interpretar um texto, é fundamental identificar a tese do autor. Qual estratégia é mais eficaz para isso?',
                'a': 'Procurar a tese sempre no último parágrafo',
                'b': 'Identificar a ideia central defendida ao longo do texto',
                'c': 'Buscar dados estatísticos e numéricos',
                'd': 'Ler apenas o título e a conclusão',
                'e': 'Decorar os argumentos secundários',
                'correta': 'B',
                'explicacao': 'A tese é a ideia central que o autor defende. Ela pode estar em qualquer parte do texto, mas perpassa todo o argumento apresentado.',
                'dificuldade': 'Fácil'
            },
            {
                'pergunta': 'Uma armadilha comum em questões de interpretação é a alternativa que copia trechos do texto, mas distorce o sentido. Como evitar esse erro?',
                'a': 'Escolher sempre a alternativa com palavras do texto',
                'b': 'Ignorar alternativas que mencionam o texto',
                'c': 'Voltar ao texto e verificar o contexto da informação',
                'd': 'Confiar na memória da leitura inicial',
                'e': 'Escolher a alternativa mais longa',
                'correta': 'C',
                'explicacao': 'É essencial voltar ao texto e verificar se a informação está sendo usada no mesmo sentido. Copiar palavras do texto não garante correção se o sentido for distorcido.',
                'dificuldade': 'Média'
            }
        ]
    
    # Questões genéricas para Linguagens
    return [
        {
            'pergunta': f'Em relação a {titulo}, qual elemento é fundamental para a compreensão adequada do tema?',
            'a': 'Memorização de regras isoladas sem contexto',
            'b': 'Compreensão dos conceitos e sua aplicação prática',
            'c': 'Decorar exemplos sem entender o padrão',
            'd': 'Ignorar o contexto comunicativo',
            'e': 'Estudar apenas teoria sem prática',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza a compreensão de conceitos aplicados em contextos reais. Em {titulo}, é essencial entender os fundamentos e saber aplicá-los.',
            'dificuldade': 'Fácil'
        },
        {
            'pergunta': f'No estudo de {titulo}, qual é a melhor estratégia de aprendizado?',
            'a': 'Estudar de forma isolada, sem conexões',
            'b': 'Relacionar com textos e situações reais de comunicação',
            'c': 'Apenas ler teoria sem praticar',
            'd': 'Decorar definições sem compreender',
            'e': 'Ignorar exemplos práticos',
            'correta': 'B',
            'explicacao': f'O ENEM cobra aplicação prática. Estudar {titulo} relacionando com textos reais e situações comunicativas garante melhor compreensão.',
            'dificuldade': 'Média'
        },
        {
            'pergunta': f'Qual competência o ENEM mais valoriza em questões sobre {titulo}?',
            'a': 'Memorização de regras gramaticais',
            'b': 'Capacidade de usar conhecimentos para interpretar textos',
            'c': 'Decorar listas de autores e obras',
            'd': 'Conhecer datas históricas',
            'e': 'Saber termos técnicos complexos',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza a aplicação de conhecimentos de {titulo} na interpretação e análise de textos em contextos reais.',
            'dificuldade': 'Média'
        }
    ]

def gerar_questoes_matematica(titulo):
    """Questões para Matemática e suas Tecnologias"""
    
    if 'Porcentagem' in titulo:
        return [
            {
                'pergunta': 'Uma loja oferece 20% de desconto em um produto que custa R$ 250,00. Qual será o preço final?',
                'a': 'R$ 200,00',
                'b': 'R$ 230,00',
                'c': 'R$ 180,00',
                'd': 'R$ 50,00',
                'e': 'R$ 150,00',
                'correta': 'A',
                'explicacao': 'Desconto de 20% = multiplicar por 0,80 (ou subtrair 20% do valor). 250 × 0,80 = R$ 200,00. Ou: 20% de 250 = 50, então 250 - 50 = 200.',
                'dificuldade': 'Fácil'
            },
            {
                'pergunta': 'Um produto teve aumento de 10% e depois desconto de 10%. Em relação ao preço inicial, o produto está:',
                'a': 'Com o mesmo preço',
                'b': '1% mais barato',
                'c': '1% mais caro',
                'd': '2% mais barato',
                'e': '20% mais barato',
                'correta': 'B',
                'explicacao': 'Preço inicial = 100. Após +10%: 110. Após -10% de 110: 110 × 0,9 = 99. Ficou 1% mais barato (100 - 99 = 1).',
                'dificuldade': 'Difícil'
            },
            {
                'pergunta': 'Para calcular um aumento de 15% sobre um valor, qual operação é correta?',
                'a': 'Multiplicar o valor por 0,15',
                'b': 'Multiplicar o valor por 1,15',
                'c': 'Dividir o valor por 1,15',
                'd': 'Multiplicar o valor por 15',
                'e': 'Dividir o valor por 0,15',
                'correta': 'B',
                'explicacao': 'Aumento de 15% = valor original (100%) + 15% = 115% = 1,15. Portanto, multiplica-se por 1,15.',
                'dificuldade': 'Média'
            }
        ]
    
    if 'Razão' in titulo or 'Proporção' in titulo:
        return [
            {
                'pergunta': 'Em uma proporção a/b = c/d, qual propriedade fundamental é sempre válida?',
                'a': 'a + b = c + d',
                'b': 'a × d = b × c',
                'c': 'a - b = c - d',
                'd': 'a ÷ d = b ÷ c',
                'e': 'a² = c²',
                'correta': 'B',
                'explicacao': 'Propriedade fundamental das proporções: o produto dos extremos (a×d) é igual ao produto dos meios (b×c).',
                'dificuldade': 'Fácil'
            },
            {
                'pergunta': 'Uma receita para 4 pessoas usa 300g de farinha. Para 10 pessoas, quantos gramas são necessários?',
                'a': '600g',
                'b': '700g',
                'c': '750g',
                'd': '800g',
                'e': '1200g',
                'correta': 'C',
                'explicacao': 'Proporção: 4/300 = 10/x → 4x = 3000 → x = 750g. São grandezas diretamente proporcionais.',
                'dificuldade': 'Média'
            },
            {
                'pergunta': 'Em um mapa com escala 1:100.000, uma distância de 5 cm representa quantos quilômetros na realidade?',
                'a': '0,5 km',
                'b': '5 km',
                'c': '50 km',
                'd': '500 km',
                'e': '5000 km',
                'correta': 'B',
                'explicacao': '1 cm = 100.000 cm = 1 km. Logo, 5 cm = 5 km na realidade.',
                'dificuldade': 'Média'
            }
        ]
    
    # Questões genéricas para Matemática
    return [
        {
            'pergunta': f'Em {titulo}, qual é a estratégia mais eficaz para resolver problemas?',
            'a': 'Decorar fórmulas sem entender conceitos',
            'b': 'Compreender os conceitos e aplicar em contextos variados',
            'c': 'Memorizar resoluções de exercícios específicos',
            'd': 'Ignorar o enunciado e aplicar fórmulas aleatórias',
            'e': 'Estudar apenas teoria sem praticar',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza compreensão e aplicação. Em {titulo}, entender conceitos permite resolver problemas diversos, não apenas decorar.',
            'dificuldade': 'Fácil'
        },
        {
            'pergunta': f'Ao estudar {titulo}, qual tipo de questão é mais comum no ENEM?',
            'a': 'Cálculos complexos sem contexto',
            'b': 'Problemas contextualizados em situações reais',
            'c': 'Demonstrações teóricas abstratas',
            'd': 'Questões que exigem apenas decorar fórmulas',
            'e': 'Exercícios puramente algébricos',
            'correta': 'B',
            'explicacao': f'O ENEM contextualiza a matemática em situações práticas. {titulo} é cobrado através de problemas do cotidiano.',
            'dificuldade': 'Média'
        },
        {
            'pergunta': f'Para ter sucesso em questões de {titulo}, o estudante deve:',
            'a': 'Apenas decorar fórmulas rapidamente',
            'b': 'Entender conceitos e praticar diferentes tipos de problemas',
            'c': 'Memorizar resoluções prontas',
            'd': 'Ignorar interpretação de enunciados',
            'e': 'Focar apenas em cálculos mentais',
            'correta': 'B',
            'explicacao': f'Sucesso em {titulo} vem da compreensão conceitual aliada à prática variada, permitindo resolver problemas diversos.',
            'dificuldade': 'Fácil'
        }
    ]

def gerar_questoes_humanas(titulo):
    """Questões para Ciências Humanas e suas Tecnologias"""
    
    if 'Brasil Colônia' in titulo:
        return [
            {
                'pergunta': 'Durante o período colonial brasileiro, qual era o principal sistema de exploração econômica implementado por Portugal?',
                'a': 'Industrialização acelerada',
                'b': 'Pacto Colonial e exploração mercantilista',
                'c': 'Livre comércio internacional',
                'd': 'Economia autossuficiente',
                'e': 'Capitalismo industrial',
                'correta': 'B',
                'explicacao': 'O Pacto Colonial estabelecia que a colônia só podia comerciar com a metrópole, garantindo lucros a Portugal através do mercantilismo.',
                'dificuldade': 'Média'
            },
            {
                'pergunta': 'Qual foi a principal forma de trabalho utilizada nos engenhos de açúcar durante o Brasil Colônia?',
                'a': 'Trabalho assalariado europeu',
                'b': 'Servidão feudal',
                'c': 'Escravidão africana',
                'd': 'Cooperativismo agrícola',
                'e': 'Trabalho mecanizado',
                'correta': 'C',
                'explicacao': 'A economia açucareira colonial foi baseada na escravidão africana, fundamental para a produção nos engenhos.',
                'dificuldade': 'Fácil'
            },
            {
                'pergunta': 'As Capitanias Hereditárias foram um sistema de administração colonial que:',
                'a': 'Garantiu total autonomia às colônias',
                'b': 'Dividiu o território em lotes dados a donatários',
                'c': 'Estabeleceu democracia direta',
                'd': 'Criou repúblicas independentes',
                'e': 'Implementou o socialismo colonial',
                'correta': 'B',
                'explicacao': 'As Capitanias Hereditárias dividiram o Brasil em faixas de terra doadas a nobres portugueses (donatários) para colonizar.',
                'dificuldade': 'Média'
            }
        ]
    
    # Questões genéricas para Humanas
    return [
        {
            'pergunta': f'No estudo de {titulo}, qual abordagem é mais valorizada pelo ENEM?',
            'a': 'Memorização de datas e nomes isolados',
            'b': 'Compreensão de processos históricos e sociais',
            'c': 'Decorar definições sem contexto',
            'd': 'Estudar apenas eventos específicos',
            'e': 'Ignorar relações causais',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza a compreensão de processos, causas e consequências. Em {titulo}, é essencial entender contextos e transformações.',
            'dificuldade': 'Fácil'
        },
        {
            'pergunta': f'Ao analisar questões de {titulo}, qual estratégia é fundamental?',
            'a': 'Buscar apenas informações factuais',
            'b': 'Relacionar eventos históricos com contextos atuais',
            'c': 'Memorizar cronologias detalhadas',
            'd': 'Ignorar aspectos sociais e econômicos',
            'e': 'Estudar períodos de forma isolada',
            'correta': 'B',
            'explicacao': f'O ENEM relaciona {titulo} com questões contemporâneas. É essencial conectar passado e presente para compreender processos.',
            'dificuldade': 'Média'
        },
        {
            'pergunta': f'Para compreender {titulo} de forma efetiva, o estudante deve:',
            'a': 'Decorar fatos isoladamente',
            'b': 'Entender causas, processos e consequências',
            'c': 'Memorizar apenas nomes e datas',
            'd': 'Estudar sem relacionar com outras áreas',
            'e': 'Focar apenas em aspectos políticos',
            'correta': 'B',
            'explicacao': f'A compreensão profunda de {titulo} vem do entendimento de processos históricos/sociais, suas causas e impactos.',
            'dificuldade': 'Fácil'
        }
    ]

def gerar_questoes_natureza(titulo):
    """Questões para Ciências da Natureza e suas Tecnologias"""
    
    if 'Química' in titulo and 'Tabela' in titulo:
        return [
            {
                'pergunta': 'Na tabela periódica, os elementos de uma mesma família (coluna) apresentam:',
                'a': 'Mesmo número de prótons',
                'b': 'Mesma massa atômica',
                'c': 'Propriedades químicas semelhantes',
                'd': 'Mesmo número de nêutrons',
                'e': 'Mesma densidade',
                'correta': 'C',
                'explicacao': 'Elementos da mesma família têm o mesmo número de elétrons na camada de valência, resultando em propriedades químicas semelhantes.',
                'dificuldade': 'Média'
            },
            {
                'pergunta': 'Os elementos são organizados na tabela periódica em ordem crescente de:',
                'a': 'Massa atômica',
                'b': 'Número atômico (número de prótons)',
                'c': 'Número de nêutrons',
                'd': 'Raio atômico',
                'e': 'Eletronegatividade',
                'correta': 'B',
                'explicacao': 'A tabela periódica moderna organiza os elementos em ordem crescente de número atômico (Z), que é o número de prótons.',
                'dificuldade': 'Fácil'
            },
            {
                'pergunta': 'Qual propriedade aumenta da direita para esquerda em um período da tabela periódica?',
                'a': 'Eletronegatividade',
                'b': 'Energia de ionização',
                'c': 'Raio atômico',
                'd': 'Caráter metálico',
                'e': 'Número atômico',
                'correta': 'C',
                'explicacao': 'O raio atômico aumenta da direita para esquerda em um período. Eletronegatividade e energia de ionização aumentam no sentido contrário.',
                'dificuldade': 'Média'
            }
        ]
    
    # Questões genéricas para Natureza
    return [
        {
            'pergunta': f'Em {titulo}, qual é o foco principal das questões do ENEM?',
            'a': 'Cálculos matemáticos complexos isolados',
            'b': 'Aplicação de conceitos científicos em situações reais',
            'c': 'Memorização de fórmulas sem contexto',
            'd': 'Nomenclatura técnica avançada',
            'e': 'Demonstrações teóricas abstratas',
            'correta': 'B',
            'explicacao': f'O ENEM contextualiza ciências em situações práticas. {titulo} é cobrado através de aplicações reais e tecnológicas.',
            'dificuldade': 'Fácil'
        },
        {
            'pergunta': f'Para resolver questões de {titulo} no ENEM, é fundamental:',
            'a': 'Apenas decorar fórmulas rapidamente',
            'b': 'Compreender conceitos e relacionar com fenômenos reais',
            'c': 'Memorizar definições sem aplicação',
            'd': 'Ignorar aspectos tecnológicos e ambientais',
            'e': 'Focar apenas em nomenclatura',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza a compreensão conceitual aplicada. Em {titulo}, é essencial entender e relacionar com fenômenos e tecnologias.',
            'dificuldade': 'Média'
        },
        {
            'pergunta': f'Questões de {titulo} no ENEM frequentemente relacionam ciência com:',
            'a': 'Apenas teoria pura sem aplicação',
            'b': 'Cotidiano, tecnologia e meio ambiente',
            'c': 'Cálculos abstratos complexos',
            'd': 'Memorização de leis isoladas',
            'e': 'Nomenclatura técnica exclusivamente',
            'correta': 'B',
            'explicacao': f'O ENEM integra ciências com cotidiano, tecnologia e questões ambientais. {titulo} é abordado de forma contextualizada.',
            'dificuldade': 'Fácil'
        }
    ]

def gerar_questoes_genericas(titulo):
    """Questões genéricas para tópicos não categorizados"""
    return [
        {
            'pergunta': f'Qual é a melhor abordagem para estudar {titulo} para o ENEM?',
            'a': 'Decorar informações isoladas',
            'b': 'Compreender conceitos e aplicá-los em contextos variados',
            'c': 'Memorizar apenas definições',
            'd': 'Estudar sem fazer exercícios',
            'e': 'Ignorar aplicações práticas',
            'correta': 'B',
            'explicacao': f'O ENEM valoriza compreensão e aplicação prática. Estudar {titulo} exige entender conceitos e usá-los em diferentes situações.',
            'dificuldade': 'Fácil'
        },
        {
            'pergunta': f'No ENEM, questões sobre {titulo} geralmente avaliam:',
            'a': 'Apenas memorização de fatos',
            'b': 'Capacidade de interpretar e aplicar conhecimentos',
            'c': 'Decorar listas e classificações',
            'd': 'Conhecimentos muito específicos',
            'e': 'Informações isoladas do contexto',
            'correta': 'B',
            'explicacao': f'O ENEM avalia competências de interpretação e aplicação. {titulo} é cobrado de forma contextualizada e interdisciplinar.',
            'dificuldade': 'Média'
        },
        {
            'pergunta': f'Para ter bom desempenho em {titulo}, o estudante deve:',
            'a': 'Apenas ler teoria sem praticar',
            'b': 'Estudar de forma integrada com outras áreas do conhecimento',
            'c': 'Memorizar informações isoladamente',
            'd': 'Ignorar conexões com o cotidiano',
            'e': 'Focar exclusivamente em definições',
            'correta': 'B',
            'explicacao': f'O ENEM é interdisciplinar. Estudar {titulo} conectando com outras áreas e com situações reais garante melhor compreensão.',
            'dificuldade': 'Fácil'
        }
    ]

if __name__ == '__main__':
    adicionar_questoes_para_todos_topicos()
