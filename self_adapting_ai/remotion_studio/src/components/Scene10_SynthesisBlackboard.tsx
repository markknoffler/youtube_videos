import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

export const Scene10_SynthesisBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Active pillar cycle (0 to 3) or final convergence
  const currentPillar = frame < 3300 ? Math.floor(frame / 800) % 4 : 4;

  // Fluid spline wave for KAN and Liquid ODE
  const waveOffset = (frame * 0.05) % (Math.PI * 2);

  return (
    <div
      style={{
        position: "absolute",
        width: 1280,
        height: 720,
        backgroundColor: "#050110",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      <svg width="1280" height="720" style={{ position: "absolute", top: 0, left: 0 }}>
        {/* Top Header */}
        <g transform="translate(640, 65)">
          <text x="0" y="0" fill="#00F0FF" fontSize="21" fontWeight="900" textAnchor="middle">
            THE 10-YEAR HORIZON: THE LIVING MATHEMATICAL BLACKBOARD (2026–2035)
          </text>
          <text x="0" y="24" fill="#E0AAFF" fontSize="12" textAnchor="middle">
            FOUR REVOLUTIONS CONVERGING TOWARD CONTINUOUS SELF-ADAPTING SYNTHETIC MINDS
          </text>
        </g>

        {/* FOUR PILLARS BANNER (Top Navigation) */}
        <g transform="translate(640, 120)">
          {[
            { label: "1. META-PLASTICITY", color: "#FF2A85" },
            { label: "2. LIQUID NEURAL ODEs", color: "#00F0FF" },
            { label: "3. KAN SPLINE SYNAPSES", color: "#5AF78E" },
            { label: "4. MEMRISTIVE CROSSBARS", color: "#FFE600" },
          ].map((pil, idx) => {
            const px = -450 + idx * 300;
            const isSelected = currentPillar === idx || currentPillar === 4;

            return (
              <g key={`pill-${idx}`} transform={`translate(${px}, 0)`}>
                <rect
                  x="-130"
                  y="-16"
                  width="260"
                  height="32"
                  fill={isSelected ? `${pil.color}22` : "rgba(20, 10, 40, 0.4)"}
                  stroke={isSelected ? pil.color : "#4A2060"}
                  strokeWidth={isSelected ? 2 : 1}
                  rx="6"
                />
                <text
                  x="0"
                  y="5"
                  fill={isSelected ? pil.color : "#888"}
                  fontSize="10.5"
                  fontWeight="900"
                  textAnchor="middle"
                >
                  {pil.label}
                </text>
              </g>
            );
          })}
        </g>

        {/* PILLAR 1: META-PLASTICITY (Frames 0 to 800) */}
        {currentPillar === 0 && (
          <g transform="translate(640, 340)">
            <circle cx="0" cy="0" r="160" fill="rgba(255, 42, 133, 0.08)" stroke="#FF2A85" strokeWidth="1" strokeDasharray="4 4" />
            <text x="0" y="-80" fill="#FF2A85" fontSize="16" fontWeight="900" textAnchor="middle">
              META-LEARNED PLASTICITY ENGINES
            </text>
            <text x="0" y="-55" fill="#FFA0C0" fontSize="11" textAnchor="middle">
              Secondary Hyper-Networks Optimize Learning Rules via Meta-Gradients
            </text>

            <rect x="-260" y="-15" width="520" height="40" fill="rgba(20, 5, 30, 0.9)" stroke="#FF2A85" strokeWidth="1.5" rx="6" />
            <text x="0" y="10" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
              ΔW_ij = f_θ(pre_i, post_j, W_ij, M_t)   [No manual Hebbian traps]
            </text>

            <text x="0" y="60" fill="#5AF78E" fontSize="12" fontWeight="700" textAnchor="middle">
              Full-Rank Stability Maintained Across Infinite Lifelong Learning Horizons
            </text>
          </g>
        )}

        {/* PILLAR 2: LIQUID NEURAL ODEs (Frames 800 to 1600) */}
        {currentPillar === 1 && (
          <g transform="translate(640, 340)">
            <text x="0" y="-100" fill="#00F0FF" fontSize="16" fontWeight="900" textAnchor="middle">
              LIQUID TIME-CONSTANT NEURAL DIFFERENTIAL EQUATIONS
            </text>
            <text x="0" y="-75" fill="#A0E0FF" fontSize="11" textAnchor="middle">
              Hasani & Rus (MIT): Routing Occurs in Continuous State Space Rather than Graph Wires
            </text>

            {/* Continuous Phase Space Wave */}
            <path
              d={`M -300,${Math.sin(waveOffset) * 40} Q -150,${Math.cos(waveOffset) * 60} 0,${Math.sin(waveOffset + 1) * 40} T 300,${Math.cos(waveOffset + 1) * 40}`}
              fill="none"
              stroke="#00F0FF"
              strokeWidth="4"
              filter="drop-shadow(0 0 8px #00F0FF)"
            />

            <rect x="-320" y="50" width="640" height="44" fill="rgba(0, 30, 50, 0.9)" stroke="#00F0FF" strokeWidth="1.5" rx="6" />
            <text x="0" y="78" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
              dx(t)/dt = -[1/τ + f(x(t), I(t))] x(t) + A f(x(t), I(t))
            </text>
          </g>
        )}

        {/* PILLAR 3: KOLMOGOROV-ARNOLD NETWORKS (Frames 1600 to 2400) */}
        {currentPillar === 2 && (
          <g transform="translate(640, 340)">
            <text x="0" y="-100" fill="#5AF78E" fontSize="16" fontWeight="900" textAnchor="middle">
              KOLMOGOROV-ARNOLD NETWORKS (KANs)
            </text>
            <text x="0" y="-75" fill="#B0FFB0" fontSize="11" textAnchor="middle">
              Liu et al. (MIT 2024): Learnable 1D B-Splines Replace Static Scalar Weights
            </text>

            {/* Learnable Spline Curve along Edge */}
            <path
              d={`M -250,30 C -120,${-80 + Math.sin(frame * 0.08) * 30} 120,${80 - Math.sin(frame * 0.08) * 30} 250,-30`}
              fill="none"
              stroke="#5AF78E"
              strokeWidth="4"
            />
            <circle cx="-250" cy="30" r="12" fill="#5AF78E" />
            <circle cx="250" cy="-30" r="12" fill="#5AF78E" />

            <rect x="-320" y="70" width="640" height="44" fill="rgba(5, 30, 15, 0.9)" stroke="#5AF78E" strokeWidth="1.5" rx="6" />
            <text x="0" y="98" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
              f(x) = ∑_(q=1)^(2n+1) Φ_q ( ∑_(p=1)^n ϕ_(q,p)(x_p) )
            </text>
          </g>
        )}

        {/* PILLAR 4: MEMRISTIVE CROSSBAR ACCELERATORS (Frames 2400 to 3300) */}
        {currentPillar === 3 && (
          <g transform="translate(640, 340)">
            <text x="0" y="-100" fill="#FFE600" fontSize="16" fontWeight="900" textAnchor="middle">
              NEUROMORPHIC IN-MEMORY CROSSBAR ARRAYS
            </text>
            <text x="0" y="-75" fill="#FFFFB0" fontSize="11" textAnchor="middle">
              Analog Physical Dot-Products via Ohm's Law & Kirchhoff's Current Law
            </text>

            {/* Crossbar Wires */}
            {[-60, 0, 60].map((y, r) => (
              <line key={`h-${r}`} x1="-180" y1={y} x2="180" y2={y} stroke="#FFE600" strokeWidth="2.5" />
            ))}
            {[-120, -40, 40, 120].map((x, c) => (
              <line key={`v-${c}`} x1={x} y1="-90" x2={x} y2="90" stroke="#00F0FF" strokeWidth="2.5" />
            ))}

            {/* Crossbar Conductance Junctions */}
            {[-60, 0, 60].map((y, r) =>
              [-120, -40, 40, 120].map((x, c) => (
                <circle key={`j-${r}-${c}`} cx={x} cy={y} r="6" fill="#FFE600" stroke="#FFFFFF" strokeWidth="1.5" />
              ))
            )}

            <rect x="-300" y="110" width="600" height="38" fill="rgba(30, 25, 0, 0.9)" stroke="#FFE600" strokeWidth="1.5" rx="6" />
            <text x="0" y="134" fill="#FFFFFF" fontSize="13" fontWeight="900" textAnchor="middle">
              I_j = ∑_i V_i · G_ij  |  0 ns Memory Bus Delay  |  In-Situ Plasticity
            </text>
          </g>
        )}

        {/* GRAND FINALE: THE LIVING MATHEMATICAL ORGANISM (Frames 3300 to 4500) */}
        {currentPillar === 4 && (
          <g transform="translate(640, 350)">
            <circle cx="0" cy="0" r="190" fill="rgba(0, 240, 255, 0.08)" stroke="#C77DFF" strokeWidth="2" />

            {/* Converged pulsating vortex core */}
            {Array.from({ length: 8 }).map((_, i) => {
              const rot = (i * 45) + frame * 0.5;
              const rad = 70 + Math.sin(frame * 0.05 + i) * 25;
              const cx = Math.cos((rot * Math.PI) / 180) * rad;
              const cy = Math.sin((rot * Math.PI) / 180) * rad;
              const colors = ["#FF2A85", "#00F0FF", "#5AF78E", "#FFE600"];

              return (
                <circle
                  key={`core-${i}`}
                  cx={cx}
                  cy={cy}
                  r="12"
                  fill={colors[i % 4]}
                  stroke="#FFFFFF"
                  strokeWidth="1.5"
                  opacity={0.85}
                />
              );
            })}

            <rect x="-240" y="-30" width="480" height="60" fill="rgba(10, 2, 25, 0.9)" stroke="#00F0FF" strokeWidth="2" rx="10" />
            <text x="0" y="-4" fill="#FFFFFF" fontSize="16" fontWeight="900" textAnchor="middle">
              THE SELF-ADAPTING MATHEMATICAL ORGANISM
            </text>
            <text x="0" y="18" fill="#5AF78E" fontSize="12" fontWeight="800" textAnchor="middle">
              CONTINUOUS · FLUID · PROFOUNDLY ALIVE
            </text>
          </g>
        )}

        {/* BOTTOM PHILOSOPHICAL CONCLUSION */}
        <g transform="translate(640, 640)">
          <text x="0" y="0" fill="#FFFFFF" fontSize="14" fontWeight="900" textAnchor="middle">
            BEYOND FROZEN SILICON AND NAIVE BIOLOGY: THE MATHEMATICAL UNIFICATION OF ADAPTATION
          </text>
          <text x="0" y="22" fill="#C77DFF" fontSize="11" textAnchor="middle">
            Hasani & Rus (Liquid ODEs) ∩ Liu et al. (KANs) ∩ In-Memory Neuromorphics ∩ Meta-Plasticity
          </text>
        </g>
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Liquid Neural ODEs Paper (Frames 800 to 1800) */}
      {frame >= 800 && frame < 1800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_liquid-01.png")}
          title="LIQUID TIME-CONSTANT NETWORKS"
          authorBadge="HASANI & RUS (MIT)"
          highlightText="Continuous Dynamic State Routing in Real-Time"
          x={40}
          y={110}
          width={290}
          height={185}
          colorTheme="cyan"
          enterFrame={800}
        />
      )}

      {/* 2. MIT Kolmogorov-Arnold Networks Paper (Frames 1800 to 2800) */}
      {frame >= 1800 && frame < 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_kan-01.png")}
          title="KOLMOGOROV-ARNOLD NETWORKS (2024)"
          authorBadge="LIU ET AL. (MIT)"
          highlightText="Learnable 1D B-Splines Replace Static Scalar Weights"
          x={950}
          y={110}
          width={290}
          height={185}
          colorTheme="green"
          enterFrame={1800}
        />
      )}

      {/* 3. The Future: Living Synthetic Minds (Frames 2800 to 4500) */}
      {frame >= 2800 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/datacenters/datacenter_supercomputer.jpg")}
          title="BEYOND FROZEN SILICON MONOLITHS"
          authorBadge="2026–2035 PARADIGM"
          highlightText="Self-Adapting Mathematical Organism"
          x={40}
          y={120}
          width={280}
          height={185}
          colorTheme="yellow"
          enterFrame={2800}
        />
      )}
    </div>
  );
};
