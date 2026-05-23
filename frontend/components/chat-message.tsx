"use client";

import { cn } from "@/lib/utils";
import { User, Bot } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  isLoading?: boolean;
}

export function ChatMessage({ role, content, isLoading }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex gap-4 py-4",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
          isUser ? "bg-primary text-primary-foreground" : "bg-accent text-accent-foreground"
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>
      <div
        className={cn(
          "flex-1 space-y-2 rounded-xl px-4 py-3",
          isUser
            ? "bg-primary/10 text-foreground ml-12"
            : "bg-card border border-border mr-12"
        )}
      >
        {isLoading ? (
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <span className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            <span className="text-sm text-muted-foreground">Generuje se odpověď...</span>
          </div>
        ) : (
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
        )}
      </div>
    </div>
  );
}
