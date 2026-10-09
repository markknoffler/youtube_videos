import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface MemristorCrossbar3DProps {
  startFrame?: number;
  width?: number;
  height?: number;
}

export const MemristorCrossbar3D: React.FC<MemristorCrossbar3DProps> = ({
  startFrame = 0,
  width = 540,
  height = 420,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const entrance = spring({ frame: relFrame, fps, config: { damping: 14 } });

  const rows = 6;
  const cols = 6;

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        backgroundColor: "rgba(14, 2, 28, 0.94)",
        border: "1.5px solid #5AF78E",
        borderRadius: 14,
        boxShadow: "0 0 35px rgba(90, 247, 142, 0.35)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
        transform: `scale(${entrance})`,
        padding: "16px 20px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <span
            style={{
              fontSize: 8.5,
              backgroundColor: "#5AF78E",
              color: "#000000",
              padding: "2px 6px",
              borderRadius: 3,
              fontWeight: 900,
            }}
          >
            PILLAR 1: ANALOG NEUROMORPHIC
          </span>
          <div style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF", marginTop: 4 }}>
            MEMRISTIVE CROSSBAR IN-SITU PLASTICITY
          </div>
        </div>
        <div style={{ fontSize: 9, color: "#5AF78E", fontWeight: 700 }}>
          ● IN-MEMORY CONDUCTANCE
        </div>
      </div>

      {/* 3D Crossbar Matrix Viewport */}
      <div
        style={{
          position: "relative",
          height: 250,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          perspective: 800,
        }}
      >
        <svg
          style={{
            width: 360,
            height: 240,
            transform: "rotateX(25deg) rotateZ(-10deg)",
            transformOrigin: "center center",
          }}
          viewBox="0 0 360 240"
        >
          {/* Horizontal Wordlines (Input Voltage V_i) */}
          {Array.from({ length: rows }).map((_, r) => {
            const y = 30 + r * 34;
            const isPulse = (relFrame + r * 10) % 60 < 20;

            return (
              <g key={`row-${r}`}>
                <line
                  x1="20"
                  y1={y}
                  x2="340"
                  y2={y}
                  stroke={isPulse ? "#FF2A85" : "rgba(199, 125, 255, 0.4)"}
                  strokeWidth={isPulse ? 3 : 1.5}
                  filter={isPulse ? "drop-shadow(0 0 6px #FF2A85)" : undefined}
                />
                <text x="5" y={y + 4} fill="#C77DFF" fontSize="8" fontFamily="monospace">
                  V_{r}
                </text>
              </g>
            );
          })}

          {/* Vertical Bitlines (Output Current I_j = sum G_ij * V_i) */}
          {Array.from({ length: cols }).map((_, c) => {
            const x = 50 + c * 50;
            return (
              <g key={`col-${c}`}>
                <line
                  x1={x}
                  y1="10"
                  x2={x}
                  y2="220"
                  stroke="rgba(90, 247, 142, 0.4)"
                  strokeWidth="1.5"
                />
                <text x={x - 6} y="235" fill="#5AF78E" fontSize="8" fontFamily="monospace">
                  I_{c}
                </text>
              </g>
            );
          })}

          {/* Memristor Crossbar Junctions */}
          {Array.from({ length: rows }).map((_, r) => {
            const y = 30 + r * 34;
            return Array.from({ length: cols }).map((_, c) => {
              const x = 50 + c * 50;
              const conductance = 0.2 + ((Math.sin(r * 2 + c * 3 + relFrame * 0.1) + 1) / 2) * 0.8;
              const isUpdated = (relFrame + r * 7 + c * 11) % 50 < 15;

              return (
                <g key={`junc-${r}-${c}`}>
                  <circle
                    cx={x}
                    cy={y}
                    r={isUpdated ? 5 : 3.5}
                    fill={isUpdated ? "#5AF78E" : "#FF2A85"}
                    opacity={conductance}
                    filter={isUpdated ? "drop-shadow(0 0 6px #5AF78E)" : undefined}
                  />
                </g>
              );
            });
          })}
        </svg>
      </div>

      {/* Telemetry Footer */}
      <div
        style={{
          backgroundColor: "rgba(18, 2, 35, 0.9)",
          border: "1px solid rgba(90, 247, 142, 0.3)",
          borderRadius: 8,
          padding: "8px 12px",
          display: "flex",
          justifyContent: "space-between",
          fontSize: 9,
          color: "#E0AAFF",
        }}
      >
        <span>VON NEUMANN BOTTLENECK: <b style={{ color: "#5AF78E" }}>BYPASSED (0 ns BUS DELAY)</b></span>
        <span>KIRCHHOFF SUMMATION: <b style={{ color: "#5AF78E" }}>O(1) ANALOG ACCUMULATION</b></span>
      </div>
    </div>
  );
};
