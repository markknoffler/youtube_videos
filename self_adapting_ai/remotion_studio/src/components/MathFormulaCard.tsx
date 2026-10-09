import React from "react";
import { useCurrentFrame } from "remotion";

interface FormulaTerm {
  symbol: string;
  label: string;
  color?: string;
}

interface MathFormulaCardProps {
  title: string;
  formula: string;
  terms?: FormulaTerm[];
  conclusion: string;
  width?: number;
}

export const MathFormulaCard: React.FC<MathFormulaCardProps> = ({
  title,
  formula,
  terms = [],
  conclusion,
  width = 560,
}) => {
  const frame = useCurrentFrame();

  // Active term highlight scanning
  const activeTermIdx = terms.length > 0 ? Math.floor(frame / 60) % terms.length : 0;

  return (
    <div
      style={{
        width,
        backgroundColor: "rgba(20, 2, 36, 0.9)",
        borderRadius: 14,
        border: "1.5px solid #C77DFF",
        boxShadow: "0 8px 30px rgba(123, 44, 191, 0.3), inset 0 0 16px rgba(157, 78, 221, 0.15)",
        padding: "16px 20px",
        display: "flex",
        flexDirection: "column",
        gap: 12,
        backdropFilter: "blur(14px)",
        boxSizing: "border-box",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 800, color: "#FF2A85", letterSpacing: 1 }}>
          {title.toUpperCase()}
        </span>
        <span style={{ fontSize: 10, color: "#E0AAFF", fontFamily: "monospace" }}>
          FORMAL PROOF
        </span>
      </div>

      {/* Main Formula Banner */}
      <div
        style={{
          backgroundColor: "#10011C",
          borderRadius: 8,
          padding: "12px 16px",
          border: "1px solid #7B2CBF",
          textAlign: "center",
          boxShadow: "inset 0 0 12px rgba(0,0,0,0.6)",
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            fontSize: 16,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: 0.5,
          }}
        >
          {formula}
        </div>
      </div>

      {/* Term Breakdown Grid */}
      {terms.length > 0 && (
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {terms.map((t, idx) => {
            const isActive = idx === activeTermIdx;
            const termColor = t.color || (isActive ? "#FF2A85" : "#C77DFF");

            return (
              <div
                key={idx}
                style={{
                  flex: "1 1 calc(50% - 10px)",
                  backgroundColor: isActive ? "rgba(255, 42, 133, 0.15)" : "rgba(31, 4, 56, 0.5)",
                  border: `1px solid ${isActive ? "#FF2A85" : "rgba(123, 44, 191, 0.4)"}`,
                  borderRadius: 6,
                  padding: "6px 10px",
                  display: "flex",
                  gap: 8,
                  alignItems: "center",
                  transition: "all 0.1s ease",
                  boxShadow: isActive ? "0 0 8px rgba(255, 42, 133, 0.4)" : "none",
                }}
              >
                <span
                  style={{
                    fontFamily: "monospace",
                    fontSize: 13,
                    fontWeight: 800,
                    color: termColor,
                  }}
                >
                  {t.symbol}
                </span>
                <span style={{ fontSize: 11, color: "#E0AAFF" }}>{t.label}</span>
              </div>
            );
          })}
        </div>
      )}

      {/* Conclusion / Takeaway */}
      <div
        style={{
          borderTop: "1px dashed #7B2CBF",
          paddingTop: 8,
          fontSize: 11.5,
          color: "#FFFFFF",
          lineHeight: 1.4,
          display: "flex",
          gap: 6,
        }}
      >
        <span style={{ color: "#FF2A85", fontWeight: 800 }}>▶ THEOREM RESULT:</span>
        <span style={{ color: "#E0AAFF" }}>{conclusion}</span>
      </div>
    </div>
  );
};
