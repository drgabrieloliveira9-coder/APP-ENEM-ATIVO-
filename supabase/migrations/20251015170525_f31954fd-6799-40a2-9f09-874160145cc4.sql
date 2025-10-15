-- Create enum for question areas
CREATE TYPE question_area AS ENUM ('Linguagens', 'Matemática', 'Ciências Humanas', 'Ciências da Natureza');

-- Create questions table
CREATE TABLE public.questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  area question_area NOT NULL,
  subject TEXT NOT NULL,
  question TEXT NOT NULL,
  option_a TEXT NOT NULL,
  option_b TEXT NOT NULL,
  option_c TEXT NOT NULL,
  option_d TEXT NOT NULL,
  option_e TEXT NOT NULL,
  correct_answer TEXT NOT NULL CHECK (correct_answer IN ('a', 'b', 'c', 'd', 'e')),
  explanation TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Create essays table
CREATE TABLE public.essays (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  score INTEGER CHECK (score >= 0 AND score <= 1000),
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Create schedules table
CREATE TABLE public.schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  hours_per_day INTEGER NOT NULL,
  days_until_exam INTEGER NOT NULL,
  schedule_data JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Create user_progress table
CREATE TABLE public.user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
  questions_answered INTEGER DEFAULT 0,
  questions_correct INTEGER DEFAULT 0,
  essays_written INTEGER DEFAULT 0,
  study_days_completed INTEGER DEFAULT 0,
  total_score INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Create question_attempts table to track individual attempts
CREATE TABLE public.question_attempts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  question_id UUID REFERENCES public.questions(id) ON DELETE CASCADE,
  user_answer TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.essays ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.question_attempts ENABLE ROW LEVEL SECURITY;

-- RLS Policies for questions (public read)
CREATE POLICY "Questions are viewable by everyone"
  ON public.questions FOR SELECT
  USING (true);

-- RLS Policies for essays (user-specific)
CREATE POLICY "Users can view their own essays"
  ON public.essays FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own essays"
  ON public.essays FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for schedules (user-specific)
CREATE POLICY "Users can view their own schedules"
  ON public.schedules FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own schedules"
  ON public.schedules FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for user_progress (user-specific)
CREATE POLICY "Users can view their own progress"
  ON public.user_progress FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own progress"
  ON public.user_progress FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own progress"
  ON public.user_progress FOR UPDATE
  USING (auth.uid() = user_id);

-- RLS Policies for question_attempts (user-specific)
CREATE POLICY "Users can view their own attempts"
  ON public.question_attempts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own attempts"
  ON public.question_attempts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Insert 20 sample questions (5 per area)

-- Linguagens
INSERT INTO public.questions (area, subject, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation) VALUES
('Linguagens', 'Português', 'Qual figura de linguagem está presente na frase: "Aquele rapaz é um verdadeiro leão"?', 'Metáfora', 'Metonímia', 'Hipérbole', 'Eufemismo', 'Ironia', 'a', 'A metáfora é uma figura de linguagem que estabelece uma comparação implícita entre dois elementos, atribuindo características de um ao outro sem usar conectivos comparativos.'),
('Linguagens', 'Inglês', 'What is the correct form of the verb in: "She ___ to the gym every day"?', 'go', 'goes', 'going', 'gone', 'went', 'b', 'Na terceira pessoa do singular do Simple Present, adicionamos "s" ao verbo. Portanto, "She goes" é a forma correta.'),
('Linguagens', 'Literatura', 'Qual movimento literário brasileiro teve como principal característica o nacionalismo e a idealização da natureza?', 'Realismo', 'Romantismo', 'Modernismo', 'Barroco', 'Parnasianismo', 'b', 'O Romantismo brasileiro (século XIX) valorizava o nacionalismo, a natureza tropical e a figura do índio como herói nacional.'),
('Linguagens', 'Artes', 'Qual artista brasileiro é considerado um dos principais nomes do movimento modernista nas artes plásticas?', 'Tarsila do Amaral', 'Cândido Portinari', 'Di Cavalcanti', 'Anita Malfatti', 'Todos os anteriores', 'e', 'Todos esses artistas foram figuras centrais do modernismo brasileiro, cada um com contribuições únicas para a arte nacional.'),
('Linguagens', 'Interpretação', 'Em um texto argumentativo, qual é a principal função do parágrafo de conclusão?', 'Apresentar novos argumentos', 'Retomar a tese e sintetizar os argumentos', 'Contradizer a introdução', 'Apresentar dados estatísticos', 'Fazer perguntas retóricas', 'b', 'O parágrafo de conclusão deve retomar a tese apresentada na introdução e sintetizar os principais argumentos desenvolvidos no texto.');

-- Matemática
INSERT INTO public.questions (area, subject, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation) VALUES
('Matemática', 'Álgebra', 'Qual é o valor de x na equação 2x + 5 = 15?', 'x = 3', 'x = 5', 'x = 7', 'x = 10', 'x = 12', 'b', 'Resolvendo: 2x + 5 = 15 → 2x = 10 → x = 5'),
('Matemática', 'Geometria', 'A área de um triângulo com base 10 cm e altura 6 cm é:', '30 cm²', '60 cm²', '16 cm²', '25 cm²', '36 cm²', 'a', 'A área do triângulo é calculada por: A = (base × altura) / 2 = (10 × 6) / 2 = 30 cm²'),
('Matemática', 'Estatística', 'A média aritmética dos números 5, 8, 10, 12 e 15 é:', '8', '9', '10', '11', '12', 'c', 'Média = (5 + 8 + 10 + 12 + 15) / 5 = 50 / 5 = 10'),
('Matemática', 'Probabilidade', 'Ao jogar um dado comum, qual é a probabilidade de obter um número par?', '1/6', '1/3', '1/2', '2/3', '5/6', 'c', 'Um dado tem 6 faces, sendo 3 números pares (2, 4, 6). Portanto, P = 3/6 = 1/2 ou 50%'),
('Matemática', 'Funções', 'Qual é o valor de f(2) para a função f(x) = 3x - 1?', '4', '5', '6', '7', '8', 'b', 'Substituindo x = 2: f(2) = 3(2) - 1 = 6 - 1 = 5');

-- Ciências Humanas
INSERT INTO public.questions (area, subject, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation) VALUES
('Ciências Humanas', 'História', 'Qual evento marcou o fim da Idade Média e o início da Idade Moderna?', 'Descobrimento da América', 'Queda de Constantinopla', 'Revolução Francesa', 'Reforma Protestante', 'Revolução Industrial', 'b', 'A queda de Constantinopla em 1453 é tradicionalmente considerada o marco do fim da Idade Média e início da Idade Moderna.'),
('Ciências Humanas', 'Geografia', 'Qual é o bioma brasileiro caracterizado por vegetação arbustiva e clima semiárido?', 'Amazônia', 'Cerrado', 'Caatinga', 'Pantanal', 'Mata Atlântica', 'c', 'A Caatinga é o único bioma exclusivamente brasileiro, com vegetação adaptada ao clima semiárido do Nordeste.'),
('Ciências Humanas', 'Sociologia', 'Segundo Karl Marx, qual é o principal fator de divisão da sociedade capitalista?', 'A religião', 'A luta de classes', 'A educação', 'A tecnologia', 'A democracia', 'b', 'Para Marx, a sociedade capitalista é dividida fundamentalmente pela luta de classes entre burguesia (donos dos meios de produção) e proletariado (trabalhadores).'),
('Ciências Humanas', 'Filosofia', 'Qual filósofo grego é conhecido pela frase "Conhece-te a ti mesmo"?', 'Platão', 'Aristóteles', 'Sócrates', 'Pitágoras', 'Tales de Mileto', 'c', 'Embora inscrita no templo de Apolo em Delfos, essa máxima foi adotada por Sócrates como fundamento de sua filosofia.'),
('Ciências Humanas', 'Atualidades', 'Qual organização internacional foi criada após a Segunda Guerra Mundial para promover a paz?', 'OEA', 'ONU', 'OTAN', 'OMC', 'FMI', 'b', 'A Organização das Nações Unidas (ONU) foi criada em 1945 com o objetivo de manter a paz e segurança internacionais.');

-- Ciências da Natureza
INSERT INTO public.questions (area, subject, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation) VALUES
('Ciências da Natureza', 'Biologia', 'A fotossíntese é um processo realizado pelos seres clorofilados. Quais são seus principais produtos?', 'Glicose e gás oxigênio', 'Glicose e gás carbônico', 'Água e gás oxigênio', 'Água e gás carbônico', 'Amido e água', 'a', 'A fotossíntese produz glicose (C₆H₁₂O₆) e gás oxigênio (O₂). A glicose é usada como energia e o oxigênio é liberado na atmosfera.'),
('Ciências da Natureza', 'Química', 'Qual é o número atômico do elemento Carbono (C)?', '4', '6', '8', '12', '14', 'b', 'O número atômico representa o número de prótons no núcleo. O Carbono tem 6 prótons, portanto seu número atômico é 6.'),
('Ciências da Natureza', 'Física', 'Qual grandeza física é medida em Newtons (N)?', 'Massa', 'Força', 'Velocidade', 'Energia', 'Potência', 'b', 'Newton é a unidade de medida de força no Sistema Internacional (SI), em homenagem a Isaac Newton.'),
('Ciências da Natureza', 'Ecologia', 'Qual é a principal consequência do efeito estufa intensificado?', 'Diminuição da temperatura global', 'Aquecimento global', 'Aumento da camada de ozônio', 'Redução dos oceanos', 'Extinção das plantas', 'b', 'O efeito estufa intensificado pela emissão de gases causa o aquecimento global, elevando a temperatura média do planeta.'),
('Ciências da Natureza', 'Genética', 'Qual cientista é considerado o pai da genética moderna?', 'Charles Darwin', 'Gregor Mendel', 'Louis Pasteur', 'Alexander Fleming', 'Albert Einstein', 'b', 'Gregor Mendel, monge e cientista, desenvolveu as leis fundamentais da hereditariedade através de experimentos com ervilhas.');