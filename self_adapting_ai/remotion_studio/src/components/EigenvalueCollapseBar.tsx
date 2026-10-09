import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface EigenvalueCollapseBarProps {
  startFrame?: number;
  width?: number;
  height?: number;
}

export const EigenvalueCollapseBar: React.FC<EigenvalueCollapseBarProps> = ({
  startFrame = 0,
  width = 540,
  height = 420,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const entrance = spring({ frame: relFrame, fps, config: { damping: 14 } });

  // Collapse progress over 180 frames (6 seconds)
  const collapseProgress = interpolate(relFrame, [20, 200], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Effective rank plunging from 64 down to 1.0
  const effectiveRank = interpolate(collapseProgress, [0, 1], [64.0, 1.05]).toFixed(2);

  const numBars = 16;

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        backgroundColor: "rgba(14, 2, 28, 0.94)",
        border: "1.5px solid #FF2A85",
        borderRadius: 14,
        boxShadow: "0 0 35px rgba(255, 42, 133, 0.35)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
        transform: `scale(${entrance})`,
        padding: "16px 20px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <span
            style={{
              fontSize: 8.5,
              backgroundColor: "#FF2A85",
              color: "#FFFFFF",
              padding: "2px 6px",
              borderRadius: 3,
              fontWeight: 800,
            }}
          >
            THEOREM 1: SPECTRAL COLLAPSE
          </span>
          <div style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF", marginTop: 4 }}>
            EIGENVALUE DECAY SPECTRUM: λ_1 ... λ_16
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 8.5, color: "#E0AAFF" }}>EFFECTIVE RANK</div>
          <div
            style={{
              fontSize: 16,
              fontWeight: 900,
              color: collapseProgress > 0.5 ? "#FF2A85" : "#5AF78E",
            }}
          >
            {effectiveRank} / 64.0
          </div>
        </div>
      </div>

      {/* 3D Bar Chart Display */}
      <div
        style={{
          position: "relative",
          height: 220,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-between",
          gap: 6,
          padding: "0 10px",
          borderBottom: "2px solid #C77DFF",
        }}
      >
        {Array.from({ length: numBars }).map((_, i) => {
          let barHeight = 0;
          if (i === 0) {
            // Dominant eigenvector lambda_1 grows to dominate
            barHeight = interpolate(collapseProgress, [0, 1], [40, 95]);
          } else {
            // All other eigenvalues decay to near zero
            const initialHeight = Math.max(10, 80 - i * 4);
            barHeight = interpolate(collapseProgress, [0, 1], [initialHeight, 3]);
          }

          const isDominant = i === 0;

          return (
            <div
              key={i}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                height: "100%",
                justifyContent: "flex-end",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: `${barHeight}%`,
                  backgroundColor: isDominant ? "#FF2A85" : "#9D4EDD",
                  borderRadius: "4px 4px 0 0",
                  boxShadow: isDominant ? "0 0 14px #FF2A85" : "none",
                  transition: "height 0.1s ease",
                  position: "relative",
                }}
              >
                {isDominant && (
                  <span
                    style={{
                      position: "absolute",
                      top: -18,
                      left: "50%",
                      transform: "translateX(-50%)",
                      fontSize: 8,
                      color: "#FF2A85",
                      fontWeight: 800,
                      whiteSpace: "nowrap",
                    }}
                  >
                    v_1
                  </span>
                )}
              </div>
              <span style={{ fontSize: 7, color: "#8E7DBE", marginTop: 4 }}>
                λ_{i + 1}
              </span>
            </div>
          );
        })}
      </div>

      {/* Bottom Educational Callout */}
      <div
        style={{
          backgroundColor: "rgba(22, 2, 42, 0.95)",
          border: "1px solid rgba(255, 42, 133, 0.4)",
          borderRadius: 8,
          padding: "8px 12px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 9.5,
        }}
      >
        <span style={{ color: "#E0AAFF" }}>LYAPUNOV STABILITY ATTRACTOR:</span>
        <span style={{ color: "#FF2A85", fontWeight: 800 }}>
          {collapseProgress > 0.7 ? "CATASTROPHIC 1D RANK COLLAPSE" : "DEGENERACY UNFOLDING"}
        </span>
      </div>
    </div>
  );
};
