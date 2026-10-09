import React from "react";
import { useCurrentFrame } from "remotion";

interface AttentionHeatmapProps {
  size?: number;
  tokens?: string[];
}

export const AttentionHeatmap: React.FC<AttentionHeatmapProps> = ({
  size = 320,
  tokens = ["The", "self", "organizing", "network", "fails", "at", "scale", "."],
}) => {
  const frame = useCurrentFrame();
  const n = tokens.length;
  const cellSize = (size - 60) / n;

  // Active query being scanned
  const activeRow = Math.floor(frame / 20) % n;

  return (
    <div
      style={{
        width: size,
        height: size,
        backgroundColor: "#130226",
        borderRadius: 14,
        border: "1.5px solid #9D4EDD",
        boxShadow: "0 0 24px rgba(255, 42, 133, 0.2)",
        padding: 14,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#FF2A85", letterSpacing: 0.5 }}>
          ATTENTION MATRIX: Softmax(QKᵀ / √d)
        </span>
        <span style={{ fontSize: 9.5, color: "#E0AAFF" }}>
          Head #1 • 8x8
        </span>
      </div>

      {/* Grid Canvas */}
      <div style={{ display: "flex", flexDirection: "column", gap: 3, marginTop: 8 }}>
        {Array.from({ length: n }).map((_, r) => (
          <div key={r} style={{ display: "flex", gap: 3, alignItems: "center" }}>
            <span style={{ fontSize: 9, color: r === activeRow ? "#FF2A85" : "#8A2BE2", width: 34, textAlign: "right" }}>
              {tokens[r].slice(0, 5)}
            </span>
            {Array.from({ length: n }).map((_, c) => {
              // Dynamic attention weight formula
              const weight = Math.abs(Math.sin((r * 1.3 + c * 1.7) + frame * 0.04));
              const isDiagonal = r === c;
              const cellVal = isDiagonal ? Math.min(1.0, weight * 0.4 + 0.6) : weight * 0.7;
              const isActive = r === activeRow;

              const bg = `rgba(255, 42, 133, ${cellVal.toFixed(2)})`;

              return (
                <div
                  key={c}
                  style={{
                    width: cellSize,
                    height: cellSize,
                    backgroundColor: bg,
                    borderRadius: 3,
                    border: isActive ? "1px solid #FFFFFF" : "1px solid rgba(199, 125, 255, 0.2)",
                    boxShadow: isActive ? "0 0 6px #FF2A85" : "none",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 7.5,
                    color: cellVal > 0.5 ? "#FFFFFF" : "#E0AAFF",
                  }}
                >
                  {cellVal.toFixed(2).slice(1)}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {/* Crossbar Status Readout */}
      <div
        style={{
          marginTop: 6,
          fontSize: 10,
          color: "#E0AAFF",
          display: "flex",
          justifyContent: "space-between",
          borderTop: "1px dashed #7B2CBF",
          paddingTop: 6,
        }}
      >
        <span>Token: [{tokens[activeRow]}]</span>
        <span style={{ color: "#FF2A85", fontWeight: 700 }}>O(1) Full-Rank Routing</span>
      </div>
    </div>
  );
};
