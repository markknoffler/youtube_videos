import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AttentionHeatmap } from "./AttentionHeatmap";

export const Sentence4_AttentionLightning: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 1450, fps, config: { damping: 14 } });

  const tokens = ["The", "self", "organizing", "network", "fails", "scale"];
  const numTokens = tokens.length;
  // Current querying token index cycling
  const activeTokenIdx = Math.floor(frame / 35) % numTokens;

  // Circular token pedestal positions
  const arenaRadius = 140;
  const centerX = 200;
  const centerY = 240;

  return (
    <div
      style={{
        position: "relative",
        width: 890,
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
      {/* LEFT: 3D Token Ring with Animated Lightning Arcs */}
      <div
        style={{
          width: 440,
          height: 480,
          backgroundColor: "rgba(18, 1, 32, 0.8)",
          border: "2px solid #FF2A85",
          borderRadius: 14,
          boxShadow: "0 0 28px rgba(255, 42, 133, 0.3)",
          position: "relative",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 14,
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", zIndex: 10 }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>TOKEN DYNAMICS ARENA</span>
          <span style={{ fontSize: 9, color: "#FF2A85", fontWeight: 700 }}>
            QUERY: [{tokens[activeTokenIdx]}]
          </span>
        </div>

        {/* Dynamic Arcs SVG Canvas */}
        <svg
          style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}
          viewBox="0 0 440 480"
        >
          {/* Circular Ground Ring */}
          <circle
            cx={centerX}
            cy={centerY}
            r={arenaRadius}
            fill="none"
            stroke="rgba(199, 125, 255, 0.2)"
            strokeWidth="1.5"
            strokeDasharray="4 4"
          />

          {/* Dynamic Bezier Lightning Arcs between active token and all other tokens */}
          {tokens.map((_, idx) => {
            if (idx === activeTokenIdx) return null;

            const angle1 = (activeTokenIdx * (360 / numTokens) * Math.PI) / 180;
            const x1 = centerX + Math.cos(angle1) * arenaRadius;
            const y1 = centerY + Math.sin(angle1) * (arenaRadius * 0.7);

            const angle2 = (idx * (360 / numTokens) * Math.PI) / 180;
            const x2 = centerX + Math.cos(angle2) * arenaRadius;
            const y2 = centerY + Math.sin(angle2) * (arenaRadius * 0.7);

            // Dynamic weight based on distance and sine
            const weight = Math.abs(Math.sin((activeTokenIdx * 2 + idx * 3) + frame * 0.05));
            const arcHeight = (idx % 2 === 0 ? -40 : 40) * weight;
            const midX = (x1 + x2) / 2;
            const midY = (y1 + y2) / 2 + arcHeight;

            // Traveling energy particle offset
            const packetT = ((frame * 3 + idx * 20) % 100) / 100;
            // Quadratic Bezier interpolation for packet position
            const px = (1 - packetT) * (1 - packetT) * x1 + 2 * (1 - packetT) * packetT * midX + packetT * packetT * x2;
            const py = (1 - packetT) * (1 - packetT) * y1 + 2 * (1 - packetT) * packetT * midY + packetT * packetT * y2;

            return (
              <g key={`arc-${idx}`}>
                {/* Bezier Energy Arc */}
                <path
                  d={`M ${x1} ${y1} Q ${midX} ${midY} ${x2} ${y2}`}
                  fill="none"
                  stroke={weight > 0.5 ? "#FF2A85" : "#7B2CBF"}
                  strokeWidth={1 + weight * 2.5}
                  strokeOpacity={0.3 + weight * 0.6}
                  strokeDasharray="5 3"
                />
                {/* Traveling Energy Packet Dot */}
                <circle
                  cx={px}
                  cy={py}
                  r={3 + weight * 2}
                  fill="#FFFFFF"
                  filter="drop-shadow(0 0 6px #FF2A85)"
                />
              </g>
            );
          })}
        </svg>

        {/* Token Pedestals */}
        <div style={{ position: "relative", width: "100%", height: 360 }}>
          {tokens.map((tok, idx) => {
            const angle = (idx * (360 / numTokens) * Math.PI) / 180;
            const x = centerX + Math.cos(angle) * arenaRadius - 38;
            const y = centerY + Math.sin(angle) * (arenaRadius * 0.7) - 18;
            const isActive = idx === activeTokenIdx;

            return (
              <div
                key={tok}
                style={{
                  position: "absolute",
                  left: x,
                  top: y,
                  width: 76,
                  padding: "4px 8px",
                  borderRadius: 8,
                  backgroundColor: isActive ? "#FF2A85" : "rgba(22, 2, 40, 0.9)",
                  border: isActive ? "2px solid #FFFFFF" : "1.5px solid #9D4EDD",
                  boxShadow: isActive ? "0 0 20px #FF2A85" : "none",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  zIndex: isActive ? 20 : 15,
                  transform: isActive ? "scale(1.15)" : "scale(1)",
                  transition: "transform 0.2s ease",
                }}
              >
                <span style={{ fontSize: 9.5, fontWeight: 800, color: "#FFFFFF" }}>{tok}</span>
                <span style={{ fontSize: 7, color: isActive ? "#FFFFFF" : "#E0AAFF" }}>
                  pos: {idx}
                </span>
              </div>
            );
          })}
        </div>

        {/* Footer HUD equation */}
        <div
          style={{
            zIndex: 10,
            backgroundColor: "rgba(10, 0, 20, 0.85)",
            padding: "6px 10px",
            borderRadius: 6,
            border: "1px dashed #FF2A85",
            fontSize: 9,
            color: "#E0AAFF",
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <span>Softmax(Q_{activeTokenIdx} K^T / √d_k)</span>
          <span style={{ color: "#FF2A85", fontWeight: 700 }}>DYNAMIC ROUTING</span>
        </div>
      </div>

      {/* RIGHT: Live Attention Matrix Heatmap Component */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10, alignItems: "center" }}>
        <AttentionHeatmap size={410} tokens={tokens} />
      </div>
    </div>
  );
};
