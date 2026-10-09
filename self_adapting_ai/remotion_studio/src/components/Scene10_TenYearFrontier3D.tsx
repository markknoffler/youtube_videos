import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AnnotatedPaperScreenshot } from "./AnnotatedPaperScreenshot";

export const Scene10_TenYearFrontier3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  // 4 Pillars rotation
  const pillarIndex = Math.floor(frame / 60) % 4;

  const pillars = [
    { title: "META-PLASTICITY", desc: "Meta-learned dynamic rules discovering stable multi-rank learning dynamics.", tag: "SCHMIDHUBER / KIRSCH" },
    { title: "LIQUID NEURAL ODEs", desc: "Continuous-time differential hidden states with dynamic time-constants.", tag: "HASANI / RUS (MIT)" },
    { title: "KOLMOGOROV-ARNOLD (KAN)", desc: "Learnable non-linear spline functions directly on the synaptic edges.", tag: "LIU ET AL. (2024)" },
    { title: "MEMRISTIVE CROSSBARS", desc: "In-memory analog crossbars breaking the Hardware Lottery co-locating compute.", tag: "NEUROMORPHIC 2035" },
  ];

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
      {/* LEFT: 4 Technological Revolutions (2026 - 2035) Interactive Cards */}
      <div
        style={{
          width: 410,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>THE 10-YEAR FRONTIER</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800 }}>2026 — 2035 ROADMAP</span>
        </div>

        {/* 4 Pillars Interactive Stacks */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {pillars.map((pil, idx) => {
            const isActive = idx === pillarIndex;

            return (
              <div
                key={idx}
                style={{
                  padding: "10px 14px",
                  borderRadius: 10,
                  backgroundColor: isActive ? "rgba(255, 42, 133, 0.25)" : "rgba(10, 0, 18, 0.85)",
                  border: isActive ? "1.5px solid #FF2A85" : "1px solid rgba(199, 125, 255, 0.2)",
                  boxShadow: isActive ? "0 0 16px rgba(255, 42, 133, 0.4)" : "none",
                  display: "flex",
                  flexDirection: "column",
                  gap: 3,
                  transition: "all 0.2s ease",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontSize: 10, fontWeight: 900, color: isActive ? "#FFFFFF" : "#C77DFF" }}>
                    {idx + 1}. {pil.title}
                  </span>
                  <span style={{ fontSize: 7.5, color: "#E0AAFF", fontWeight: 700 }}>{pil.tag}</span>
                </div>
                <div style={{ fontSize: 8.5, color: "#FFFFFF", opacity: isActive ? 1 : 0.7 }}>
                  {pil.desc}
                </div>
              </div>
            );
          })}
        </div>

        {/* Grand Synthesis Verdict */}
        <div
          style={{
            backgroundColor: "#200133",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #7B2CBF",
            fontSize: 9,
            color: "#5AF78E",
            textAlign: "center",
            fontWeight: 800,
          }}
        >
          NOT A STATIC MONOLITH. A SELF-ADAPTING MATHEMATICAL ORGANISM.
        </div>
      </div>

      {/* RIGHT: KAN & Liquid Network Paper Spotlight */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <AnnotatedPaperScreenshot
          imageSrc="assets/papers/kan_paper.png"
          title="KAN: Kolmogorov-Arnold Networks"
          authors="Ziming Liu, Yixuan Wang et al. (MIT & Caltech)"
          venue="ArXiv 2024"
          arxivId="2404.19756"
          width={420}
          height={460}
          highlights={[
            {
              topPercent: 32,
              leftPercent: 8,
              widthPercent: 84,
              heightPercent: 6,
              color: "#FF2A85",
              noteText: "LEARNABLE SPLINE FUNCTIONS ON EDGES!",
              notePosition: "bottom",
            },
            {
              topPercent: 58,
              leftPercent: 10,
              widthPercent: 80,
              heightPercent: 8,
              color: "#5AF78E",
              noteText: "★ SHIFTS POWER TO SYNAPTIC DEPTH",
              notePosition: "top",
            },
          ]}
        />
      </div>
    </div>
  );
};
