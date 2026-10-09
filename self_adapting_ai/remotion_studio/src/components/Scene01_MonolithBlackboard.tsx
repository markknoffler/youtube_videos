import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { HolographicAssetWindow } from "./HolographicAssetWindow";

// 3D Isometric projection helper
function project3D(x: number, y: number, z: number, camYaw: number, camPitch: number, zoom = 1) {
  // Rotate Y
  const radY = (camYaw * Math.PI) / 180;
  const x1 = x * Math.cos(radY) + z * Math.sin(radY);
  const z1 = -x * Math.sin(radY) + z * Math.cos(radY);

  // Rotate X
  const radX = (camPitch * Math.PI) / 180;
  const y2 = y * Math.cos(radX) - z1 * Math.sin(radX);
  const z2 = y * Math.sin(radX) + z1 * Math.cos(radX);

  // Perspective projection
  const fov = 750;
  const scale = (fov / (fov + z2)) * zoom;
  return {
    px: 640 + x1 * scale,
    py: 360 + y2 * scale,
    scale,
    z: z2,
  };
}

export const Scene01_MonolithBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Master pedagogical camera motion
  const camYaw = interpolate(frame, [0, 4500], [-15, 25]);
  const camPitch = interpolate(frame, [0, 4500], [18, 12]);
  const zoom = interpolate(frame, [0, 800, 1800, 2700, 4500], [0.95, 1.05, 1.15, 1.1, 0.9]);

  // Phase 1: 0 - 104 frames (Welcome & Coordinate Grid Emergence)
  const gridSpread = spring({ frame, fps, config: { damping: 20 }, from: 0, to: 1 });

  // Phase 2: 104 - 388 frames (5 Frontier Model Branches)
  const branchProgress = spring({ frame: frame - 104, fps, config: { damping: 16 }, from: 0, to: 1 });

  // Phase 3: 672 - 1038 frames (Monolith Convergence)
  const monolithMorph = interpolate(frame, [672, 950], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 4: 1038 - 1700 frames (Pre-training SGD Matrix Updates)
  const isTrainingPhase = frame >= 1038 && frame < 1700;

  // Phase 5: 1700 - 2100 frames (Cryogenic Freeze Shockwave)
  const freezeWave = interpolate(frame, [1700, 1820], [0, 600], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const isFrozen = frame >= 1760;

  // Phase 6: 2642 - 3426 frames (Q, K, V Projections & Dot-Product Attention)
  const qkvPhase = frame >= 2642 && frame < 3426;
  const tokenTravel = ((frame - 2642) * 4) % 400;

  // Phase 7: 3426 - 4500 frames (Three Theoretical Pillars Rise)
  const pillarRise = spring({ frame: frame - 3426, fps, config: { damping: 18 }, from: 0, to: 1 });

  // 5 Frontier Model Nodes (2026 SOTA Frontier)
  const models = [
    { name: "GPT-6 Astra", org: "OpenAI", angle: -54, color: "#FF2A85" },
    { name: "Claude 5.5", org: "Anthropic", angle: 18, color: "#C77DFF" },
    { name: "Gemini 4", org: "Google DeepMind", angle: 90, color: "#9D4EDD" },
    { name: "Llama 5", org: "Meta AI", angle: 162, color: "#00F0FF" },
    { name: "Mythos", org: "Frontier Lab", angle: 234, color: "#5AF78E" },
  ];

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
        <defs>
          <radialGradient id="chalkGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF2A85" stopOpacity="0.18" />
            <stop offset="100%" stopColor="#070112" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="freezeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#7B2CBF" stopOpacity="0.3" />
          </linearGradient>
        </defs>

        {/* Ambient Center Glow */}
        <circle cx="640" cy="360" r="450" fill="url(#chalkGlow)" />

        {/* 1. 3D CHALKBOARD COORDINATE GRID (Sprouts progressively) */}
        {Array.from({ length: 11 }).map((_, i) => {
          const coord = (i - 5) * 80;
          const p1 = project3D(coord, 180, -400 * gridSpread, camYaw, camPitch, zoom);
          const p2 = project3D(coord, 180, 400 * gridSpread, camYaw, camPitch, zoom);
          const p3 = project3D(-400 * gridSpread, 180, coord, camYaw, camPitch, zoom);
          const p4 = project3D(400 * gridSpread, 180, coord, camYaw, camPitch, zoom);

          return (
            <g key={`grid-${i}`} opacity={gridSpread * 0.35}>
              <line x1={p1.px} y1={p1.py} x2={p2.px} y2={p2.py} stroke="#7B2CBF" strokeWidth="1" strokeDasharray="3 3" />
              <line x1={p3.px} y1={p3.py} x2={p4.px} y2={p4.py} stroke="#7B2CBF" strokeWidth="1" strokeDasharray="3 3" />
            </g>
          );
        })}

        {/* 2. PHASE: 5 FRONTIER MODEL NODES & RADIAL CHALK BRANCHES */}
        {frame >= 104 && frame < 848 && (
          <g>
            {models.map((m, idx) => {
              const rad = (m.angle * Math.PI) / 180;
              const radius = 280 * branchProgress;
              const nx = Math.cos(rad) * radius;
              const nz = Math.sin(rad) * radius;
              const ny = -40;

              const origin = project3D(0, ny, 0, camYaw, camPitch, zoom);
              const target = project3D(nx, ny, nz, camYaw, camPitch, zoom);

              // Traveling photon packets along branch
              const photonOffset = ((frame * 3 + idx * 25) % 100) / 100;
              const px = origin.px + (target.px - origin.px) * photonOffset;
              const py = origin.py + (target.py - origin.py) * photonOffset;

              return (
                <g key={m.name}>
                  {/* Radial Laser Conduit */}
                  <line
                    x1={origin.px}
                    y1={origin.py}
                    x2={target.px}
                    y2={target.py}
                    stroke={m.color}
                    strokeWidth={2}
                    strokeOpacity={0.6}
                    strokeDasharray="6 4"
                  />
                  {/* Photon Packet */}
                  <circle cx={px} cy={py} r="3.5" fill="#FFFFFF" filter="drop-shadow(0 0 6px #FFF)" />

                  {/* Model Node */}
                  <circle
                    cx={target.px}
                    cy={target.py}
                    r={18 * target.scale * branchProgress}
                    fill="#150228"
                    stroke={m.color}
                    strokeWidth={2.5}
                  />
                  <text
                    x={target.px}
                    y={target.py - 24 * target.scale}
                    fill="#FFFFFF"
                    fontSize={11 * target.scale}
                    fontWeight="800"
                    textAnchor="middle"
                  >
                    {m.name}
                  </text>
                  <text
                    x={target.px}
                    y={target.py + 30 * target.scale}
                    fill={m.color}
                    fontSize={8.5 * target.scale}
                    textAnchor="middle"
                  >
                    {m.org}
                  </text>
                </g>
              );
            })}

            {/* Central Convergence Hub */}
            {(() => {
              const hub = project3D(0, -40, 0, camYaw, camPitch, zoom);
              return (
                <g>
                  <circle cx={hub.px} cy={hub.py} r={32 * hub.scale} fill="#240342" stroke="#FF2A85" strokeWidth={2.5} />
                  <circle cx={hub.px} cy={hub.py} r={44 * hub.scale} fill="none" stroke="#FF2A85" strokeWidth={1} strokeDasharray="4 4" />
                  <text x={hub.px} y={hub.py + 4} fill="#FFFFFF" fontSize={9.5 * hub.scale} fontWeight="900" textAnchor="middle">
                    SHARED ENGINE
                  </text>
                </g>
              );
            })()}
          </g>
        )}

        {/* 3. PHASE: MONOLITH CRYSTAL ASSEMBLY (672 - 1038 frames) */}
        {frame >= 672 && (
          <g>
            {/* 3D Crystalline Transformer Monolith Pillar */}
            {(() => {
              const height = 240;
              const width = 120;
              const depth = 120;
              const py = -height / 2;

              // 8 vertices of the 3D Monolith
              const v = [
                project3D(-width / 2, py - height / 2, -depth / 2, camYaw, camPitch, zoom),
                project3D(width / 2, py - height / 2, -depth / 2, camYaw, camPitch, zoom),
                project3D(width / 2, py - height / 2, depth / 2, camYaw, camPitch, zoom),
                project3D(-width / 2, py - height / 2, depth / 2, camYaw, camPitch, zoom),
                project3D(-width / 2, py + height / 2, -depth / 2, camYaw, camPitch, zoom),
                project3D(width / 2, py + height / 2, -depth / 2, camYaw, camPitch, zoom),
                project3D(width / 2, py + height / 2, depth / 2, camYaw, camPitch, zoom),
                project3D(-width / 2, py + height / 2, depth / 2, camYaw, camPitch, zoom),
              ];

              const monolithColor = isFrozen ? "#3A1054" : "#FF2A85";
              const strokeColor = isFrozen ? "#00F0FF" : "#FF2A85";

              return (
                <g opacity={monolithMorph}>
                  {/* Faces */}
                  <polygon
                    points={`${v[2].px},${v[2].py} ${v[3].px},${v[3].py} ${v[7].px},${v[7].py} ${v[6].px},${v[6].py}`}
                    fill={monolithColor}
                    fillOpacity={0.4}
                    stroke={strokeColor}
                    strokeWidth={2}
                  />
                  <polygon
                    points={`${v[1].px},${v[1].py} ${v[2].px},${v[2].py} ${v[6].px},${v[6].py} ${v[5].px},${v[5].py}`}
                    fill={monolithColor}
                    fillOpacity={0.6}
                    stroke={strokeColor}
                    strokeWidth={2}
                  />
                  <polygon
                    points={`${v[0].px},${v[0].py} ${v[1].px},${v[1].py} ${v[2].px},${v[2].py} ${v[3].px},${v[3].py}`}
                    fill="#1F0238"
                    stroke={strokeColor}
                    strokeWidth={2}
                  />

                  {/* Core Monolith Inscription */}
                  <text
                    x={v[6].px - 20}
                    y={(v[2].py + v[6].py) / 2}
                    fill="#FFFFFF"
                    fontSize={11 * zoom}
                    fontWeight="900"
                    transform={`rotate(-5, ${v[6].px}, ${(v[2].py + v[6].py) / 2})`}
                  >
                    TRANSFORMER
                  </text>
                  <text
                    x={v[6].px - 20}
                    y={(v[2].py + v[6].py) / 2 + 18}
                    fill={strokeColor}
                    fontSize={10 * zoom}
                    fontWeight="800"
                  >
                    {isFrozen ? "dW/dt = 0.000" : "ATTENTION ENGINE"}
                  </text>
                </g>
              );
            })()}
          </g>
        )}

        {/* 4. PHASE: WEIGHT LATTICE & PRE-TRAINING SGD (1038 - 1700 frames) */}
        {isTrainingPhase && (
          <g>
            {/* 3D Parameter Matrix Grid */}
            {Array.from({ length: 6 }).map((_, r) =>
              Array.from({ length: 6 }).map((_, c) => {
                const mx = (c - 2.5) * 36 + 280;
                const my = (r - 2.5) * 36 - 40;
                const p = project3D(mx, my, 0, camYaw, camPitch, zoom);

                // Flashing gradient update activity
                const val = Math.sin(frame * 0.2 + r * 1.5 + c * 2.1).toFixed(2);
                const isUpdating = Math.sin(frame * 0.3 + r + c) > 0;

                return (
                  <g key={`param-${r}-${c}`}>
                    <rect
                      x={p.px - 14 * p.scale}
                      y={p.py - 14 * p.scale}
                      width={28 * p.scale}
                      height={28 * p.scale}
                      fill={isUpdating ? "rgba(90, 247, 142, 0.25)" : "rgba(199, 125, 255, 0.15)"}
                      stroke={isUpdating ? "#5AF78E" : "#7B2CBF"}
                      strokeWidth={1}
                    />
                    <text
                      x={p.px}
                      y={p.py + 4 * p.scale}
                      fill={isUpdating ? "#5AF78E" : "#E0AAFF"}
                      fontSize={8 * p.scale}
                      textAnchor="middle"
                    >
                      {val}
                    </text>
                  </g>
                );
              })
            )}

            {/* Gradient Streams Streaming into Lattice */}
            {Array.from({ length: 4 }).map((_, i) => {
              const streamProgress = ((frame * 4 + i * 25) % 100) / 100;
              const startX = 640 - 240 + streamProgress * 240;
              const startY = 160 + Math.sin(frame * 0.1 + i) * 30;

              return (
                <g key={`stream-${i}`}>
                  <line x1={startX - 30} y1={startY} x2={startX} y2={startY} stroke="#5AF78E" strokeWidth="2" strokeDasharray="4 2" />
                  <circle cx={startX} cy={startY} r="3" fill="#5AF78E" filter="drop-shadow(0 0 6px #5AF78E)" />
                </g>
              );
            })}

            {/* In-Canvas SGD Formula */}
            <text x="640" y="520" fill="#FFFFFF" fontSize="16" fontWeight="900" textAnchor="middle">
              W_(t+1) = W_t - η ∇L(W_t)
            </text>
            <text x="640" y="542" fill="#5AF78E" fontSize="11" textAnchor="middle">
              ACTIVE STOCHASTIC GRADIENT DESCENT: Δw_ij ≠ 0
            </text>
          </g>
        )}

        {/* 5. PHASE: CRYOGENIC FREEZE SHOCKWAVE (1700 - 2100 frames) */}
        {frame >= 1700 && frame < 2271 && (
          <g>
            {/* Expanding Shockwave Circle */}
            <circle
              cx="640"
              cy="360"
              r={freezeWave}
              fill="none"
              stroke="#00F0FF"
              strokeWidth="4"
              strokeDasharray="8 6"
              opacity={Math.max(0, 1 - freezeWave / 600)}
            />
            {/* Ice Frost Spikes */}
            {Array.from({ length: 12 }).map((_, i) => {
              const ang = (i * 30 * Math.PI) / 180;
              const r = freezeWave * 0.8;
              const x1 = 640 + Math.cos(ang) * (r - 25);
              const y1 = 360 + Math.sin(ang) * (r - 25);
              const x2 = 640 + Math.cos(ang) * r;
              const y2 = 360 + Math.sin(ang) * r;

              return <line key={`frost-${i}`} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#00F0FF" strokeWidth="2.5" />;
            })}

            {/* Frozen Invariance Formula Laser Chalk */}
            <g transform="translate(640, 520)">
              <rect x="-240" y="-22" width="480" height="44" fill="rgba(10, 2, 25, 0.9)" stroke="#00F0FF" strokeWidth="1.5" rx="6" />
              <text x="0" y="2" fill="#00F0FF" fontSize="16" fontWeight="900" textAnchor="middle">
                W_inference = W_0 ⟹ dW / dt = 0.000
              </text>
              <text x="0" y="16" fill="#C77DFF" fontSize="9.5" textAnchor="middle">
                FROZEN SILICON INVARIANCE: WEIGHTS LOCKED FOREVER
              </text>
            </g>
          </g>
        )}

        {/* 6. PHASE: Q, K, V PROJECTION PLANES & DOT PRODUCT ATTENTION (2642 - 3426 frames) */}
        {qkvPhase && (
          <g>
            {/* Token Vector Arrow entering */}
            {(() => {
              const tx = -300 + tokenTravel;
              const p = project3D(tx, -40, 0, camYaw, camPitch, zoom);
              return (
                <g>
                  <circle cx={p.px} cy={p.py} r="8" fill="#FF2A85" filter="drop-shadow(0 0 10px #FF2A85)" />
                  <text x={p.px} y={p.py - 14} fill="#FFFFFF" fontSize="11" fontWeight="800" textAnchor="middle">
                    Token x_i
                  </text>
                </g>
              );
            })()}

            {/* 3 Projected Subspaces: Q (Magenta Up), K (Cyan Right), V (Gold Down) */}
            {(() => {
              const origin = project3D(0, -40, 0, camYaw, camPitch, zoom);
              const qTarget = project3D(0, -180, -100, camYaw, camPitch, zoom);
              const kTarget = project3D(180, -40, 100, camYaw, camPitch, zoom);
              const vTarget = project3D(0, 100, 150, camYaw, camPitch, zoom);

              return (
                <g>
                  {/* Q Vector */}
                  <line x1={origin.px} y1={origin.py} x2={qTarget.px} y2={qTarget.py} stroke="#FF2A85" strokeWidth="3" />
                  <circle cx={qTarget.px} cy={qTarget.py} r="6" fill="#FF2A85" />
                  <text x={qTarget.px + 14} y={qTarget.py} fill="#FF2A85" fontSize="13" fontWeight="900">
                    Query Q = x W_Q
                  </text>

                  {/* K Vector */}
                  <line x1={origin.px} y1={origin.py} x2={kTarget.px} y2={kTarget.py} stroke="#00F0FF" strokeWidth="3" />
                  <circle cx={kTarget.px} cy={kTarget.py} r="6" fill="#00F0FF" />
                  <text x={kTarget.px + 14} y={kTarget.py} fill="#00F0FF" fontSize="13" fontWeight="900">
                    Key K = x W_K
                  </text>

                  {/* V Vector */}
                  <line x1={origin.px} y1={origin.py} x2={vTarget.px} y2={vTarget.py} stroke="#FFD166" strokeWidth="3" />
                  <circle cx={vTarget.px} cy={vTarget.py} r="6" fill="#FFD166" />
                  <text x={vTarget.px + 14} y={vTarget.py} fill="#FFD166" fontSize="13" fontWeight="900">
                    Value V = x W_V
                  </text>

                  {/* Dot-Product Angle Arc */}
                  <path
                    d={`M ${qTarget.px} ${qTarget.py} Q ${origin.px} ${origin.py} ${kTarget.px} ${kTarget.py}`}
                    fill="none"
                    stroke="#FFFFFF"
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                  />
                  <text x={origin.px + 40} y={origin.py - 60} fill="#FFFFFF" fontSize="12" fontWeight="800">
                    cos(θ) = Q · K^T / √d_k
                  </text>
                </g>
              );
            })()}

            {/* Dynamic Formula Display */}
            <g transform="translate(640, 580)">
              <text x="0" y="0" fill="#FFFFFF" fontSize="17" fontWeight="900" textAnchor="middle">
                Attention(Q, K, V) = softmax( (Q K^T) / √d_k ) V
              </text>
              <text x="0" y="20" fill="#FF2A85" fontSize="10.5" textAnchor="middle">
                O(1) CONSTANT DEPTH: DIRECT BILINEAR METRIC PROJECTION
              </text>
            </g>
          </g>
        )}

        {/* 7. PHASE: THREE THEORETICAL PILLARS (3426 - 4500 frames) */}
        {frame >= 3426 && (
          <g>
            {[
              { id: "T1", title: "THEOREM 1: RANK COLLAPSE", sub: "Lyapunov Decay: Rank(W) → 1", x: -280, color: "#FF2A85" },
              { id: "T2", title: "THEOREM 2: ROUTING BOUNDS", sub: "Moore Bound: Ω(log N / log Δ)", x: 0, color: "#C77DFF" },
              { id: "T3", title: "THEOREM 3: HARDWARE LOTTERY", sub: "Dense Systolic vs Sparse Latency", x: 280, color: "#5AF78E" },
            ].map((p, idx) => {
              const h = 200 * pillarRise;
              const pos = project3D(p.x, 140 - h / 2, 0, camYaw, camPitch, zoom);
              const top = project3D(p.x, 140 - h, 0, camYaw, camPitch, zoom);
              const base = project3D(p.x, 140, 0, camYaw, camPitch, zoom);

              return (
                <g key={p.id}>
                  {/* Pillar Column */}
                  <line x1={base.px} y1={base.py} x2={top.px} y2={top.py} stroke={p.color} strokeWidth={8 * pos.scale} />
                  <rect
                    x={pos.px - 90 * pos.scale}
                    y={top.py - 40 * pos.scale}
                    width={180 * pos.scale}
                    height={36 * pos.scale}
                    fill="rgba(15, 2, 30, 0.95)"
                    stroke={p.color}
                    strokeWidth={1.5}
                    rx="4"
                  />
                  <text
                    x={pos.px}
                    y={top.py - 22 * pos.scale}
                    fill="#FFFFFF"
                    fontSize={10.5 * pos.scale}
                    fontWeight="900"
                    textAnchor="middle"
                  >
                    {p.title}
                  </text>
                  <text
                    x={pos.px}
                    y={top.py - 10 * pos.scale}
                    fill={p.color}
                    fontSize={8 * pos.scale}
                    textAnchor="middle"
                  >
                    {p.sub}
                  </text>
                </g>
              );
            })}
          </g>
        )}
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. ArXiv Attention Paper (Frames 80 to 1100) */}
      {frame >= 80 && frame < 1100 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_attention-01.png")}
          title="ARXIV:1706.03762 — ATTENTION IS ALL YOU NEED"
          authorBadge="VASWANI ET AL. (2017)"
          highlightText="Section 3.2: Multi-Head Self-Attention Primitive"
          x={40}
          y={110}
          width={280}
          height={190}
          colorTheme="cyan"
          enterFrame={80}
        />
      )}

      {/* 2. Top500 GPU Cluster Datacenter (Frames 1100 to 2200) */}
      {frame >= 1100 && frame < 2200 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/datacenters/datacenter_supercomputer.jpg")}
          title="FRONTIER PRE-TRAINING CLUSTER (10,000+ GPUS)"
          authorBadge="TOP500 SUPERCOMPUTER"
          highlightText="Megawatts Consumed to Optimize Invariant Weights"
          x={960}
          y={110}
          width={280}
          height={185}
          colorTheme="magenta"
          enterFrame={1100}
        />
      )}

      {/* 3. Ilya Sutskever Holographic Citation (Frames 2200 to 3400) */}
      {frame >= 2200 && frame < 3400 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/ilya_sutskever.jpg")}
          title="THE FROZEN PARAMETRIC LANDSCAPE"
          authorBadge="ILYA SUTSKEVER (OPENAI)"
          highlightText="Frozen Weights Etched into Silicon Like Stone"
          x={40}
          y={120}
          width={220}
          height={185}
          colorTheme="purple"
          enterFrame={2200}
        />
      )}
    </div>
  );
};
