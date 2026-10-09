import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene06_MooreBound3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  // Sparse graph multi-hop step (0 to 4 hops)
  const currentHop = Math.floor(frame / 20) % 5;

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
      {/* LEFT: Sparse Graph Multi-Hop Latency (Moore Bound) */}
      <div
        style={{
          width: 410,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>SPARSE PHYSICAL GRAPH</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800 }}>O(log N) LATENCY</span>
        </div>

        {/* 5-Hop Chain SVG */}
        <div
          style={{
            height: 260,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(255, 42, 133, 0.4)",
            position: "relative",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="370" height="220" viewBox="0 0 370 220">
            {/* Hop chain coordinates */}
            {[
              { x: 40, y: 110, name: "T_1" },
              { x: 105, y: 60, name: "H_1" },
              { x: 185, y: 150, name: "H_2" },
              { x: 265, y: 70, name: "H_3" },
              { x: 330, y: 110, name: "T_N" },
            ].map((node, idx, arr) => (
              <React.Fragment key={idx}>
                {idx < arr.length - 1 && (
                  <line
                    x1={node.x}
                    y1={node.y}
                    x2={arr[idx + 1].x}
                    y2={arr[idx + 1].y}
                    stroke={idx < currentHop ? "#FF2A85" : "#7B2CBF"}
                    strokeWidth={idx < currentHop ? "3" : "1.5"}
                    strokeDasharray={idx < currentHop ? "none" : "4 3"}
                  />
                )}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r="14"
                  fill={idx === currentHop ? "#FF2A85" : "#1B012E"}
                  stroke={idx <= currentHop ? "#FFFFFF" : "#C77DFF"}
                  strokeWidth="2"
                  filter={idx === currentHop ? "drop-shadow(0 0 10px #FF2A85)" : "none"}
                />
                <text
                  x={node.x}
                  y={node.y + 4}
                  textAnchor="middle"
                  fill="#FFFFFF"
                  fontSize="8"
                  fontWeight="800"
                >
                  {node.name}
                </text>
              </React.Fragment>
            ))}
          </svg>

          {/* Current Hop Counter */}
          <div
            style={{
              position: "absolute",
              top: 10,
              backgroundColor: "#200133",
              border: "1px solid #FF2A85",
              borderRadius: 6,
              padding: "4px 10px",
              fontSize: 8.5,
              color: "#FFFFFF",
              fontWeight: 800,
            }}
          >
            ROUTING HOP: {currentHop + 1} / 5 (LATENCY ACCUMULATING)
          </div>
        </div>

        {/* Moore Bound Formula */}
        <div
          style={{
            backgroundColor: "#160128",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #7B2CBF",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 9,
            color: "#E0AAFF",
          }}
        >
          <span>MOORE BOUND:</span>
          <span style={{ color: "#FF2A85", fontWeight: 800 }}>Diameter ≥ log(N) / log(Δ)</span>
        </div>
      </div>

      {/* RIGHT: Transformer Instant O(1) Depth Attention */}
      <div
        style={{
          width: 410,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>TRANSFORMER ATTENTION BUS</span>
          <span style={{ fontSize: 8.5, color: "#5AF78E", fontWeight: 800 }}>O(1) LAYER DEPTH</span>
        </div>

        {/* Direct Pairwise Laser Link */}
        <div
          style={{
            height: 260,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.4)",
            position: "relative",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="370" height="220" viewBox="0 0 370 220">
            {/* Direct Instantaneous Beam from Token 1 to Token N */}
            <line
              x1="50"
              y1="110"
              x2="320"
              y2="110"
              stroke="#5AF78E"
              strokeWidth="4"
              filter="drop-shadow(0 0 10px #5AF78E)"
            />

            {/* Token 1 */}
            <circle cx="50" cy="110" r="18" fill="#1C0230" stroke="#5AF78E" strokeWidth="2.5" />
            <text x="50" y="114" textAnchor="middle" fill="#FFFFFF" fontSize="9" fontWeight="900">
              T_1
            </text>

            {/* Token N */}
            <circle cx="320" cy="110" r="18" fill="#1C0230" stroke="#5AF78E" strokeWidth="2.5" />
            <text x="320" y="114" textAnchor="middle" fill="#FFFFFF" fontSize="9" fontWeight="900">
              T_N
            </text>

            {/* Intermediate Token Bus Arcs */}
            <path d="M 50 110 Q 185 30 320 110" fill="none" stroke="#C77DFF" strokeWidth="1.5" strokeDasharray="4 4" />
            <path d="M 50 110 Q 185 190 320 110" fill="none" stroke="#C77DFF" strokeWidth="1.5" strokeDasharray="4 4" />
          </svg>

          <div
            style={{
              position: "absolute",
              top: 10,
              backgroundColor: "#160128",
              border: "1px solid #5AF78E",
              borderRadius: 6,
              padding: "4px 10px",
              fontSize: 8.5,
              color: "#5AF78E",
              fontWeight: 800,
            }}
          >
            INSTANT DIRECT COUPLING (ZERO MULTI-HOP PENALTY)
          </div>
        </div>

        {/* Scalability Conclusion */}
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
          "Transformers decouple parameter complexity from sequence length N."
        </div>
      </div>
    </div>
  );
};
