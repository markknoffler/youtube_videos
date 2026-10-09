import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AnnotatedPaperScreenshot } from "./AnnotatedPaperScreenshot";
import { ScientistQuoteCard } from "./ScientistQuoteCard";

export const Scene07_HardwareLottery3D: React.FC = () => {
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
      {/* LEFT: Real Hardware Lottery Paper with Highlighting & Handwriting */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <AnnotatedPaperScreenshot
          imageSrc="assets/papers/hardware_lottery_paper.png"
          title="The Hardware Lottery"
          authors="Sara Hooker (Google Brain)"
          venue="Communications of the ACM (2020)"
          arxivId="2009.06489"
          width={430}
          height={460}
          highlights={[
            {
              topPercent: 35,
              leftPercent: 8,
              widthPercent: 84,
              heightPercent: 6,
              color: "#FF2A85",
              noteText: "HARDWARE DETERMINES RESEARCH SUCCESS!",
              notePosition: "bottom",
            },
            {
              topPercent: 60,
              leftPercent: 10,
              widthPercent: 78,
              heightPercent: 8,
              color: "#C77DFF",
              noteText: "★ DENSE GEMM WINS IN SILICON",
              notePosition: "top",
            },
          ]}
        />
      </div>

      {/* RIGHT: Hardware Utilization Comparison & Sara Hooker Quote */}
      <div
        style={{
          width: 400,
          height: 460,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <ScientistQuoteCard
          scientistName="Sara Hooker"
          role="Head of Cohere For AI (ex-Google Brain)"
          institution="Cohere / CACM"
          quoteText="An idea wins not because it is universally superior, but because it is suited to the hardware software co-design of its era."
          highlightPhrase="suited to the hardware software co-design"
          width={400}
        />

        {/* Hardware Arithmetic Intensity Comparison */}
        <div
          style={{
            backgroundColor: "rgba(18, 1, 32, 0.9)",
            border: "2px solid #FF2A85",
            borderRadius: 14,
            padding: 14,
            boxShadow: "0 0 24px rgba(255, 42, 133, 0.25)",
            display: "flex",
            flexDirection: "column",
            gap: 12,
          }}
        >
          <div style={{ fontSize: 10.5, fontWeight: 900, color: "#FFFFFF" }}>
            H100 SXM5 HARDWARE UTILIZATION
          </div>

          {/* Dense GEMM Bar */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "#5AF78E", fontWeight: 700 }}>
              <span>DENSE TRANSFORMER (GEMM)</span>
              <span>92.4% UTILIZATION</span>
            </div>
            <div style={{ width: "100%", height: 10, backgroundColor: "#150125", borderRadius: 5, marginTop: 4, overflow: "hidden" }}>
              <div style={{ width: "92.4%", height: "100%", backgroundColor: "#5AF78E", boxShadow: "0 0 8px #5AF78E" }} />
            </div>
          </div>

          {/* Sparse Pointer Chasing Bar */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "#FF2A85", fontWeight: 700 }}>
              <span>DYNAMIC REWIRING GRAPH</span>
              <span>7.2% UTILIZATION (THRASHING)</span>
            </div>
            <div style={{ width: "100%", height: 10, backgroundColor: "#150125", borderRadius: 5, marginTop: 4, overflow: "hidden" }}>
              <div style={{ width: "7.2%", height: "100%", backgroundColor: "#FF2A85", boxShadow: "0 0 8px #FF2A85" }} />
            </div>
          </div>

          <div style={{ fontSize: 8.5, color: "#E0AAFF", borderTop: "1px dashed #7B2CBF", paddingTop: 6 }}>
            DRAM latency thrashes irregular graph traversals, collapsing FLOP efficiency.
          </div>
        </div>
      </div>
    </div>
  );
};
