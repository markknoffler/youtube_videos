import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface LifelongMemoryPipelineProps {
  startFrame?: number;
  width?: number;
  height?: number;
  isFrozen?: boolean;
}

export const LifelongMemoryPipeline: React.FC<LifelongMemoryPipelineProps> = ({
  startFrame = 0,
  width = 680,
  height = 420,
  isFrozen = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const entrance = spring({ frame: relFrame, fps, config: { damping: 14 } });

  // Token traversal cycle (token flies from left to right every 60 frames)
  const tokenCycle = (relFrame * 4) % (width - 120);

  const stages = [
    { title: "DATA STREAM", sub: "Trillions of Tokens", icon: "🌐", color: "#C77DFF" },
    { title: "HBM3 MEMORY", sub: "1.8T Parameters", icon: "💾", color: "#FF2A85" },
    { title: "TRANSFORMER CORE", sub: "Dense Attention GEMM", icon: "⚡", color: "#5AF78E" },
    { title: "INFERENCE OUTPUT", sub: "Logits / Next Token", icon: "🎯", color: "#E0AAFF" },
  ];

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        backgroundColor: "rgba(14, 2, 28, 0.94)",
        border: `1.5px solid ${isFrozen ? "#00F0FF" : "#FF2A85"}`,
        borderRadius: 14,
        boxShadow: isFrozen
          ? "0 0 35px rgba(0, 240, 255, 0.4), inset 0 0 30px rgba(0, 240, 255, 0.15)"
          : "0 0 35px rgba(255, 42, 133, 0.35)",
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
      {/* Top Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <span
            style={{
              fontSize: 8.5,
              backgroundColor: isFrozen ? "#00F0FF" : "#FF2A85",
              color: isFrozen ? "#000000" : "#FFFFFF",
              padding: "2px 6px",
              borderRadius: 3,
              fontWeight: 800,
            }}
          >
            {isFrozen ? "CRYO-FREEZE IMMUTABILITY" : "COMPUTATIONAL PIPELINE"}
          </span>
          <span style={{ marginLeft: 8, fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>
            {isFrozen ? "FROZEN SILICON BEDROCK (dW/dt = 0)" : "LIVE MODEL FORWARD PASS"}
          </span>
        </div>
        <div style={{ fontSize: 9, color: isFrozen ? "#00F0FF" : "#5AF78E", fontWeight: 700 }}>
          {isFrozen ? "🔒 PARAMETERS RIGID" : "● ACTIVATIONS ACTIVE"}
        </div>
      </div>

      {/* Main 4-Stage Horizontal Pipeline */}
      <div
        style={{
          position: "relative",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          margin: "15px 0",
        }}
      >
        {/* Connecting glowing conduits */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: 40,
            right: 40,
            height: 3,
            backgroundColor: isFrozen ? "rgba(0, 240, 255, 0.3)" : "rgba(255, 42, 133, 0.3)",
            transform: "translateY(-50%)",
            zIndex: 1,
          }}
        />

        {/* Traveling prompt token particle */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: 40 + tokenCycle,
            width: 14,
            height: 14,
            borderRadius: "50%",
            backgroundColor: "#5AF78E",
            boxShadow: "0 0 12px #5AF78E",
            transform: "translate(-50%, -50%)",
            zIndex: 3,
          }}
        />

        {stages.map((st, i) => (
          <div
            key={i}
            style={{
              position: "relative",
              width: 130,
              backgroundColor: "rgba(25, 3, 45, 0.95)",
              border: `1.5px solid ${isFrozen ? "#00F0FF" : st.color}`,
              borderRadius: 10,
              padding: "10px 8px",
              textAlign: "center",
              zIndex: 2,
              boxShadow: `0 0 15px ${st.color}33`,
            }}
          >
            <div style={{ fontSize: 20, marginBottom: 4 }}>{st.icon}</div>
            <div style={{ fontSize: 9.5, fontWeight: 800, color: "#FFFFFF", marginBottom: 2 }}>
              {st.title}
            </div>
            <div style={{ fontSize: 8, color: st.color, fontWeight: 700 }}>{st.sub}</div>

            {/* Ice frost overlay if frozen */}
            {isFrozen && (
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backgroundColor: "rgba(0, 240, 255, 0.12)",
                  borderRadius: 10,
                  border: "1px solid rgba(0, 240, 255, 0.4)",
                  pointerEvents: "none",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <span style={{ fontSize: 16 }}>🔒</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Real-time Weight Mutation Telemetry */}
      <div
        style={{
          backgroundColor: "rgba(20, 2, 38, 0.9)",
          border: "1px solid rgba(199, 125, 255, 0.3)",
          borderRadius: 8,
          padding: "8px 14px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 9.5,
        }}
      >
        <div style={{ display: "flex", gap: 16 }}>
          <span>
            SYNAPSE DELTA:{" "}
            <span style={{ color: "#00F0FF", fontWeight: 800 }}>Δw_ij = 0.00000000</span>
          </span>
          <span>
            PARAMETRIC STABILITY:{" "}
            <span style={{ color: "#5AF78E", fontWeight: 800 }}>100.0% INVARIANT</span>
          </span>
        </div>
        <div style={{ color: "#E0AAFF", fontFamily: "monospace" }}>
          MEMORY REALLOCATION: <span style={{ color: "#FF2A85", fontWeight: 800 }}>DISABLED</span>
        </div>
      </div>
    </div>
  );
};
