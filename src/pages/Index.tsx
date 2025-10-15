import { Link } from "react-router-dom";
import { BookOpen, HelpCircle, Edit3, TrendingUp, Award, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Navbar from "@/components/Navbar";

const stats = [
  { label: "Resumos", value: "900+", icon: BookOpen, color: "text-primary" },
  { label: "Questões", value: "5.000+", icon: HelpCircle, color: "text-primary" },
  { label: "Simulados", value: "Ilimitados", icon: Target, color: "text-primary" },
  { label: "Redações", value: "IA Corrige", icon: Edit3, color: "text-primary" },
];

const features = [
  {
    title: "Resumos Completos",
    description: "Mais de 900 resumos de todas as matérias do ENEM, organizados por área de conhecimento.",
    icon: BookOpen,
    href: "/resumos",
  },
  {
    title: "Questões Práticas",
    description: "Milhares de questões com feedback visual e explicações detalhadas para seu aprendizado.",
    icon: HelpCircle,
    href: "/questoes",
  },
  {
    title: "Correção de Redação",
    description: "Inteligência Artificial avalia sua redação e fornece nota de 0 a 1000 com feedback detalhado.",
    icon: Edit3,
    href: "/redacao",
  },
  {
    title: "Acompanhe seu Progresso",
    description: "Gráficos e estatísticas para visualizar sua evolução e identificar pontos de melhoria.",
    icon: TrendingUp,
    href: "/progresso",
  },
];

export default function Index() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <section className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Award className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-primary">Prepare-se para o ENEM 2025</span>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-6 text-glow">
            Sua Aprovação Começa Aqui
          </h1>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Plataforma completa com resumos, questões, simulados e correção automática de redação.
            Estude de forma inteligente e alcance seus objetivos.
          </p>

          <div className="flex flex-wrap gap-4 justify-center">
            <Button size="lg" asChild className="hover-glow">
              <Link to="/areas">
                <BookOpen className="mr-2 h-5 w-5" />
                Começar a Estudar
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild className="hover-glow">
              <Link to="/questoes">
                <HelpCircle className="mr-2 h-5 w-5" />
                Fazer Questões
              </Link>
            </Button>
          </div>
        </section>

        {/* Stats Grid */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.label} className="card-glow hover-glow">
                <CardContent className="pt-6 text-center">
                  <Icon className={`h-8 w-8 mx-auto mb-2 ${stat.color}`} />
                  <div className="text-2xl font-bold mb-1">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </CardContent>
              </Card>
            );
          })}
        </section>

        {/* Features Grid */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 text-glow">
            Tudo que Você Precisa para Passar
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Card key={feature.title} className="card-glow hover-glow transition-all duration-300">
                  <CardHeader>
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 rounded-lg bg-primary/10">
                        <Icon className="h-6 w-6 text-primary" />
                      </div>
                      <CardTitle>{feature.title}</CardTitle>
                    </div>
                    <CardDescription className="text-base">
                      {feature.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" asChild className="w-full">
                      <Link to={feature.href}>Acessar</Link>
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>

        {/* CTA Section */}
        <section className="text-center bg-gradient-card rounded-2xl p-8 md:p-12 card-glow">
          <Award className="h-16 w-16 text-primary mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4">Conquiste seu Selo de Aprovado</h2>
          <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
            Ao atingir 900 pontos em nossos simulados, você receberá o selo especial "Aprovado no ENEM!"
          </p>
          <Button size="lg" asChild className="hover-glow">
            <Link to="/questoes">
              Começar Agora
            </Link>
          </Button>
        </section>
      </main>
    </div>
  );
}
