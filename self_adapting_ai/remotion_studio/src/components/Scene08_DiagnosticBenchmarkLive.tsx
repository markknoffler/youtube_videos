import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AnimatedLossChart } from "./AnimatedLossChart";

export const Scene08_DiagnosticBenchmarkLive: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

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
      {/* LEFT: Live Animated Loss Chart & Racing Curves */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <AnimatedLossChart width={430} height={460} />
      </div>

      {/* RIGHT: In-Context KV Associative Recall Visual Probe */}
      <div
        style={{
          width: 400,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>IN-CONTEXT KV RETRIEVAL</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800 }}>LIVE PROBE</span>
        </div>

        {/* KV Binding Pair sequence */}
        <div
          style={{
            backgroundColor: "rgba(10, 0, 18, 0.85)",
            borderRadius: 10,
            border: "1px dashed rgba(199, 125, 255, 0.3)",
            padding: 12,
            display: "flex",
            flexDirection: "column",
            gap: 8,
          }}
        >
          <div style={{ fontSize: 9, color: "#C77DFF", fontWeight: 700 }}>TOKEN SEQUENCE IN CONTEXT</div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {["(K1, V1)", "(K2, V2)", "(K3, V3)", "(K4, V4)", "QUERY: K3"].map((tok, i) => (
              <span
                key={i}
                style={{
                  fontSize: 8.5,
                  padding: "3px 6px",
                  borderRadius: 4,
                  backgroundColor: tok.includes("QUERY") ? "#FF2A85" : "#1B012E",
                  color: "#FFFFFF",
                  fontWeight: tok.includes("QUERY") ? 800 : 500,
                  border: tok.includes("QUERY") ? "1px solid #FFFFFF" : "1px solid #7B2CBF",
                }}
              >
                {tok}
              </span>
            ))}
          </div>
        </div>

        {/* Retrieval Verdict Cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {/* Transformer Result */}
          <div
            style={{
              backgroundColor: "rgba(10, 0, 18, 0.9)",
              border: "1.5px solid #5AF78E",
              borderRadius: 8,
              padding: "10px 12px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 9.5, fontWeight: 900, color: "#5AF78E" }}>TRANSFORMER</span>
              <span style={{ fontSize: 10, fontWeight: 800, color: "#5AF78E" }}>92.3% ACCURACY</span>
            </div>
            <div style={{ fontSize: 8.5, color: "#FFFFFF", marginTop: 4 }}>
              OUTPUT: [V3] (PERFECT ASSOCIATIVE RETRIEVAL)
            </div>
          </div>

          {/* Dynamic Rewiring Result */}
          <div
            style={{
              backgroundColor: "rgba(10, 0, 18, 0.9)",
              border: "1.5px solid #FF2A85",
              borderRadius: 8,
              padding: "10px 12px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 9.5, fontWeight: 900, color: "#FF2A85" }}>DYNAMIC REWIRING</span>
              <span style={{ fontSize: 10, fontWeight: 800, color: "#FF2A85" }}>7.7% ACCURACY</span>
            </div>
            <div style={{ fontSize: 8.5, color: "#FFFFFF", marginTop: 4 }}>
              OUTPUT: [CROSSTALK NOISE / RANDOM CHANCE]
            </div>
          </div>
        </div>

        {/* Summary Metric */}
        <div
          style={{
            backgroundColor: "#200133",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #7B2CBF",
            fontSize: 9,
            color: "#E0AAFF",
            textAlign: "center",
          }}
        >
          THEOREMS 1, 2, AND 3 CONFIRMED IN EMPIRICAL SILICON
        </div>
      </div>
    </div>
  );
};
