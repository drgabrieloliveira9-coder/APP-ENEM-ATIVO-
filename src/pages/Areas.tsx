import { Link } from "react-router-dom";
import { BookOpen, Atom, Calculator, Globe } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";

const areas = [
  {
    id: "linguagens",
    title: "Linguagens, Códigos e suas Tecnologias",
    description: "Português, Literatura, Língua Estrangeira, Artes, Educação Física e Tecnologias da Informação",
    icon: BookOpen,
    color: "bg-blue-500/10 text-blue-500",
    resumosCount: 250,
  },
  {
    id: "matematica",
    title: "Matemática e suas Tecnologias",
    description: "Matemática e suas aplicações em diversos contextos",
    icon: Calculator,
    color: "bg-green-500/10 text-green-500",
    resumosCount: 200,
  },
  {
    id: "natureza",
    title: "Ciências da Natureza e suas Tecnologias",
    description: "Química, Física e Biologia",
    icon: Atom,
    color: "bg-purple-500/10 text-purple-500",
    resumosCount: 250,
  },
  {
    id: "humanas",
    title: "Ciências Humanas e suas Tecnologias",
    description: "História, Geografia, Filosofia e Sociologia",
    icon: Globe,
    color: "bg-orange-500/10 text-orange-500",
    resumosCount: 200,
  },
];

export default function Areas() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 text-glow">Áreas de Conhecimento</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Escolha uma área para acessar resumos, questões e conteúdos específicos
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {areas.map((area) => {
            const Icon = area.icon;
            return (
              <Card key={area.id} className="card-glow hover-glow transition-all duration-300">
                <CardHeader>
                  <div className={`w-16 h-16 rounded-xl ${area.color} flex items-center justify-center mb-4`}>
                    <Icon className="h-8 w-8" />
                  </div>
                  <CardTitle className="text-xl">{area.title}</CardTitle>
                  <CardDescription className="text-base mt-2">
                    {area.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">
                      {area.resumosCount}+ resumos disponíveis
                    </span>
                    <Button asChild>
                      <Link to={`/resumos?area=${area.id}`}>
                        Acessar
                      </Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
}
