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

export const Scene02_BiologicalBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const camYaw = interpolate(frame, [0, 4500], [-10, 20]);
  const camPitch = interpolate(frame, [0, 4500], [15, 8]);
  const zoom = interpolate(frame, [0, 1400, 2800, 4500], [1.0, 1.2, 1.05, 0.95]);

  // Phase 1: 0 - 870 frames (86B Neurons & 20W Budget)
  const brainRadius = spring({ frame, fps, config: { damping: 18 }, from: 0, to: 1 });

  // Phase 2: 1110 - 1440 frames (Dendritic Sprouting & Pruning)
  const isSproutingPhase = frame >= 1110 && frame < 2100;
  const sproutProg = spring({ frame: frame - 1110, fps, config: { damping: 15 }, from: 0, to: 1 });

  // Phase 3: 1440 - 2070 frames (STDP Spike Timing Curve)
  const isSTDPPhase = frame >= 1440 && frame < 2460;
  const deltaT = ((frame - 1440) * 0.4) % 60 - 30; // sweeps -30ms to +30ms

  // Phase 4: 2880 - 4500 frames (Biological vs Silicon Confrontation)
  const isConfrontation = frame >= 2880;

  // 18 Organic Brain Nodes arranged in 3D ellipsoidal neocortical sheet
  const bioNodes = Array.from({ length: 18 }).map((_, i) => {
    const theta = (i / 18) * Math.PI * 2;
    const phi = ((i % 5) / 5) * Math.PI - Math.PI / 2;
    const r = 240;
    return {
      x: r * Math.cos(phi) * Math.cos(theta),
      y: (r * 0.7) * Math.sin(phi) - 20,
      z: r * Math.cos(phi) * Math.sin(theta),
      id: i,
    };
  });

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
        {/* Ambient Biological Glow */}
        <circle cx="640" cy="360" r="480" fill="#5AF78E" opacity="0.04" />

        {/* 1. 3D BIOLOGICAL NEURAL GRAPH */}
        {bioNodes.map((n, idx) => {
          const p = project3D(n.x * brainRadius, n.y * brainRadius, n.z * brainRadius, camYaw, camPitch, zoom);
          const isFiring = Math.sin(frame * 0.15 + idx * 1.8) > 0.6;

          return (
            <g key={`bio-node-${n.id}`}>
              {/* Sprouting Connections to neighbors */}
              {bioNodes
                .filter((_, j) => Math.abs(idx - j) <= 2 && idx !== j)
                .map((neighbor) => {
                  const np = project3D(
                    neighbor.x * brainRadius,
                    neighbor.y * brainRadius,
                    neighbor.z * brainRadius,
                    camYaw,
                    camPitch,
                    zoom
                  );

                  // Sprouting growth / Pruning fade
                  const edgeThick = isSproutingPhase
                    ? Math.sin(frame * 0.1 + idx) > 0
                      ? 3 * sproutProg
                      : 0.6
                    : 1.5;
                  const edgeColor = edgeThick > 1.5 ? "#5AF78E" : "rgba(199, 125, 255, 0.4)";

                  return (
                    <line
                      key={`edge-${idx}-${neighbor.id}`}
                      x1={p.px}
                      y1={p.py}
                      x2={np.px}
                      y2={np.py}
                      stroke={edgeColor}
                      strokeWidth={edgeThick}
                    />
                  );
                })}

              {/* Action Potential Spike Pulse */}
              {isFiring && (
                <circle cx={p.px} cy={p.py} r={14 * p.scale} fill="none" stroke="#5AF78E" strokeWidth={2}>
                  <animate attributeName="r" values="6;22" dur="0.6s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="1;0" dur="0.6s" repeatCount="indefinite" />
                </circle>
              )}

              {/* Neuron Soma */}
              <circle
                cx={p.px}
                cy={p.py}
                r={6 * p.scale}
                fill={isFiring ? "#5AF78E" : "#C77DFF"}
                filter={isFiring ? "drop-shadow(0 0 10px #5AF78E)" : undefined}
              />
            </g>
          );
        })}

        {/* 2. METABOLIC POWER TELEMETRY (0 - 870 frames) */}
        {frame < 1110 && (
          <g transform="translate(640, 100)">
            <text x="0" y="0" fill="#5AF78E" fontSize="24" fontWeight="900" textAnchor="middle">
              86 BILLION NEURONS • 20 WATTS
            </text>
            <text x="0" y="24" fill="#C77DFF" fontSize="12" textAnchor="middle">
              METABOLIC GLUCOSE CONSUMPTION: ZERO GLOBAL CLOCKS
            </text>
          </g>
        )}

        {/* 3. STDP TIMING GRAPH (1440 - 2460 frames) */}
        {isSTDPPhase && (
          <g transform="translate(240, 520)">
            {/* Coordinate Axes */}
            <line x1="-160" y1="0" x2="160" y2="0" stroke="#FFFFFF" strokeWidth="1.5" />
            <line x1="0" y1="-80" x2="0" y2="80" stroke="#FFFFFF" strokeWidth="1.5" />
            <text x="170" y="4" fill="#FFFFFF" fontSize="10">Δt (ms)</text>
            <text x="0" y="-90" fill="#FFFFFF" fontSize="10" textAnchor="middle">Δw (Plasticity)</text>

            {/* LTP Curve (t > 0, Reinforcement) */}
            <path
              d="M 0,-60 Q 40,-15 150,-2"
              fill="none"
              stroke="#5AF78E"
              strokeWidth="3"
            />
            <text x="80" y="-40" fill="#5AF78E" fontSize="10" fontWeight="800">
              LTP (Potentiation)
            </text>

            {/* LTD Curve (t < 0, Depression) */}
            <path
              d="M -150,2 Q -40,15 0,60"
              fill="none"
              stroke="#FF2A85"
              strokeWidth="3"
            />
            <text x="-120" y="40" fill="#FF2A85" fontSize="10" fontWeight="800">
              LTD (Depression)
            </text>

            {/* Current Delta T Marker */}
            <line x1={deltaT * 4} y1="-70" x2={deltaT * 4} y2="70" stroke="#00F0FF" strokeWidth="2" strokeDasharray="3 3" />
            <circle cx={deltaT * 4} cy={deltaT > 0 ? -40 : 40} r="5" fill="#00F0FF" />
            <text x={deltaT * 4} y="-78" fill="#00F0FF" fontSize="9.5" textAnchor="middle">
              Δt = {deltaT.toFixed(1)} ms
            </text>

            {/* STDP Equation */}
            <text x="0" y="115" fill="#FFFFFF" fontSize="12" fontWeight="800" textAnchor="middle">
              Δw_ij = A_+ exp(-Δt / τ_+) - A_- exp(Δt / τ_-)
            </text>
          </g>
        )}

        {/* 4. CONFRONTATION: BIOLOGY VS SILICON MONOLITH (2880 - 4500 frames) */}
        {isConfrontation && (
          <g>
            {/* Silicon Grid on the Right */}
            <g transform="translate(940, 360)">
              <rect x="-140" y="-140" width="280" height="280" fill="rgba(15, 2, 30, 0.9)" stroke="#FF2A85" strokeWidth="2" rx="8" />
              <text x="0" y="-110" fill="#FF2A85" fontSize="14" fontWeight="900" textAnchor="middle">
                SILICON GPU MONOLITH
              </text>
              <text x="0" y="-90" fill="#FFFFFF" fontSize="10" textAnchor="middle">
                100 MEGAWATTS • FROZEN fp16
              </text>
              {/* Rigid systolic cells */}
              {Array.from({ length: 4 }).map((_, r) =>
                Array.from({ length: 4 }).map((_, c) => (
                  <rect
                    key={`silicon-${r}-${c}`}
                    x={(c - 2) * 50 + 10}
                    y={(r - 2) * 50 + 20}
                    width="40"
                    height="40"
                    fill="#240342"
                    stroke="#FF2A85"
                    strokeWidth="1"
                  />
                ))
              )}
              <text x="0" y="115" fill="#00F0FF" fontSize="11" fontWeight="800" textAnchor="middle">
                dW / dt = 0.000 (INVARIANT)
              </text>
            </g>

            {/* Contrast Label */}
            <text x="640" y="660" fill="#FFFFFF" fontSize="15" fontWeight="900" textAnchor="middle">
              WHY DID AI ABANDON FLUID PLASTICITY FOR FROZEN TENSORS?
            </text>
          </g>
        )}
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Donald Hebb 1949 Portrait (Frames 100 to 1100) */}
      {frame >= 100 && frame < 1100 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/donald_hebb.jpg")}
          title="SYNAPTIC PLASTICITY POSTULATE (1949)"
          authorBadge="DONALD O. HEBB"
          highlightText="Neurons That Fire Together, Wire Together"
          x={40}
          y={110}
          width={220}
          height={185}
          colorTheme="green"
          enterFrame={100}
        />
      )}

      {/* 2. Predictive Coding Paper (Frames 1100 to 2200) */}
      {frame >= 1100 && frame < 2200 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_predictive_coding-01.png")}
          title="BIOLOGICAL PLASTICITY IN VISUAL CORTEX"
          authorBadge="NATURE NEUROSCIENCE"
          highlightText="Continuous Dendritic Arborization & Synaptic Pruning"
          x={960}
          y={110}
          width={280}
          height={190}
          colorTheme="magenta"
          enterFrame={1100}
        />
      )}

      {/* 3. GPU Racks vs 20W Biological Mind (Frames 2200 to 3600) */}
      {frame >= 2200 && frame < 3600 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/datacenters/gpu_cluster_racks.jpg")}
          title="MEGAWATT GPU CLUSTER VS 20W BIO BRAIN"
          authorBadge="INDUSTRIAL INFRASTRUCTURE"
          highlightText="10 MW Substation Power vs 20 Watts Refrigerator Bulb"
          x={40}
          y={120}
          width={280}
          height={185}
          colorTheme="cyan"
          enterFrame={2200}
        />
      )}
    </div>
  );
};
