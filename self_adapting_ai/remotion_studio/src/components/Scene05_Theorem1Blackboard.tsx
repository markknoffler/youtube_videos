import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene05_Theorem1Blackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Progress of rank collapse over time (frame 800 to 3600)
  const collapseProgress = interpolate(frame, [800, 3200], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Effective rank drops from 16.0 to 1.05
  const effectiveRank = (16 - collapseProgress * 14.95).toFixed(2);

  // 16 Singular Value / Eigenvalue Bars
  const bars = Array.from({ length: 16 }).map((_, i) => {
    if (i === 0) {
      // Dominant eigenvalue λ_1 grows to dominate
      return { val: 1.0 + collapseProgress * 0.5, color: "#FF2A85" };
    }
    // Subordinate eigenvalues λ_2 ... λ_16 exponentially decay to zero!
    const decay = Math.exp(-collapseProgress * (3 + i * 0.4));
    return { val: Math.max(0.02, (1 - i / 16) * decay), color: "#00F0FF" };
  });

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#070112",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Ambient Center Glow */}
        <circle cx="640" cy="360" r="460" fill="#FF2A85" opacity="0.04" />

        {/* Top Header */}
        <g transform="translate(640, 75)">
          <text x="0" y="0" fill="#FF2A85" fontSize="22" fontWeight="900" textAnchor="middle">
            THEOREM 1: RANK COLLAPSE IN LOCAL PLASTICITY
          </text>
          <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
            LYAPUNOV STABILITY: SUBSPACES EXPONENTIALLY CONTRACT TO DOMINANT EIGENVECTOR
          </text>
        </g>

        {/* LIVE SVD SPECTRAL BAR DECOMPOSITION */}
        <g transform="translate(640, 420)">
          {/* Baseline Axis */}
          <line x1="-360" y1="0" x2="360" y2="0" stroke="#FFFFFF" strokeWidth="2" />

          {/* 16 Spectral Bars */}
          {bars.map((b, i) => {
            const bx = -320 + i * 42;
            const barH = b.val * 220;

            return (
              <g key={`bar-${i}`}>
                {/* Bar */}
                <rect
                  x={bx - 14}
                  y={-barH}
                  width="28"
                  height={barH}
                  fill={b.color}
                  opacity={i === 0 ? 0.95 : 0.75}
                  rx="3"
                />
                <text x={bx} y="20" fill="#FFFFFF" fontSize="10" textAnchor="middle">
                  λ_{i + 1}
                </text>
                <text x={bx} y={-barH - 8} fill={b.color} fontSize="9.5" fontWeight="800" textAnchor="middle">
                  {b.val.toFixed(2)}
                </text>
              </g>
            );
          })}

          {/* Effective Rank Telemetry */}
          <g transform="translate(0, 90)">
            <rect x="-180" y="-18" width="360" height="36" fill="rgba(20, 2, 40, 0.9)" stroke="#FF2A85" strokeWidth="1.5" rx="6" />
            <text x="0" y="5" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
              EFFECTIVE RANK: <tspan fill="#FF2A85">{effectiveRank}</tspan> / 16.00
            </text>
          </g>
        </g>

        {/* Mathematical Proof Statement in Laser Chalk */}
        <g transform="translate(640, 590)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="15" fontWeight="900" textAnchor="middle">
            dw/dt = α H^T H w - β (w^T H^T H w) w
          </text>
          <text x="0" y="22" fill="#5AF78E" fontSize="11" textAnchor="middle">
            THE OJA TRAP: RATIO λ_1 / λ_k → ∞ ⟹ REPRESENTATION CRUSHED TO 1D LINE
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Erkki Oja (1982) Subspace Theorem (Frames 80 to 1400) */}
      {frame >= 80 && frame < 1400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_predictive_coding-01.png")}
          title="ERKKI OJA (1982) — SUBSPACE CONVERGENCE"
          authorBadge="JOURNAL OF MATH BIOLOGY"
          highlightText="Lyapunov Analysis: Weight Vector Locks to Dominant Eigenvector"
          x={40}
          y={110}
          width={280}
          height={185}
          colorTheme="magenta"
          enterFrame={80}
        />
      )}

      {/* 2. Donald Hebb Local Invariance (Frames 1400 to 2800) */}
      {frame >= 1400 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/donald_hebb.jpg")}
          title="LOCAL PLASTICITY LACKS ORTHOGONALIZATION"
          authorBadge="THE OJA TRAP"
          highlightText="λ_1 Subspace Crushes Multi-Relational Capacity to Rank 1"
          x={960}
          y={110}
          width={240}
          height={185}
          colorTheme="purple"
          enterFrame={1400}
        />
      )}

      {/* 3. Full-Rank Contrast: Transformer Attention (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_attention-01.png")}
          title="FULL-RANK BILINEAR ATTENTION CONTRAST"
          authorBadge="VASWANI ET AL."
          highlightText="Dynamic Runtime Metric Evades Eigenvalue Collapse"
          x={40}
          y={120}
          width={280}
          height={185}
          colorTheme="cyan"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
