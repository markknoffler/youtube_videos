import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AnnotatedPaperScreenshot } from "./AnnotatedPaperScreenshot";
import { MoERouter } from "./MoERouter";
import { ScientistQuoteCard } from "./ScientistQuoteCard";

export const Scene09_ImplicitMetaOptimization: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  // Phase toggling between Von Oswald paper (first half) and MoE / DeepMind quotes (second half)
  const isSecondHalf = frame > 2200;

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
      {!isSecondHalf ? (
        <>
          {/* LEFT: Von Oswald Paper with Highlighting & Handwriting */}
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <AnnotatedPaperScreenshot
              imageSrc="assets/papers/von_oswald_paper.png"
              title="Transformers Learn In-Context by Gradient Descent"
              authors="Johannes von Oswald et al. (ETH Zurich & DeepMind)"
              venue="ICML 2023"
              arxivId="2212.07677"
              width={430}
              height={460}
              highlights={[
                {
                  topPercent: 30,
                  leftPercent: 8,
                  widthPercent: 84,
                  heightPercent: 6,
                  color: "#FF2A85",
                  noteText: "ATTENTION RUNS IMPLICIT GRADIENT DESCENT!",
                  notePosition: "bottom",
                },
                {
                  topPercent: 55,
                  leftPercent: 10,
                  widthPercent: 80,
                  heightPercent: 8,
                  color: "#C77DFF",
                  noteText: "★ FORWARD PASS = META-OPTIMIZER",
                  notePosition: "top",
                },
              ]}
            />
          </div>

          {/* RIGHT: Demis Hassabis Quote & Mechanistic Takeaway */}
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
              scientistName="Demis Hassabis"
              role="CEO & Co-founder"
              institution="Google DeepMind"
              quoteText="To build true artificial general intelligence, our architectures must integrate the fast meta-learning dynamics of biology with scalable mathematical foundations."
              highlightPhrase="fast meta-learning dynamics of biology"
              width={400}
            />

            {/* In-Context Optimization Card */}
            <div
              style={{
                backgroundColor: "rgba(18, 1, 32, 0.9)",
                border: "2px solid #5AF78E",
                borderRadius: 14,
                padding: 16,
                boxShadow: "0 0 24px rgba(90, 247, 142, 0.25)",
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >
              <div style={{ fontSize: 11, fontWeight: 900, color: "#5AF78E" }}>
                THE IMPLICIT META-OPTIMIZER BREAKTHROUGH
              </div>
              <div style={{ fontSize: 9.5, color: "#FFFFFF", lineHeight: 1.5 }}>
                Transformers do not need to mutate weights because their forward activation dynamics simulate an inner optimization algorithm in activation space.
              </div>
              <div style={{ fontSize: 8.5, color: "#E0AAFF", borderTop: "1px dashed #7B2CBF", paddingTop: 6 }}>
                Weights are the fixed compiler; activation streams are the executing adaptive program.
              </div>
            </div>
          </div>
        </>
      ) : (
        <>
          {/* Dynamic MoE Router (DeepSeek-V3) */}
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <MoERouter width={420} height={360} />
          </div>

          {/* Meta-Plasticity Research Spotlight */}
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
              <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>META-PLASTICITY FRONTIER</span>
              <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800 }}>KIRSCH & SCHMIDHUBER</span>
            </div>

            <div
              style={{
                backgroundColor: "rgba(10, 0, 18, 0.85)",
                borderRadius: 10,
                border: "1px dashed rgba(199, 125, 255, 0.3)",
                padding: 14,
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >
              <div style={{ fontSize: 10, color: "#C77DFF", fontWeight: 800 }}>LEARNING TO LEARN PLASTICITY</div>
              <div style={{ fontSize: 9, color: "#E0AAFF", lineHeight: 1.5 }}>
                Instead of rigid hand-crafted biological Hebbian formulas, secondary meta-networks discover self-stabilizing plasticity rules via meta-gradients.
              </div>
            </div>

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
              META-GRADIENTS BRIDGE BIO-PLASTICITY AND SCALABLE SILICON
            </div>
          </div>
        </>
      )}
    </div>
  );
};
