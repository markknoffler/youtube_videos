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

export const Scene03_SelfOrganizingBlackboard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const camYaw = interpolate(frame, [0, 4500], [-12, 18]);
  const camPitch = interpolate(frame, [0, 4500], [16, 10]);
  const zoom = interpolate(frame, [0, 1500, 3000, 4500], [0.95, 1.15, 1.1, 0.9]);

  // Phase 1: 0 - 964 frames (Hebb 1949: Neurons that fire together wire together)
  const isHebbPhase = frame < 1108;
  const hebbPulse = Math.sin(frame * 0.2) > 0;

  // Phase 2: 1108 - 1677 frames (Oja 1982: Principal Component Alignment)
  const isOjaPhase = frame >= 1108 && frame < 1861;
  const ojaAngle = interpolate(frame, [1108, 1500], [45, 0], { extrapolateRight: "clamp" });

  // Phase 3: 1677 - 2484 frames (Kohonen SOM Topological Folding)
  const isKohonenPhase = frame >= 1677 && frame < 2907;

  // Phase 4: 2907 - 4500 frames (The Scaling Wall & Representational Collapse)
  const isCollapsePhase = frame >= 2907;
  const chaosFactor = interpolate(frame, [3283, 3600], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Dynamic Graph Nodes (morphing through the phases)
  const graphNodes = Array.from({ length: 16 }).map((_, i) => {
    const row = Math.floor(i / 4);
    const col = i % 4;

    // Normal grid position
    let gx = (col - 1.5) * 80;
    let gy = (row - 1.5) * 80;
    let gz = 0;

    // If collapsing: points scatter or pull toward 1D axis
    if (isCollapsePhase) {
      gx = gx * (1 - chaosFactor * 0.85); // Collapse into 1D line!
      gy = gy + Math.sin(frame * 0.2 + i) * 30 * chaosFactor;
    }

    return { gx, gy, gz, id: i };
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
        <circle cx="640" cy="360" r="460" fill="#C77DFF" opacity="0.05" />

        {/* 1. HEBB PHASE (0 - 964 frames): Two Neurons Wiring Together */}
        {isHebbPhase && (
          <g>
            {(() => {
              const n1 = project3D(-140, -40, 0, camYaw, camPitch, zoom);
              const n2 = project3D(140, -40, 0, camYaw, camPitch, zoom);

              return (
                <g>
                  {/* Synaptic Bridge Line */}
                  <line
                    x1={n1.px}
                    y1={n1.py}
                    x2={n2.px}
                    y2={n2.py}
                    stroke={hebbPulse ? "#5AF78E" : "#7B2CBF"}
                    strokeWidth={hebbPulse ? 6 : 2}
                  />

                  {/* Firing action potentials */}
                  <circle cx={n1.px} cy={n1.py} r={18} fill="#240342" stroke="#5AF78E" strokeWidth={3} />
                  <circle cx={n2.px} cy={n2.py} r={18} fill="#240342" stroke="#5AF78E" strokeWidth={3} />

                  <text x={n1.px} y={n1.py - 28} fill="#FFFFFF" fontSize="12" fontWeight="900" textAnchor="middle">
                    Presynaptic x_j
                  </text>
                  <text x={n2.px} y={n2.py - 28} fill="#FFFFFF" fontSize="12" fontWeight="900" textAnchor="middle">
                    Postsynaptic y_i
                  </text>

                  {/* Famous Adage Text */}
                  <text x="640" y="240" fill="#5AF78E" fontSize="20" fontWeight="900" textAnchor="middle">
                    "NEURONS THAT FIRE TOGETHER, WIRE TOGETHER"
                  </text>
                  <text x="640" y="270" fill="#C77DFF" fontSize="12" textAnchor="middle">
                    DONALD HEBB (1949): Δw_ij = η · y_i · x_j
                  </text>
                </g>
              );
            })()}
          </g>
        )}

        {/* 2. OJA'S RULE PHASE (1108 - 1861 frames): Principal Eigenvector Convergence */}
        {isOjaPhase && (
          <g transform="translate(640, 360)">
            {/* Input Covariance Ellipse */}
            <ellipse cx="0" cy="0" rx="180" ry="70" fill="rgba(123, 44, 191, 0.15)" stroke="#7B2CBF" strokeWidth="1.5" />

            {/* Rotating Weight Vector aligning with Principal Axis */}
            {(() => {
              const rad = (ojaAngle * Math.PI) / 180;
              const vx = Math.cos(rad) * 170;
              const vy = Math.sin(rad) * 60;
              return (
                <g>
                  <line x1="0" y1="0" x2={vx} y2={vy} stroke="#00F0FF" strokeWidth="4" />
                  <circle cx={vx} cy={vy} r="6" fill="#00F0FF" />
                  <text x={vx + 14} y={vy} fill="#00F0FF" fontSize="12" fontWeight="900">
                    Weight Vector w → v_1 (Dominant Eigenvector)
                  </text>
                </g>
              );
            })()}

            {/* Oja's Formula */}
            <text x="0" y="160" fill="#FFFFFF" fontSize="16" fontWeight="900" textAnchor="middle">
              dw/dt = C w - (w^T C w) w
            </text>
            <text x="0" y="184" fill="#C77DFF" fontSize="11" textAnchor="middle">
              ERKKI OJA (1982): NORMALIZED HEBBIAN CONVERGENCE
            </text>
          </g>
        )}

        {/* 3. DYNAMIC REWIRING & COLLAPSE PHASE (2082 - 4500 frames) */}
        {(isKohonenPhase || isCollapsePhase) && (
          <g>
            {/* Node Connections */}
            {graphNodes.map((n, idx) => {
              const p = project3D(n.gx, n.gy, n.gz, camYaw, camPitch, zoom);

              return (
                <g key={`gn-${n.id}`}>
                  {graphNodes
                    .filter((_, j) => j > idx && (Math.abs(idx - j) === 1 || Math.abs(idx - j) === 4))
                    .map((neighbor) => {
                      const np = project3D(neighbor.gx, neighbor.gy, neighbor.gz, camYaw, camPitch, zoom);
                      const edgeColor = isCollapsePhase ? "#FF2A85" : "#5AF78E";

                      return (
                        <line
                          key={`ge-${idx}-${neighbor.id}`}
                          x1={p.px}
                          y1={p.py}
                          x2={np.px}
                          y2={np.py}
                          stroke={edgeColor}
                          strokeWidth={isCollapsePhase ? 1 : 2}
                          strokeOpacity={isCollapsePhase ? 0.4 : 0.8}
                        />
                      );
                    })}

                  <circle
                    cx={p.px}
                    cy={p.py}
                    r={isCollapsePhase ? 4 : 7 * p.scale}
                    fill={isCollapsePhase ? "#FF2A85" : "#00F0FF"}
                  />
                </g>
              );
            })}

            {/* Collapse Warning */}
            {isCollapsePhase && (
              <g transform="translate(640, 580)">
                <text x="0" y="0" fill="#FF2A85" fontSize="20" fontWeight="900" textAnchor="middle">
                  REPRESENTATIONAL COLLAPSE: 1D ATTRACTOR
                </text>
                <text x="0" y="24" fill="#FFFFFF" fontSize="12" textAnchor="middle">
                  LOCAL HEBBIAN PLASTICITY CANNOT PRESERVE MULTI-RELATIONAL RANK
                </text>
              </g>
            )}
          </g>
        )}
      </svg>

      {/* HOLOGRAPHIC REAL-WORLD EXTERNAL ASSET WINDOWS */}
      {/* 1. Donald Hebb Synapse Portrait (Frames 80 to 1100) */}
      {frame >= 80 && frame < 1100 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/researchers/donald_hebb.jpg")}
          title="DONALD HEBB (1949) — SYNAPSE GROWTH"
          authorBadge="THE ORGANIZATION OF BEHAVIOR"
          highlightText="Neurons That Fire Together, Wire Together"
          x={40}
          y={110}
          width={240}
          height={185}
          colorTheme="purple"
          enterFrame={80}
        />
      )}

      {/* 2. Weight Agnostic Neural Networks Paper (Frames 1100 to 2300) */}
      {frame >= 1100 && frame < 2300 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_wann-01.png")}
          title="NEURIPS 2019: WEIGHT AGNOSTIC NETWORKS"
          authorBadge="GAIER & HA (GOOGLE BRAIN)"
          highlightText="Topologies Learn Tasks Without Weight Updates"
          x={950}
          y={110}
          width={290}
          height={190}
          colorTheme="cyan"
          enterFrame={1100}
        />
      )}

      {/* 3. Representation Collapse Citation (Frames 2300 to 3600) */}
      {frame >= 2300 && frame < 3600 && (
        <HolographicAssetWindow
          src={staticFile("assets/real_world/papers/paper_predictive_coding-01.png")}
          title="THE SCALING WALL & DYNAMIC REWIRING"
          authorBadge="THEORETICAL DEAD END"
          highlightText="Unsupervised Topological Adaptation Collapses at Scale"
          x={40}
          y={120}
          width={280}
          height={185}
          colorTheme="magenta"
          enterFrame={2300}
        />
      )}
    </div>
  );
};
