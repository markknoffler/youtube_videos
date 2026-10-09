import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene07_Theorem3Blackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Pulse clock for systolic matrix multiplication
  const clock = Math.floor(frame / 6) % 12;

  // Credit assignment horizon growth
  const horizonT = Math.floor(interpolate(frame, [2200, 4200], [4, 2048], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  }));

  // Local variance explosion factor
  const varianceFactor = interpolate(frame, [2200, 4200], [1, 28], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#05020D",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Ambient Grid Background */}
        <defs>
          <radialGradient id="systolicGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.12" />
            <stop offset="100%" stopColor="#05020D" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="stallGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF0055" stopOpacity="0.12" />
            <stop offset="100%" stopColor="#05020D" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Top Header */}
        <g transform="translate(640, 65)">
          <text x="0" y="0" fill="#FF2A85" fontSize="21" fontWeight="900" textAnchor="middle">
            THEOREM 3: THE HARDWARE LOTTERY & CREDIT ASSIGNMENT BARRIER
          </text>
          <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
            SYSTOLIC GEMM INTENSITY O(d) VS IRREGULAR POINTER CHASSIS O(1) & VARIANCE EXPLOSION
          </text>
        </g>

        {/* SECTION 1: THE HARDWARE DICHOTOMY (Frames 0 to 2200) */}
        {frame < 2200 && (
          <g transform="translate(0, 110)">
            {/* LEFT: DENSE SYSTOLIC ARRAY (TRANSFORMERS / GPUS) */}
            <g transform="translate(330, 180)">
              <circle cx="0" cy="0" r="260" fill="url(#systolicGlow)" />
              <text x="0" y="-140" fill="#00F0FF" fontSize="15" fontWeight="900" textAnchor="middle">
                DENSE SYSTOLIC TENSOR ARRAY (GEMM)
              </text>
              <text x="0" y="-120" fill="#A0E0FF" fontSize="11" textAnchor="middle">
                Arithmetic Intensity I ≈ O(d) = 150 FLOPs/Byte | 989.4 TFLOPS
              </text>

              {/* 5x5 MAC Grid */}
              {Array.from({ length: 5 }).map((_, r) =>
                Array.from({ length: 5 }).map((_, c) => {
                  const macX = -100 + c * 50;
                  const macY = -80 + r * 50;
                  const isFired = (r + c) === (clock % 9);
                  return (
                    <g key={`mac-${r}-${c}`}>
                      <rect
                        x={macX - 18}
                        y={macY - 18}
                        width="36"
                        height="36"
                        fill={isFired ? "#00F0FF" : "rgba(0, 240, 255, 0.08)"}
                        stroke="#00F0FF"
                        strokeWidth={isFired ? 2.5 : 1}
                        rx="4"
                      />
                      <text
                        x={macX}
                        y={macY + 4}
                        fill={isFired ? "#000000" : "#A0E0FF"}
                        fontSize="9"
                        fontWeight="900"
                        textAnchor="middle"
                      >
                        MAC
                      </text>
                    </g>
                  );
                })
              )}

              <rect x="-180" y="160" width="360" height="34" fill="rgba(0, 40, 60, 0.9)" stroke="#00F0FF" strokeWidth="1.5" rx="6" />
              <text x="0" y="182" fill="#5AF78E" fontSize="11" fontWeight="800" textAnchor="middle">
                PEAK GPU COMPUTE SATURATION: 99.2% ALU UTILIZATION
              </text>
            </g>

            {/* SEPARATOR AXIS */}
            <line x1="640" y1="40" x2="640" y2="460" stroke="#7B2CBF" strokeWidth="1.5" strokeDasharray="4 4" />

            {/* RIGHT: SPARSE POINTER-CHASING GRAPH (SELF-ORGANIZATION) */}
            <g transform="translate(950, 180)">
              <circle cx="0" cy="0" r="260" fill="url(#stallGlow)" />
              <text x="0" y="-140" fill="#FF0055" fontSize="15" fontWeight="900" textAnchor="middle">
                SPARSE GRAPH POINTER CHASING (BIO)
              </text>
              <text x="0" y="-120" fill="#FFB0C0" fontSize="11" textAnchor="middle">
                Arithmetic Intensity I ≈ O(1) = 0.1 FLOPs/Byte | 18.2 TFLOPS
              </text>

              {/* Irregular Pointer Nodes & Cache Miss Thrashing */}
              {Array.from({ length: 8 }).map((_, i) => {
                const angle = (i / 8) * Math.PI * 2 + frame * 0.01;
                const rad = 75 + ((i * 37) % 45);
                const nx = Math.cos(angle) * rad;
                const ny = Math.sin(angle) * rad;
                const isStalled = (i + Math.floor(frame / 10)) % 3 === 0;

                return (
                  <g key={`sparse-node-${i}`}>
                    {/* Random Pointer Wire */}
                    <line
                      x1={nx}
                      y1={ny}
                      x2={Math.cos(angle + 1.2) * (rad - 20)}
                      y2={Math.sin(angle + 1.2) * (rad - 20)}
                      stroke={isStalled ? "#FF0055" : "#550020"}
                      strokeWidth={isStalled ? 2 : 1}
                      strokeDasharray="3 3"
                    />
                    <circle
                      cx={nx}
                      cy={ny}
                      r="16"
                      fill={isStalled ? "#FF0055" : "rgba(255, 0, 85, 0.15)"}
                      stroke="#FF0055"
                      strokeWidth="1.5"
                    />
                    <text x={nx} y={ny + 4} fill="#FFFFFF" fontSize="9" fontWeight="900" textAnchor="middle">
                      {isStalled ? "MISS" : `v_${i}`}
                    </text>
                  </g>
                );
              })}

              <rect x="-180" y="160" width="360" height="34" fill="rgba(60, 0, 20, 0.9)" stroke="#FF0055" strokeWidth="1.5" rx="6" />
              <text x="0" y="182" fill="#FF5555" fontSize="11" fontWeight="800" textAnchor="middle">
                MEMORY BUS BOTTLENECK: 95.4% IDLE PIPELINE STALL
              </text>
            </g>
          </g>
        )}

        {/* SECTION 2: TEMPORAL CREDIT ASSIGNMENT & VARIANCE EXPLOSION (Frames 2200 to 4500) */}
        {frame >= 2200 && (
          <g transform="translate(0, 110)">
            {/* LEFT: BACKPROPAGATION - DETERMINISTIC VECTOR DERIVATIVE */}
            <g transform="translate(330, 180)">
              <text x="0" y="-140" fill="#5AF78E" fontSize="15" fontWeight="900" textAnchor="middle">
                BACKPROPAGATION: REVERSE GRAPH
              </text>
              <text x="0" y="-120" fill="#A0FFA0" fontSize="11" textAnchor="middle">
                Exact Analytic Chain Rule: Var(∇_backprop) = 0
              </text>

              {/* Exact Green Gradient Vector flowing back */}
              <line x1="-140" y1="0" x2="140" y2="0" stroke="#5AF78E" strokeWidth="4" />
              <polygon points="140,0 120,-8 120,8" fill="#5AF78E" />
              <circle cx="-140" cy="0" r="12" fill="#5AF78E" />
              <circle cx="140" cy="0" r="12" fill="#5AF78E" />

              <g transform="translate(0, 50)">
                <text x="0" y="0" fill="#FFFFFF" fontSize="12" fontWeight="900" textAnchor="middle">
                  ∇_W L = (∂L / ∂y) · (∂y / ∂h) · (∂h / ∂W)
                </text>
                <text x="0" y="24" fill="#5AF78E" fontSize="11" textAnchor="middle">
                  Zero Variance: Every gradient vector points toward true minimum
                </text>
              </g>

              <rect x="-180" y="150" width="360" height="34" fill="rgba(0, 60, 30, 0.9)" stroke="#5AF78E" strokeWidth="1.5" rx="6" />
              <text x="0" y="172" fill="#5AF78E" fontSize="11" fontWeight="800" textAnchor="middle">
                DATA EFFICIENCY: O(1) SAMPLES PER UPDATE
              </text>
            </g>

            {/* SEPARATOR AXIS */}
            <line x1="640" y1="40" x2="640" y2="460" stroke="#7B2CBF" strokeWidth="1.5" strokeDasharray="4 4" />

            {/* RIGHT: LOCAL THREE-FACTOR PLASTICITY - VARIANCE EXPLOSION */}
            <g transform="translate(950, 180)">
              <text x="0" y="-140" fill="#FF0055" fontSize="15" fontWeight="900" textAnchor="middle">
                LOCAL 3-FACTOR REWARD PERTURBATION
              </text>
              <text x="0" y="-120" fill="#FFB0C0" fontSize="11" textAnchor="middle">
                Var(∇_local) ∝ e^(Ω(T)) · σ_neuromod^2 (Explodes with Horizon T)
              </text>

              {/* Noisy Exploding Vector Cloud */}
              {Array.from({ length: 24 }).map((_, i) => {
                const angle = (i / 24) * Math.PI * 2 + Math.sin(frame * 0.1 + i);
                const len = 30 + (i % 7) * varianceFactor * 2.5;
                const vx = Math.cos(angle) * len;
                const vy = Math.sin(angle) * len;

                return (
                  <line
                    key={`noise-vec-${i}`}
                    x1="0"
                    y1="0"
                    x2={vx}
                    y2={vy}
                    stroke="#FF0055"
                    strokeWidth="1.5"
                    opacity={0.7}
                  />
                );
              })}
              <circle cx="0" cy="0" r="10" fill="#FF0055" />

              <g transform="translate(0, 90)">
                <text x="0" y="0" fill="#FFFFFF" fontSize="12" fontWeight="900" textAnchor="middle">
                  Horizon T = {horizonT} steps | Variance = {(varianceFactor * 14.2).toFixed(1)}x
                </text>
                <text x="0" y="24" fill="#FF5555" fontSize="11" textAnchor="middle">
                  Noise swamps gradient ⟹ Requires millions of extra episodes
                </text>
              </g>

              <rect x="-180" y="150" width="360" height="34" fill="rgba(60, 0, 20, 0.9)" stroke="#FF0055" strokeWidth="1.5" rx="6" />
              <text x="0" y="172" fill="#FF5555" fontSize="11" fontWeight="800" textAnchor="middle">
                CREDIT BLINDNESS: HIGH-DIMENSIONAL DIFFUSION
              </text>
            </g>
          </g>
        )}

        {/* BOTTOM MATHEMATICAL CONCLUSION */}
        <g transform="translate(640, 630)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
            THE SILICON TRAP: LOCAL PLASTICITY IS PARALYZED BY HARDWARE STALLS AND TEMPORAL NOISE
          </text>
          <text x="0" y="22" fill="#C77DFF" fontSize="11" textAnchor="middle">
            Hooker (2021) Hardware Lottery ∩ Williams (1992) REINFORCE Variance Scaling
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Sara Hooker Hardware Lottery Paper (Frames 80 to 1400) */}
      {frame >= 80 && frame < 1400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_hardware_lottery-01.png")}
          title="COMMUNICATIONS OF THE ACM (2021)"
          authorBadge="SARA HOOKER"
          highlightText="The Hardware Lottery: Ideas Succeed by Matching Silicon"
          x={25}
          y={110}
          width={200}
          height={185}
          colorTheme="magenta"
          enterFrame={80}
        />
      )}

      {/* 2. Sara Hooker Portrait (Frames 1400 to 2800) */}
      {frame >= 1400 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/sara_hooker.png")}
          title="SARA HOOKER — HARDWARE LOTTERY"
          authorBadge="COHERE FOR AI"
          highlightText="Dense Systolic Compute Dominates Sparse Irregular Graphs"
          x={960}
          y={110}
          width={240}
          height={185}
          colorTheme="yellow"
          enterFrame={1400}
        />
      )}

      {/* 3. Systolic Supercomputer Cluster (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/datacenters/datacenter_supercomputer.jpg")}
          title="NVIDIA H100 SYSTOLIC CLUSTER"
          authorBadge="989.4 TFLOPS DENSE GEMM"
          highlightText="Arithmetic Intensity O(d) vs Pointer Chasing O(1) Stalls"
          x={25}
          y={120}
          width={200}
          height={185}
          colorTheme="cyan"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
