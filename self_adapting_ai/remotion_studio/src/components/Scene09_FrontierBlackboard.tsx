import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene09_FrontierBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dynamic MoE Routing Gate activation cycle
  const activeExpert = Math.floor(frame / 20) % 8;

  // In-context gradient descent step progress
  const gdStep = interpolate(frame, [800, 2200], [0, 4], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#060214",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Top Header */}
        <g transform="translate(640, 65)">
          <text x="0" y="0" fill="#00F0FF" fontSize="21" fontWeight="900" textAnchor="middle">
            THE FRONTIER: HOW MODERN ARCHITECTURES ACTUALLY ADAPT
          </text>
          <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
            IN-CONTEXT GRADIENT DESCENT, MULTI-HEAD LATENT ATTENTION & META-PLASTICITY
          </text>
        </g>

        {/* SECTION 1: IMPLICIT IN-CONTEXT GRADIENT DESCENT (Frames 0 to 2200) */}
        {frame < 2200 && (
          <g transform="translate(640, 220)">
            <text x="0" y="-80" fill="#5AF78E" fontSize="15" fontWeight="900" textAnchor="middle">
              VON OSWALD ET AL. (2022): ATTENTION AS AN IMPLICIT META-OPTIMIZER
            </text>
            <text x="0" y="-55" fill="#A0FFA0" fontSize="11" textAnchor="middle">
              The forward pass simulates gradient descent on an internal objective without mutating weights
            </text>

            {/* Token Stream with Implicit Gradient Vector */}
            <g transform="translate(-400, 20)">
              {Array.from({ length: 6 }).map((_, i) => {
                const tx = i * 140;
                const isStep = Math.floor(gdStep) >= i;
                return (
                  <g key={`token-step-${i}`} transform={`translate(${tx}, 0)`}>
                    <rect
                      x="-55"
                      y="-30"
                      width="110"
                      height="60"
                      fill={isStep ? "rgba(0, 240, 255, 0.2)" : "rgba(40, 10, 60, 0.5)"}
                      stroke={isStep ? "#00F0FF" : "#7B2CBF"}
                      strokeWidth={isStep ? 2.5 : 1}
                      rx="8"
                    />
                    <text x="0" y="-8" fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                      {`Token x_${i + 1}`}
                    </text>
                    <text x="0" y="16" fill={isStep ? "#5AF78E" : "#888"} fontSize="9.5" fontWeight="700" textAnchor="middle">
                      {isStep ? `ΔW_${i + 1} Step` : "Pending"}
                    </text>
                  </g>
                );
              })}
            </g>

            {/* Mathematical Derivation */}
            <g transform="translate(0, 160)">
              <rect x="-360" y="-28" width="720" height="56" fill="rgba(10, 5, 25, 0.9)" stroke="#00F0FF" strokeWidth="1.5" rx="8" />
              <text x="0" y="-4" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
                W_eff(t) = W_0 - η ∑_(τ=1)^t e_τ x_τ^T  ≡  Self-Attention Layer
              </text>
              <text x="0" y="18" fill="#5AF78E" fontSize="11" textAnchor="middle">
                Transformers do not need biological rewiring — their forward dynamics ARE learning algorithms!
              </text>
            </g>
          </g>
        )}

        {/* SECTION 2: DEEPSEEK-V3 MOE ROUTING & MLA KV COMPRESSION (Frames 2200 to 4500) */}
        {frame >= 2200 && (
          <g transform="translate(0, 110)">
            {/* LEFT: MULTI-HEAD LATENT ATTENTION (MLA) */}
            <g transform="translate(330, 180)">
              <text x="0" y="-140" fill="#00F0FF" fontSize="15" fontWeight="900" textAnchor="middle">
                MULTI-HEAD LATENT ATTENTION (MLA)
              </text>
              <text x="0" y="-120" fill="#A0E0FF" fontSize="11" textAnchor="middle">
                DeepSeek-V3: Low-Rank KV Compression (93.3% Cache Reduction)
              </text>

              {/* Compression Bottleneck Diagram */}
              <g transform="translate(0, -30)">
                {/* Full Hidden State (512-dim) */}
                <rect x="-140" y="-20" width="280" height="30" fill="rgba(0, 240, 255, 0.15)" stroke="#00F0FF" rx="4" />
                <text x="0" y="0" fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                  Hidden Representation h_t (d = 7168)
                </text>

                {/* Down-projection arrows */}
                <line x1="-70" y1="10" x2="-20" y2="40" stroke="#00F0FF" strokeWidth="2" />
                <line x1="70" y1="10" x2="20" y2="40" stroke="#00F0FF" strokeWidth="2" />

                {/* Compressed Latent KV (512-dim) */}
                <rect x="-60" y="40" width="120" height="32" fill="#00F0FF" stroke="#FFFFFF" rx="4" />
                <text x="0" y="60" fill="#000000" fontSize="11" fontWeight="900" textAnchor="middle">
                  c_KV (d_c = 512)
                </text>

                {/* Up-projection to 128 Heads */}
                <line x1="-20" y1="72" x2="-80" y2="100" stroke="#00F0FF" strokeWidth="2" />
                <line x1="20" y1="72" x2="80" y2="100" stroke="#00F0FF" strokeWidth="2" />

                <rect x="-160" y="100" width="320" height="28" fill="rgba(0, 240, 255, 0.2)" stroke="#00F0FF" rx="4" />
                <text x="0" y="118" fill="#5AF78E" fontSize="10.5" fontWeight="800" textAnchor="middle">
                  Decoupled RoPE Key & Value Reconstruction
                </text>
              </g>

              <rect x="-180" y="150" width="360" height="34" fill="rgba(0, 40, 60, 0.9)" stroke="#00F0FF" strokeWidth="1.5" rx="6" />
              <text x="0" y="172" fill="#00F0FF" fontSize="11" fontWeight="800" textAnchor="middle">
                LATENT FACTORIZATION BEATS PHYSICAL REWIRING
              </text>
            </g>

            {/* SEPARATOR AXIS */}
            <line x1="640" y1="40" x2="640" y2="460" stroke="#7B2CBF" strokeWidth="1.5" strokeDasharray="4 4" />

            {/* RIGHT: FINE-GRAINED MIXTURE OF EXPERTS (MoE) */}
            <g transform="translate(950, 180)">
              <text x="0" y="-140" fill="#FF2A85" fontSize="15" fontWeight="900" textAnchor="middle">
                FINE-GRAINED MoE (256 EXPERTS)
              </text>
              <text x="0" y="-120" fill="#FFB0C0" fontSize="11" textAnchor="middle">
                Top-8 Routed Experts + 1 Shared Expert (37B Active / 671B Total)
              </text>

              {/* 8 Active Experts Visualizer */}
              <g transform="translate(0, -30)">
                {Array.from({ length: 8 }).map((_, i) => {
                  const ex = -120 + (i % 4) * 80;
                  const ey = Math.floor(i / 4) * 60;
                  const isActive = i === activeExpert;

                  return (
                    <g key={`exp-${i}`} transform={`translate(${ex}, ${ey})`}>
                      <rect
                        x="-34"
                        y="-22"
                        width="68"
                        height="44"
                        fill={isActive ? "#FF2A85" : "rgba(255, 42, 133, 0.15)"}
                        stroke="#FF2A85"
                        strokeWidth={isActive ? 2.5 : 1}
                        rx="6"
                      />
                      <text x="0" y="-4" fill={isActive ? "#FFFFFF" : "#FFB0C0"} fontSize="9.5" fontWeight="900" textAnchor="middle">
                        {`Expert ${i + 1}`}
                      </text>
                      <text x="0" y="14" fill={isActive ? "#FFFFFF" : "#888"} fontSize="8.5" textAnchor="middle">
                        {isActive ? "ACTIVE" : "Idle"}
                      </text>
                    </g>
                  );
                })}
              </g>

              {/* Routing Equation */}
              <g transform="translate(0, 100)">
                <text x="0" y="0" fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                  y = ∑_(i ∈ Shared) E_i(x) + ∑_(k=1)^8 g_k(x) · E_k(x)
                </text>
              </g>

              <rect x="-180" y="150" width="360" height="34" fill="rgba(60, 10, 30, 0.9)" stroke="#FF2A85" strokeWidth="1.5" rx="6" />
              <text x="0" y="172" fill="#5AF78E" fontSize="11" fontWeight="800" textAnchor="middle">
                DYNAMIC MODULARITY WITHOUT HARDWARE STALLS
              </text>
            </g>
          </g>
        )}

        {/* BOTTOM MATHEMATICAL CONCLUSION */}
        <g transform="translate(640, 630)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
            THE MODERN SYNTHESIS: ATTENTION IS ROUTING, KV-COMPRESSION IS MEMORY, MoE IS MODULARITY
          </text>
          <text x="0" y="22" fill="#5AF78E" fontSize="11" textAnchor="middle">
            von Oswald (2022) In-Context Meta-Optimization ∩ DeepSeek (2024) Multi-Head Latent Attention
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. von Oswald In-Context Gradient Descent Paper (Frames 80 to 1400) */}
      {frame >= 80 && frame < 1400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_in_context-01.png")}
          title="IN-CONTEXT LEARNING BY GRADIENT DESCENT"
          authorBadge="VON OSWALD ET AL. (2022)"
          highlightText="Attention Forward Pass Computes Meta-Optimization Steps"
          x={40}
          y={110}
          width={290}
          height={185}
          colorTheme="cyan"
          enterFrame={80}
        />
      )}

      {/* 2. DeepSeek-V3 Technical Report (Frames 1400 to 2800) */}
      {frame >= 1400 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_deepseek_v3.png")}
          title="DEEPSEEK-V3 ARCHITECTURAL REPORT"
          authorBadge="MLA & 256 ROUTED EXPERTS"
          highlightText="93.3% KV Compression & Dynamic Gating on Systolic Arrays"
          x={950}
          y={110}
          width={290}
          height={185}
          colorTheme="magenta"
          enterFrame={1400}
        />
      )}

      {/* 3. Google DeepMind Meta-Plasticity (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/logos/google_deepmind_logo.png")}
          title="FRONTIER META-PLASTICITY RESEARCH"
          authorBadge="GOOGLE DEEPMIND"
          highlightText="Secondary Hypernetworks Discovering Plasticity Rules"
          x={40}
          y={120}
          width={280}
          height={175}
          colorTheme="green"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
