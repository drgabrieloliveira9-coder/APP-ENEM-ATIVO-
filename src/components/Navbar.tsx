import { Link, useLocation } from "react-router-dom";
import { BookOpen, Home, FileText, HelpCircle, Edit3, Calendar, TrendingUp, Menu, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { useState } from "react";

const navigation = [
  { name: "Início", href: "/", icon: Home },
  { name: "Áreas", href: "/areas", icon: BookOpen },
  { name: "Resumos", href: "/resumos", icon: FileText },
  { name: "Questões", href: "/questoes", icon: HelpCircle },
  { name: "Redação", href: "/redacao", icon: Edit3 },
  { name: "Cronograma", href: "/cronograma", icon: Calendar },
  { name: "Progresso", href: "/progresso", icon: TrendingUp },
];

export default function Navbar() {
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const NavLinks = ({ mobile = false }) => (
    <>
      {navigation.map((item) => {
        const Icon = item.icon;
        const isActive = location.pathname === item.href;
        return (
          <Link
            key={item.name}
            to={item.href}
            onClick={() => mobile && setOpen(false)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-300 ${
              isActive
                ? "bg-primary text-primary-foreground shadow-glow"
                : "text-muted-foreground hover:text-foreground hover:bg-secondary"
            }`}
          >
            <Icon className="h-5 w-5" />
            <span className="font-medium">{item.name}</span>
          </Link>
        );
      })}
    </>
  );

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-gradient-primary">
              <BookOpen className="h-6 w-6 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-glow">ENEM Study</span>
              <span className="text-xs text-muted-foreground">2025</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-2">
            <NavLinks />
          </div>

          {/* WhatsApp Button & Mobile Menu */}
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              className="hover-glow"
              asChild
            >
              <a
                href="https://wa.me/5531993065681?text=Ol%C3%A1%2C%20tenho%20d%C3%BAvidas%20sobre%20o%20ENEM%20Study%20App..."
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <MessageCircle className="h-4 w-4" />
                <span className="hidden sm:inline">Suporte</span>
              </a>
            </Button>

            {/* Mobile Menu */}
            <Sheet open={open} onOpenChange={setOpen}>
              <SheetTrigger asChild className="md:hidden">
                <Button variant="ghost" size="icon">
                  <Menu className="h-6 w-6" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[280px] bg-card">
                <div className="flex flex-col gap-4 mt-8">
                  <NavLinks mobile />
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </nav>
  );
}
