import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene05_RankCollapse3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  // Mode 1 dominance progression
  const collapseT = Math.min(1, (frame % 150) / 100);
  const lambda1Height = 40 + collapseT * 120;
  const otherLambdaHeight = Math.max(4, 80 * (1 - collapseT));

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
      {/* LEFT: Theorem 1 Spectral Collapse Mechanics */}
      <div
        style={{
          width: 440,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>THEOREM 1: SPECTRAL RANK COLLAPSE</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800, border: "1px solid #FF2A85", padding: "2px 6px", borderRadius: 4 }}>
            OJA'S DYNAMICS
          </span>
        </div>

        {/* Differential Equation Card */}
        <div
          style={{
            backgroundColor: "rgba(10, 0, 18, 0.9)",
            borderRadius: 8,
            border: "1px dashed #7B2CBF",
            padding: "8px 12px",
            fontSize: 10,
            color: "#E0AAFF",
            textAlign: "center",
          }}
        >
          dW/dt = η·E[y xᵀ] - α·(y yᵀ) W
        </div>

        {/* Spectral Decomposition Eigenvalue Bar Chart */}
        <div
          style={{
            height: 240,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(255, 42, 133, 0.4)",
            position: "relative",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-around",
            padding: "16px 20px 30px",
            boxSizing: "border-box",
          }}
        >
          {/* Mode 1 (Surging Dominant Eigenvalue) */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
            <span style={{ fontSize: 9, color: "#FF2A85", fontWeight: 800 }}>λ₁</span>
            <div
              style={{
                width: 38,
                height: lambda1Height,
                backgroundColor: "#FF2A85",
                borderRadius: "4px 4px 0 0",
                boxShadow: "0 0 16px #FF2A85",
                transition: "height 0.1s linear",
              }}
            />
            <span style={{ position: "absolute", bottom: 10, fontSize: 8, color: "#FFFFFF" }}>MODE 1</span>
          </div>

          {/* Subordinate Modes λ2 - λ6 (Collapsing to Zero) */}
          {Array.from({ length: 5 }).map((_, idx) => (
            <div key={idx} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
              <span style={{ fontSize: 9, color: "#7B2CBF", fontWeight: 700 }}>λ{idx + 2}</span>
              <div
                style={{
                  width: 32,
                  height: otherLambdaHeight * (1 - idx * 0.15),
                  backgroundColor: "#5A189A",
                  borderRadius: "4px 4px 0 0",
                  transition: "height 0.1s linear",
                }}
              />
              <span style={{ position: "absolute", bottom: 10, fontSize: 8, color: "#E0AAFF" }}>MODE {idx + 2}</span>
            </div>
          ))}
        </div>

        {/* Mathematical Consequence */}
        <div
          style={{
            backgroundColor: "#160128",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #FF2A85",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 9.5,
            color: "#FFFFFF",
          }}
        >
          <span>ASYMPTOTIC RANK:</span>
          <span style={{ color: "#FF2A85", fontWeight: 900 }}>lim_t→∞ rank(W) = 1</span>
        </div>
      </div>

      {/* RIGHT: Singular Value Spectrum & Loss of Multi-relational Context */}
      <div
        style={{
          width: 390,
          height: 460,
          backgroundColor: "rgba(20, 2, 38, 0.85)",
          border: "2px solid #C77DFF",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 28px rgba(199, 125, 255, 0.3)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>REPRESENTATION COLLAPSE</span>
          <span style={{ fontSize: 8.5, color: "#C77DFF", fontWeight: 700 }}>SINGULAR SPECTRUM</span>
        </div>

        {/* 2D Contour Map / Phase Portrait */}
        <div
          style={{
            height: 270,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.4)",
            position: "relative",
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="340" height="240" viewBox="0 0 340 240">
            {/* Coordinate grid */}
            <line x1="20" y1="120" x2="320" y2="120" stroke="#7B2CBF" strokeWidth="1" strokeDasharray="3 3" />
            <line x1="170" y1="20" x2="170" y2="220" stroke="#7B2CBF" strokeWidth="1" strokeDasharray="3 3" />

            {/* Elliptical manifolds flattening into a 1D line */}
            <ellipse
              cx="170"
              cy="120"
              rx={120}
              ry={Math.max(4, 90 * (1 - collapseT))}
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2.5"
              transform={`rotate(-25 170 120)`}
            />

            {/* Dominant Vector Arrow */}
            <line x1="70" y1="165" x2="270" y2="75" stroke="#FFFFFF" strokeWidth="3" filter="drop-shadow(0 0 8px #FF2A85)" />
            <circle cx="270" cy="75" r="5" fill="#FF2A85" />
          </svg>

          {/* Alert Tag */}
          <div
            style={{
              position: "absolute",
              bottom: 8,
              backgroundColor: "rgba(35, 1, 50, 0.9)",
              border: "1px solid #FF2A85",
              borderRadius: 6,
              padding: "4px 10px",
              fontSize: 8.5,
              color: "#FF2A85",
              fontWeight: 800,
            }}
          >
            MANIFOLD COLLAPSES TO 1-DIMENSIONAL LINE
          </div>
        </div>

        {/* Empirical Impact */}
        <div
          style={{
            backgroundColor: "#160128",
            border: "1px solid #7B2CBF",
            borderRadius: 8,
            padding: "8px 12px",
            fontSize: 9,
            color: "#E0AAFF",
            textAlign: "center",
          }}
        >
          "The network can only amplify the loudest single correlation in its sensory history."
        </div>
      </div>
    </div>
  );
};
