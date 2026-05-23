"use client";

import { Lightbulb } from "lucide-react";

interface ExamplePromptsProps {
  onSelectPrompt: (prompt: string) => void;
}

const EXAMPLE_PROMPTS = [
  {
    label: "eRecept",
    prompt: "Jak zjistím, proč eRecept nefunguje?",
  },
  {
    label: "Certifikáty",
    prompt: "Co mám ověřit, když je certifikát neplatný?",
  },
  {
    label: "Integrace",
    prompt: "Jak vyřeším problém s integrací s externím systémem?",
  },
  {
    label: "VZP",
    prompt: "Jaký je doporučený postup pro podporu související s VZP?",
  },
];

export function ExamplePrompts({ onSelectPrompt }: ExamplePromptsProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-muted-foreground">
        <Lightbulb className="h-4 w-4" />
        <span className="text-xs font-medium uppercase tracking-wide">Zkuste se zeptat</span>
      </div>
      <div className="grid grid-cols-1 gap-2">
        {EXAMPLE_PROMPTS.map((example) => (
          <button
            key={example.label}
            onClick={() => onSelectPrompt(example.prompt)}
            className="group flex items-start gap-2 rounded-lg border border-border bg-card p-3 text-left transition-all hover:border-primary/50 hover:bg-primary/5"
          >
            <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded shrink-0">
              {example.label}
            </span>
            <span className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
              {example.prompt}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
