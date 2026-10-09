import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Sentence6_CryoFreeze: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 2700, fps, config: { damping: 14 } });

  // Frost shockwave progression (0 to 6 columns)
  const freezeProgress = interpolate(frame, [2730, 3100], [0, 6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Temperature plunge
  const temperature = Math.max(
    0,
    interpolate(frame, [2730, 3100], [300, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  ).toFixed(1);

  // Gradient rate
  const gradientFlux = Math.max(
    0,
    interpolate(frame, [2730, 3100], [1.428, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  ).toFixed(6);

  const gridSize = 6;

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
        padding: "0 20px",
        boxSizing: "border-box",
      }}
    >
      {/* LEFT: Cryo Diagnostics HUD Card */}
      <div
        style={{
          width: 250,
          height: 440,
          backgroundColor: "rgba(18, 1, 32, 0.85)",
          border: "2px solid #FF2A85",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 24px rgba(255, 42, 133, 0.3)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>CRYO-METRICS</span>
          <span
            style={{
              fontSize: 8.5,
              color: "#FFFFFF",
              backgroundColor: freezeProgress >= 5.5 ? "#FF2A85" : "#7B2CBF",
              padding: "2px 6px",
              borderRadius: 4,
              fontWeight: 800,
            }}
          >
            {freezeProgress >= 5.5 ? "PERMANENT LOCK" : "FREEZING..."}
          </span>
        </div>

        {/* Temperature Gauge */}
        <div
          style={{
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            padding: 12,
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.4)",
          }}
        >
          <div style={{ fontSize: 9, color: "#C77DFF" }}>LATTICE TEMPERATURE</div>
          <div style={{ fontSize: 24, fontWeight: 900, color: "#FF2A85", marginTop: 4 }}>
            {temperature} K
          </div>
          <div
            style={{
              width: "100%",
              height: 6,
              backgroundColor: "#20023B",
              borderRadius: 3,
              marginTop: 8,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${(parseFloat(temperature) / 300) * 100}%`,
                height: "100%",
                backgroundColor: "#FF2A85",
                transition: "width 0.1s linear",
              }}
            />
          </div>
        </div>

        {/* Weight Gradient Rate */}
        <div
          style={{
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            padding: 12,
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.4)",
          }}
        >
          <div style={{ fontSize: 9, color: "#C77DFF" }}>WEIGHT DERIVATIVE: dW/dt</div>
          <div style={{ fontSize: 18, fontWeight: 900, color: "#FFFFFF", marginTop: 4 }}>
            {gradientFlux}
          </div>
          <div style={{ fontSize: 8.5, color: "#E0AAFF", marginTop: 4 }}>
            {freezeProgress >= 5.5 ? "ALL GRADIENTS ZEROED" : "OPTIMIZATION HALTED"}
          </div>
        </div>

        {/* Status Badge */}
        <div
          style={{
            padding: "8px 10px",
            backgroundColor: "#2B0145",
            borderRadius: 8,
            border: "1px solid #FF2A85",
            fontSize: 9,
            color: "#FFFFFF",
            textAlign: "center",
            fontWeight: 700,
          }}
        >
          INFERENCE = PARAMETRIC MONUMENT
        </div>
      </div>

      {/* RIGHT: 6x6 3D Parameter Lattice Undergoing Shockwave Freeze */}
      <div
        style={{
          width: 530,
          height: 440,
          backgroundColor: "rgba(20, 2, 38, 0.85)",
          border: "2px solid #C77DFF",
          borderRadius: 14,
          padding: 16,
          boxShadow: "0 0 30px rgba(199, 125, 255, 0.3)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          alignItems: "center",
          boxSizing: "border-box",
        }}
      >
        <div style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 12, fontWeight: 900, color: "#FFFFFF" }}>
            70 BILLION PARAMETER SILICON LATTICE
          </span>
          <span style={{ fontSize: 9.5, color: "#C77DFF", fontWeight: 700 }}>
            {Math.round((freezeProgress / 6) * 100)}% FROZEN
          </span>
        </div>

        {/* 6x6 Grid of Weight Nodes */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
            gap: 12,
            padding: 10,
          }}
        >
          {Array.from({ length: gridSize * gridSize }).map((_, idx) => {
            const col = idx % gridSize;
            const row = Math.floor(idx / gridSize);
            const isFrozen = col <= freezeProgress;

            return (
              <div
                key={idx}
                style={{
                  width: 54,
                  height: 46,
                  borderRadius: 8,
                  backgroundColor: isFrozen ? "rgba(20, 2, 36, 0.95)" : "rgba(255, 42, 133, 0.3)",
                  border: isFrozen ? "1.5px solid #7B2CBF" : "2px solid #FF2A85",
                  boxShadow: isFrozen ? "inset 0 0 10px rgba(123, 44, 191, 0.8)" : "0 0 14px #FF2A85",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  transition: "all 0.2s ease",
                }}
              >
                {isFrozen ? (
                  <>
                    <span style={{ fontSize: 14, color: "#C77DFF" }}>🔒</span>
                    <span style={{ fontSize: 7, color: "#8A2BE2", fontWeight: 700 }}>FROZEN</span>
                  </>
                ) : (
                  <>
                    <span style={{ fontSize: 8.5, fontWeight: 900, color: "#FFFFFF" }}>W_{row}{col}</span>
                    <span style={{ fontSize: 7, color: "#FF2A85", fontWeight: 800 }}>LIVE</span>
                  </>
                )}
              </div>
            );
          })}
        </div>

        {/* Bottom Warning Banner */}
        <div
          style={{
            width: "100%",
            backgroundColor: "rgba(10, 0, 20, 0.9)",
            border: "1px dashed #FF2A85",
            borderRadius: 8,
            padding: "8px 12px",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 9.5,
            color: "#E0AAFF",
          }}
        >
          <span>SYNAPSE TOPOLOGY: LOCKED</span>
          <span style={{ color: "#FF2A85", fontWeight: 800 }}>ZERO RUNTIME EDGE MUTATIONS</span>
        </div>
      </div>
    </div>
  );
};
