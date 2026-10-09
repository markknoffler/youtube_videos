import React from "react";
import { useCurrentFrame } from "remotion";
import subtitleData from "../data/subtitles.json";

interface SubtitleItem {
  index: number;
  startSec: number;
  endSec: number;
  startFrame: number;
  endFrame: number;
  text: string;
}

const HIGHLIGHT_KEYWORDS = [
  "Transformer", "monolith", "paradox", "plasticity", "synapses", "synaptic",
  "biological", "86 billion", "20 watts", "megawatts", "Hebb", "Oja",
  "Kohonen", "WANN", "bilinear", "attention", "induction heads",
  "rank collapse", "Moore bound", "Hardware Lottery", "systolic",
  "DeepSeek", "MoE", "MLA", "Kolmogorov-Arnold", "KAN", "Liquid",
  "neural", "in-context", "silicon", "intelligence", "architecture",
  "GPT-6", "GPT-4", "Claude", "Gemini", "Llama", "Mistral", "Astra", "Mythos"
];

function highlightText(text: string) {
  const words = text.split(" ");
  return words.map((word, i) => {
    const cleanWord = word.replace(/[^a-zA-Z0-9-]/g, "");
    const isHighlight = HIGHLIGHT_KEYWORDS.some(
      (kw) => kw.toLowerCase() === cleanWord.toLowerCase()
    );
    if (isHighlight) {
      return (
        <span
          key={i}
          style={{
            display: "inline-block",
            color: "#FF5EAA",
            fontWeight: 700,
            marginRight: "0.25em",
          }}
        >
          {word}
        </span>
      );
    }
    return (
      <span
        key={i}
        style={{
          display: "inline-block",
          color: "#FFFFFF",
          marginRight: "0.25em",
        }}
      >
        {word}
      </span>
    );
  });
}

export const CyberSubtitles: React.FC<{ sceneKey: keyof typeof subtitleData }> = ({
  sceneKey,
}) => {
  const frame = useCurrentFrame();

  const items: SubtitleItem[] = (subtitleData as Record<string, SubtitleItem[]>)[sceneKey] || [];

  let activeItem: SubtitleItem | null = null;
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    if (frame >= item.startFrame && frame <= item.endFrame) {
      activeItem = item;
      break;
    }
  }

  if (!activeItem) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        bottom: 14,
        left: "50%",
        transform: "translateX(-50%)",
        maxWidth: 820,
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        border: "1px solid rgba(255, 42, 133, 0.35)",
        borderRadius: 5,
        padding: "3px 12px 4px",
        zIndex: 90,
        textAlign: "center",
        pointerEvents: "none",
        backdropFilter: "blur(6px)",
        boxShadow: "0 2px 12px rgba(0, 0, 0, 0.85)",
      }}
    >
      <div
        style={{
          fontSize: 14.5,
          lineHeight: 1.3,
          fontWeight: 600,
          fontFamily: "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif",
          textShadow: "0 1px 3px rgba(0, 0, 0, 0.95)",
          letterSpacing: 0.1,
        }}
      >
        {highlightText(activeItem.text)}
      </div>
    </div>
  );
};
