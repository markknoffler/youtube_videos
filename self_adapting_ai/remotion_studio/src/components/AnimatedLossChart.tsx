import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface AnimatedLossChartProps {
  width?: number;
  height?: number;
  startFrame?: number;
  durationFrames?: number;
}

export const AnimatedLossChart: React.FC<AnimatedLossChartProps> = ({
  width = 560,
  height = 320,
  startFrame = 0,
  durationFrames = 800,
}) => {
  const frame = useCurrentFrame();
  const relFrame = Math.max(0, frame - startFrame);

  // Smooth progress over durationFrames
  const progress = interpolate(relFrame, [0, durationFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Current values
  const currentEpoch = Math.floor(progress * 100);
  const tfAcc = interpolate(progress, [0, 0.3, 0.7, 1], [10, 58, 86, 92.3]);
  const soAcc = interpolate(progress, [0, 0.2, 0.5, 1], [10, 14, 8.2, 7.7]);
  const tfLoss = interpolate(progress, [0, 0.4, 1], [4.12, 1.05, 0.24]);
  const soLoss = interpolate(progress, [0, 0.3, 1], [4.15, 3.82, 3.79]);
  const tfRank = interpolate(progress, [0, 1], [15.2, 14.56]);
  const soRank = interpolate(progress, [0, 0.3, 0.7, 1], [15.0, 8.2, 3.4, 2.1]);

  // Points for SVG sparkline (up to current epoch)
  const sparkPointsCount = Math.max(2, Math.floor(progress * 30));
  const tfPoints: string[] = [];
  const soPoints: string[] = [];

  for (let i = 0; i < sparkPointsCount; i++) {
    const t = i / 30;
    const x = 30 + t * 240;
    // Loss curve mapping: high loss = top, low loss = bottom
    const yTf = 80 - (4.12 - (4.12 - 0.24) * Math.pow(t, 0.6)) * 16;
    const ySo = 80 - (4.15 - (4.15 - 3.79) * t) * 16;
    tfPoints.push(`${x.toFixed(1)},${Math.max(10, Math.min(85, yTf)).toFixed(1)}`);
    soPoints.push(`${x.toFixed(1)},${Math.max(10, Math.min(85, ySo)).toFixed(1)}`);
  }

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "#120224",
        borderRadius: 14,
        border: "1.5px solid #9D4EDD",
        boxShadow: "0 0 28px rgba(157, 78, 221, 0.25)",
        padding: "14px 18px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#FF2A85", letterSpacing: 0.5 }}>
          DIAGNOSTIC BENCHMARK: IN-CONTEXT RECALL
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 6, height: 6, borderRadius: "50%", backgroundColor: "#5AF78E", boxShadow: "0 0 6px #5AF78E" }} />
          <span style={{ fontSize: 10, color: "#E0AAFF" }}>
            Epoch {currentEpoch} / 100
          </span>
        </div>
      </div>

      {/* SVG Real-Time Loss Trajectory Curves */}
      <div style={{ position: "relative", height: 85, backgroundColor: "#0D011A", borderRadius: 8, border: "1px solid #3C096C", padding: "4px 8px" }}>
        <div style={{ position: "absolute", top: 4, left: 8, fontSize: 9, color: "#8E7DBE" }}>
          Cross-Entropy Loss (Log-Scale)
        </div>
        <div style={{ position: "absolute", top: 4, right: 8, fontSize: 9, display: "flex", gap: 10 }}>
          <span style={{ color: "#C77DFF" }}>■ Transformer: {tfLoss.toFixed(2)}</span>
          <span style={{ color: "#FF2A85" }}>■ SO-DRN: {soLoss.toFixed(2)}</span>
        </div>
        <svg width="100%" height="80" style={{ overflow: "visible" }}>
          {/* Grid lines */}
          <line x1="30" y1="20" x2="520" y2="20" stroke="#250442" strokeDasharray="3 3" />
          <line x1="30" y1="45" x2="520" y2="45" stroke="#250442" strokeDasharray="3 3" />
          <line x1="30" y1="70" x2="520" y2="70" stroke="#250442" strokeDasharray="3 3" />

          {/* Transformer Loss Curve */}
          {tfPoints.length > 1 && (
            <polyline
              fill="none"
              stroke="#C77DFF"
              strokeWidth="2.5"
              points={tfPoints.join(" ")}
              strokeLinecap="round"
            />
          )}
          {/* SO-DRN Loss Curve */}
          {soPoints.length > 1 && (
            <polyline
              fill="none"
              stroke="#FF2A85"
              strokeWidth="2.5"
              points={soPoints.join(" ")}
              strokeLinecap="round"
            />
          )}
        </svg>
      </div>

      {/* Bar Chart Comparisons */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10, margin: "6px 0" }}>
        {/* Metric 1: Recall Accuracy */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10.5, marginBottom: 4 }}>
            <span style={{ color: "#FFFFFF" }}>Associative Recall Accuracy (%)</span>
            <span style={{ color: "#E0AAFF" }}>
              TF: <b style={{ color: "#C77DFF" }}>{tfAcc.toFixed(1)}%</b> vs SO-DRN: <b style={{ color: "#FF2A85" }}>{soAcc.toFixed(1)}%</b>
            </span>
          </div>
          {/* Progress Bars */}
          <div style={{ display: "flex", gap: 8 }}>
            <div style={{ flex: 1, height: 10, backgroundColor: "#20033B", borderRadius: 5, overflow: "hidden" }}>
              <div
                style={{
                  width: `${tfAcc}%`,
                  height: "100%",
                  backgroundColor: "#C77DFF",
                  boxShadow: "0 0 10px #C77DFF",
                  borderRadius: 5,
                }}
              />
            </div>
            <div style={{ flex: 1, height: 10, backgroundColor: "#20033B", borderRadius: 5, overflow: "hidden" }}>
              <div
                style={{
                  width: `${soAcc}%`,
                  height: "100%",
                  backgroundColor: "#FF2A85",
                  boxShadow: "0 0 10px #FF2A85",
                  borderRadius: 5,
                }}
              />
            </div>
          </div>
        </div>

        {/* Metric 2: Effective Rank */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10.5, marginBottom: 4 }}>
            <span style={{ color: "#FFFFFF" }}>Subspace Rank (64-dim)</span>
            <span style={{ color: "#E0AAFF" }}>
              TF: <b style={{ color: "#C77DFF" }}>{tfRank.toFixed(1)}</b> vs SO-DRN: <b style={{ color: "#FF2A85" }}>{soRank.toFixed(1)} [COLLAPSE]</b>
            </span>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <div style={{ flex: 1, height: 10, backgroundColor: "#20033B", borderRadius: 5, overflow: "hidden" }}>
              <div
                style={{
                  width: `${(tfRank / 16) * 100}%`,
                  height: "100%",
                  backgroundColor: "#9D4EDD",
                  borderRadius: 5,
                }}
              />
            </div>
            <div style={{ flex: 1, height: 10, backgroundColor: "#20033B", borderRadius: 5, overflow: "hidden" }}>
              <div
                style={{
                  width: `${(soRank / 16) * 100}%`,
                  height: "100%",
                  backgroundColor: "#FF2A85",
                  borderRadius: 5,
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Benchmark Conclusion */}
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
        <span>Dataset: Synthetic In-Context KV Pairs (T=128)</span>
        <span style={{ color: "#FF2A85", fontWeight: 700 }}>P &lt; 0.0001 (10 Trials)</span>
      </div>
    </div>
  );
};
