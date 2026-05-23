"use client";

import { useState, useEffect, useCallback } from "react";
import { ChatMessage } from "@/components/chat-message";
import { ChatComposer } from "@/components/chat-composer";
import { ThemeSelector } from "@/components/theme-selector";
import { TranscriptPanel } from "@/components/transcript-panel";
import { ExamplePrompts } from "@/components/example-prompts";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  getThemes,
  getTranscripts,
  postAnswer,
  type Theme,
  type TranscriptResult,
} from "@/lib/api";
import { Database, Zap, MessageSquare, AlertCircle } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  // Theme state
  const [themes, setThemes] = useState<Theme[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<Theme | null>(null);
  const [themesLoading, setThemesLoading] = useState(true);
  const [themesError, setThemesError] = useState<string | null>(null);

  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [chatError, setChatError] = useState<string | null>(null);
  const [pendingPrompt, setPendingPrompt] = useState("");

  // Transcript state
  const [transcripts, setTranscripts] = useState<TranscriptResult[]>([]);
  const [transcriptsLoading, setTranscriptsLoading] = useState(false);
  const [transcriptsError, setTranscriptsError] = useState<string | null>(null);
  const [currentPrompt, setCurrentPrompt] = useState<string>("");

  // Fetch themes on mount
  useEffect(() => {
    async function fetchThemes() {
      try {
        setThemesLoading(true);
        setThemesError(null);
        const response = await getThemes();
        setThemes(response.themes);
        // Auto-select first theme if available
        if (response.themes.length > 0) {
          setSelectedTheme(response.themes[0]);
        }
      } catch (err) {
        setThemesError(
          err instanceof Error ? err.message : "Nepodařilo se načíst témata"
        );
      } finally {
        setThemesLoading(false);
      }
    }
    fetchThemes();
  }, []);

  // Fetch transcripts when prompt or theme changes
  const fetchTranscripts = useCallback(
    async (prompt: string) => {
      if (!selectedTheme || !prompt) return;

      try {
        setTranscriptsLoading(true);
        setTranscriptsError(null);
        const response = await getTranscripts(selectedTheme.id, prompt);
        setTranscripts(response.results);
      } catch (err) {
        setTranscriptsError(
          err instanceof Error ? err.message : "Nepodařilo se načíst přepisy"
        );
      } finally {
        setTranscriptsLoading(false);
      }
    },
    [selectedTheme]
  );

  // Handle message submission
  const handleSubmit = async (prompt: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: prompt,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsGenerating(true);
    setChatError(null);
    setCurrentPrompt(prompt);
    setPendingPrompt("");

    // Fetch answer and transcripts in parallel
    try {
      const [answerResponse] = await Promise.all([
        postAnswer(prompt),
        fetchTranscripts(prompt),
      ]);

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: answerResponse.message,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setChatError(
        err instanceof Error
          ? err.message
          : "Nepodařilo se získat odpověď. Zkontrolujte prosím, zda běží API."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  // Handle example prompt selection
  const handleExamplePrompt = (prompt: string) => {
    setPendingPrompt(prompt);
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <header className="border-b border-border bg-card/50">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 border border-primary/20">
              <Database className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground">
                XDent RAG
              </h1>
              <p className="text-sm text-muted-foreground">
                Odpovědi založené na přepisech, poháněné živým RAG vyhledáváním
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          {/* Left Sidebar - Themes & Examples */}
          <aside className="lg:col-span-3 space-y-6">
            {/* Product Info */}
            <div className="rounded-xl border border-border bg-card p-4">
              <div className="flex items-center gap-2 mb-3">
                <Zap className="h-4 w-4 text-primary" />
                <h2 className="text-sm font-semibold text-foreground">
                  Jak to funguje
                </h2>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Ptejte se na podporu lékařské ordinace. Systém pomocí sémantického
                vyhledávání najde odpovídající přepisy hovorů a poté vytvoří
                kontextové odpovědi založené na skutečných podpůrných interakcích.
              </p>
            </div>

            {/* Theme Selector */}
            <div className="rounded-xl border border-border bg-card p-4">
              <h2 className="text-sm font-semibold text-foreground mb-3">
                Témata
              </h2>
              <ThemeSelector
                themes={themes}
                selectedTheme={selectedTheme}
                onSelectTheme={setSelectedTheme}
                isLoading={themesLoading}
                error={themesError}
              />
            </div>

            {/* Example Prompts */}
            <div className="rounded-xl border border-border bg-card p-4">
              <ExamplePrompts onSelectPrompt={handleExamplePrompt} />
            </div>
          </aside>

          {/* Center - Chat Area */}
          <section className="lg:col-span-6 flex flex-col min-h-150">
            <div className="flex-1 rounded-xl border border-border bg-card overflow-hidden flex flex-col">
              {/* Chat Header */}
              <div className="border-b border-border px-4 py-3 bg-card">
                <div className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4 text-primary" />
                  <span className="text-sm font-medium text-foreground">
                    Konverzace
                  </span>
                  {messages.length > 0 && (
                    <span className="text-xs text-muted-foreground">
                      ({messages.length} zpráv)
                    </span>
                  )}
                </div>
              </div>

              {/* Messages Area */}
              <div className="flex-1 overflow-hidden">
                {!hasMessages ? (
                  /* Empty State */
                  <div className="flex flex-col items-center justify-center h-full px-6 py-12 text-center">
                    <div className="rounded-full bg-primary/10 p-4 mb-4">
                      <Database className="h-8 w-8 text-primary" />
                    </div>
                    <h3 className="text-lg font-semibold text-foreground mb-2">
                      Začněte konverzaci
                    </h3>
                    <p className="text-sm text-muted-foreground max-w-sm mb-6">
                      Položte otázku k pracovním postupům podpory lékařské
                      ordinace. Váš dotaz bude porovnán se skutečnými přepisy
                      podpůrných hovorů pomocí RAG vyhledávání.
                    </p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {["eRecept", "Certificates", "VZP", "Integrations"].map(
                        (topic) => (
                          <span
                            key={topic}
                            className="text-xs bg-muted text-muted-foreground px-2.5 py-1 rounded-full"
                          >
                            {topic}
                          </span>
                        )
                      )}
                    </div>
                  </div>
                ) : (
                  /* Messages List */
                  <ScrollArea className="h-100">
                    <div className="px-4">
                      {messages.map((message) => (
                        <ChatMessage
                          key={message.id}
                          role={message.role}
                          content={message.content}
                        />
                      ))}
                      {isGenerating && (
                        <ChatMessage
                          role="assistant"
                          content=""
                          isLoading={true}
                        />
                      )}
                    </div>
                  </ScrollArea>
                )}
              </div>

              {/* Error State */}
              {chatError && (
                <div className="mx-4 mb-4 rounded-lg border border-destructive/30 bg-destructive/10 p-3">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-destructive shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm text-destructive font-medium">
                        Chyba
                      </p>
                      <p className="text-xs text-destructive/80">{chatError}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Composer */}
              <div className="p-4 border-t border-border">
                <ChatComposer
                  onSubmit={handleSubmit}
                  isLoading={isGenerating}
                  initialValue={pendingPrompt}
                />
              </div>
            </div>
          </section>

          {/* Right Sidebar - RAG Trace */}
          <aside className="lg:col-span-3">
            <div className="rounded-xl border border-border bg-card p-4 sticky top-6">
              <div className="flex items-center gap-2 mb-4">
                <Database className="h-4 w-4 text-primary" />
                <h2 className="text-sm font-semibold text-foreground">
                  RAG stopa
                </h2>
                {transcripts.length > 0 && (
                  <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded">
                    {transcripts.length} zásahů
                  </span>
                )}
              </div>
              <TranscriptPanel
                transcripts={transcripts}
                selectedTheme={selectedTheme}
                isLoading={transcriptsLoading}
                error={transcriptsError}
                currentPrompt={currentPrompt}
              />
            </div>
          </aside>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-12">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <p className="text-xs text-muted-foreground text-center">
            XDent RAG Demo • Asistent znalostí pro zdravotnictví • Připojeno k{" "}
            <code className="text-primary bg-primary/10 px-1 rounded">
              {process.env.NEXT_PUBLIC_API_URL || "localhost:8000"}
            </code>
          </p>
        </div>
      </footer>
    </div>
  );
}
