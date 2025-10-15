import { useEffect, useState } from "react";
import { Trophy, Target, BookOpen, PenTool, Calendar, Award } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import Navbar from "@/components/Navbar";
import { supabase } from "@/integrations/supabase/client";

interface UserProgress {
  questions_answered: number;
  questions_correct: number;
  essays_written: number;
  study_days_completed: number;
  total_score: number;
}

export default function Progresso() {
  const [progress, setProgress] = useState<UserProgress>({
    questions_answered: 0,
    questions_correct: 0,
    essays_written: 0,
    study_days_completed: 0,
    total_score: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const { data: user } = await supabase.auth.getUser();
      
      if (user.user) {
        const { data, error } = await supabase
          .from("user_progress")
          .select()
          .eq("user_id", user.user.id)
          .single();

        if (error && error.code !== "PGRST116") throw error;

        if (data) {
          setProgress(data);
        }
      }
    } catch (error) {
      console.error("Error loading progress:", error);
    } finally {
      setLoading(false);
    }
  };

  const accuracyPercentage = progress.questions_answered > 0
    ? Math.round((progress.questions_correct / progress.questions_answered) * 100)
    : 0;

  const totalActivities =
    progress.questions_answered + progress.essays_written + progress.study_days_completed;
  const overallProgress = Math.min(Math.round((totalActivities / 100) * 100), 100);

  const isApproved = progress.total_score >= 900;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-glow">Meu Progresso</h1>
          <p className="text-muted-foreground">
            Acompanhe sua evolução nos estudos para o ENEM
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto" />
          </div>
        ) : (
          <div className="max-w-6xl mx-auto space-y-6">
            {/* Overall Progress */}
            <Card className="card-glow">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-6 w-6 text-primary" />
                  Progresso Geral
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium">Atividades Concluídas</span>
                      <span className="text-sm text-muted-foreground">
                        {overallProgress}%
                      </span>
                    </div>
                    <Progress value={overallProgress} className="h-3" />
                  </div>
                  <div className="text-center pt-4">
                    <div className="text-5xl font-bold text-primary mb-2">
                      {totalActivities}
                    </div>
                    <div className="text-muted-foreground">
                      atividades realizadas
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stats Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="card-glow">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base flex items-center gap-2">
                    <BookOpen className="h-5 w-5 text-primary" />
                    Questões
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-1">
                    {progress.questions_answered}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    respondidas
                  </div>
                  <div className="mt-3 pt-3 border-t">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Acertos</span>
                      <span className="font-semibold text-success">
                        {accuracyPercentage}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base flex items-center gap-2">
                    <PenTool className="h-5 w-5 text-primary" />
                    Redações
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-1">
                    {progress.essays_written}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    escritas
                  </div>
                  <div className="mt-3 pt-3 border-t">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Pontuação média</span>
                      <span className="font-semibold">
                        {progress.essays_written > 0
                          ? Math.round(progress.total_score / progress.essays_written)
                          : 0}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-primary" />
                    Dias de Estudo
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-1">
                    {progress.study_days_completed}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    concluídos
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Trophy className="h-5 w-5 text-primary" />
                    Pontuação Total
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-1">
                    {progress.total_score}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    pontos acumulados
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Achievement Badge */}
            {isApproved && (
              <Card className="card-glow border-success bg-success/5">
                <CardContent className="pt-6">
                  <div className="text-center">
                    <Award className="h-16 w-16 text-success mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-success mb-2">
                      🎉 Parabéns! Aprovado no ENEM!
                    </h2>
                    <p className="text-muted-foreground">
                      Você atingiu mais de 900 pontos! Continue assim!
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
