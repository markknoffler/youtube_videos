import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { SystolicHardwareGrid } from "./SystolicHardwareGrid";

export const Sentence8_SystolicPowerGrid: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 3800, fps, config: { damping: 14 } });

  // Power surges
  const gigawatts = (1.21 + Math.sin(frame * 0.1) * 0.04).toFixed(2);
  const pflops = (197.4 + Math.sin(frame * 0.08) * 1.5).toFixed(1);

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
      {/* LEFT: Power Grid & Supercomputer Telemetry */}
      <div
        style={{
          width: 380,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>PLANETARY COMPUTE GRID</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800, border: "1px solid #FF2A85", padding: "2px 6px", borderRadius: 4 }}>
            MAX UTILIZATION
          </span>
        </div>

        {/* High Voltage Power Line Graphic */}
        <div
          style={{
            height: 120,
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
          <svg width="340" height="100" viewBox="0 0 340 100">
            {/* Electrical Transmission Pylon Tower */}
            <line x1="80" y1="20" x2="80" y2="90" stroke="#C77DFF" strokeWidth="2.5" />
            <line x1="60" y1="40" x2="100" y2="40" stroke="#C77DFF" strokeWidth="2" />
            <line x1="50" y1="60" x2="110" y2="60" stroke="#C77DFF" strokeWidth="2" />

            <line x1="260" y1="20" x2="260" y2="90" stroke="#C77DFF" strokeWidth="2.5" />
            <line x1="240" y1="40" x2="280" y2="40" stroke="#C77DFF" strokeWidth="2" />
            <line x1="230" y1="60" x2="290" y2="60" stroke="#C77DFF" strokeWidth="2" />

            {/* Pulsing High Voltage Wire Cables */}
            <path
              d="M 60 40 Q 170 85 240 40"
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2.5"
              strokeDasharray="8 4"
              strokeDashoffset={-frame * 3}
              filter="drop-shadow(0 0 8px #FF2A85)"
            />
            <path
              d="M 50 60 Q 170 105 230 60"
              fill="none"
              stroke="#E0AAFF"
              strokeWidth="2"
              strokeDasharray="6 3"
              strokeDashoffset={-frame * 2.5}
            />
          </svg>
        </div>

        {/* Real-time Surge Readouts */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <div style={{ backgroundColor: "#150125", padding: "8px 12px", borderRadius: 8, border: "1px solid #7B2CBF" }}>
            <div style={{ fontSize: 8.5, color: "#C77DFF" }}>GRID POWER DRAW</div>
            <div style={{ fontSize: 20, fontWeight: 900, color: "#FF2A85", marginTop: 2 }}>
              {gigawatts} GW
            </div>
            <div style={{ fontSize: 8, color: "#E0AAFF" }}>Dedicated utility-scale substation feeds</div>
          </div>

          <div style={{ backgroundColor: "#150125", padding: "8px 12px", borderRadius: 8, border: "1px solid #7B2CBF" }}>
            <div style={{ fontSize: 8.5, color: "#C77DFF" }}>CLUSTER FP8 COMPUTE</div>
            <div style={{ fontSize: 20, fontWeight: 900, color: "#FFFFFF", marginTop: 2 }}>
              {pflops} PFLOPS
            </div>
            <div style={{ fontSize: 8, color: "#E0AAFF" }}>32,768 NVIDIA H100 SXM5 GPUs in NVLink mesh</div>
          </div>
        </div>

        {/* Bottom Capex Banner */}
        <div
          style={{
            backgroundColor: "#200133",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #FF2A85",
            fontSize: 9.5,
            color: "#FFFFFF",
            textAlign: "center",
            fontWeight: 800,
          }}
        >
          GLOBAL CAPEX: $100B+ SCALING THIS ARCHITECTURE
        </div>
      </div>

      {/* RIGHT: Systolic Hardware Array in 100% Compute Saturation */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10, alignItems: "center" }}>
        <SystolicHardwareGrid size={440} />
      </div>
    </div>
  );
};
