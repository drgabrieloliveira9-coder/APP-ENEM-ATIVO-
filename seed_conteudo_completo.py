import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

def adicionar_explicacoes_detalhadas():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Buscar tópicos existentes
    cur.execute('SELECT id, title, area_id FROM topics')
    topics = cur.fetchall()
    
    explicacoes_por_tema = {
        'Interpretação de Textos': {
            'conteudo': '''A interpretação de textos é fundamental no ENEM. Você deve:

1. LEITURA ATENTA: Leia o texto completo antes de ir às questões
2. IDENTIFIQUE O GÊNERO: Reconheça se é notícia, crônica, artigo, etc.
3. CONTEXTO: Entenda o contexto histórico e social do texto
4. INFERÊNCIAS: Vá além do que está explícito, compreenda as entrelinhas
5. VOCABULÁRIO: Use o contexto para deduzir palavras desconhecidas

O ENEM cobra principalmente:
- Compreensão global do texto
- Identificação de tese e argumentos
- Reconhecimento de recursos expressivos
- Relação entre textos (intertextualidade)''',
            'exemplos': 'Exemplo: Se o texto fala sobre "O Brasil enfrenta desafios educacionais", a tese está clara. Os parágrafos seguintes trarão argumentos que sustentam essa afirmação.',
            'dicas': 'Dica de ouro: Grife palavras-chave! Identifique conectivos (porém, todavia, portanto) que mostram a direção do argumento.'
        },
        'Funções da Linguagem': {
            'conteudo': '''As 6 funções da linguagem segundo Jakobson:

1. REFERENCIAL/DENOTATIVA: Foco na informação objetiva
   - Textos jornalísticos, científicos, didáticos
   - Linguagem clara e objetiva

2. EMOTIVA/EXPRESSIVA: Foco no emissor, suas emoções
   - Poesias líricas, diários, autobiografias
   - Uso de 1ª pessoa, interjeições

3. CONATIVA/APELATIVA: Foco no receptor, persuasão
   - Propagandas, discursos políticos, ordens
   - Verbos no imperativo, vocativos

4. FÁTICA: Foco no canal de comunicação
   - "Alô?", "Entende?", "Tá me ouvindo?"
   - Testa/mantém o contato

5. METALINGUÍSTICA: Foco no código (a própria língua)
   - Dicionários, gramáticas, poemas sobre poesia
   - Língua explicando a língua

6. POÉTICA: Foco na mensagem, na forma
   - Poesias, textos literários
   - Figuras de linguagem, ritmo, sonoridade''',
            'exemplos': 'Propaganda: "COMPRE JÁ!" = Conativa | Poema: "Amor é fogo que arde sem se ver" = Poética | Notícia: "Inflação sobe 0,5%" = Referencial',
            'dicas': 'Memorize: REFerencial = inFORMAÇÃO | EMOtiva = EMOções | CONativa = CONvencer | FÁTica = conFIRMAR contato'
        },
        'Razão e Proporção': {
            'conteudo': '''RAZÃO é a divisão entre dois números: a/b (b≠0)

PROPORÇÃO é a igualdade entre duas razões: a/b = c/d

PROPRIEDADE FUNDAMENTAL: Se a/b = c/d, então: a×d = b×c

GRANDEZAS PROPORCIONAIS:
- DIRETAMENTE: quando uma aumenta, a outra aumenta na mesma proporção
  Exemplo: velocidade e distância (tempo constante)

- INVERSAMENTE: quando uma aumenta, a outra diminui
  Exemplo: velocidade e tempo (distância constante)

DIVISÃO PROPORCIONAL:
- Direta: dividir em partes proporcionais aos números dados
- Inversa: dividir inversamente proporcional''',
            'exemplos': 'Exemplo prático: 3 pedreiros fazem uma obra em 12 dias. Quantos dias levam 4 pedreiros? (Inversamente proporcional: mais pedreiros = menos dias) | 3 pedreiros --- 12 dias | 4 pedreiros --- x dias | 3/4 = x/12 → x = 9 dias',
            'dicas': 'Macete: Grandezas DIRETAMENTE proporcionais = setas NO MESMO SENTIDO ↑↑ | INVERSAMENTE = setas em SENTIDOS OPOSTOS ↑↓'
        },
        'Porcentagem': {
            'conteudo': '''PORCENTAGEM representa uma fração de denominador 100.

15% = 15/100 = 0,15

CÁLCULOS ESSENCIAIS:
1. Calcular X% de um valor: multiplique o valor por X/100
2. Aumento percentual: Valor × (1 + percentual/100)
3. Desconto percentual: Valor × (1 - percentual/100)
4. Variação percentual: [(Valor Final - Valor Inicial)/Valor Inicial] × 100

AUMENTOS/DESCONTOS SUCESSIVOS:
Não some os percentuais! Multiplique os fatores.
Exemplo: 10% de aumento + 10% de desconto ≠ 0%
1,10 × 0,90 = 0,99 = -1% (houve perda!)''',
            'exemplos': 'Exemplo: Uma camisa de R$ 80 tem 25% de desconto. Preço final? | R$ 80 × (1 - 0,25) = R$ 80 × 0,75 = R$ 60 | OU: 25% de 80 = 20, então 80 - 20 = 60',
            'dicas': 'Atalho mental: 10% = divida por 10 | 5% = metade de 10% | 1% = divida por 100 | 50% = metade | 25% = um quarto'
        },
        'Brasil Colônia': {
            'conteudo': '''PERÍODO COLONIAL (1500-1822):

1. PRÉ-COLONIAL (1500-1530):
   - Exploração do pau-brasil
   - Escambo com indígenas
   - Feitorias no litoral

2. CAPITANIAS HEREDITÁRIAS (1534-1549):
   - Divisão do território em 15 lotes
   - Doadas a donatários da nobreza
   - Maioria fracassou (exceto PE e SP)

3. GOVERNO-GERAL (1549-1808):
   - Centralização administrativa
   - 1º Gov-Geral: Tomé de Sousa
   - Salvador = primeira capital

ECONOMIA COLONIAL:
- CICLO DO AÇÚCAR (séc XVI-XVII): Nordeste, mão de obra escrava africana
- CICLO DO OURO (séc XVIII): Minas Gerais, capitação, derrama
- PACTO COLONIAL: Brasil só podia comerciar com Portugal

SOCIEDADE:
- Hierarquia rígida: Senhores → Homens livres pobres → Escravizados
- Patriarcal, rural, escravocrata''',
            'exemplos': 'Exemplo ENEM: Questões relacionam o pacto colonial com a dependência econômica atual. Entender que o Brasil exportava matéria-prima e importava manufaturados é chave.',
            'dicas': 'Memorize os ciclos econômicos na ordem: Pau-brasil → Açúcar → Ouro → Café (já no Império). Cada um deslocou o eixo econômico do país.'
        },
        'Química - Tabela Periódica': {
            'conteudo': '''A TABELA PERIÓDICA organiza os elementos por:

PERÍODOS (linhas horizontais): 7 períodos
- Indicam o número de camadas eletrônicas

FAMÍLIAS/GRUPOS (colunas verticais): 18 grupos
- Elementos com propriedades químicas semelhantes
- Mesma quantidade de elétrons na camada de valência

PRINCIPAIS FAMÍLIAS:
- Grupo 1 (Metais Alcalinos): Li, Na, K - muito reativos
- Grupo 2 (Metais Alcalino-terrosos): Be, Mg, Ca
- Grupos 3-12 (Metais de Transição): Fe, Cu, Zn
- Grupo 17 (Halogênios): F, Cl, Br, I - muito reativos
- Grupo 18 (Gases Nobres): He, Ne, Ar - inertes (não reagem)

PROPRIEDADES PERIÓDICAS:
- RAIO ATÔMICO: Aumenta ↓ e ← na tabela
- ELETRONEGATIVIDADE: Aumenta ↑ e → (F é o maior)
- ENERGIA DE IONIZAÇÃO: Aumenta ↑ e →''',
            'exemplos': 'Exemplo: Por que NaCl existe? Na (metal alcalino) perde 1 elétron facilmente. Cl (halogênio) ganha 1 elétron facilmente. Resultado: ligação iônica estável!',
            'dicas': 'Macete para eletronegatividade: F.O.N.Cl.Br (do maior para o menor) - Flúor, Oxigênio, Nitrogênio, Cloro, Bromo'
        },
        'Física - Cinemática': {
            'conteudo': '''CINEMÁTICA estuda o movimento SEM considerar suas causas.

CONCEITOS FUNDAMENTAIS:
- Posição (S): onde o corpo está [m]
- Deslocamento (ΔS): variação de posição [m]
- Velocidade (V): variação de posição no tempo [m/s]
- Aceleração (a): variação de velocidade no tempo [m/s²]

MOVIMENTO UNIFORME (MU):
- Velocidade constante, aceleração = 0
- Fórmula: S = S₀ + v×t

MOVIMENTO UNIFORMEMENTE VARIADO (MUV):
- Aceleração constante ≠ 0
- Fórmulas:
  • V = V₀ + a×t
  • S = S₀ + V₀×t + (a×t²)/2
  • V² = V₀² + 2×a×ΔS (Equação de Torricelli)

QUEDA LIVRE:
- Movimento vertical com a = g ≈ 10 m/s²
- Use as fórmulas do MUV com a = g''',
            'exemplos': 'Exemplo: Carro a 20m/s freia com a=-5m/s². Quanto percorre até parar? | V²=V₀²+2aΔS → 0²=20²+2(-5)ΔS → ΔS=40m',
            'dicas': 'Dica: Na queda livre, no vácuo, todos os corpos caem com a mesma aceleração, independente da massa! (Galileu provou isso)'
        },
        'Biologia - Citologia': {
            'conteudo': '''CITOLOGIA estuda as CÉLULAS - unidades básicas da vida.

TIPOS DE CÉLULAS:
1. PROCARIONTES (sem núcleo):
   - Bactérias e Arqueas
   - Material genético disperso (nucleoide)
   - Sem organelas membranosas

2. EUCARIONTES (com núcleo):
   - Animais, plantas, fungos, protistas
   - Núcleo delimitado por carioteca
   - Organelas especializadas

PRINCIPAIS ORGANELAS:
- MITOCÔNDRIA: Respiração celular, produção de ATP ("energia")
- RIBOSSOMOS: Síntese de proteínas
- RETÍCULO ENDOPLASMÁTICO: Transporte de substâncias (Rugoso tem ribossomos, Liso não)
- COMPLEXO DE GOLGI: "Correio" - empacota e secreta
- LISOSSOMOS: Digestão intracelular
- CLOROPLASTOS (só vegetais): Fotossíntese

MEMBRANA PLASMÁTICA:
- Modelo Mosaico Fluido (Singer e Nicolson)
- Bicamada lipídica + proteínas
- Permeabilidade seletiva''',
            'exemplos': 'Exemplo: Célula muscular tem MUITAS mitocôndrias. Por quê? Porque músculo precisa de muita energia (ATP) para contração!',
            'dicas': 'Memorize: RER (Rugoso) = Ribossomos = pRoteínas | REL (Liso) = Lipídios | Mitocôndria = Usina de energia'
        }
    }
    
    count = 0
    for topic_id, title, area_id in topics:
        titulo_base = title.split(' - ')[0] if ' - ' in title else title
        
        if titulo_base in explicacoes_por_tema:
            dados = explicacoes_por_tema[titulo_base]
            cur.execute('''INSERT INTO explicacoes (topic_id, titulo, conteudo_detalhado, exemplos, dicas) 
                          VALUES (?,?,?,?,?)''',
                       (topic_id, titulo_base, dados['conteudo'], dados['exemplos'], dados['dicas']))
            count += 1
    
    conn.commit()
    print(f'✅ {count} explicações detalhadas adicionadas!')
    return conn, cur

def adicionar_questoes():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    questoes = [
        # Linguagens
        {
            'titulo': 'Interpretação de Textos',
            'pergunta': '''Leia o trecho: "A educação brasileira enfrenta desafios históricos. Todavia, iniciativas recentes demonstram avanços significativos na inclusão escolar." 

Qual a relação estabelecida pelo conectivo "Todavia"?''',
            'a': 'Adição de informações complementares',
            'b': 'Oposição entre os desafios e os avanços',
            'c': 'Explicação dos desafios históricos',
            'd': 'Conclusão sobre a educação brasileira',
            'e': 'Exemplificação de iniciativas recentes',
            'correta': 'B',
            'explicacao': 'O conectivo "Todavia" é adversativo, indicando OPOSIÇÃO. A primeira oração apresenta um problema (desafios), a segunda mostra um contraste (avanços apesar dos desafios). Outros conectivos adversativos: porém, contudo, entretanto, no entanto.'
        },
        {
            'titulo': 'Funções da Linguagem',
            'pergunta': 'Em qual opção a função CONATIVA da linguagem é predominante?',
            'a': 'O dicionário define "casa" como local de moradia',
            'b': 'Compre já! Aproveite esta oferta imperdível!',
            'c': 'Ah, como é bom recordar os tempos de infância...',
            'd': 'A taxa de juros subiu 0,5% neste mês',
            'e': 'Amor é fogo que arde sem se ver',
            'correta': 'B',
            'explicacao': 'Função CONATIVA/APELATIVA: foco no RECEPTOR, busca persuadir, convencer. Usa verbos no IMPERATIVO (Compre! Aproveite!). | A: Metalinguística | C: Emotiva | D: Referencial | E: Poética'
        },
        # Matemática
        {
            'titulo': 'Razão e Proporção',
            'pergunta': 'Três funcionários dividirão R$ 2.400,00 em partes proporcionais ao tempo de trabalho: 2, 3 e 5 anos. Quanto receberá quem trabalhou 3 anos?',
            'a': 'R$ 480,00',
            'b': 'R$ 600,00',
            'c': 'R$ 720,00',
            'd': 'R$ 800,00',
            'e': 'R$ 1.200,00',
            'correta': 'C',
            'explicacao': 'DIVISÃO PROPORCIONAL: Some as partes (2+3+5=10). Cada "parte" vale 2400/10 = R$240. Quem trabalhou 3 anos recebe 3 partes: 3 × 240 = R$ 720,00. Verificação: 2×240 + 3×240 + 5×240 = 480+720+1200 = 2400 ✓'
        },
        {
            'titulo': 'Porcentagem',
            'pergunta': 'Uma mercadoria sofreu aumento de 20% e depois desconto de 20%. Em relação ao preço original, o preço final:',
            'a': 'Permaneceu igual',
            'b': 'Aumentou 4%',
            'c': 'Diminuiu 4%',
            'd': 'Aumentou 2%',
            'e': 'Diminuiu 2%',
            'correta': 'C',
            'explicacao': 'PEGADINHA clássica! Aumentos/descontos sucessivos NÃO se anulam. Use fatores: Aumento 20% = ×1,20 | Desconto 20% = ×0,80 | Resultado: 1,20 × 0,80 = 0,96 = -4% (DIMINUIU 4%). Se fosse R$100: 100→120→96'
        },
        # Humanas
        {
            'titulo': 'Brasil Colônia',
            'pergunta': 'O Pacto Colonial estabelecia que o Brasil deveria:',
            'a': 'Comercializar livremente com todos os países europeus',
            'b': 'Produzir manufaturas para exportação',
            'c': 'Exportar apenas para Portugal e comprar produtos portugueses',
            'd': 'Desenvolver indústrias próprias para consumo interno',
            'e': 'Estabelecer acordos comerciais com a Inglaterra',
            'correta': 'C',
            'explicacao': 'PACTO COLONIAL = Exclusivo Metropolitano. Regra do mercantilismo: Colônia (Brasil) SÓ comercializa com Metrópole (Portugal). Brasil exportava matéria-prima barata e importava manufaturados caros. Isso gerou dependência econômica estrutural que marca o país até hoje.'
        },
        # Natureza
        {
            'titulo': 'Química - Tabela Periódica',
            'pergunta': 'Qual elemento é o MAIS eletronegativo da tabela periódica?',
            'a': 'Oxigênio (O)',
            'b': 'Nitrogênio (N)',
            'c': 'Cloro (Cl)',
            'd': 'Flúor (F)',
            'e': 'Bromo (Br)',
            'correta': 'D',
            'explicacao': 'FLÚOR (F) é o elemento mais eletronegativo! Eletronegatividade AUMENTA → e ↑ na tabela. F está no canto superior direito. Ordem: F > O > N > Cl > Br (memorize: F.O.N.Cl.Br). Eletronegatividade = tendência de ATRAIR elétrons.'
        },
        {
            'titulo': 'Física - Cinemática',
            'pergunta': 'Um carro em MUV parte do repouso com aceleração 2m/s². Após 5 segundos, sua velocidade será:',
            'a': '5 m/s',
            'b': '7 m/s',
            'c': '10 m/s',
            'd': '12 m/s',
            'e': '15 m/s',
            'correta': 'C',
            'explicacao': 'Use: V = V₀ + a×t | Dados: V₀=0 (repouso), a=2m/s², t=5s | V = 0 + 2×5 = 10 m/s. Dica: No MUV, se parte do repouso, a velocidade cresce linearmente com o tempo!'
        },
        {
            'titulo': 'Biologia - Citologia',
            'pergunta': 'Qual organela é responsável pela respiração celular?',
            'a': 'Ribossomo',
            'b': 'Lisossomo',
            'c': 'Mitocôndria',
            'd': 'Complexo de Golgi',
            'e': 'Retículo Endoplasmático',
            'correta': 'C',
            'explicacao': 'MITOCÔNDRIA = "Usina de energia da célula". Realiza RESPIRAÇÃO CELULAR: quebra glicose com O₂ para produzir ATP (energia). Equação: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP. Músculos têm MUITAS mitocôndrias por precisarem de muita energia!'
        },
        {
            'titulo': 'Geometria Plana - Áreas',
            'pergunta': 'Um terreno retangular tem 15m de comprimento e 8m de largura. Sua área em m² é:',
            'a': '23',
            'b': '46',
            'c': '92',
            'd': '120',
            'e': '150',
            'correta': 'D',
            'explicacao': 'Área do RETÂNGULO = base × altura (ou comprimento × largura). A = 15 × 8 = 120 m². Não confunda com PERÍMETRO (soma dos lados): P = 2(15+8) = 46m.'
        },
        {
            'titulo': 'Brasil Imperial',
            'pergunta': 'O período regencial (1831-1840) foi marcado por:',
            'a': 'Estabilidade política e crescimento econômico',
            'b': 'Revoltas regionais e crise de autoridade',
            'c': 'Expansão territorial e guerras externas',
            'd': 'Abolição da escravatura',
            'e': 'Proclamação da República',
            'correta': 'B',
            'explicacao': 'PERÍODO REGENCIAL = fase TURBULENTA. Dom Pedro I abdicou, Dom Pedro II era criança. Regentes governaram (1831-1840). Principais revoltas: Cabanagem (PA), Sabinada (BA), Balaiada (MA), Farroupilha (RS). Solução: GOLPE DA MAIORIDADE antecipou coroação de D. Pedro II aos 14 anos.'
        }
    ]
    
    count = 0
    for q in questoes:
        cur.execute('SELECT id FROM topics WHERE title LIKE ? LIMIT 1', (f'%{q["titulo"]}%',))
        result = cur.fetchone()
        if result:
            topic_id = result[0]
            cur.execute('''INSERT INTO questoes 
                          (topic_id, pergunta, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta_correta, explicacao, dificuldade)
                          VALUES (?,?,?,?,?,?,?,?,?,?)''',
                       (topic_id, q['pergunta'], q['a'], q['b'], q['c'], q['d'], q['e'], 
                        q['correta'], q['explicacao'], 'Média'))
            count += 1
    
    conn.commit()
    conn.close()
    print(f'✅ {count} questões com explicações adicionadas!')

if __name__ == '__main__':
    print('Adicionando conteúdo completo ao banco...')
    adicionar_explicacoes_detalhadas()
    adicionar_questoes()
    print('✅ Processo concluído!')
