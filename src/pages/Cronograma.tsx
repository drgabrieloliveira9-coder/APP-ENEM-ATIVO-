import { useState } from "react";
import { Calendar, Download, Save } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import Navbar from "@/components/Navbar";
import { supabase } from "@/integrations/supabase/client";

interface ScheduleDay {
  day: number;
  subjects: string[];
  hours: number;
}

const subjects = [
  "Português",
  "Literatura",
  "Inglês",
  "Matemática",
  "Física",
  "Química",
  "Biologia",
  "História",
  "Geografia",
  "Sociologia",
  "Filosofia",
];

export default function Cronograma() {
  const { toast } = useToast();
  const [hoursPerDay, setHoursPerDay] = useState(4);
  const [daysUntilExam, setDaysUntilExam] = useState(90);
  const [schedule, setSchedule] = useState<ScheduleDay[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const generateSchedule = () => {
    setIsGenerating(true);

    const newSchedule: ScheduleDay[] = [];
    const subjectsPerDay = Math.ceil(hoursPerDay / 2);
    
    for (let day = 1; day <= daysUntilExam; day++) {
      const daySubjects: string[] = [];
      const startIndex = ((day - 1) * subjectsPerDay) % subjects.length;
      
      for (let i = 0; i < subjectsPerDay && daySubjects.length < subjects.length; i++) {
        const subjectIndex = (startIndex + i) % subjects.length;
        daySubjects.push(subjects[subjectIndex]);
      }
      
      newSchedule.push({
        day,
        subjects: daySubjects,
        hours: hoursPerDay,
      });
    }

    setSchedule(newSchedule);
    setIsGenerating(false);

    toast({
      title: "Cronograma gerado!",
      description: `${daysUntilExam} dias de estudo programados.`,
    });
  };

  const saveSchedule = async () => {
    try {
      const { data: user } = await supabase.auth.getUser();
      
      if (!user.user) {
        toast({
          title: "Erro",
          description: "Você precisa estar logado para salvar o cronograma.",
          variant: "destructive",
        });
        return;
      }

      const { error } = await supabase.from("schedules").insert([{
        user_id: user.user.id,
        hours_per_day: hoursPerDay,
        days_until_exam: daysUntilExam,
        schedule_data: schedule as any,
      }]);

      if (error) throw error;

      toast({
        title: "Cronograma salvo!",
        description: "Seu cronograma foi salvo com sucesso.",
      });
    } catch (error: any) {
      toast({
        title: "Erro ao salvar",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const downloadCSV = () => {
    let csv = "Dia,Matérias,Horas\n";
    
    schedule.forEach((day) => {
      csv += `${day.day},"${day.subjects.join(", ")}",${day.hours}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    
    link.setAttribute("href", url);
    link.setAttribute("download", "cronograma-enem.csv");
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast({
      title: "Download iniciado!",
      description: "Seu cronograma foi exportado em CSV.",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-glow">Cronograma de Estudos</h1>
          <p className="text-muted-foreground">
            Crie seu planejamento personalizado para o ENEM
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          <Card className="card-glow md:col-span-1">
            <CardHeader>
              <CardTitle>Configurações</CardTitle>
              <CardDescription>
                Personalize seu cronograma de estudos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label htmlFor="hours">Horas de estudo por dia</Label>
                <Input
                  id="hours"
                  type="number"
                  min="1"
                  max="12"
                  value={hoursPerDay}
                  onChange={(e) => setHoursPerDay(Number(e.target.value))}
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="days">Dias até o ENEM</Label>
                <Input
                  id="days"
                  type="number"
                  min="1"
                  max="365"
                  value={daysUntilExam}
                  onChange={(e) => setDaysUntilExam(Number(e.target.value))}
                  className="mt-2"
                />
              </div>

              <Button
                onClick={generateSchedule}
                disabled={isGenerating}
                className="w-full hover-glow"
              >
                <Calendar className="mr-2 h-5 w-5" />
                Gerar Cronograma
              </Button>

              {schedule.length > 0 && (
                <>
                  <Button
                    onClick={saveSchedule}
                    variant="secondary"
                    className="w-full"
                  >
                    <Save className="mr-2 h-5 w-5" />
                    Salvar Cronograma
                  </Button>

                  <Button
                    onClick={downloadCSV}
                    variant="outline"
                    className="w-full"
                  >
                    <Download className="mr-2 h-5 w-5" />
                    Baixar CSV
                  </Button>
                </>
              )}
            </CardContent>
          </Card>

          <Card className="card-glow md:col-span-2">
            <CardHeader>
              <CardTitle>Seu Cronograma</CardTitle>
              <CardDescription>
                {schedule.length > 0
                  ? `${schedule.length} dias de estudo programados`
                  : "Gere um cronograma para visualizar"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {schedule.length > 0 ? (
                <div className="max-h-[600px] overflow-y-auto space-y-3">
                  {schedule.map((day) => (
                    <div
                      key={day.day}
                      className="p-4 rounded-lg border border-border bg-muted/30 hover:bg-muted/50 transition-colors"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-semibold text-primary">
                          Dia {day.day}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {day.hours}h
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {day.subjects.map((subject) => (
                          <span
                            key={subject}
                            className="px-2 py-1 bg-primary/20 text-primary text-sm rounded"
                          >
                            {subject}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <Calendar className="h-16 w-16 mx-auto mb-4 opacity-50" />
                  <p>Configure e gere seu cronograma de estudos</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
