import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Sentence5_ResidualHighway: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 2100, fps, config: { damping: 14 } });

  // Stream particle movement
  const streamOffset = (frame * 6) % 600;
  // Bypass packet movement
  const bypassOffset = (frame * 5) % 400;

  return (
    <div
      style={{
        position: "relative",
        width: 860,
        height: 520,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${Math.max(0.01, entrance)})`,
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg
        style={{ position: "absolute", width: "100%", height: "100%", pointerEvents: "none" }}
        viewBox="0 0 860 520"
      >
        {/* Main Residual Highway Tube */}
        <defs>
          <linearGradient id="highwayGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#7B2CBF" stopOpacity="0.2" />
            <stop offset="50%" stopColor="#FF2A85" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#C77DFF" stopOpacity="0.2" />
          </linearGradient>
        </defs>

        {/* Highway Pipe Bounds */}
        <rect
          x="60"
          y="230"
          width="740"
          height="60"
          rx="30"
          fill="url(#highwayGrad)"
          stroke="#C77DFF"
          strokeWidth="2"
        />

        {/* Residual Stream Particles Rushing Through Center */}
        {Array.from({ length: 14 }).map((_, i) => {
          const px = 80 + ((streamOffset + i * 45) % 700);
          return (
            <circle
              key={i}
              cx={px}
              cy={260}
              r="4.5"
              fill="#FFFFFF"
              filter="drop-shadow(0 0 8px #FF2A85)"
            />
          );
        })}

        {/* Skip Connection Arched Bypass Pipeline: x + Sublayer(x) */}
        <path
          d="M 160 230 C 220 90, 640 90, 700 230"
          fill="none"
          stroke="#FF2A85"
          strokeWidth="3.5"
          strokeDasharray="8 4"
          filter="drop-shadow(0 0 10px #FF2A85)"
        />
        {/* Bypass Traveling Energy Pulse */}
        {Array.from({ length: 4 }).map((_, j) => {
          const t = ((bypassOffset + j * 90) % 360) / 360;
          // Cubic Bezier interpolation for the arc
          const x0 = 160, y0 = 230;
          const x1 = 220, y1 = 90;
          const x2 = 640, y2 = 90;
          const x3 = 700, y3 = 230;
          const cx = Math.pow(1 - t, 3) * x0 + 3 * Math.pow(1 - t, 2) * t * x1 + 3 * (1 - t) * Math.pow(t, 2) * x2 + Math.pow(t, 3) * x3;
          const cy = Math.pow(1 - t, 3) * y0 + 3 * Math.pow(1 - t, 2) * t * y1 + 3 * (1 - t) * Math.pow(t, 2) * y2 + Math.pow(t, 3) * y3;

          return (
            <circle
              key={`bp-${j}`}
              cx={cx}
              cy={cy}
              r="5"
              fill="#FFFFFF"
              filter="drop-shadow(0 0 8px #FF2A85)"
            />
          );
        })}

        {/* Summation Node '+' at (x=700, y=260) */}
        <circle cx="700" cy="260" r="18" fill="#24023B" stroke="#FF2A85" strokeWidth="2.5" />
        <line x1="692" y1="260" x2="708" y2="260" stroke="#FFFFFF" strokeWidth="2.5" />
        <line x1="700" y1="252" x2="700" y2="268" stroke="#FFFFFF" strokeWidth="2.5" />

        {/* LayerNorm Ring 1 */}
        <ellipse cx="230" cy="260" rx="14" ry="40" fill="none" stroke="#C77DFF" strokeWidth="3" strokeDasharray="4 2" />
        {/* LayerNorm Ring 2 */}
        <ellipse cx="610" cy="260" rx="14" ry="40" fill="none" stroke="#C77DFF" strokeWidth="3" strokeDasharray="4 2" />
      </svg>

      {/* Top Bypass Label */}
      <div
        style={{
          position: "absolute",
          top: 66,
          backgroundColor: "rgba(22, 2, 40, 0.9)",
          border: "1.5px solid #FF2A85",
          borderRadius: 8,
          padding: "4px 14px",
          color: "#FFFFFF",
          fontSize: 11,
          fontWeight: 800,
          boxShadow: "0 0 16px rgba(255, 42, 133, 0.4)",
        }}
      >
        IDENTITY SKIP HIGHWAY: x + Sublayer(x)
      </div>

      {/* Central 3D MLP Expansion Chamber */}
      <div
        style={{
          position: "absolute",
          left: 310,
          top: 175,
          width: 240,
          height: 170,
          backgroundColor: "rgba(25, 2, 45, 0.85)",
          border: "2px solid #FF2A85",
          borderRadius: 14,
          boxShadow: "0 0 30px rgba(255, 42, 133, 0.35)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 12,
          boxSizing: "border-box",
          zIndex: 10,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 10, fontWeight: 900, color: "#FFFFFF" }}>FEED-FORWARD MLP</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 700 }}>4× d_model EXPANSION</span>
        </div>

        {/* Dynamic Synaptic Matrix in MLP */}
        <div style={{ display: "flex", justifyContent: "space-around", alignItems: "center", height: 80 }}>
          {/* Input Layer (4 nodes) */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#C77DFF", boxShadow: "0 0 6px #C77DFF" }} />
            ))}
          </div>
          {/* Expanded Hidden Layer (8 nodes) */}
          <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
            {Array.from({ length: 8 }).map((_, j) => (
              <div
                key={j}
                style={{
                  width: 9,
                  height: 9,
                  borderRadius: "50%",
                  backgroundColor: (frame + j * 4) % 20 < 10 ? "#FF2A85" : "#9D4EDD",
                  boxShadow: "0 0 8px #FF2A85",
                }}
              />
            ))}
          </div>
          {/* Output Layer (4 nodes) */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {Array.from({ length: 4 }).map((_, k) => (
              <div key={k} style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#C77DFF", boxShadow: "0 0 6px #C77DFF" }} />
            ))}
          </div>
        </div>

        <div style={{ fontSize: 8.5, color: "#E0AAFF", textAlign: "center" }}>
          GELU(x W_1 + b_1) W_2 + b_2
        </div>
      </div>

      {/* Bottom Telemetry HUD */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          display: "flex",
          gap: 20,
          backgroundColor: "rgba(15, 1, 30, 0.85)",
          padding: "6px 16px",
          borderRadius: 8,
          border: "1px solid rgba(199, 125, 255, 0.3)",
          fontSize: 9.5,
          color: "#E0AAFF",
        }}
      >
        <span>GRADIENT VANISHING: <b style={{ color: "#5AF78E" }}>PREVENTED</b></span>
        <span>•</span>
        <span>STREAM THROUGHPUT: <b style={{ color: "#FF2A85" }}>100% UNIMPEDED</b></span>
      </div>
    </div>
  );
};
