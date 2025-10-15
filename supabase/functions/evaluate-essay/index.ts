import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { content, title } = await req.json();
    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");

    if (!LOVABLE_API_KEY) {
      throw new Error("LOVABLE_API_KEY is not configured");
    }

    // Validate essay content
    if (!content || content.trim().length < 100) {
      return new Response(
        JSON.stringify({ 
          error: "A redação deve ter no mínimo 100 palavras" 
        }),
        {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const wordCount = content.trim().split(/\s+/).length;

    // System prompt for essay evaluation
    const systemPrompt = `Você é um avaliador especializado em redações do ENEM. Avalie a redação seguindo os critérios do ENEM:
1. Domínio da norma culta (0-200 pontos)
2. Compreensão da proposta (0-200 pontos)
3. Argumentação (0-200 pontos)
4. Coesão (0-200 pontos)
5. Proposta de intervenção (0-200 pontos)

Forneça:
- Uma nota total de 0 a 1000 pontos
- Feedback detalhado com pontos fortes e áreas de melhoria
- Seja construtivo e educativo

Responda em formato JSON:
{
  "score": número entre 0 e 1000,
  "feedback": "texto detalhado do feedback"
}`;

    const response = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${LOVABLE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "google/gemini-2.5-flash",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: `Título: ${title}\n\nRedação (${wordCount} palavras):\n${content}` },
        ],
        response_format: { type: "json_object" },
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        return new Response(
          JSON.stringify({ error: "Limite de requisições excedido. Tente novamente mais tarde." }),
          {
            status: 429,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
          }
        );
      }
      if (response.status === 402) {
        return new Response(
          JSON.stringify({ error: "Créditos insuficientes. Adicione créditos ao seu workspace." }),
          {
            status: 402,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
          }
        );
      }
      throw new Error(`AI gateway error: ${response.status}`);
    }

    const data = await response.json();
    const aiResponse = JSON.parse(data.choices[0].message.content);

    return new Response(
      JSON.stringify({
        score: aiResponse.score,
        feedback: aiResponse.feedback,
        wordCount,
      }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Error in evaluate-essay function:", error);
    return new Response(
      JSON.stringify({ 
        error: error instanceof Error ? error.message : "Erro ao avaliar redação" 
      }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
