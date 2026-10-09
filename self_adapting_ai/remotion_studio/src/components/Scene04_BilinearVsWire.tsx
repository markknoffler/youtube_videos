import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ScientistQuoteCard } from "./ScientistQuoteCard";

export const Scene04_BilinearVsWire: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  // Amplitude of scalar wire
  const wireSignal = Math.sin(frame * 0.1) * 30;
  // Dynamic bilinear angle
  const angle = (frame * 1.5) % 360;

  return (
    <div
      style={{
        position: "relative",
        width: 860,
        height: 520,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        transform: `scale(${Math.max(0.01, entrance)})`,
        fontFamily: "'JetBrains Mono', monospace",
        padding: "0 10px",
        boxSizing: "border-box",
      }}
    >
      {/* LEFT: Static Scalar Wire vs Dynamic Metric Attention */}
      <div
        style={{
          width: 420,
          height: 460,
          backgroundColor: "rgba(18, 1, 32, 0.85)",
          border: "2px solid #FF2A85",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 28px rgba(255, 42, 133, 0.3)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>THE MATHEMATICAL CHASM</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800 }}>WIRE vs METRIC</span>
        </div>

        {/* 1. Static Scalar Wire (Top Half) */}
        <div
          style={{
            height: 160,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.3)",
            padding: 10,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div style={{ fontSize: 9, color: "#C77DFF", fontWeight: 700 }}>
            STATIC GRAPH WIRE: SCALAR MULTIPLICATION
          </div>
          {/* Wire Waveform SVG */}
          <svg width="360" height="70" viewBox="0 0 360 70">
            <line x1="20" y1="35" x2="340" y2="35" stroke="#7B2CBF" strokeWidth="2" />
            <path
              d={`M 20 35 Q 100 ${35 + wireSignal} 180 35 T 340 35`}
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2.5"
            />
            {/* Scalar Weight Node W_ij */}
            <circle cx="180" cy="35" r="14" fill="#200133" stroke="#FF2A85" strokeWidth="2" />
            <text x="180" y="38" textAnchor="middle" fill="#FFFFFF" fontSize="8" fontWeight="800">
              W_ij
            </text>
          </svg>
          <div style={{ fontSize: 8.5, color: "#E0AAFF" }}>
            y = W_ij · x_j → Cannot compute content-dependent metric
          </div>
        </div>

        {/* 2. Dynamic Bilinear Metric (Bottom Half) */}
        <div
          style={{
            height: 180,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(255, 42, 133, 0.4)",
            padding: 10,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div style={{ fontSize: 9, color: "#FF2A85", fontWeight: 700 }}>
            ATTENTION: INSTANTANEOUS METRIC TENSOR
          </div>
          {/* Rotating Vector Dot Product Arc */}
          <svg width="360" height="90" viewBox="0 0 360 90">
            {/* Query Vector Q */}
            <line x1="180" y1="75" x2="180" y2="15" stroke="#FF2A85" strokeWidth="3" filter="drop-shadow(0 0 6px #FF2A85)" />
            <text x="180" y="10" textAnchor="middle" fill="#FF2A85" fontSize="8" fontWeight="800">Q_i</text>

            {/* Rotating Key Vector K */}
            <line
              x1="180"
              y1="75"
              x2={180 + Math.cos((angle * Math.PI) / 180) * 60}
              y2={75 - Math.sin((angle * Math.PI) / 180) * 60}
              stroke="#C77DFF"
              strokeWidth="3"
              filter="drop-shadow(0 0 6px #C77DFF)"
            />
            <circle cx="180" cy="75" r="4" fill="#FFFFFF" />
          </svg>
          <div style={{ fontSize: 8.5, color: "#5AF78E", fontWeight: 700 }}>
            Softmax(Q_i · K_j^T / √d) → Dynamic O(1) pairwise lookup
          </div>
        </div>
      </div>

      {/* RIGHT: Anthropic Induction Heads Spotlight & Scientist Quote */}
      <div style={{ width: 410, display: "flex", flexDirection: "column", gap: 12 }}>
        <ScientistQuoteCard
          scientistName="Chris Olah"
          role="Co-founder & Interpretability Lead"
          institution="Anthropic"
          quoteText="Transformers spontaneously develop induction heads that copy prior tokens via bilinear matching. They form an implicit in-context learning circuit."
          highlightPhrase="induction heads that copy prior tokens"
          width={410}
        />

        <div
          style={{
            backgroundColor: "rgba(22, 2, 40, 0.9)",
            border: "1.5px solid #7B2CBF",
            borderRadius: 12,
            padding: "12px 16px",
            display: "flex",
            flexDirection: "column",
            gap: 6,
          }}
        >
          <div style={{ fontSize: 10, fontWeight: 800, color: "#FFFFFF" }}>
            THE MODULAR EMERGENCE PARADOX:
          </div>
          <div style={{ fontSize: 9, color: "#E0AAFF", lineHeight: 1.4 }}>
            Biological dynamic graphs fail to create bilinear attention. But rigid static Transformers spontaneously birth algorithmic circuits without moving a single synapse.
          </div>
        </div>
      </div>
    </div>
  );
};
