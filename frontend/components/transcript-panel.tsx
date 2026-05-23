"use client";

import { cn } from "@/lib/utils";
import type { TranscriptResult, Theme } from "@/lib/api";
import { FileText, AlertCircle, Search } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

interface TranscriptPanelProps {
  transcripts: TranscriptResult[];
  selectedTheme: Theme | null;
  isLoading?: boolean;
  error?: string | null;
  currentPrompt?: string;
}

export function TranscriptPanel({
  transcripts,
  selectedTheme,
  isLoading,
  error,
  currentPrompt,
}: TranscriptPanelProps) {
  if (error) {
    return (
      <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-destructive">
              Nepodařilo se načíst přepisy
            </p>
            <p className="text-xs text-destructive/80 mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!currentPrompt) {
    return (
      <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
        <div className="rounded-full bg-muted p-3 mb-3">
          <Search className="h-5 w-5 text-muted-foreground" />
        </div>
        <p className="text-sm text-muted-foreground">
          Položte otázku a zobrazí se odpovídající přepisy
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-3 p-1">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-lg bg-muted/50 p-3 animate-pulse">
            <div className="h-3 w-16 bg-muted rounded mb-2" />
            <div className="h-4 w-full bg-muted rounded mb-1" />
            <div className="h-4 w-3/4 bg-muted rounded" />
          </div>
        ))}
      </div>
    );
  }

  if (transcripts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
        <div className="rounded-full bg-muted p-3 mb-3">
          <FileText className="h-5 w-5 text-muted-foreground" />
        </div>
        <p className="text-sm font-medium text-foreground mb-1">Nebyly nalezeny žádné shody</p>
        <p className="text-xs text-muted-foreground">
          Žádné přepisy neodpovídají vašemu dotazu v rámci prahu vzdálenosti.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {selectedTheme && (
        <div className="flex items-center gap-2 mb-3 px-1">
          <span className="text-xs text-muted-foreground">Téma:</span>
          <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded">
            {selectedTheme.name}
          </span>
        </div>
      )}
      <ScrollArea className="h-100 pr-2">
        <div className="space-y-2">
          {transcripts.map((transcript, index) => (
            <div
              key={transcript.id}
              className="rounded-lg border border-border bg-card/50 p-3 hover:bg-card transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-muted-foreground">
                  #{index + 1} • ID: {transcript.transcript_id}
                </span>
                <span
                  className={cn(
                    "text-xs font-mono px-2 py-0.5 rounded",
                    transcript.distance < 0.2
                      ? "bg-emerald-500/20 text-emerald-400"
                      : transcript.distance < 0.3
                        ? "bg-amber-500/20 text-amber-400"
                        : "bg-orange-500/20 text-orange-400"
                  )}
                >
                  {transcript.distance.toFixed(3)}
                </span>
              </div>
              <p className="text-sm text-foreground/90 leading-relaxed line-clamp-4">
                {transcript.clear_transcript}
              </p>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
