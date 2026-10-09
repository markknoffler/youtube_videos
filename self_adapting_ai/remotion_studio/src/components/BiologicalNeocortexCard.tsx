import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const BiologicalNeocortexCard: React.FC<{
  width?: number;
  height?: number;
  startFrame?: number;
}> = ({ width = 500, height = 420, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const entrance = spring({ frame: relFrame, fps, config: { damping: 14 } });
  const rotY = (relFrame * 1.2) % 360;
  const pulse = Math.sin(relFrame * 0.1) * 0.1 + 1;

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(18, 1, 32, 0.92)",
        border: "1.5px solid #FF2A85",
        borderRadius: 14,
        padding: "16px 20px",
        boxShadow: "0 0 30px rgba(255, 42, 133, 0.35)",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        alignItems: "center",
        transform: `scale(${entrance})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      <div style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>BIOLOGICAL NEOCORTICAL MESH</span>
        <span
          style={{
            fontSize: 8.5,
            color: "#FF2A85",
            fontWeight: 800,
            border: "1px solid #FF2A85",
            padding: "2px 6px",
            borderRadius: 4,
          }}
        >
          86B NEURONS • 100T SYNAPSES
        </span>
      </div>

      {/* 3D Rotating Neocortex Sphere */}
      <div
        style={{
          position: "relative",
          width: 240,
          height: 240,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg style={{ width: "100%", height: "100%" }} viewBox="0 0 260 260">
          {/* Outer Auroral Glow */}
          <circle
            cx="130"
            cy="130"
            r={100 * pulse}
            fill="none"
            stroke="rgba(255, 42, 133, 0.25)"
            strokeWidth="2"
            strokeDasharray="6 4"
          />
          {/* Neocortical 6-Layer Ribbons */}
          {Array.from({ length: 6 }).map((_, l) => {
            const r = 40 + l * 12;
            return (
              <circle
                key={l}
                cx="130"
                cy="130"
                r={r}
                fill="none"
                stroke={l % 2 === 0 ? "#C77DFF" : "#7B2CBF"}
                strokeWidth="1.5"
                strokeDasharray={`${l * 4 + 6} ${l * 2 + 4}`}
                strokeDashoffset={relFrame * (l % 2 === 0 ? 1 : -1)}
              />
            );
          })}

          {/* Traveling Synaptic Action Potential Pulses */}
          {Array.from({ length: 18 }).map((_, n) => {
            const angle = ((n * 20 + rotY) * Math.PI) / 180;
            const radius = 50 + (n * 13) % 55;
            const cx = 130 + Math.cos(angle) * radius;
            const cy = 130 + Math.sin(angle) * (radius * 0.75);

            return (
              <g key={n}>
                <circle cx={cx} cy={cy} r={2.5} fill="#FF2A85" filter="drop-shadow(0 0 6px #FF2A85)" />
                {n % 3 === 0 && (
                  <line x1={cx} y1={cy} x2="130" y2="130" stroke="#FF2A85" strokeWidth="1" strokeOpacity="0.3" />
                )}
              </g>
            );
          })}

          {/* Central Spiking Core */}
          <circle cx="130" cy="130" r="14" fill="#24023B" stroke="#FFFFFF" strokeWidth="2" />
          <circle cx="130" cy="130" r="6" fill="#FF2A85" />
        </svg>

        <div
          style={{
            position: "absolute",
            bottom: 4,
            fontSize: 8.5,
            color: "#E0AAFF",
            fontWeight: 700,
          }}
        >
          ASYNCHRONOUS DYNAMICAL GRAPH
        </div>
      </div>

      {/* Metabolic Spec Footer */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 9.5,
          color: "#E0AAFF",
          borderTop: "1px dashed rgba(199, 125, 255, 0.3)",
          paddingTop: 8,
        }}
      >
        <span>METABOLIC POWER BUDGET</span>
        <span style={{ color: "#5AF78E", fontWeight: 800 }}>≈ 20 WATTS TOTAL (GLUCOSE)</span>
      </div>
    </div>
  );
};
