import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

def adicionar_explicacoes_para_todos_topicos():
    """Adiciona explicações detalhadas para TODOS os 500 tópicos do ENEM"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Buscar todos os tópicos que ainda não têm explicação
    cur.execute('''
        SELECT t.id, t.title, a.name as area_name
        FROM topics t
        LEFT JOIN explicacoes e ON t.id = e.topic_id
        JOIN areas a ON t.area_id = a.id
        WHERE e.id IS NULL
        ORDER BY a.id, t.id
    ''')
    
    topicos_sem_explicacao = cur.fetchall()
    total = len(topicos_sem_explicacao)
    
    print(f'📚 Adicionando explicações para {total} tópicos...\n')
    
    count = 0
    for topic_id, title, area_name in topicos_sem_explicacao:
        # Gerar conteúdo baseado na área e título do tópico
        conteudo, exemplos, dicas = gerar_conteudo_educacional(title, area_name)
        
        cur.execute('''
            INSERT INTO explicacoes (topic_id, titulo, conteudo_detalhado, exemplos, dicas)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic_id, title, conteudo, exemplos, dicas))
        
        count += 1
        if count % 50 == 0:
            print(f'✅ {count}/{total} explicações adicionadas...')
    
    conn.commit()
    conn.close()
    print(f'\n✅ CONCLUÍDO! {count} explicações detalhadas adicionadas ao banco!')
    print(f'📊 Total de explicações no banco: {count + 25} de 500 tópicos')

def gerar_conteudo_educacional(titulo, area):
    """Gera conteúdo educacional estruturado baseado no título e área"""
    
    # Templates por área do conhecimento
    if 'Linguagens' in area:
        return gerar_conteudo_linguagens(titulo)
    elif 'Matemática' in area:
        return gerar_conteudo_matematica(titulo)
    elif 'Humanas' in area:
        return gerar_conteudo_humanas(titulo)
    elif 'Natureza' in area:
        return gerar_conteudo_natureza(titulo)
    else:
        return gerar_conteudo_generico(titulo)

def gerar_conteudo_linguagens(titulo):
    """Conteúdo para Linguagens, Códigos e suas Tecnologias"""
    
    conteudo_base = {
        'Gêneros Textuais': (
            '📝 GÊNEROS TEXTUAIS\n\n'
            'Os gêneros textuais são formas de organização da linguagem adaptadas a situações comunicativas específicas.\n\n'
            'PRINCIPAIS GÊNEROS:\n'
            '• NARRATIVOS: Conto, romance, crônica, notícia, relato\n'
            '• DESCRITIVOS: Retrato, paisagem, caracterização\n'
            '• DISSERTATIVOS: Artigo de opinião, editorial, ensaio\n'
            '• INSTRUCIONAIS: Receita, manual, bula, regulamento\n'
            '• EXPOSITIVOS: Verbete, reportagem, resumo, resenha\n\n'
            'CARACTERÍSTICAS IMPORTANTES:\n'
            '1. Cada gênero tem estrutura própria\n'
            '2. O contexto determina o gênero adequado\n'
            '3. Conhecer o gênero facilita a interpretação',
            'Ex: NOTÍCIA usa linguagem objetiva e estrutura do lide (quem, o quê, quando, onde, como, por quê). '
            'CRÔNICA usa linguagem subjetiva e reflexiva sobre fatos cotidianos.',
            'DICA: Identifique o PROPÓSITO do texto - informar, convencer, instruir ou entreter!'
        ),
        'Funções da Linguagem': (
            '🗣️ FUNÇÕES DA LINGUAGEM\n\n'
            'As 6 funções da linguagem segundo Jakobson:\n\n'
            '1. REFERENCIAL: Informa objetivamente (notícias, textos científicos)\n'
            '2. EMOTIVA: Expressa emoções do emissor (poesias líricas, diários)\n'
            '3. CONATIVA: Convence o receptor (propagandas, discursos)\n'
            '4. FÁTICA: Testa/mantém contato ("Alô?", "Entendeu?")\n'
            '5. METALINGUÍSTICA: Código explica código (dicionários, gramáticas)\n'
            '6. POÉTICA: Foco na forma da mensagem (poesias, slogans)',
            'REFERENCIAL: "Inflação subiu 0,5%" | EMOTIVA: "Ah, como sofro de saudades!" | '
            'CONATIVA: "Compre agora!" | FÁTICA: "Oi, tudo bem?" | '
            'METALINGUÍSTICA: "Substantivo é..." | POÉTICA: "Amor é fogo que arde"',
            'Memorize: REF=INFO | EMO=SENTIMENTO | CON=CONVENCER | FÁT=CONTATO | META=CÓDIGO | POÉ=ARTE'
        )
    }
    
    if titulo in conteudo_base:
        return conteudo_base[titulo]
    
    # Conteúdo genérico para outros tópicos de Linguagens
    if 'Literatura' in titulo:
        return (
            f'📚 {titulo.upper()}\n\n'
            'CONTEXTO HISTÓRICO E LITERÁRIO:\n'
            f'O estudo de {titulo} é fundamental para compreender a evolução da literatura brasileira e portuguesa.\n\n'
            'CARACTERÍSTICAS PRINCIPAIS:\n'
            '• Contexto histórico e social da época\n'
            '• Principais autores e obras representativas\n'
            '• Características estilísticas do movimento\n'
            '• Influências e rupturas com movimentos anteriores\n\n'
            'IMPORTÂNCIA PARA O ENEM:\n'
            'O ENEM cobra análise de textos literários, identificação de características dos movimentos '
            'e compreensão do contexto histórico-social das obras.',
            f'Exemplo: Leia trechos de autores representativos de {titulo}, identifique as características '
            'do movimento e relacione com o contexto da época.',
            f'DICA: Relacione sempre a literatura com o momento histórico! O ENEM adora questões interdisciplinares.'
        )
    
    if 'Gramática' in titulo:
        return (
            f'📖 {titulo.upper()}\n\n'
            'CONCEITOS FUNDAMENTAIS:\n'
            f'O domínio de {titulo} é essencial para a compreensão e produção textual eficaz.\n\n'
            'PONTOS IMPORTANTES:\n'
            '• Reconhecer estruturas gramaticais em contexto\n'
            '• Compreender a função comunicativa das escolhas gramaticais\n'
            '• Aplicar as normas em situações de uso formal da língua\n\n'
            'APLICAÇÃO NO ENEM:\n'
            'O ENEM não cobra gramática isolada, mas sim a compreensão de como as escolhas '
            'gramaticais produzem sentido nos textos.',
            f'Exemplo: Identifique como {titulo.lower()} contribui para o sentido global do texto, '
            'não apenas decore regras!',
            'DICA: A gramática do ENEM é CONTEXTUAL - sempre relacione com a produção de sentido!'
        )
    
    if 'Inglês' in titulo or 'Espanhol' in titulo:
        return (
            f'🌍 {titulo.upper()}\n\n'
            'LEITURA EM LÍNGUA ESTRANGEIRA:\n'
            'O ENEM avalia a capacidade de compreensão de textos em língua estrangeira.\n\n'
            'ESTRATÉGIAS DE LEITURA:\n'
            '• Identificar cognatos (palavras semelhantes ao português)\n'
            '• Usar o contexto para deduzir significados\n'
            '• Reconhecer palavras-chave e ideias principais\n'
            '• Relacionar com conhecimentos prévios\n\n'
            'FOCO DO ENEM:\n'
            'As questões testam compreensão textual, não conhecimento gramatical profundo.',
            'Exemplo: Ao ler um texto em inglês/espanhol, identifique primeiro o tema geral, '
            'depois busque informações específicas.',
            'DICA: Não traduza palavra por palavra! Busque compreender o SENTIDO GLOBAL do texto.'
        )
    
    if 'Arte' in titulo or 'Música' in titulo or 'Teatro' in titulo or 'Cinema' in titulo:
        return (
            f'🎨 {titulo.upper()}\n\n'
            'MANIFESTAÇÕES ARTÍSTICAS E CULTURAIS:\n'
            f'O estudo de {titulo} envolve compreender as expressões culturais e seus contextos.\n\n'
            'ASPECTOS IMPORTANTES:\n'
            '• Contexto histórico e cultural das manifestações artísticas\n'
            '• Principais movimentos e representantes\n'
            '• Relação entre arte e sociedade\n'
            '• Diversidade cultural brasileira e mundial\n\n'
            'NO ENEM:\n'
            'O exame cobra a capacidade de interpretar manifestações artísticas e relacioná-las '
            'com seus contextos de produção.',
            f'Exemplo: Analise obras de {titulo.lower()} considerando o período histórico, '
            'influências culturais e mensagem comunicada.',
            'DICA: Arte é COMUNICAÇÃO - busque entender o que o artista quer expressar!'
        )
    
    # Conteúdo genérico para demais tópicos de Linguagens
    return (
        f'📚 {titulo.upper()}\n\n'
        'FUNDAMENTOS DO ESTUDO:\n'
        f'{titulo} é um componente essencial dos estudos de Linguagens, Códigos e suas Tecnologias.\n\n'
        'PRINCIPAIS ASPECTOS:\n'
        '• Compreensão dos conceitos fundamentais\n'
        '• Aplicação em contextos comunicativos reais\n'
        '• Análise crítica de textos e manifestações linguísticas\n'
        '• Relação com questões sociais e culturais\n\n'
        'IMPORTÂNCIA PARA O ENEM:\n'
        'O ENEM valoriza a capacidade de usar conhecimentos de linguagem para interpretar '
        'e produzir textos em diferentes contextos.',
        f'Exemplo prático: Identifique elementos de {titulo.lower()} em textos variados e '
        'compreenda como contribuem para o sentido.',
        f'DICA: Sempre relacione {titulo.lower()} com a PRÁTICA comunicativa, não apenas teoria!'
    )

def gerar_conteudo_matematica(titulo):
    """Conteúdo para Matemática e suas Tecnologias"""
    
    conteudo_base = {
        'Razão e Proporção': (
            '🔢 RAZÃO E PROPORÇÃO\n\n'
            'CONCEITOS FUNDAMENTAIS:\n'
            '• RAZÃO: Comparação entre dois números através da divisão (a/b, com b≠0)\n'
            '• PROPORÇÃO: Igualdade entre duas razões (a/b = c/d)\n\n'
            'PROPRIEDADES IMPORTANTES:\n'
            '1. Produto dos extremos = Produto dos meios (a×d = b×c)\n'
            '2. Razões equivalentes formam proporções\n'
            '3. Grandezas diretamente e inversamente proporcionais\n\n'
            'APLICAÇÕES:\n'
            '• Escalas e mapas\n'
            '• Receitas e misturas\n'
            '• Velocidade média\n'
            '• Densidade populacional',
            'Exemplo: Se 3/4 = 6/8, então 3×8 = 4×6 = 24 (produto dos extremos = produto dos meios). '
            'Aplicação prática: Em uma receita para 4 pessoas usa-se 200g de farinha, para 6 pessoas: 4/200 = 6/x → x = 300g',
            'DICA: Monte a proporção identificando as grandezas! Se aumenta junto = direta, se uma aumenta e outra diminui = inversa.'
        ),
        'Porcentagem': (
            '💯 PORCENTAGEM\n\n'
            'FUNDAMENTOS:\n'
            'Porcentagem é uma razão com denominador 100: x% = x/100\n\n'
            'CÁLCULOS ESSENCIAIS:\n'
            '• Calcular X% de um valor: (X/100) × valor\n'
            '• Aumento percentual: valor × (1 + taxa/100)\n'
            '• Desconto percentual: valor × (1 - taxa/100)\n'
            '• Variação percentual: [(final - inicial)/inicial] × 100\n\n'
            'APLICAÇÕES PRÁTICAS:\n'
            '• Descontos e acréscimos\n'
            '• Juros simples e compostos\n'
            '• Estatísticas e gráficos\n'
            '• Inflação e índices econômicos',
            'Exemplo 1: 20% de 500 = (20/100) × 500 = 100\n'
            'Exemplo 2: Produto de R$200 com 15% de desconto = 200 × (1-0,15) = 200 × 0,85 = R$170\n'
            'Exemplo 3: De 80 para 100 = [(100-80)/80] × 100 = 25% de aumento',
            'DICA: Aumento de 10% = multiplicar por 1,10 | Desconto de 10% = multiplicar por 0,90'
        )
    }
    
    if titulo in conteudo_base:
        return conteudo_base[titulo]
    
    # Conteúdo genérico para outros tópicos de Matemática
    if 'Geometria' in titulo:
        return (
            f'📐 {titulo.upper()}\n\n'
            'CONCEITOS GEOMÉTRICOS:\n'
            f'{titulo} estuda as propriedades das figuras e suas relações espaciais.\n\n'
            'ELEMENTOS IMPORTANTES:\n'
            '• Identificação de formas e suas propriedades\n'
            '• Fórmulas de cálculo (perímetro, área, volume)\n'
            '• Relações entre elementos geométricos\n'
            '• Aplicações práticas em situações reais\n\n'
            'NO ENEM:\n'
            'Questões contextualizadas envolvendo cálculos geométricos em situações do cotidiano.',
            f'Exemplo: Use as fórmulas de {titulo.lower()} para resolver problemas práticos como '
            'calcular área de terrenos, volume de recipientes ou distâncias.',
            'DICA: Desenhe a situação! Visualizar geometricamente facilita muito a resolução.'
        )
    
    if 'Função' in titulo or 'Funções' in titulo:
        return (
            f'📊 {titulo.upper()}\n\n'
            'ESTUDO DE FUNÇÕES:\n'
            f'{titulo} relaciona elementos de dois conjuntos através de uma regra matemática.\n\n'
            'CONCEITOS FUNDAMENTAIS:\n'
            '• Domínio e imagem da função\n'
            '• Gráfico e representação visual\n'
            '• Crescimento e decrescimento\n'
            '• Raízes, máximos e mínimos\n\n'
            'APLICAÇÕES:\n'
            'Funções modelam fenômenos reais: crescimento populacional, queda livre, '
            'juros, custos, receitas, etc.',
            f'Exemplo: Em {titulo.lower()}, identifique o padrão de variação das grandezas '
            'e use o gráfico para interpretar a situação.',
            'DICA: O gráfico CONTA UMA HISTÓRIA - aprenda a ler e interpretar visualmente!'
        )
    
    if 'Probabilidade' in titulo or 'Estatística' in titulo or 'Análise Combinatória' in titulo:
        return (
            f'🎲 {titulo.upper()}\n\n'
            'ANÁLISE DE DADOS E EVENTOS:\n'
            f'{titulo} estuda padrões, chances e organização de informações.\n\n'
            'CONCEITOS ESSENCIAIS:\n'
            '• Espaço amostral e eventos\n'
            '• Cálculo de probabilidades\n'
            '• Análise de dados e gráficos\n'
            '• Técnicas de contagem\n\n'
            'APLICAÇÕES PRÁTICAS:\n'
            'Usado em pesquisas, jogos, previsões, análise de riscos e tomada de decisões.',
            f'Exemplo: Em {titulo.lower()}, identifique o total de possibilidades e casos favoráveis '
            'para calcular probabilidades ou organizar informações.',
            'DICA: Organize as informações! Tabelas e diagramas ajudam muito na visualização.'
        )
    
    if 'Trigonometria' in titulo:
        return (
            f'📐 {titulo.upper()}\n\n'
            'RELAÇÕES TRIGONOMÉTRICAS:\n'
            f'{titulo} estuda as relações entre ângulos e lados em triângulos.\n\n'
            'FUNDAMENTOS:\n'
            '• Razões trigonométricas: seno, cosseno, tangente\n'
            '• Círculo trigonométrico\n'
            '• Ângulos notáveis (30°, 45°, 60°)\n'
            '• Identidades e equações trigonométricas\n\n'
            'APLICAÇÕES:\n'
            'Cálculos de altura, distância, navegação, ondas, movimento circular.',
            'Exemplo: sen 30° = 1/2, cos 30° = √3/2, tan 30° = √3/3. '
            'Use essas razões para resolver triângulos retângulos.',
            'DICA: Memorize os valores dos ângulos notáveis - caem sempre no ENEM!'
        )
    
    # Conteúdo genérico para demais tópicos de Matemática
    return (
        f'🔢 {titulo.upper()}\n\n'
        'FUNDAMENTOS MATEMÁTICOS:\n'
        f'{titulo} é um conceito fundamental da matemática aplicado em diversas situações.\n\n'
        'PRINCIPAIS ASPECTOS:\n'
        '• Compreensão dos conceitos básicos\n'
        '• Aplicação de fórmulas e propriedades\n'
        '• Resolução de problemas contextualizados\n'
        '• Interpretação de resultados\n\n'
        'RELEVÂNCIA NO ENEM:\n'
        'O ENEM cobra aplicação prática dos conceitos matemáticos em situações reais.',
        f'Exemplo: Identifique os dados do problema, aplique os conceitos de {titulo.lower()} '
        'e interprete o resultado no contexto da questão.',
        f'DICA: Entenda o CONCEITO por trás de {titulo.lower()}, não apenas decore fórmulas!'
    )

def gerar_conteudo_humanas(titulo):
    """Conteúdo para Ciências Humanas e suas Tecnologias"""
    
    if 'Brasil' in titulo or 'República' in titulo or 'Era Vargas' in titulo or 'Ditadura' in titulo:
        return (
            f'🇧🇷 {titulo.upper()}\n\n'
            'CONTEXTO HISTÓRICO BRASILEIRO:\n'
            f'O período de {titulo} representa um momento crucial da história do Brasil.\n\n'
            'ASPECTOS FUNDAMENTAIS:\n'
            '• Contexto político, econômico e social\n'
            '• Principais eventos e personagens\n'
            '• Transformações e permanências\n'
            '• Legado e impactos contemporâneos\n\n'
            'IMPORTÂNCIA PARA O ENEM:\n'
            'O ENEM valoriza a capacidade de relacionar eventos históricos com processos sociais '
            'e políticos, além de comparar com questões atuais.',
            f'Exemplo: Analise {titulo} identificando: atores sociais envolvidos, conflitos, mudanças '
            'estruturais e relações com o presente.',
            'DICA: História é sobre PROCESSOS, não apenas datas! Entenda causas, desenvolvimentos e consequências.'
        )
    
    if 'Guerra' in titulo or 'Revolução' in titulo or 'Iluminismo' in titulo or 'Renascimento' in titulo:
        return (
            f'🌍 {titulo.upper()}\n\n'
            'CONTEXTO HISTÓRICO MUNDIAL:\n'
            f'{titulo} representa um marco fundamental na história mundial.\n\n'
            'PONTOS ESSENCIAIS:\n'
            '• Causas e contexto histórico\n'
            '• Desenvolvimento dos acontecimentos\n'
            '• Consequências e impactos globais\n'
            '• Relações com o Brasil e América\n\n'
            'NO ENEM:\n'
            'Questões relacionam eventos mundiais com processos históricos brasileiros e atuais.',
            f'Exemplo: Ao estudar {titulo}, identifique as conexões com a história do Brasil '
            'e com questões contemporâneas.',
            'DICA: Pense GLOBALMENTE - eventos mundiais impactam o Brasil e vice-versa!'
        )
    
    if 'Geografia' in titulo or 'Clima' in titulo or 'Relevo' in titulo or 'Hidrografia' in titulo:
        return (
            f'🗺️ {titulo.upper()}\n\n'
            'GEOGRAFIA FÍSICA E AMBIENTAL:\n'
            f'O estudo de {titulo} é fundamental para compreender o espaço geográfico.\n\n'
            'CONCEITOS IMPORTANTES:\n'
            '• Características e processos naturais\n'
            '• Relação com atividades humanas\n'
            '• Impactos ambientais e sustentabilidade\n'
            '• Distribuição espacial e regional\n\n'
            'APLICAÇÃO NO ENEM:\n'
            'O exame cobra a relação entre elementos naturais e sociedade, além de questões ambientais.',
            f'Exemplo: Analise como {titulo.lower()} influencia(m) as atividades econômicas, '
            'distribuição populacional e questões ambientais.',
            'DICA: Geografia é a relação SOCIEDADE-NATUREZA - sempre conecte os dois aspectos!'
        )
    
    if 'Urbanização' in titulo or 'Demografia' in titulo or 'Migração' in titulo:
        return (
            f'🏙️ {titulo.upper()}\n\n'
            'GEOGRAFIA HUMANA E SOCIAL:\n'
            f'{titulo} estuda a organização e dinâmica das populações no espaço.\n\n'
            'ASPECTOS FUNDAMENTAIS:\n'
            '• Processos e características populacionais\n'
            '• Causas e consequências dos movimentos\n'
            '• Desigualdades e questões sociais\n'
            '• Transformações espaciais\n\n'
            'NO ENEM:\n'
            'Questões relacionam processos populacionais com desenvolvimento, desigualdade e sustentabilidade.',
            f'Exemplo: Em {titulo}, analise dados demográficos, identifique padrões '
            'e relacione com questões socioeconômicas.',
            'DICA: Use gráficos e tabelas! O ENEM adora questões com interpretação de dados.'
        )
    
    if 'Filosofia' in titulo or 'Sociologia' in titulo:
        return (
            f'💭 {titulo.upper()}\n\n'
            'PENSAMENTO E SOCIEDADE:\n'
            f'{titulo} desenvolve o pensamento crítico sobre questões humanas e sociais.\n\n'
            'CONCEITOS ESSENCIAIS:\n'
            '• Principais pensadores e correntes\n'
            '• Conceitos fundamentais da área\n'
            '• Aplicação a questões contemporâneas\n'
            '• Análise crítica da realidade social\n\n'
            'IMPORTÂNCIA NO ENEM:\n'
            'O exame valoriza a capacidade de usar conceitos filosóficos/sociológicos para '
            'analisar criticamente a sociedade.',
            f'Exemplo: Use conceitos de {titulo.lower()} para interpretar fenômenos sociais, '
            'políticos e culturais atuais.',
            'DICA: Filosofia e Sociologia são ferramentas de ANÁLISE CRÍTICA da realidade!'
        )
    
    # Conteúdo genérico para outros tópicos de Humanas
    return (
        f'📚 {titulo.upper()}\n\n'
        'FUNDAMENTOS DAS CIÊNCIAS HUMANAS:\n'
        f'{titulo} é essencial para compreender processos históricos, sociais e espaciais.\n\n'
        'PRINCIPAIS ELEMENTOS:\n'
        '• Contexto histórico e social\n'
        '• Processos e transformações\n'
        '• Relações de poder e desigualdades\n'
        '• Conexões com o presente\n\n'
        'NO ENEM:\n'
        'O exame cobra interpretação de processos históricos e sociais, relacionando passado e presente.',
        f'Exemplo: Ao estudar {titulo}, identifique atores sociais, conflitos, mudanças '
        'e permanências ao longo do tempo.',
        f'DICA: Ciências Humanas = compreender o HUMANO no tempo e espaço!'
    )

def gerar_conteudo_natureza(titulo):
    """Conteúdo para Ciências da Natureza e suas Tecnologias"""
    
    if 'Química' in titulo:
        return (
            f'🧪 {titulo.upper()}\n\n'
            'FUNDAMENTOS QUÍMICOS:\n'
            f'{titulo} estuda a composição, propriedades e transformações da matéria.\n\n'
            'CONCEITOS ESSENCIAIS:\n'
            '• Estrutura e propriedades das substâncias\n'
            '• Reações e transformações químicas\n'
            '• Cálculos estequiométricos\n'
            '• Aplicações tecnológicas e ambientais\n\n'
            'NO ENEM:\n'
            'Questões contextualizadas relacionando química com cotidiano, meio ambiente e tecnologia.',
            f'Exemplo: Em {titulo.lower()}, identifique as substâncias envolvidas, tipo de reação '
            'e calcule quantidades usando relações estequiométricas.',
            'DICA: Química está no DIA A DIA - sempre busque aplicações práticas dos conceitos!'
        )
    
    if 'Física' in titulo:
        return (
            f'⚡ {titulo.upper()}\n\n'
            'FUNDAMENTOS FÍSICOS:\n'
            f'{titulo} estuda os fenômenos naturais e as leis que regem o universo.\n\n'
            'CONCEITOS FUNDAMENTAIS:\n'
            '• Grandezas físicas e unidades\n'
            '• Leis e princípios físicos\n'
            '• Aplicações práticas e tecnológicas\n'
            '• Relação com energia e meio ambiente\n\n'
            'APLICAÇÃO NO ENEM:\n'
            'O exame cobra interpretação de fenômenos físicos em situações reais e tecnológicas.',
            f'Exemplo: Use as leis de {titulo.lower()} para explicar fenômenos do cotidiano '
            'e resolver problemas práticos.',
            'DICA: Física EXPLICA o mundo! Relacione sempre com fenômenos que você observa.'
        )
    
    if 'Biologia' in titulo or 'Ecologia' in titulo or 'Genética' in titulo or 'Evolução' in titulo:
        return (
            f'🧬 {titulo.upper()}\n\n'
            'FUNDAMENTOS BIOLÓGICOS:\n'
            f'{titulo} estuda os seres vivos, suas características e relações.\n\n'
            'CONCEITOS ESSENCIAIS:\n'
            '• Processos biológicos fundamentais\n'
            '• Relações entre estrutura e função\n'
            '• Interações ecológicas e ambientais\n'
            '• Aplicações em saúde e biotecnologia\n\n'
            'NO ENEM:\n'
            'Questões relacionam conceitos biológicos com saúde, meio ambiente e biotecnologia.',
            f'Exemplo: Em {titulo.lower()}, identifique processos, estruturas e suas funções, '
            'relacionando com aplicações práticas.',
            'DICA: Biologia = estudo da VIDA! Conecte sempre com saúde, ambiente e tecnologia.'
        )
    
    # Conteúdo genérico para Ciências da Natureza
    return (
        f'🔬 {titulo.upper()}\n\n'
        'FUNDAMENTOS CIENTÍFICOS:\n'
        f'{titulo} explora os fenômenos naturais e suas aplicações tecnológicas.\n\n'
        'ASPECTOS IMPORTANTES:\n'
        '• Compreensão de conceitos científicos\n'
        '• Interpretação de fenômenos naturais\n'
        '• Aplicações tecnológicas e ambientais\n'
        '• Relação com questões contemporâneas\n\n'
        'RELEVÂNCIA NO ENEM:\n'
        'O exame valoriza a aplicação de conhecimentos científicos em contextos reais.',
        f'Exemplo: Use conceitos de {titulo.lower()} para interpretar fenômenos, '
        'resolver problemas e avaliar impactos tecnológicos.',
        f'DICA: Ciências da Natureza = entender COMO o mundo funciona!'
    )

def gerar_conteudo_generico(titulo):
    """Conteúdo genérico para tópicos não categorizados"""
    return (
        f'📖 {titulo.upper()}\n\n'
        'FUNDAMENTOS DO ESTUDO:\n'
        f'{titulo} é um componente importante dos estudos para o ENEM.\n\n'
        'PRINCIPAIS ASPECTOS:\n'
        '• Compreensão dos conceitos fundamentais\n'
        '• Aplicação em situações práticas\n'
        '• Relação com outras áreas do conhecimento\n'
        '• Interpretação crítica e contextualizada\n\n'
        'NO ENEM:\n'
        'O exame cobra aplicação de conhecimentos em contextos reais e interdisciplinares.',
        f'Exemplo prático: Identifique os elementos principais de {titulo.lower()} '
        'e relacione com situações do cotidiano ou questões atuais.',
        f'DICA: Estude {titulo.lower()} de forma integrada com outras áreas!'
    )

if __name__ == '__main__':
    adicionar_explicacoes_para_todos_topicos()
