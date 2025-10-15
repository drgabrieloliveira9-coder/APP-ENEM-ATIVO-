import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, FileText } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";

// Dados de exemplo - em produção virão do backend
const resumosExemplo = [
  {
    id: 1,
    titulo: "Funções Sintáticas do Que",
    area: "linguagens",
    materia: "Português",
    conteudo: "O 'que' pode exercer diversas funções sintáticas nas orações...",
    tags: ["gramática", "sintaxe"],
  },
  {
    id: 2,
    titulo: "Romantismo no Brasil",
    area: "linguagens",
    materia: "Literatura",
    conteudo: "O Romantismo brasileiro teve início em 1836...",
    tags: ["literatura", "movimentos literários"],
  },
  {
    id: 3,
    titulo: "Funções Quadráticas",
    area: "matematica",
    materia: "Matemática",
    conteudo: "Uma função quadrática é dada por f(x) = ax² + bx + c...",
    tags: ["álgebra", "funções"],
  },
  {
    id: 4,
    titulo: "Eletroquímica",
    area: "natureza",
    materia: "Química",
    conteudo: "Estudo das reações químicas que produzem corrente elétrica...",
    tags: ["química", "energia"],
  },
  {
    id: 5,
    titulo: "Revolução Francesa",
    area: "humanas",
    materia: "História",
    conteudo: "A Revolução Francesa (1789-1799) foi um período de intensa mudança...",
    tags: ["história", "revoluções"],
  },
];

export default function Resumos() {
  const [searchParams] = useSearchParams();
  const areaFilter = searchParams.get("area");
  const [search, setSearch] = useState("");
  const [selectedResumo, setSelectedResumo] = useState<number | null>(null);

  const filteredResumos = resumosExemplo.filter((resumo) => {
    const matchesArea = !areaFilter || resumo.area === areaFilter;
    const matchesSearch = resumo.titulo.toLowerCase().includes(search.toLowerCase()) ||
                         resumo.materia.toLowerCase().includes(search.toLowerCase());
    return matchesArea && matchesSearch;
  });

  const areaNames: Record<string, string> = {
    linguagens: "Linguagens",
    matematica: "Matemática",
    natureza: "Ciências da Natureza",
    humanas: "Ciências Humanas",
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 text-glow">Resumos</h1>
          {areaFilter && (
            <Badge variant="outline" className="mb-4">
              {areaNames[areaFilter]}
            </Badge>
          )}
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <Input
              placeholder="Buscar por título ou matéria..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Lista de Resumos */}
          <div className="lg:col-span-1 space-y-4">
            {filteredResumos.map((resumo) => (
              <Card
                key={resumo.id}
                className={`cursor-pointer transition-all duration-300 hover-glow ${
                  selectedResumo === resumo.id ? "ring-2 ring-primary" : ""
                }`}
                onClick={() => setSelectedResumo(resumo.id)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-primary/10">
                      <FileText className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <CardTitle className="text-base">{resumo.titulo}</CardTitle>
                      <CardDescription className="text-sm mt-1">
                        {resumo.materia}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>

          {/* Conteúdo do Resumo */}
          <div className="lg:col-span-2">
            {selectedResumo ? (
              <Card className="card-glow">
                <CardHeader>
                  <CardTitle className="text-2xl">
                    {filteredResumos.find((r) => r.id === selectedResumo)?.titulo}
                  </CardTitle>
                  <div className="flex gap-2 mt-2">
                    {filteredResumos.find((r) => r.id === selectedResumo)?.tags.map((tag) => (
                      <Badge key={tag} variant="secondary">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </CardHeader>
                <CardContent className="prose prose-invert max-w-none">
                  <p className="text-foreground">
                    {filteredResumos.find((r) => r.id === selectedResumo)?.conteudo}
                  </p>
                  <p className="text-muted-foreground mt-4">
                    [Conteúdo completo do resumo será exibido aqui...]
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card className="card-glow h-full flex items-center justify-center">
                <CardContent className="text-center py-12">
                  <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                  <p className="text-lg text-muted-foreground">
                    Selecione um resumo para visualizar o conteúdo
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
