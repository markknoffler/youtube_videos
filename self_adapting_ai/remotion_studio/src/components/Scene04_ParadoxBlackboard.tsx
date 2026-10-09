import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

function project3D(x: number, y: number, z: number, camYaw: number, camPitch: number, zoom = 1) {
  const radY = (camYaw * Math.PI) / 180;
  const x1 = x * Math.cos(radY) + z * Math.sin(radY);
  const z1 = -x * Math.sin(radY) + z * Math.cos(radY);

  const radX = (camPitch * Math.PI) / 180;
  const y2 = y * Math.cos(radX) - z1 * Math.sin(radX);
  const z2 = y * Math.sin(radX) + z1 * Math.cos(radX);

  const fov = 750;
  const scale = (fov / (fov + z2)) * zoom;
  return { px: 640 + x1 * scale, py: 360 + y2 * scale, scale, z: z2 };
}

export const Scene04_ParadoxBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const camYaw = interpolate(frame, [0, 4500], [-8, 16]);
  const camPitch = interpolate(frame, [0, 4500], [14, 8]);
  const zoom = interpolate(frame, [0, 1600, 3000, 4500], [0.95, 1.15, 1.1, 0.95]);

  // Phase 1: 0 - 906 frames (The Paradox Confrontation)
  const isConfrontation = frame < 1053;

  // Phase 2: 1053 - 1728 frames (Static Wire vs Dynamic Bilinear Attention)
  const isWireVsAttention = frame >= 1053 && frame < 2149;
  const signalProgress = ((frame * 3) % 100) / 100;

  // Phase 3: 2149 - 3334 frames (Mechanistic Interpretability: Induction Heads)
  const isInductionHead = frame >= 2149 && frame < 3646;

  // Phase 4: 3646 - 4500 frames (Transition to 3 Theorems)
  const isThreeTheorems = frame >= 3646;

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
        {/* Ambient Radial Nebulae */}
        <circle cx="640" cy="360" r="450" fill="#FF2A85" opacity="0.04" />

        {/* 1. TOP TITLE */}
        <g transform="translate(640, 80)">
          <text x="0" y="0" fill="#FF2A85" fontSize="22" fontWeight="900" textAnchor="middle">
            THE MODULAR EMERGENCE PARADOX
          </text>
          <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
            STATIC WIRES (W_ij) VS DYNAMIC BILINEAR METRIC ATTENTION (Q · K^T)
          </text>
        </g>

        {/* 2. STATIC WIRE VS BILINEAR ATTENTION COMPARISON (1053 - 2149 frames) */}
        {isWireVsAttention && (
          <g>
            {/* Left: Static Physical Wire */}
            <g transform="translate(340, 340)">
              <rect x="-180" y="-120" width="360" height="240" fill="rgba(20, 2, 40, 0.85)" stroke="#7B2CBF" strokeWidth="1.5" rx="8" />
              <text x="0" y="-85" fill="#C77DFF" fontSize="13" fontWeight="900" textAnchor="middle">
                STATIC GRAPH WIRE
              </text>
              {/* Two Nodes connected by fixed edge */}
              <circle cx="-90" cy="0" r="16" fill="#240342" stroke="#7B2CBF" strokeWidth="2" />
              <circle cx="90" cy="0" r="16" fill="#240342" stroke="#7B2CBF" strokeWidth="2" />
              <text x="-90" y="4" fill="#FFFFFF" fontSize="10" textAnchor="middle">x_i</text>
              <text x="90" y="4" fill="#FFFFFF" fontSize="10" textAnchor="middle">x_j</text>

              {/* Wire */}
              <line x1="-74" y1="0" x2="74" y2="0" stroke="#7B2CBF" strokeWidth="3" />
              {/* Traveling signal */}
              <circle cx={-74 + 148 * signalProgress} cy="0" r="4" fill="#FF2A85" />

              <text x="0" y="30" fill="#FFFFFF" fontSize="11" textAnchor="middle">
                y = W_ij · x_i (Linear Scalar)
              </text>
              <text x="0" y="55" fill="#FF2A85" fontSize="9.5" textAnchor="middle">
                LIMITATION: INPUT-INDEPENDENT ROUTING
              </text>
            </g>

            {/* Right: Transformer Dynamic Attention Field */}
            <g transform="translate(940, 340)">
              <rect x="-180" y="-120" width="360" height="240" fill="rgba(20, 2, 40, 0.85)" stroke="#00F0FF" strokeWidth="1.5" rx="8" />
              <text x="0" y="-85" fill="#00F0FF" fontSize="13" fontWeight="900" textAnchor="middle">
                TRANSFORMER ATTENTION FIELD
              </text>

              {/* Dynamic vectors rotating based on input token */}
              {(() => {
                const angle = Math.sin(frame * 0.05) * 45;
                const rad = (angle * Math.PI) / 180;
                const qx = Math.cos(rad) * 60;
                const qy = Math.sin(rad) * 60;

                return (
                  <g>
                    <line x1="0" y1="0" x2={qx} y2={qy} stroke="#FF2A85" strokeWidth="3" />
                    <line x1="0" y1="0" x2="60" y2="0" stroke="#00F0FF" strokeWidth="3" />
                    <circle cx="0" cy="0" r="5" fill="#FFFFFF" />
                    <text x={qx + 10} y={qy} fill="#FF2A85" fontSize="10" fontWeight="800">Q(x_i)</text>
                    <text x="75" y="4" fill="#00F0FF" fontSize="10" fontWeight="800">K(x_j)</text>
                  </g>
                );
              })()}

              <text x="0" y="50" fill="#FFFFFF" fontSize="11" textAnchor="middle">
                A_ij = softmax( Q_i · K_j^T / √d_k )
              </text>
              <text x="0" y="75" fill="#5AF78E" fontSize="9.5" textAnchor="middle">
                INSTANTANEOUS INPUT-DEPENDENT METRIC
              </text>
            </g>
          </g>
        )}

        {/* 3. INDUCTION HEAD MECHANISM (2149 - 3334 frames) */}
        {isInductionHead && (
          <g transform="translate(640, 380)">
            <rect x="-380" y="-130" width="760" height="260" fill="rgba(15, 2, 30, 0.9)" stroke="#5AF78E" strokeWidth="2" rx="10" />
            <text x="0" y="-95" fill="#5AF78E" fontSize="16" fontWeight="900" textAnchor="middle">
              INDUCTION HEAD CIRCUIT (ANTHROPIC TRANSFORMER CIRCUITS)
            </text>
            <text x="0" y="-72" fill="#E0AAFF" fontSize="11" textAnchor="middle">
              PATTERN MATCHING: [A] [B] ... [A] ⟹ COPIES [B] FORWARD
            </text>

            {/* Token Sequence Tape */}
            {["[A]", "[B]", "...", "[A]", "→ [B]"].map((tok, i) => {
              const tx = (i - 2) * 110;
              const isTarget = i === 4;
              const isMatch = i === 0 || i === 3;

              return (
                <g key={`tok-${i}`} transform={`translate(${tx}, 0)`}>
                  <rect
                    x="-40"
                    y="-25"
                    width="80"
                    height="50"
                    fill={isTarget ? "#5AF78E" : isMatch ? "#FF2A85" : "#240342"}
                    stroke="#FFFFFF"
                    strokeWidth={1.5}
                    rx="6"
                  />
                  <text x="0" y="8" fill={isTarget ? "#000" : "#FFF"} fontSize="15" fontWeight="900" textAnchor="middle">
                    {tok}
                  </text>
                </g>
              );
            })}

            {/* Induction Search Arrow jumping back */}
            <path
              d="M 110,-35 Q 0,-85 -220,-35"
              fill="none"
              stroke="#00F0FF"
              strokeWidth="2.5"
              strokeDasharray="6 4"
            />
            <text x="-55" y="-75" fill="#00F0FF" fontSize="11" fontWeight="800">
              PREVIOUS TOKEN SEARCH (ATTENTION HEAD 1)
            </text>

            {/* Copy Forward Arrow */}
            <path
              d="M -110,35 Q 50,85 220,35"
              fill="none"
              stroke="#5AF78E"
              strokeWidth="2.5"
            />
            <text x="55" y="70" fill="#5AF78E" fontSize="11" fontWeight="800">
              COPY CONTINUATION FORWARD (ATTENTION HEAD 2)
            </text>

            <text x="0" y="110" fill="#FFFFFF" fontSize="11" textAnchor="middle">
              EMERGES IN FROZEN WEIGHTS VIA IN-CONTEXT IMPLICIT GRADIENT DESCENT
            </text>
          </g>
        )}

        {/* 4. THE ROAD TO THREE THEOREMS (3646 - 4500 frames) */}
        {isThreeTheorems && (
          <g transform="translate(640, 360)">
            <text x="0" y="-80" fill="#FFFFFF" fontSize="20" fontWeight="900" textAnchor="middle">
              THE THREE MATHEMATICAL DEAD ENDS OF REWIRING
            </text>

            {[
              { id: "1", title: "THEOREM 1: RANK COLLAPSE", text: "Homogeneous Hebbian dynamics plunge effective rank to 1", color: "#FF2A85", y: -20 },
              { id: "2", title: "THEOREM 2: ROUTING EXPRESSIVITY", text: "Moore bound forces logarithmic multi-hop latency in sparse graphs", color: "#C77DFF", y: 40 },
              { id: "3", title: "THEOREM 3: HARDWARE LOTTERY", text: "Systolic Tensor Core GEMM crushes sparse pointer-chasing memory bandwidth", color: "#5AF78E", y: 100 },
            ].map((th) => (
              <g key={th.id} transform={`translate(0, ${th.y})`}>
                <rect x="-360" y="-18" width="720" height="36" fill="rgba(20, 2, 40, 0.9)" stroke={th.color} strokeWidth="1.5" rx="6" />
                <text x="-340" y="5" fill={th.color} fontSize="12" fontWeight="900">
                  {th.title}:
                </text>
                <text x="-80" y="5" fill="#FFFFFF" fontSize="10.5">
                  {th.text}
                </text>
              </g>
            ))}
          </g>
        )}
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Chris Olah Mechanistic Circuits (Frames 80 to 1100) */}
      {frame >= 80 && frame < 1100 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/chris_olah.png")}
          title="CHRIS OLAH — MECHANISTIC CIRCUITS"
          authorBadge="ANTHROPIC RESEARCH"
          highlightText="Induction Heads Execute In-Context Learning"
          x={40}
          y={110}
          width={240}
          height={185}
          colorTheme="purple"
          enterFrame={80}
        />
      )}

      {/* 2. Anthropic Transformer Circuits Paper (Frames 1100 to 2300) */}
      {frame >= 1100 && frame < 2300 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_transformer_circuits.png")}
          title="IN-CONTEXT LEARNING & INDUCTION HEADS"
          authorBadge="OLSSON ET AL. (2022)"
          highlightText="Bilinear Attention Discovers Algorithmic Routing"
          x={950}
          y={110}
          width={290}
          height={190}
          colorTheme="cyan"
          enterFrame={1100}
        />
      )}

      {/* 3. Anthropic & OpenAI Frontier Labs (Frames 2300 to 3600) */}
      {frame >= 2300 && frame < 3600 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/logos/anthropic_logo.svg")}
          title="CIRCUIT SPECIALIZATION WITHOUT REWIRING"
          authorBadge="TOP AI LABS"
          highlightText="Weights Fixed, Activation Flow Dynamically Routes"
          x={40}
          y={120}
          width={260}
          height={175}
          colorTheme="yellow"
          enterFrame={2300}
        />
      )}
    </div>
  );
};
