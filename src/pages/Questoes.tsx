import { useState, useEffect } from "react";
import { CheckCircle2, XCircle, Filter } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import Navbar from "@/components/Navbar";
import { supabase } from "@/integrations/supabase/client";

interface Question {
  id: string;
  area: string;
  subject: string;
  question: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  option_e: string;
  correct_answer: string;
  explanation: string;
}

const areas = ["Todas", "Linguagens", "Matemática", "Ciências Humanas", "Ciências da Natureza"];

export default function Questoes() {
  const { toast } = useToast();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedArea, setSelectedArea] = useState("Todas");
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [stats, setStats] = useState({ corretas: 0, total: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQuestions();
  }, [selectedArea]);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      let query = supabase.from("questions").select("*");
      
      if (selectedArea !== "Todas") {
        query = query.eq("area", selectedArea as any);
      }

      const { data, error } = await query;

      if (error) throw error;

      if (data && data.length > 0) {
        setQuestions(data);
        setCurrentIndex(0);
        setSelectedAnswer("");
        setShowFeedback(false);
      }
    } catch (error) {
      console.error("Error loading questions:", error);
      toast({
        title: "Erro ao carregar questões",
        description: "Tente novamente mais tarde.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentIndex];

  const handleSubmit = async () => {
    if (!selectedAnswer || !currentQuestion) return;
    
    setShowFeedback(true);
    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    
    setStats((prev) => ({
      corretas: prev.corretas + (isCorrect ? 1 : 0),
      total: prev.total + 1,
    }));

    try {
      const { data: user } = await supabase.auth.getUser();
      
      if (user.user) {
        await supabase.from("question_attempts").insert({
          user_id: user.user.id,
          question_id: currentQuestion.id,
          user_answer: selectedAnswer,
          is_correct: isCorrect,
        });

        const { data: progress } = await supabase
          .from("user_progress")
          .select()
          .eq("user_id", user.user.id)
          .single();

        if (progress) {
          await supabase
            .from("user_progress")
            .update({
              questions_answered: progress.questions_answered + 1,
              questions_correct: progress.questions_correct + (isCorrect ? 1 : 0),
              updated_at: new Date().toISOString(),
            })
            .eq("user_id", user.user.id);
        } else {
          await supabase.from("user_progress").insert({
            user_id: user.user.id,
            questions_answered: 1,
            questions_correct: isCorrect ? 1 : 0,
          });
        }
      }
    } catch (error) {
      console.error("Error saving attempt:", error);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedAnswer("");
      setShowFeedback(false);
    } else {
      toast({
        title: "Parabéns!",
        description: "Você completou todas as questões desta área!",
      });
    }
  };

  const isCorrect = currentQuestion && selectedAnswer === currentQuestion.correct_answer;

  const alternativas = currentQuestion ? [
    { id: "a", texto: currentQuestion.option_a },
    { id: "b", texto: currentQuestion.option_b },
    { id: "c", texto: currentQuestion.option_c },
    { id: "d", texto: currentQuestion.option_d },
    { id: "e", texto: currentQuestion.option_e },
  ] : [];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2 text-glow">Questões</h1>
            <p className="text-muted-foreground">Pratique com questões e receba feedback imediato</p>
          </div>
          <div className="flex items-center gap-4">
            <Select value={selectedArea} onValueChange={setSelectedArea}>
              <SelectTrigger className="w-[200px]">
                <Filter className="mr-2 h-4 w-4" />
                <SelectValue placeholder="Área" />
              </SelectTrigger>
              <SelectContent>
                {areas.map((area) => (
                  <SelectItem key={area} value={area}>
                    {area}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Card className="card-glow">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary">
                    {stats.total > 0 ? Math.round((stats.corretas / stats.total) * 100) : 0}%
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {stats.corretas} de {stats.total} corretas
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Questão */}
        <div className="max-w-4xl mx-auto">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto" />
            </div>
          ) : currentQuestion ? (
            <Card className="card-glow mb-6">
              <CardHeader>
                <div className="flex items-center justify-between mb-4">
                  <Badge variant="outline">{currentQuestion.subject}</Badge>
                  <Badge variant="secondary">{currentQuestion.area}</Badge>
                </div>
                <div className="text-sm text-muted-foreground mb-2">
                  Questão {currentIndex + 1} de {questions.length}
                </div>
                <CardTitle className="text-xl leading-relaxed">
                  {currentQuestion.question}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup value={selectedAnswer} onValueChange={setSelectedAnswer}>
                  <div className="space-y-3">
                    {alternativas.map((alt) => {
                      const isSelected = selectedAnswer === alt.id;
                      const isCorrectAnswer = alt.id === currentQuestion.correct_answer;
                    
                    let cardClass = "p-4 rounded-lg border-2 transition-all duration-300 cursor-pointer hover:border-primary/50";
                    
                    if (showFeedback) {
                      if (isCorrectAnswer) {
                        cardClass += " border-success bg-success/10";
                      } else if (isSelected && !isCorrect) {
                        cardClass += " border-destructive bg-destructive/10";
                      } else {
                        cardClass += " border-border";
                      }
                    } else {
                      cardClass += isSelected ? " border-primary bg-primary/10" : " border-border";
                    }

                    return (
                      <div key={alt.id} className={cardClass}>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3 flex-1">
                            <RadioGroupItem value={alt.id} id={alt.id} disabled={showFeedback} />
                            <Label
                              htmlFor={alt.id}
                              className="cursor-pointer flex-1 text-base"
                            >
                              <span className="font-semibold mr-2">{alt.id.toUpperCase()})</span>
                              {alt.texto}
                            </Label>
                          </div>
                          {showFeedback && isCorrectAnswer && (
                            <CheckCircle2 className="h-6 w-6 text-success" />
                          )}
                          {showFeedback && isSelected && !isCorrect && (
                            <XCircle className="h-6 w-6 text-destructive" />
                          )}
                        </div>
                      </div>
                      );
                    })}
                  </div>
                </RadioGroup>

                {/* Feedback */}
                {showFeedback && (
                  <Card className={`mt-6 ${isCorrect ? "border-success" : "border-destructive"}`}>
                    <CardHeader>
                      <div className="flex items-center gap-2">
                        {isCorrect ? (
                          <>
                            <CheckCircle2 className="h-6 w-6 text-success" />
                            <CardTitle className="text-success">Resposta Correta!</CardTitle>
                          </>
                        ) : (
                          <>
                            <XCircle className="h-6 w-6 text-destructive" />
                            <CardTitle className="text-destructive">Resposta Incorreta</CardTitle>
                          </>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-foreground leading-relaxed">{currentQuestion.explanation}</p>
                    </CardContent>
                  </Card>
                )}

                {/* Botões */}
                <div className="flex gap-4 mt-6">
                  {!showFeedback ? (
                    <Button
                      onClick={handleSubmit}
                      disabled={!selectedAnswer}
                      className="flex-1 hover-glow"
                      size="lg"
                    >
                      Confirmar Resposta
                    </Button>
                  ) : (
                    <Button 
                      onClick={handleNext} 
                      className="flex-1 hover-glow" 
                      size="lg"
                      disabled={currentIndex === questions.length - 1}
                    >
                      {currentIndex === questions.length - 1 ? "Última Questão" : "Próxima Questão"}
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Nenhuma questão encontrada para esta área.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
