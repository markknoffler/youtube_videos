import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene02_STDPSynapse3D: React.FC<{ startFrame?: number }> = ({ startFrame = 1500 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: Math.max(0, frame - startFrame), fps, config: { damping: 14 } });

  // Delta t millisecond cycle (-40ms to +40ms)
  const deltaT = ((frame % 120) - 60) * 0.8;
  const isLTP = deltaT > 0;
  // Synaptic weight delta based on STDP exponential
  const deltaW = isLTP
    ? 0.85 * Math.exp(-deltaT / 15)
    : -0.65 * Math.exp(deltaT / 20);

  // Synapse thickness scaling with LTP
  const cleftWidth = isLTP ? 14 + deltaW * 8 : 14;

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
      {/* LEFT: Microscopic Synaptic Cleft Biomechanics */}
      <div
        style={{
          width: 440,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>BIOCHEMICAL SYNAPSE JUNCTION</span>
          <span
            style={{
              fontSize: 8.5,
              color: "#FFFFFF",
              backgroundColor: isLTP ? "#5AF78E" : "#FF2A85",
              padding: "2px 6px",
              borderRadius: 4,
              fontWeight: 800,
            }}
          >
            {isLTP ? "LTP: STRENGTHENING" : "LTD: DEPRESSION"}
          </span>
        </div>

        {/* Synapse SVG Diagram */}
        <div
          style={{
            height: 260,
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(255, 42, 133, 0.4)",
            position: "relative",
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="400" height="250" viewBox="0 0 400 250">
            {/* Pre-Synaptic Bouton (Left Bulb) */}
            <path
              d="M 20 50 C 120 50, 160 80, 170 125 C 160 170, 120 200, 20 200"
              fill="rgba(35, 2, 60, 0.8)"
              stroke="#C77DFF"
              strokeWidth="2.5"
            />
            {/* Neurotransmitter Vesicles inside Bouton */}
            {Array.from({ length: 9 }).map((_, i) => {
              const vx = 60 + (i % 3) * 32;
              const vy = 90 + Math.floor(i / 3) * 28;
              return (
                <circle
                  key={i}
                  cx={vx}
                  cy={vy}
                  r="6"
                  fill="#FF2A85"
                  stroke="#FFFFFF"
                  strokeWidth="1"
                  filter="drop-shadow(0 0 4px #FF2A85)"
                />
              );
            })}

            {/* Post-Synaptic Spine (Right Bulb) */}
            <path
              d={`M 380 50 C 280 50, ${220 + cleftWidth} 80, ${210 + cleftWidth} 125 C ${220 + cleftWidth} 170, 280 200, 380 200`}
              fill="rgba(30, 2, 50, 0.8)"
              stroke="#FF2A85"
              strokeWidth="2.5"
            />

            {/* AMPA / NMDA Receptor Gates on Post-synaptic Membrane */}
            {Array.from({ length: 6 }).map((_, r) => {
              const ry = 75 + r * 20;
              const rx = 210 + cleftWidth;
              return (
                <rect
                  key={r}
                  x={rx}
                  y={ry}
                  width="6"
                  height="12"
                  rx="2"
                  fill={isLTP ? "#5AF78E" : "#9D4EDD"}
                  stroke="#FFFFFF"
                  strokeWidth="1"
                />
              );
            })}

            {/* Action Potential Waveform Arrow */}
            <path
              d="M 120 20 Q 140 10 160 20 T 200 20"
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2"
              strokeDasharray="4 2"
            />
          </svg>

          {/* Real-time Delta t Badge */}
          <div
            style={{
              position: "absolute",
              top: 10,
              backgroundColor: "#160128",
              border: "1px solid #7B2CBF",
              borderRadius: 6,
              padding: "4px 10px",
              fontSize: 9,
              color: "#E0AAFF",
            }}
          >
            SPIKE DELAY Δt = {deltaT > 0 ? `+${deltaT.toFixed(1)}` : deltaT.toFixed(1)} ms
          </div>
        </div>

        {/* Plasticity Formula HUD */}
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
          <span>ΔW = A₊ · exp(-Δt / τ₊)</span>
          <span style={{ color: deltaW > 0 ? "#5AF78E" : "#FF2A85", fontWeight: 800 }}>
            PLASTICITY FLUX: {deltaW > 0 ? `+${deltaW.toFixed(3)}` : deltaW.toFixed(3)}
          </span>
        </div>
      </div>

      {/* RIGHT: STDP Exponential Curve & Glial Pruning */}
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>STDP TIME CONTOUR</span>
          <span style={{ fontSize: 8.5, color: "#C77DFF", fontWeight: 700 }}>BI et al. (1998)</span>
        </div>

        {/* STDP Graph Coordinate System */}
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
          <svg width="350" height="220" viewBox="0 0 350 220">
            {/* Coordinate Axes */}
            <line x1="20" y1="110" x2="330" y2="110" stroke="#7B2CBF" strokeWidth="1.5" />
            <line x1="175" y1="20" x2="175" y2="200" stroke="#7B2CBF" strokeWidth="1.5" />

            {/* Labels */}
            <text x="310" y="105" fill="#E0AAFF" fontSize="9">Δt (ms)</text>
            <text x="180" y="30" fill="#E0AAFF" fontSize="9">ΔW (LTP)</text>
            <text x="180" y="195" fill="#E0AAFF" fontSize="9">ΔW (LTD)</text>

            {/* LTP Curve (Positive Quadrant) */}
            <path
              d="M 175 40 Q 210 100 320 108"
              fill="none"
              stroke="#5AF78E"
              strokeWidth="3"
              filter="drop-shadow(0 0 6px #5AF78E)"
            />

            {/* LTD Curve (Negative Quadrant) */}
            <path
              d="M 30 112 Q 140 120 175 180"
              fill="none"
              stroke="#FF2A85"
              strokeWidth="3"
              filter="drop-shadow(0 0 6px #FF2A85)"
            />

            {/* Live Indicator Point moving on curve */}
            <circle
              cx={175 + deltaT * 3}
              cy={110 - deltaW * 90}
              r="6"
              fill="#FFFFFF"
              filter="drop-shadow(0 0 8px #FF2A85)"
            />
          </svg>
        </div>

        {/* Structural Plasticity Takeaway */}
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
          "NEURONS THAT FIRE TOGETHER, WIRE TOGETHER"
        </div>
      </div>
    </div>
  );
};
