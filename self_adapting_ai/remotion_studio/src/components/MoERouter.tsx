import React from "react";
import { useCurrentFrame } from "remotion";

interface MoERouterProps {
  width?: number;
  height?: number;
}

export const MoERouter: React.FC<MoERouterProps> = ({
  width = 540,
  height = 300,
}) => {
  const frame = useCurrentFrame();

  const experts = [
    { id: 1, name: "Math & Proofs" },
    { id: 14, name: "Code Synthesis" },
    { id: 42, name: "Logical Deduct" },
    { id: 89, name: "Grammar & Lang" },
    { id: 128, name: "Fact Retrieval" },
    { id: 195, name: "Symbolic Calc" },
    { id: 211, name: "Algorithmic" },
    { id: 256, name: "Commonsense" },
  ];

  // Active expert shifts over time
  const activeExpertIdx = Math.floor(frame / 22) % experts.length;

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "#120224",
        borderRadius: 14,
        border: "1.5px solid #C77DFF",
        boxShadow: "0 0 28px rgba(199, 125, 255, 0.25)",
        padding: 16,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#C77DFF" }}>
          DEEPSEEK-V3 DYNAMIC MOE ROUTER
        </span>
        <span style={{ fontSize: 9.5, color: "#FF2A85", fontWeight: 700 }}>
          Top-8 / 256 Experts
        </span>
      </div>

      {/* Visual Dispatch Flow */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", margin: "12px 0" }}>
        {/* Input Token Token */}
        <div
          style={{
            padding: "8px 12px",
            backgroundColor: "#2B054D",
            border: "1.5px solid #FF2A85",
            borderRadius: 8,
            boxShadow: "0 0 12px #FF2A85",
            color: "#FFFFFF",
            fontSize: 11,
            fontWeight: 700,
          }}
        >
          Token [x_t]
        </div>

        {/* Central Router Gate */}
        <div
          style={{
            width: 70,
            height: 70,
            borderRadius: "50%",
            backgroundColor: "#1F0438",
            border: "2px solid #C77DFF",
            boxShadow: "0 0 20px rgba(199, 125, 255, 0.6)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 9,
            color: "#E0AAFF",
            textAlign: "center",
          }}
        >
          <span>Top-8 Gate</span>
          <span style={{ color: "#FF2A85", fontWeight: 700 }}>Softmax</span>
        </div>

        {/* Grid of Expert Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6, width: 260 }}>
          {experts.map((exp, idx) => {
            const isActive = idx === activeExpertIdx || idx === (activeExpertIdx + 1) % experts.length;
            return (
              <div
                key={exp.id}
                style={{
                  padding: "5px 8px",
                  borderRadius: 6,
                  backgroundColor: isActive ? "#FF2A85" : "rgba(42, 6, 75, 0.5)",
                  border: isActive ? "1px solid #FFFFFF" : "1px solid #5A189A",
                  boxShadow: isActive ? "0 0 10px #FF2A85" : "none",
                  fontSize: 8.5,
                  color: isActive ? "#FFFFFF" : "#D8B4F8",
                  fontWeight: isActive ? 700 : 400,
                  display: "flex",
                  justifyContent: "space-between",
                  transition: "all 0.1s ease-out",
                }}
              >
                <span>E#{exp.id}</span>
                <span>{exp.name}</span>
              </div>
            );
          })}
        </div>
      </div>

      <div
        style={{
          borderTop: "1px dashed #7B2CBF",
          paddingTop: 6,
          fontSize: 9.5,
          color: "#E0AAFF",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>Conditional Compute: 37B active parameters out of 671B</span>
        <span style={{ color: "#5AF78E" }}>Zero Cache Thrash</span>
      </div>
    </div>
  );
};
