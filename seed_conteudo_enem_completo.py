import sqlite3
from pathlib import Path

DB_PATH = Path('data.db')

# Dicionário completo de explicações por matéria do ENEM
EXPLICACOES_COMPLETAS = {
    # LINGUAGENS E CÓDIGOS
    'Interpretação de Textos': {
        'conteudo': '''A interpretação de textos é a habilidade mais cobrada no ENEM. Envolve:

1. COMPREENSÃO GLOBAL: Entender a ideia central do texto completo
2. IDENTIFICAÇÃO DE INFORMAÇÕES: Localizar dados específicos 
3. INFERÊNCIA: Deduzir informações implícitas (nas entrelinhas)
4. RECONHECIMENTO DE GÊNEROS: Saber diferenciar notícia, crônica, artigo, etc.
5. INTERTEXTUALIDADE: Relacionar diferentes textos sobre o mesmo tema

ESTRATÉGIAS DE LEITURA:
- Leia o título e observe imagens/gráficos antes do texto
- Identifique o tema já no primeiro parágrafo
- Grife palavras-chave e conectivos (mas, porém, portanto)
- Identifique a tese do autor (qual seu posicionamento?)
- Relacione com conhecimentos prévios e contexto atual

ARMADILHAS COMUNS:
- Alternativas que copiam trechos do texto mas distorcem o sentido
- Generalizações excessivas ou restrições não mencionadas
- Inversão de causa e consequência''',
        'exemplos': '''EXEMPLO PRÁTICO: Texto: "Apesar dos avanços tecnológicos, a desigualdade digital persiste no Brasil."
- TESE: Há desigualdade digital
- CONCESSÃO (apesar de): Reconhece avanços
- ADVERSATIVA: Mas o problema continua
Questão típica: "Qual a crítica do texto?" → A persistência da desigualdade apesar do progresso''',
        'dicas': 'DICA DE OURO: Sempre volte ao texto! Não responda "de cabeça". A resposta SEMPRE está no texto, explícita ou implícita.'
    },
    
    'Gêneros Textuais': {
        'conteudo': '''Gêneros textuais são formas de organizar a linguagem para diferentes situações:

NARRATIVO: Conta uma história com personagens, tempo, espaço
- Romance, conto, crônica, notícia
- Elementos: narrador, enredo, clímax, desfecho

DESCRITIVO: Caracteriza seres, objetos, lugares
- Retrato físico/psicológico, paisagem
- Uso intenso de adjetivos e locuções adjetivas

DISSERTATIVO-ARGUMENTATIVO: Defende uma tese com argumentos
- Artigo de opinião, editorial, ensaio
- Estrutura: introdução (tese) → desenvolvimento (argumentos) → conclusão

INJUNTIVO/INSTRUCIONAL: Orienta, dá ordens/instruções
- Receita, manual, bula, regulamento
- Verbos no imperativo ou infinitivo

EXPOSITIVO: Explica, informa objetivamente
- Verbete, reportagem, texto didático
- Linguagem clara, objetiva, impessoal''',
        'exemplos': '''CRÔNICA: Texto curto, cotidiano, reflexivo, tom pessoal (Luis Fernando Veríssimo)
NOTÍCIA: Objetiva, lide (quem, o quê, quando, onde, por quê, como)
EDITORIAL: Opinião do jornal sobre fato atual, sem assinatura
ARTIGO DE OPINIÃO: Opinião assinada, 1ª pessoa permitida''',
        'dicas': 'Identifique O PROPÓSITO do texto: informar? entreter? convencer? instruir? Isso revela o gênero!'
    },

    'Figuras de Linguagem': {
        'conteudo': '''Figuras de linguagem são recursos expressivos que enriquecem o texto:

METÁFORA: Comparação implícita (sem "como")
- "Meu coração é um balde despejado" (Fernando Pessoa)

COMPARAÇÃO/SÍMILE: Comparação explícita (com "como", "tal qual")
- "O amor é como um fogo que arde sem se ver"

METONÍMIA: Substituição de palavra por relação lógica
- "Li Machado de Assis" (obra pelo autor)
- "Tomei dois copos" (conteúdo pelo continente)

HIPÉRBOLE: Exagero intencional
- "Chorei rios de lágrimas"

PERSONIFICAÇÃO/PROSOPOPEIA: Atribui características humanas a seres inanimados
- "O vento sussurrava segredos"

ANTÍTESE: Oposição de ideias
- "Amor e ódio", "Alegria e tristeza"

PARADOXO: Ideias contraditórias que fazem sentido
- "Tristeza alegre" (Vinicius de Moraes)

EUFEMISMO: Suavizar expressão desagradável
- "Ele nos deixou" (= morreu)

IRONIA: Dizer o contrário do que se pensa
- "Que educado!" (para alguém grosseiro)''',
        'exemplos': '''ENEM adora cobrar METÁFORA em poemas!
"Minha terra tem palmeiras onde canta o sabiá" - metonímia (parte pelo todo = Brasil)
"Ela é uma flor" - metáfora (mulher = delicada, bela)''',
        'dicas': 'Metáfora SEM "como" / Comparação COM "como" - não confunda!'
    },

    'Literatura Brasileira - Barroco': {
        'conteudo': '''BARROCO (século XVII - 1601-1768): Primeiro movimento literário brasileiro

CONTEXTO HISTÓRICO:
- Contrarreforma católica (reação ao protestantismo)
- Brasil colonial, exploração do ouro
- Conflito fé × razão, céu × terra

CARACTERÍSTICAS:
- DUALISMO/CONFLITO: Espiritual × Carnal, Deus × Diabo
- CULTISMO (Gongorismo): Jogo de palavras, rebuscamento
- CONCEPTISMO (Quevedismo): Jogo de ideias, raciocínio complexo
- Linguagem rebuscada, inversões sintáticas (hipérbato)
- Figuras: antítese, paradoxo, hipérbole

PRINCIPAIS AUTORES:
GREGÓRIO DE MATOS (Boca do Inferno):
- Poesia satírica (crítica à sociedade baiana)
- Poesia lírica (amor, dualismo espírito×carne)
- Poesia religiosa (culpa, pecado, arrependimento)

PADRE ANTÔNIO VIEIRA:
- Sermões (oratória barroca)
- Defesa dos índios e escravizados
- "Sermão da Sexagésima" (crítica a pregadores vazios)''',
        'exemplos': '''GREGÓRIO DE MATOS - Dualismo:
"Que és terra, homem, e em terra hás de tornar-te,
Te lembra hoje Deus por sua Igreja;
Lembra-te Deus que és pó para humilhar-te"
→ Tema da morte, efemeridade da vida, memento mori''',
        'dicas': 'BARROCO = CONFLITO! Sempre há tensão entre opostos. Procure antíteses e paradoxos.'
    },

    'Gramática - Classes de Palavras': {
        'conteudo': '''10 CLASSES GRAMATICAIS (palavras da língua):

VARIÁVEIS (flexionam):
1. SUBSTANTIVO: Nomeia seres (mesa, João, amor)
2. ADJETIVO: Caracteriza substantivo (bonito, azul)
3. ARTIGO: Determina substantivo (o, a, um, uma)
4. PRONOME: Substitui/acompanha substantivo (eu, este, meu)
5. NUMERAL: Indica número/ordem (dois, primeiro)
6. VERBO: Ação, estado, fenômeno (correr, ser, chover)

INVARIÁVEIS (não flexionam):
7. ADVÉRBIO: Modifica verbo, adjetivo, outro advérbio (muito, aqui, hoje)
8. PREPOSIÇÃO: Liga termos (a, de, para, com, em)
9. CONJUNÇÃO: Liga orações (e, mas, que, se)
10. INTERJEIÇÃO: Emoção (Ai! Oba! Nossa!)

DICA DE IDENTIFICAÇÃO:
- Substantivo: Pode usar artigo na frente? (O/A ___)
- Adjetivo: Característica? Pode variar em gênero? (bonito/bonita)
- Advérbio: Termina em -mente? Indica circunstância?
- Preposição: Palavra pequena que liga? (Morei EM SP)
- Conjunção: Liga orações? (Estudei MAS não passei)''',
        'exemplos': '''Frase: "O jovem estudante chegou MUITO cedo AQUI."
O = artigo / jovem = adjetivo / estudante = substantivo
chegou = verbo / MUITO = advérbio (intensidade)
cedo = advérbio (tempo) / AQUI = advérbio (lugar)''',
        'dicas': 'Advérbio modifica VERBO, ADJETIVO ou OUTRO ADVÉRBIO. Adjetivo só modifica SUBSTANTIVO!'
    },

    'Variação Linguística': {
        'conteudo': '''Variação linguística são as diferenças no uso da língua:

TIPOS DE VARIAÇÃO:

1. REGIONAL/DIATÓPICA: Por região geográfica
- "Aipim" (RJ) = "Macaxeira" (NE) = "Mandioca" (Sul)
- Sotaques diferentes (paulista, carioca, gaúcho)

2. SOCIAL/DIASTRÁTICA: Por classe social, escolaridade
- Norma culta × norma popular
- "Nós fomos" (culta) × "Nóis foi" (popular)

3. SITUACIONAL/DIAFÁSICA: Por contexto/situação
- Formal (reunião, prova) × Informal (amigos, família)
- "Você poderia..." (formal) × "Cê pode..." (informal)

4. HISTÓRICA/DIACRÔNICA: Ao longo do tempo
- "Vossa mercê" → "vosmecê" → "você" → "cê"
- Arcaísmos (palavras antigas): "asinha" = rápido

PRECONCEITO LINGUÍSTICO:
- NÃO existe "português errado" e "certo" absoluto
- Existe adequação ao contexto
- Variedades populares são legítimas e sistemáticas
- Respeitar todas as formas de falar''',
        'exemplos': '''REGIONAL: "Tu vai" (RS) × "Você vai" (SP)
SOCIAL: "Os menino" (popular) × "Os meninos" (culta)
SITUACIONAL: WhatsApp ("blz, vlw") × E-mail formal ("Prezado senhor...")''',
        'dicas': 'ENEM NUNCA diz que uma variante é "errada"! Fala em ADEQUAÇÃO ao contexto.'
    },

    # MATEMÁTICA
    'Razão e Proporção': {
        'conteudo': '''RAZÃO: Comparação entre dois números por divisão (a/b)

PROPORÇÃO: Igualdade entre duas razões
a/b = c/d → Lê-se: "a está para b assim como c está para d"

PROPRIEDADE FUNDAMENTAL:
a/b = c/d ⟺ a·d = b·c (produto dos meios = produto dos extremos)

TIPOS DE PROPORÇÃO:

1. DIRETAMENTE PROPORCIONAL:
- Se uma grandeza aumenta, a outra aumenta na mesma proporção
- Se dobra uma, dobra a outra
- Exemplo: distância e consumo de combustível

2. INVERSAMENTE PROPORCIONAL:
- Se uma aumenta, a outra diminui
- Se dobra uma, a outra cai pela metade
- Exemplo: velocidade e tempo (mesma distância)

DIVISÃO PROPORCIONAL:
- Direta: x/a = y/b = z/c = k (constante)
- Inversa: x·a = y·b = z·c = k (constante)

REGRA DE TRÊS:
Direta: a/b = c/x → setas mesmo sentido ↑↑
Inversa: a/b = x/c → setas sentidos opostos ↑↓''',
        'exemplos': '''Ex: 5 operários fazem uma obra em 12 dias. Quantos dias levam 8 operários?
INVERSAMENTE PROPORCIONAL (+ operários = - dias)
5 op --- 12 dias
8 op --- x dias
5/8 = x/12 (inverter um lado!)
5·12 = 8·x → 60 = 8x → x = 7,5 dias''',
        'dicas': 'ATALHO: Na dúvida se é direta ou inversa? Pergunte: "Dobrando uma, a outra dobra ou cai pela metade?"'
    },

    'Porcentagem': {
        'conteudo': '''PORCENTAGEM: Fração de denominador 100
25% = 25/100 = 0,25

CÁLCULOS ESSENCIAIS:

1. Calcular x% de um valor:
   Valor × (x/100)
   Ex: 30% de 200 = 200 × 0,30 = 60

2. Fator de aumento: (1 + i/100)
   Ex: Aumento de 15% → multiplica por 1,15

3. Fator de desconto: (1 - i/100)
   Ex: Desconto de 20% → multiplica por 0,80

4. Variação percentual:
   Δ% = [(Vfinal - Vinicial)/Vinicial] × 100

AUMENTOS/DESCONTOS SUCESSIVOS:
⚠️ NÃO SOME OS PERCENTUAIS!
Multiplique os fatores:
- 10% aumento + 20% aumento: 1,10 × 1,20 = 1,32 = +32%
- 20% aumento + 20% desconto: 1,20 × 0,80 = 0,96 = -4%

PORCENTAGEM DO PORCENTAGEM:
"30% de 40%" = 0,30 × 0,40 = 0,12 = 12%''',
        'exemplos': '''Ex: Preço subiu 50% e depois caiu 50%. Voltou ao original?
NÃO! 1,50 × 0,50 = 0,75 = -25% (perdeu 25%)
Se era R$100: 100→150→75''',
        'dicas': 'DECOREBA ÚTIL: 50%=metade | 25%=1/4 | 10%=÷10 | 1%=÷100 | 200%=dobro'
    },

    'Funções do 1º Grau': {
        'conteudo': '''FUNÇÃO AFIM: f(x) = ax + b (reta no plano cartesiano)

COEFICIENTES:
- a = coeficiente angular (inclinação da reta)
- b = coeficiente linear (onde corta eixo y)

COEFICIENTE ANGULAR (a):
- a > 0: função CRESCENTE (reta sobe ↗)
- a < 0: função DECRESCENTE (reta desce ↘)
- a = 0: função CONSTANTE (reta horizontal)

ZERO DA FUNÇÃO (raiz):
Valor de x onde f(x) = 0
ax + b = 0 → x = -b/a

GRÁFICO:
- Sempre uma RETA
- Precisa de 2 pontos para traçar
- Corta eixo y em (0, b)
- Corta eixo x em (-b/a, 0)

APLICAÇÕES:
- Conversão de temperatura: C = (5/9)(F-32)
- Custo total: C = Fixo + Variável·quantidade
- Depreciação linear''',
        'exemplos': '''Ex: Táxi cobra R$5 de bandeirada + R$3 por km
f(x) = 5 + 3x onde x = km rodados
- Bandeirada = coef. linear (b=5)
- Preço/km = coef. angular (a=3)
10km: f(10) = 5 + 3(10) = R$35''',
        'dicas': 'Crescente ou decrescente? Olhe o "a"! Positivo=sobe, Negativo=desce'
    },

    'Probabilidade': {
        'conteudo': '''PROBABILIDADE: Chance de um evento ocorrer

FÓRMULA BÁSICA:
P(A) = número de casos favoráveis / número de casos possíveis

PROPRIEDADES:
- 0 ≤ P(A) ≤ 1 (ou 0% ≤ P ≤ 100%)
- P(certo) = 1
- P(impossível) = 0
- P(não A) = 1 - P(A)

EVENTOS:
- MUTUAMENTE EXCLUSIVOS: Não ocorrem juntos
  P(A ou B) = P(A) + P(B)
  
- INDEPENDENTES: Um não afeta o outro
  P(A e B) = P(A) × P(B)

PROBABILIDADE CONDICIONAL:
P(A|B) = probabilidade de A dado que B ocorreu
P(A|B) = P(A∩B) / P(B)

COMPLEMENTAR:
P(pelo menos 1) = 1 - P(nenhum)
Útil quando é mais fácil calcular o complemento!''',
        'exemplos': '''Ex: Dados honestos (2 dados)
- Total de resultados: 6 × 6 = 36
- P(soma=7): (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6 casos
  P = 6/36 = 1/6

Ex: 3 moedas. P(pelo menos 1 cara)?
P(nenhuma cara) = P(todas coroa) = (1/2)³ = 1/8
P(pelo menos 1 cara) = 1 - 1/8 = 7/8''',
        'dicas': 'MACETE: "Pelo menos 1" → use o complementar! P = 1 - P(nenhum)'
    },

    'Geometria Plana - Áreas': {
        'conteudo': '''FÓRMULAS DE ÁREA DAS PRINCIPAIS FIGURAS:

QUADRADO: A = l² (lado ao quadrado)

RETÂNGULO: A = b × h (base × altura)

TRIÂNGULO: A = (b × h)/2
- Equilátero: A = (l²√3)/4

PARALELOGRAMO: A = b × h

TRAPÉZIO: A = [(B + b) × h]/2
(B = base maior, b = base menor)

LOSANGO: A = (D × d)/2 (diagonais)

CÍRCULO: A = πr² (pi × raio²)
- Setor circular: A = (θ/360°) × πr²

POLÍGONO REGULAR: A = (P × a)/2
(P = perímetro, a = apótema)

RELAÇÕES:
- Área do círculo inscrito no quadrado: A = (l²π)/4
- Razão de áreas com semelhança: A₁/A₂ = k²''',
        'exemplos': '''Ex: Terreno retangular 15m × 8m
A = 15 × 8 = 120 m²

Ex: Triângulo base 10cm, altura 6cm
A = (10 × 6)/2 = 30 cm²

Ex: Círculo raio 5cm
A = π × 5² = 25π ≈ 78,5 cm²''',
        'dicas': 'NUNCA confunda ÁREA com PERÍMETRO! Área=m², Perímetro=m'
    },

    # CIÊNCIAS HUMANAS
    'Brasil Colônia': {
        'conteudo': '''BRASIL COLÔNIA (1500-1822):

PERÍODO PRÉ-COLONIAL (1500-1530):
- Exploração do pau-brasil
- Escambo com indígenas
- Feitorias no litoral
- Expedições guarda-costas (franceConteúdo expandido em desenvolvimento...''',
        'exemplos': 'Exemplos práticos em desenvolvimento...',
        'dicas': 'Dicas de estudo em desenvolvimento...'
    }
}

def adicionar_explicacoes_completas():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Buscar todos os tópicos
    cur.execute('SELECT id, title FROM topics ORDER BY id')
    topics = cur.fetchall()
    
    count = 0
    for topic_id, title in topics:
        # Verificar se já existe explicação
        existing = cur.execute('SELECT id FROM explicacoes WHERE topic_id=?', (topic_id,)).fetchone()
        if existing:
            continue
            
        # Extrair título base
        titulo_base = title.split(' - ')[0].strip()
        
        # Buscar explicação correspondente
        if titulo_base in EXPLICACOES_COMPLETAS:
            dados = EXPLICACOES_COMPLETAS[titulo_base]
            cur.execute('''INSERT INTO explicacoes (topic_id, titulo, conteudo_detalhado, exemplos, dicas) 
                          VALUES (?,?,?,?,?)''',
                       (topic_id, titulo_base, dados['conteudo'], dados['exemplos'], dados['dicas']))
            count += 1
    
    conn.commit()
    conn.close()
    print(f'✅ {count} novas explicações adicionadas!')

if __name__ == '__main__':
    adicionar_explicacoes_completas()
