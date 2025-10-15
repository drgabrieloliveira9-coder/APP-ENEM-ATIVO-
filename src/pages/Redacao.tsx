import { useState } from "react";
import { Send, FileText, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import Navbar from "@/components/Navbar";
import { supabase } from "@/integrations/supabase/client";

export default function Redacao() {
  const { toast } = useToast();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [result, setResult] = useState<{ score: number; feedback: string } | null>(null);
  const [essays, setEssays] = useState<any[]>([]);

  const wordCount = content.trim().split(/\s+/).filter(Boolean).length;

  const handleSubmit = async () => {
    if (!title.trim()) {
      toast({
        title: "Título obrigatório",
        description: "Por favor, adicione um título para sua redação.",
        variant: "destructive",
      });
      return;
    }

    if (wordCount < 100) {
      toast({
        title: "Redação muito curta",
        description: "A redação deve ter no mínimo 100 palavras.",
        variant: "destructive",
      });
      return;
    }

    setIsEvaluating(true);

    try {
      const { data: evalData, error: evalError } = await supabase.functions.invoke(
        "evaluate-essay",
        {
          body: { title, content },
        }
      );

      if (evalError) throw evalError;

      const { data: user } = await supabase.auth.getUser();
      
      if (user.user) {
        const { error: insertError } = await supabase.from("essays").insert({
          user_id: user.user.id,
          title,
          content,
          score: evalData.score,
          feedback: evalData.feedback,
        });

        if (insertError) throw insertError;

        // Update progress
        const { data: progress } = await supabase
          .from("user_progress")
          .select()
          .eq("user_id", user.user.id)
          .single();

        if (progress) {
          await supabase
            .from("user_progress")
            .update({
              essays_written: progress.essays_written + 1,
              total_score: progress.total_score + evalData.score,
              updated_at: new Date().toISOString(),
            })
            .eq("user_id", user.user.id);
        } else {
          await supabase.from("user_progress").insert({
            user_id: user.user.id,
            essays_written: 1,
            total_score: evalData.score,
          });
        }
      }

      setResult({ score: evalData.score, feedback: evalData.feedback });
      
      toast({
        title: "Redação avaliada!",
        description: `Nota: ${evalData.score}/1000 pontos`,
      });
    } catch (error: any) {
      toast({
        title: "Erro ao avaliar",
        description: error.message || "Tente novamente mais tarde.",
        variant: "destructive",
      });
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleNewEssay = () => {
    setTitle("");
    setContent("");
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2 text-glow">Redação ENEM</h1>
            <p className="text-muted-foreground">
              Escreva sua redação e receba avaliação automática com IA
            </p>
          </div>
          <Card className="card-glow">
            <CardContent className="pt-6">
              <div className="text-center">
                <FileText className="h-8 w-8 text-primary mx-auto mb-2" />
                <div className="text-sm text-muted-foreground">
                  {wordCount} palavras
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="max-w-4xl mx-auto">
          {!result ? (
            <Card className="card-glow">
              <CardHeader>
                <CardTitle>Nova Redação</CardTitle>
                <CardDescription>
                  Mínimo de 100 palavras. A IA avaliará com base nos critérios do ENEM.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Título da Redação
                  </label>
                  <Input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Ex: A importância da educação no Brasil"
                    disabled={isEvaluating}
                  />
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Texto da Redação
                  </label>
                  <Textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Escreva sua redação aqui..."
                    className="min-h-[400px] resize-none"
                    disabled={isEvaluating}
                  />
                </div>

                <Button
                  onClick={handleSubmit}
                  disabled={isEvaluating || wordCount < 100}
                  className="w-full hover-glow"
                  size="lg"
                >
                  <Send className="mr-2 h-5 w-5" />
                  {isEvaluating ? "Avaliando..." : "Enviar para Avaliação"}
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              <Card className="card-glow border-primary">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Resultado da Avaliação</CardTitle>
                    <TrendingUp className="h-6 w-6 text-primary" />
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="text-center py-8">
                    <div className="text-6xl font-bold text-primary mb-2">
                      {result.score}
                    </div>
                    <div className="text-muted-foreground">pontos de 1000</div>
                    <div className="mt-4">
                      <div className="h-3 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-primary transition-all duration-500"
                          style={{ width: `${(result.score / 1000) * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold mb-3">Feedback Detalhado</h3>
                    <div className="bg-muted/50 rounded-lg p-4">
                      <p className="text-foreground leading-relaxed whitespace-pre-wrap">
                        {result.feedback}
                      </p>
                    </div>
                  </div>

                  <Button
                    onClick={handleNewEssay}
                    className="w-full hover-glow"
                    size="lg"
                  >
                    Escrever Nova Redação
                  </Button>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader>
                  <CardTitle>Sua Redação</CardTitle>
                </CardHeader>
                <CardContent>
                  <h3 className="font-semibold text-lg mb-2">{title}</h3>
                  <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {content}
                  </p>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
