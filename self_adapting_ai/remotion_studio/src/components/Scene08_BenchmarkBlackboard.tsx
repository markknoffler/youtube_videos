import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene08_BenchmarkBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Training epoch progress (0 to 100 epochs from frame 1200 to 3800)
  const epoch = Math.floor(interpolate(frame, [1200, 3800], [1, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  }));

  // Dynamic accuracy interpolation
  const tfAcc = interpolate(frame, [1200, 2400], [6.25, 92.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const drnAcc = interpolate(frame, [1200, 2400], [6.25, 7.7], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const tfRank = interpolate(frame, [2800, 4000], [16.0, 14.56], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const drnRank = interpolate(frame, [2800, 4000], [16.0, 2.10], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Polyline points for Transformer accuracy curve
  const tfPoints = Array.from({ length: Math.min(60, Math.floor(epoch * 0.6)) }).map((_, i) => {
    const ex = i * (460 / 60);
    const prog = i / 60;
    const accVal = 6.25 + (92.3 - 6.25) * (1 - Math.exp(-prog * 7));
    const ey = -(accVal / 100) * 160;
    return `${ex},${ey}`;
  }).join(" ");

  // Polyline points for DRN accuracy curve
  const drnPoints = Array.from({ length: Math.min(60, Math.floor(epoch * 0.6)) }).map((_, i) => {
    const ex = i * (460 / 60);
    const accVal = 6.25 + Math.sin(i * 0.4) * 1.5;
    const ey = -(accVal / 100) * 160;
    return `${ex},${ey}`;
  }).join(" ");

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#060111",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Top Header */}
        <g transform="translate(640, 65)">
          <text x="0" y="0" fill="#00F0FF" fontSize="21" fontWeight="900" textAnchor="middle">
            EMPIRICAL BENCHMARK: IN-CONTEXT KEY-VALUE ASSOCIATIVE RECALL
          </text>
          <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
            CONTROLLED TEST (m = 16 PAIRS): TRANSFORMER 92.3% VS SELF-ORGANIZING DRN 7.7%
          </text>
        </g>

        {/* SECTION 1: TASK SEQUENCE PROTOCOL (Frames 0 to 1400) */}
        {frame < 1400 && (
          <g transform="translate(640, 200)">
            <text x="0" y="-50" fill="#E0AAFF" fontSize="13" fontWeight="800" textAnchor="middle">
              TASK: RETRIEVE VALUE BOUND TO QUERY KEY WITHOUT MODIFYING PERMANENT WEIGHTS
            </text>

            {/* Sequence Tokens [K1:V1] ... [K16:V16] ... [Query=K7] -> [?] */}
            <g transform="translate(-480, 0)">
              {Array.from({ length: 8 }).map((_, i) => {
                const tx = i * 110;
                const isTarget = i === 4;
                return (
                  <g key={`pair-${i}`} transform={`translate(${tx}, 0)`}>
                    <rect
                      x="-48"
                      y="-25"
                      width="96"
                      height="50"
                      fill={isTarget ? "rgba(0, 240, 255, 0.2)" : "rgba(30, 10, 50, 0.6)"}
                      stroke={isTarget ? "#00F0FF" : "#7B2CBF"}
                      strokeWidth={isTarget ? 2 : 1}
                      rx="6"
                    />
                    <text x="0" y="-4" fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                      {`[K_${i + 1} : V_${i + 1}]`}
                    </text>
                    <text x="0" y="16" fill={isTarget ? "#00F0FF" : "#A0A0A0"} fontSize="9" textAnchor="middle">
                      {isTarget ? "TARGET PAIR" : `Pair ${i + 1}`}
                    </text>
                  </g>
                );
              })}

              {/* Ellipsis */}
              <text x="890" y="5" fill="#C77DFF" fontSize="18" fontWeight="900" textAnchor="middle">
                ... [K_16 : V_16]
              </text>

              {/* Query Token */}
              <g transform="translate(1000, 0)">
                <rect x="-42" y="-25" width="84" height="50" fill="rgba(255, 42, 133, 0.2)" stroke="#FF2A85" strokeWidth="2" rx="6" />
                <text x="0" y="-4" fill="#FFFFFF" fontSize="11" fontWeight="900" textAnchor="middle">
                  [Q = K_5]
                </text>
                <text x="0" y="16" fill="#FF2A85" fontSize="9" fontWeight="800" textAnchor="middle">
                  QUERY
                </text>
              </g>
            </g>

            {/* In-context binding requirement */}
            <g transform="translate(0, 120)">
              <rect x="-340" y="-20" width="680" height="40" fill="rgba(10, 5, 25, 0.8)" stroke="#C77DFF" strokeWidth="1" rx="8" />
              <text x="0" y="5" fill="#5AF78E" fontSize="12" fontWeight="700" textAnchor="middle">
                REQUIREMENT: ZERO-SHOT DYNAMIC ATTRIBUTE ROUTING IN FORWARD PASS
              </text>
            </g>
          </g>
        )}

        {/* SECTION 2: LIVE EMPIRICAL DIVERGENCE (Frames 1400 to 4500) */}
        {frame >= 1400 && (
          <g transform="translate(0, 110)">
            {/* LEFT: EMPIRICAL LOSS / ACCURACY PLOT */}
            <g transform="translate(140, 240)">
              <text x="230" y="-170" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
                LEARNING DYNAMICS (EPOCH {epoch} / 100)
              </text>

              {/* Coordinate Axes */}
              <line x1="0" y1="0" x2="460" y2="0" stroke="#FFFFFF" strokeWidth="2" />
              <line x1="0" y1="0" x2="0" y2="-170" stroke="#FFFFFF" strokeWidth="2" />

              {/* Y Axis Grid Lines */}
              <line x1="0" y1="-80" x2="460" y2="-80" stroke="#331A4A" strokeWidth="1" strokeDasharray="3 3" />
              <text x="-15" y="-76" fill="#888" fontSize="10" textAnchor="end">50%</text>

              <line x1="0" y1="-160" x2="460" y2="-160" stroke="#331A4A" strokeWidth="1" strokeDasharray="3 3" />
              <text x="-15" y="-156" fill="#888" fontSize="10" textAnchor="end">100%</text>

              <text x="-15" y="4" fill="#888" fontSize="10" textAnchor="end">0%</text>
              <text x="460" y="20" fill="#888" fontSize="10" textAnchor="end">Epoch 100</text>

              {/* Chance Baseline (6.25%) */}
              <line x1="0" y1="-10" x2="460" y2="-10" stroke="#FF5555" strokeWidth="1.5" strokeDasharray="4 4" />
              <text x="465" y="-8" fill="#FF5555" fontSize="9">Chance 6.25%</text>

              {/* Transformer Curve */}
              {tfPoints && (
                <polyline
                  points={`0,${-(6.25 / 100) * 160} ${tfPoints}`}
                  fill="none"
                  stroke="#00F0FF"
                  strokeWidth="3.5"
                />
              )}

              {/* DRN Curve */}
              {drnPoints && (
                <polyline
                  points={`0,${-(6.25 / 100) * 160} ${drnPoints}`}
                  fill="none"
                  stroke="#FF2A85"
                  strokeWidth="2.5"
                />
              )}

              {/* Legend */}
              <g transform="translate(20, -130)">
                <line x1="0" y1="0" x2="30" y2="0" stroke="#00F0FF" strokeWidth="3" />
                <text x="40" y="4" fill="#00F0FF" fontSize="11" fontWeight="800">
                  Transformer: {tfAcc.toFixed(1)}% Acc
                </text>

                <line x1="0" y1="24" x2="30" y2="24" stroke="#FF2A85" strokeWidth="2.5" />
                <text x="40" y="28" fill="#FF2A85" fontSize="11" fontWeight="800">
                  Rewiring DRN: {drnAcc.toFixed(1)}% Acc
                </text>
              </g>
            </g>

            {/* SEPARATOR AXIS */}
            <line x1="660" y1="40" x2="660" y2="460" stroke="#7B2CBF" strokeWidth="1.5" strokeDasharray="4 4" />

            {/* RIGHT: THEOREM 1 VERIFICATION (SVD EFFECTIVE RANK SPECTRUM) */}
            <g transform="translate(960, 240)">
              <text x="0" y="-170" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
                SVD EFFECTIVE RANK (THEORETICAL VERIFICATION)
              </text>

              {/* Transformer Rank Bar */}
              <g transform="translate(-140, -100)">
                <text x="0" y="0" fill="#00F0FF" fontSize="12" fontWeight="800">TRANSFORMER (L=4)</text>
                <rect x="0" y="10" width="280" height="26" fill="rgba(0, 240, 255, 0.15)" stroke="#00F0FF" rx="4" />
                <rect x="0" y="10" width={(tfRank / 16) * 280} height="26" fill="#00F0FF" rx="4" />
                <text x="290" y="28" fill="#00F0FF" fontSize="12" fontWeight="900">
                  {tfRank.toFixed(2)} / 16.0
                </text>
                <text x="0" y="52" fill="#A0E0FF" fontSize="10">
                  Full multi-dimensional representation maintained
                </text>
              </g>

              {/* Self-Organizing DRN Rank Bar */}
              <g transform="translate(-140, 0)">
                <text x="0" y="0" fill="#FF2A85" fontSize="12" fontWeight="800">SELF-ORGANIZING DRN</text>
                <rect x="0" y="10" width="280" height="26" fill="rgba(255, 42, 133, 0.15)" stroke="#FF2A85" rx="4" />
                <rect x="0" y="10" width={(drnRank / 16) * 280} height="26" fill="#FF2A85" rx="4" />
                <text x="290" y="28" fill="#FF2A85" fontSize="12" fontWeight="900">
                  {drnRank.toFixed(2)} / 16.0
                </text>
                <text x="0" y="52" fill="#FF77AA" fontSize="10">
                  Severe Rank Collapse: Blinded by associative crosstalk
                </text>
              </g>

              {/* Cross-talk metric badge */}
              <g transform="translate(0, 110)">
                <rect x="-180" y="-18" width="360" height="36" fill="rgba(40, 5, 20, 0.9)" stroke="#FF2A85" strokeWidth="1.5" rx="6" />
                <text x="0" y="5" fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                  CROSSTALK INTERFERENCE: <tspan fill="#FF2A85">0.89</tspan> (TF: 0.04)
                </text>
              </g>
            </g>
          </g>
        )}

        {/* BOTTOM MATHEMATICAL CONCLUSION */}
        <g transform="translate(640, 630)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
            EMPIRICAL VERIFICATION: DYNAMIC TOPOLOGY COLLAPSES UNDER ASSOCIATIVE IN-CONTEXT RETRIEVAL
          </text>
          <text x="0" y="22" fill="#5AF78E" fontSize="11" textAnchor="middle">
            Factorized Attention Subspaces Achieve 92.3% Accuracy While Local Hebbian Networks Fail at Random Chance (7.7%)
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Controlled Diagnostic Benchmark Protocol (Frames 80 to 1400) */}
      {frame >= 80 && frame < 1400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_predictive_coding-01.png")}
          title="CONTROLLED BENCHMARK PROTOCOL"
          authorBadge="16 KEY-VALUE PAIRS"
          highlightText="Zero-Shot Dynamic Associative Binding Test"
          x={40}
          y={110}
          width={280}
          height={185}
          colorTheme="cyan"
          enterFrame={80}
        />
      )}

      {/* 2. PyTorch Training Loop Framework (Frames 1400 to 2800) */}
      {frame >= 1400 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/logos/pytorch_logo.svg")}
          title="PYTORCH 100-EPOCH CONVERGENCE LOOP"
          authorBadge="EMPIRICAL TELEMETRY"
          highlightText="Transformer: 92.3% Acc | DRN: 7.7% Flatline"
          x={960}
          y={110}
          width={240}
          height={175}
          colorTheme="yellow"
          enterFrame={1400}
        />
      )}

      {/* 3. Representation Collapse Verification (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_wann-01.png")}
          title="TOPOLOGY REWIRING COLLAPSE VERIFIED"
          authorBadge="THEOREM 1 EMPIRICAL PROOF"
          highlightText="Effective Rank 2.10 / 64: Associative Crosstalk Failure"
          x={40}
          y={120}
          width={280}
          height={185}
          colorTheme="magenta"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
