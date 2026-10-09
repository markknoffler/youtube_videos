import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { AnnotatedPaperScreenshot } from "./AnnotatedPaperScreenshot";

export const Scene03_WeightAgnostic3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const pulse = Math.sin(frame * 0.1) * 0.1 + 1;

  // NEAT topological node mutations
  const nodes = [
    { x: 50, y: 120, label: "IN_1" },
    { x: 50, y: 220, label: "IN_2" },
    { x: 160, y: 70, label: "HID_1" },
    { x: 170, y: 180, label: "MUT_NODE" },
    { x: 160, y: 270, label: "HID_2" },
    { x: 280, y: 120, label: "OUT_1" },
    { x: 280, y: 220, label: "OUT_2" },
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
      {/* LEFT: NEAT & Weight Agnostic Network Topology Growth */}
      <div
        style={{
          width: 370,
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
          <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>WANN & NEAT TOPOLOGY</span>
          <span style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 800, border: "1px solid #FF2A85", padding: "2px 6px", borderRadius: 4 }}>
            WEIGHT AGNOSTIC
          </span>
        </div>

        {/* Evolving Network Graph Canvas */}
        <div
          style={{
            height: 270,
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
          <svg width="340" height="260" viewBox="0 0 340 260">
            {/* Edge Connections with traveling weight value */}
            <line x1="50" y1="120" x2="160" y2="70" stroke="#7B2CBF" strokeWidth="2" />
            <line x1="50" y1="220" x2="160" y2="270" stroke="#7B2CBF" strokeWidth="2" />
            <line x1="160" y1="70" x2="280" y2="120" stroke="#7B2CBF" strokeWidth="2" />
            <line x1="160" y1="270" x2="280" y2="220" stroke="#7B2CBF" strokeWidth="2" />

            {/* Mutated Edge with animated dashed stroke */}
            <line
              x1="50"
              y1="120"
              x2="170"
              y2="180"
              stroke="#FF2A85"
              strokeWidth="2.5"
              strokeDasharray="6 3"
              strokeDashoffset={-frame * 2}
            />
            <line
              x1="170"
              y1="180"
              x2="280"
              y2="120"
              stroke="#FF2A85"
              strokeWidth="2.5"
              strokeDasharray="6 3"
              strokeDashoffset={-frame * 2}
            />

            {/* Nodes */}
            {nodes.map((node, i) => {
              const isMut = node.label === "MUT_NODE";
              return (
                <g key={i}>
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={isMut ? 14 * pulse : 12}
                    fill={isMut ? "#25023D" : "#1A012C"}
                    stroke={isMut ? "#FF2A85" : "#C77DFF"}
                    strokeWidth="2"
                    filter={isMut ? "drop-shadow(0 0 8px #FF2A85)" : "none"}
                  />
                  <text
                    x={node.x}
                    y={node.y + 3}
                    textAnchor="middle"
                    fill="#FFFFFF"
                    fontSize="7"
                    fontWeight="800"
                  >
                    {isMut ? "W_0" : `N${i}`}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Shared Single Weight Badge */}
          <div
            style={{
              position: "absolute",
              top: 8,
              left: 10,
              backgroundColor: "#200133",
              border: "1px solid #FF2A85",
              borderRadius: 6,
              padding: "4px 8px",
              fontSize: 8.5,
              color: "#FFFFFF",
              fontWeight: 800,
            }}
          >
            SHARED WEIGHT W = -1.50
          </div>
        </div>

        {/* Bipedal Walking & Car Racing Task Badge */}
        <div
          style={{
            backgroundColor: "#160128",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #7B2CBF",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 9,
            color: "#E0AAFF",
          }}
        >
          <span>TASKS: BIPEDAL WALKER • CAR RACING</span>
          <span style={{ color: "#5AF78E", fontWeight: 800 }}>ZERO WEIGHT TUNING</span>
        </div>
      </div>

      {/* RIGHT: Real Paper Spotlight with Handwritten Annotations */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <AnnotatedPaperScreenshot
          imageSrc="assets/papers/wann_paper.png"
          title="Weight Agnostic Neural Networks"
          authors="Adam Gaier, David Ha (Google Brain)"
          venue="NeurIPS 2019"
          arxivId="1906.04358"
          width={460}
          height={460}
          highlights={[
            {
              topPercent: 32,
              leftPercent: 8,
              widthPercent: 84,
              heightPercent: 6,
              color: "#FF2A85",
              noteText: "TOPOLOGY ALONE ENCODES FUNCTION!",
              notePosition: "bottom",
            },
            {
              topPercent: 55,
              leftPercent: 12,
              widthPercent: 76,
              heightPercent: 8,
              color: "#C77DFF",
              noteText: "★ SHARED SINGLE WEIGHT!",
              notePosition: "top",
            },
          ]}
        />
      </div>
    </div>
  );
};
