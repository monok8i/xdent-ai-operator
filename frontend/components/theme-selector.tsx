"use client";

import { cn } from "@/lib/utils";
import type { Theme } from "@/lib/api";
import { Layers, CheckCircle2 } from "lucide-react";

interface ThemeSelectorProps {
  themes: Theme[];
  selectedTheme: Theme | null;
  onSelectTheme: (theme: Theme) => void;
  isLoading?: boolean;
  error?: string | null;
}

export function ThemeSelector({
  themes,
  selectedTheme,
  onSelectTheme,
  isLoading,
  error,
}: ThemeSelectorProps) {
  if (error) {
    return (
      <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-3">
        <p className="text-sm text-destructive">{error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-2">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-10 rounded-lg bg-muted animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (themes.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-card p-3 text-center">
        <Layers className="h-6 w-6 mx-auto text-muted-foreground mb-2" />
        <p className="text-sm text-muted-foreground">No themes available</p>
      </div>
    );
  }

  return (
    <div className="space-y-1.5">
      {themes.map((theme) => {
        const isSelected = selectedTheme?.id === theme.id;
        return (
          <button
            key={theme.id}
            onClick={() => onSelectTheme(theme)}
            className={cn(
              "w-full flex items-center justify-between gap-2 rounded-lg px-3 py-2.5 text-left text-sm transition-all",
              isSelected
                ? "bg-primary/15 text-primary border border-primary/30"
                : "bg-card hover:bg-accent border border-transparent text-foreground"
            )}
          >
            <span className="truncate">{theme.name}</span>
            {isSelected && (
              <CheckCircle2 className="h-4 w-4 shrink-0 text-primary" />
            )}
          </button>
        );
      })}
    </div>
  );
}
