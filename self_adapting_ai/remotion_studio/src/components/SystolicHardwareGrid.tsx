import React from "react";
import { useCurrentFrame } from "remotion";

interface SystolicHardwareGridProps {
  size?: number;
}

export const SystolicHardwareGrid: React.FC<SystolicHardwareGridProps> = ({
  size = 340,
}) => {
  const frame = useCurrentFrame();
  const gridSize = 6;
  const cellSize = (size - 60) / gridSize;

  // Wavefront propagation: diagonal wave across the systolic array
  const wave = (frame * 0.15) % (gridSize * 2);

  return (
    <div
      style={{
        width: size,
        height: size,
        backgroundColor: "#110222",
        borderRadius: 14,
        border: "1.5px solid #FF2A85",
        boxShadow: "0 0 28px rgba(255, 42, 133, 0.25)",
        padding: 14,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#FF2A85" }}>
          SYSTOLIC TENSOR ARRAY (GEMM)
        </span>
        <span style={{ fontSize: 9.5, color: "#5AF78E", fontWeight: 700 }}>
          94.8% FLOPS
        </span>
      </div>

      {/* Grid of Multiply-Accumulate Processing Elements */}
      <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 8 }}>
        {Array.from({ length: gridSize }).map((_, r) => (
          <div key={r} style={{ display: "flex", gap: 4 }}>
            {Array.from({ length: gridSize }).map((_, c) => {
              const diagDist = r + c;
              const isWave = Math.abs(diagDist - wave) < 1.1;
              const bg = isWave ? "#FF2A85" : "rgba(123, 44, 191, 0.35)";
              const glow = isWave ? "0 0 10px #FF2A85" : "none";

              return (
                <div
                  key={c}
                  style={{
                    width: cellSize,
                    height: cellSize,
                    backgroundColor: bg,
                    borderRadius: 4,
                    border: isWave ? "1.5px solid #FFFFFF" : "1px solid rgba(199, 125, 255, 0.3)",
                    boxShadow: glow,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 7.5,
                    color: isWave ? "#FFFFFF" : "#E0AAFF",
                    fontWeight: isWave ? 800 : 400,
                    transition: "background-color 0.08s",
                  }}
                >
                  MAC
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {/* Hardware Utilization Readout */}
      <div
        style={{
          marginTop: 6,
          borderTop: "1px dashed #7B2CBF",
          paddingTop: 6,
          display: "flex",
          justifyContent: "space-between",
          fontSize: 9.5,
          color: "#E0AAFF",
        }}
      >
        <span>Dense Core: Active</span>
        <span style={{ color: "#FF2A85" }}>Sparse Graph: 7.2% thrashing</span>
      </div>
    </div>
  );
};
