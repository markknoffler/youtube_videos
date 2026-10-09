import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Sentence7_SiliconVsBiology: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 3300, fps, config: { damping: 14 } });
  const pulse = Math.sin(frame * 0.15) * 0.1 + 1;

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
      {/* LEFT: Biological Sprouting Attempt Blocked by Firewall */}
      <div
        style={{
          width: 390,
          height: 460,
          backgroundColor: "rgba(18, 1, 32, 0.85)",
          border: "2px solid #FF2A85",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 28px rgba(255, 42, 133, 0.3)",
          position: "relative",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FF2A85" }}>BIOLOGICAL ADAPTATION ATTEMPT</span>
          <span style={{ fontSize: 8.5, color: "#FFFFFF", backgroundColor: "#FF2A85", padding: "2px 6px", borderRadius: 4 }}>
            MUTATION DENIED
          </span>
        </div>

        {/* Dendrite Sprouting Canvas */}
        <div
          style={{
            position: "relative",
            width: "100%",
            height: 280,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            overflow: "hidden",
            border: "1px dashed rgba(255, 42, 133, 0.4)",
          }}
        >
          <svg style={{ width: "100%", height: "100%" }} viewBox="0 0 350 280">
            {/* Primary Dendrite Trunk */}
            <path
              d="M 40 240 Q 90 180 140 140 T 220 80"
              fill="none"
              stroke="#C77DFF"
              strokeWidth="4"
              filter="drop-shadow(0 0 8px #C77DFF)"
            />
            {/* Branch 1 trying to sprout */}
            <path
              d="M 140 140 Q 180 160 250 170"
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2.5"
              strokeDasharray="6 3"
              strokeDashoffset={-frame * 2}
            />
            {/* Branch 2 trying to sprout */}
            <path
              d="M 90 180 Q 130 220 230 230"
              fill="none"
              stroke="#E0AAFF"
              strokeWidth="2"
              strokeDasharray="4 2"
            />

            {/* Glowing Growth Cones */}
            <circle cx="220" cy="80" r="6" fill="#FFFFFF" filter="drop-shadow(0 0 8px #FF2A85)" />
            <circle cx="250" cy="170" r="5" fill="#FF2A85" />
            <circle cx="230" cy="230" r="4" fill="#C77DFF" />

            {/* Impassable Silicon Barrier Wall at x=270 */}
            <line x1="270" y1="20" x2="270" y2="260" stroke="#FF2A85" strokeWidth="4" strokeDasharray="10 4" />
            {/* Warning Forcefield pulses */}
            <rect
              x="268"
              y="20"
              width="60"
              height="240"
              fill="rgba(255, 42, 133, 0.15)"
              stroke="none"
            />
            {/* Collision Shockwave at impact point (x=270, y=170) */}
            <circle
              cx="270"
              cy="170"
              r={12 * pulse}
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2"
            />
          </svg>

          {/* Barrier Alert Tag */}
          <div
            style={{
              position: "absolute",
              right: 8,
              top: 110,
              backgroundColor: "rgba(35, 1, 50, 0.95)",
              border: "1px solid #FF2A85",
              borderRadius: 6,
              padding: "4px 8px",
              fontSize: 8,
              color: "#FF2A85",
              fontWeight: 800,
              textAlign: "center",
              lineHeight: 1.3,
            }}
          >
            SILICON<br />FIREWALL<br />ENGAGED
          </div>
        </div>

        {/* Dynamic Plasticity Rates */}
        <div style={{ display: "flex", gap: 8 }}>
          <div style={{ flex: 1, backgroundColor: "#140124", padding: "6px 8px", borderRadius: 6, border: "1px solid #7B2CBF" }}>
            <div style={{ fontSize: 8, color: "#C77DFF" }}>SPROUTING RATE</div>
            <div style={{ fontSize: 13, fontWeight: 900, color: "#FF2A85" }}>0.00%</div>
          </div>
          <div style={{ flex: 1, backgroundColor: "#140124", padding: "6px 8px", borderRadius: 6, border: "1px solid #7B2CBF" }}>
            <div style={{ fontSize: 8, color: "#C77DFF" }}>PRUNING RATE</div>
            <div style={{ fontSize: 13, fontWeight: 900, color: "#FF2A85" }}>0.00%</div>
          </div>
        </div>
      </div>

      {/* VS DIVIDER */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 6,
        }}
      >
        <span style={{ fontSize: 16, fontWeight: 900, color: "#FF2A85", textShadow: "0 0 10px #FF2A85" }}>
          VS
        </span>
      </div>

      {/* RIGHT: Rigid Silicon Circuit Monolith */}
      <div
        style={{
          width: 390,
          height: 460,
          backgroundColor: "rgba(20, 2, 38, 0.85)",
          border: "2px solid #C77DFF",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 28px rgba(199, 125, 255, 0.3)",
          position: "relative",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>RIGID SILICON WAFER</span>
          <span style={{ fontSize: 8.5, color: "#C77DFF", fontWeight: 700, border: "1px solid #C77DFF", padding: "2px 6px", borderRadius: 4 }}>
            FIXED TOPOLOGY
          </span>
        </div>

        {/* Silicon PCB Circuit Pattern */}
        <div
          style={{
            position: "relative",
            width: "100%",
            height: 280,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            overflow: "hidden",
            border: "1px dashed rgba(199, 125, 255, 0.4)",
          }}
        >
          <svg style={{ width: "100%", height: "100%" }} viewBox="0 0 350 280">
            {/* Fixed Metallic Copper Traces */}
            <g stroke="#9D4EDD" strokeWidth="2.5" fill="none">
              <path d="M 20 50 L 120 50 L 160 90 L 320 90" />
              <path d="M 20 120 L 80 120 L 130 170 L 320 170" />
              <path d="M 20 200 L 150 200 L 190 240 L 320 240" />
              <path d="M 120 50 L 120 160 L 80 200" strokeDasharray="4 4" />
            </g>

            {/* Fixed Logic Gates */}
            {Array.from({ length: 6 }).map((_, idx) => {
              const gx = 60 + (idx % 3) * 110;
              const gy = 60 + Math.floor(idx / 3) * 110;
              return (
                <rect
                  key={idx}
                  x={gx}
                  y={gy}
                  width="44"
                  height="28"
                  rx="4"
                  fill="#1B012E"
                  stroke="#FF2A85"
                  strokeWidth="1.5"
                />
              );
            })}

            {/* Electron Flow Pulses along rigid wires */}
            <circle cx={(frame * 4) % 320} cy="90" r="3" fill="#FFFFFF" filter="drop-shadow(0 0 6px #C77DFF)" />
            <circle cx={((frame * 4 + 100) % 320)} cy="170" r="3" fill="#FFFFFF" filter="drop-shadow(0 0 6px #C77DFF)" />
          </svg>
        </div>

        {/* Architectural Verdict */}
        <div
          style={{
            backgroundColor: "#160128",
            border: "1px solid #7B2CBF",
            borderRadius: 8,
            padding: "8px 12px",
            fontSize: 9.5,
            color: "#E0AAFF",
            textAlign: "center",
          }}
        >
          "A FROZEN CRYSTALLINE MONUMENT IN SILICON"
        </div>
      </div>
    </div>
  );
};
