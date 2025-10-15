import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Areas from "./pages/Areas";
import Resumos from "./pages/Resumos";
import Questoes from "./pages/Questoes";
import Redacao from "./pages/Redacao";
import Cronograma from "./pages/Cronograma";
import Progresso from "./pages/Progresso";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
        <Route path="/areas" element={<Areas />} />
        <Route path="/resumos" element={<Resumos />} />
        <Route path="/questoes" element={<Questoes />} />
        <Route path="/redacao" element={<Redacao />} />
        <Route path="/cronograma" element={<Cronograma />} />
        <Route path="/progresso" element={<Progresso />} />
        <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
