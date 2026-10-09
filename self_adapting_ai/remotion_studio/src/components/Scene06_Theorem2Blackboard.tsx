import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene06_Theorem2Blackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Multi-hop signal progression across sparse hops (0 to 6 hops)
  const hopCycle = ((frame * 2) % 180) / 30; // 0 to 6 hops
  const currentHop = Math.floor(hopCycle);

  // Moore bound N growth
  const N = Math.floor(interpolate(frame, [0, 4500], [1000, 100000]));
  const diameter = Math.ceil(Math.log(N) / Math.log(4));

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#06010F",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Top Header */}
        <g transform="translate(640, 75)">
          <text x="0" y="0" fill="#C77DFF" fontSize="22" fontWeight="900" textAnchor="middle">
            THEOREM 2: ROUTING EXPRESSIVITY & THE MOORE BOUND
          </text>
          <text x="0" y="24" fill="#E0AAFF" fontSize="12" textAnchor="middle">
            DIAMETER Ω(log N / log Δ): MULTI-HOP LATENCY VS O(1) TRANSFORMER ATTENTION
          </text>
        </g>

        {/* TOP: SPARSE GRAPH (Multi-hop logarithmic delay & signal decay) */}
        <g transform="translate(640, 240)">
          <text x="-480" y="-30" fill="#FF2A85" fontSize="13" fontWeight="900">
            SPARSE BIOLOGICAL GRAPH: DEGREE BOUND Δ = 4
          </text>

          {/* 6 Hops connecting Token 1 to Token N */}
          {Array.from({ length: 7 }).map((_, i) => {
            const hx = -420 + i * 140;
            const isReached = currentHop >= i;
            const isCurrent = currentHop === i;
            const signalStrength = Math.max(0.1, 1.0 - i * 0.15); // hop-by-hop attenuation!

            return (
              <g key={`hop-${i}`}>
                {i < 6 && (
                  <line
                    x1={hx + 18}
                    y1="0"
                    x2={hx + 122}
                    y2="0"
                    stroke={isReached ? "#FF2A85" : "#3A1054"}
                    strokeWidth={isReached ? 3 * signalStrength : 1.5}
                  />
                )}
                <circle
                  cx={hx}
                  cy="0"
                  r={isCurrent ? 18 : 14}
                  fill={isCurrent ? "#FF2A85" : "#1A0230"}
                  stroke={isReached ? "#FF2A85" : "#7B2CBF"}
                  strokeWidth={2}
                />
                <text x={hx} y="4" fill="#FFFFFF" fontSize="9.5" fontWeight="800" textAnchor="middle">
                  {i === 0 ? "x_1" : i === 6 ? `x_${N}` : `Hop ${i}`}
                </text>
                <text x={hx} y="32" fill="#E0AAFF" fontSize="8.5" textAnchor="middle">
                  {(signalStrength * 100).toFixed(0)}% energy
                </text>
              </g>
            );
          })}
        </g>

        {/* BOTTOM: TRANSFORMER O(1) DIRECT METRIC ROUTE */}
        <g transform="translate(640, 440)">
          <text x="-480" y="-30" fill="#00F0FF" fontSize="13" fontWeight="900">
            TRANSFORMER ATTENTION: O(1) CONSTANT PATH LENGTH
          </text>

          {/* Token 1 directly connects to Token N instantaneously */}
          <circle cx="-420" cy="0" r="16" fill="#00F0FF" stroke="#FFFFFF" strokeWidth={2} />
          <text x="-420" y="4" fill="#000000" fontSize="10" fontWeight="900" textAnchor="middle">x_1</text>

          <circle cx="420" cy="0" r="16" fill="#00F0FF" stroke="#FFFFFF" strokeWidth={2} />
          <text x="420" y="4" fill="#000000" fontSize="10" fontWeight="900" textAnchor="middle">x_{N}</text>

          {/* Direct Instantaneous Attention Arc */}
          <path
            d="M -404,0 Q 0,-80 404,0"
            fill="none"
            stroke="#00F0FF"
            strokeWidth="3.5"
            filter="drop-shadow(0 0 10px #00F0FF)"
          />
          <text x="0" y="-55" fill="#00F0FF" fontSize="13" fontWeight="900" textAnchor="middle">
            DIRECT ALL-TO-ALL ATTENTION: 100% SIGNAL FIDELITY (DEPTH = 1)
          </text>
        </g>

        {/* MATHEMATICAL PROOF STATEMENT */}
        <g transform="translate(640, 600)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="15" fontWeight="900" textAnchor="middle">
            Moore Bound: Diameter D ≥ ⌊ log_(Δ-1)(N) ⌋ ⟹ Multi-hop Delay Penalty
          </text>
          <text x="0" y="24" fill="#5AF78E" fontSize="11" textAnchor="middle">
            TO ELIMINATE DELAY, PHYSICAL GRAPHS REQUIRE O(N^2) EDGES — AN UNSCALABLE GEOMETRIC TRAP
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Attention O(1) Constant Depth (Frames 80 to 1400) */}
      {frame >= 80 && frame < 1400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_attention-01.png")}
          title="O(1) CONSTANT DEPTH: DIRECT ATTENTION"
          authorBadge="VASWANI ET AL."
          highlightText="Every Token Direct to Every Other Token"
          x={950}
          y={110}
          width={290}
          height={185}
          colorTheme="cyan"
          enterFrame={80}
        />
      )}

      {/* 2. Top500 Cluster Multi-Hop Latency (Frames 1400 to 2800) */}
      {frame >= 1400 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/datacenters/datacenter_supercomputer.jpg")}
          title="ROUTING SCALING ACROSS 100,000 NODES"
          authorBadge="EXTREMAL GRAPH THEORY"
          highlightText="Moore Bound: Diameter D ≥ ⌊log_(Δ-1)(N)⌋"
          x={40}
          y={110}
          width={280}
          height={185}
          colorTheme="purple"
          enterFrame={1400}
        />
      )}

      {/* 3. Hardware Scaling Contrast (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/logos/nvidia_logo.svg")}
          title="CONSTANT BIPARTITE ROUTING"
          authorBadge="TOPOLOGICAL ADVANTAGE"
          highlightText="Decouples Parameter Complexity From Sequence Length"
          x={960}
          y={120}
          width={270}
          height={175}
          colorTheme="green"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
