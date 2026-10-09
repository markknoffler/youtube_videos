import React, { useMemo } from "react";
import { useCurrentFrame } from "remotion";

interface Node {
  id: number;
  x: number;
  y: number;
  radius: number;
  baseColor: string;
}

interface Edge {
  from: number;
  to: number;
  weight: number;
}

interface SynapticNetworkProps {
  width?: number;
  height?: number;
  nodeCount?: number;
}

export const SynapticNetwork: React.FC<SynapticNetworkProps> = ({
  width = 540,
  height = 360,
  nodeCount = 14,
}) => {
  const frame = useCurrentFrame();

  // Deterministic node placement
  const nodes: Node[] = useMemo(() => {
    const list: Node[] = [];
    const colors = ["#FF2A85", "#C77DFF", "#E0AAFF", "#FF70A6", "#9D4EDD"];
    for (let i = 0; i < nodeCount; i++) {
      const angle = (i / nodeCount) * Math.PI * 2 + (i % 3) * 0.4;
      const dist = 70 + (i % 4) * 35;
      const cx = width / 2 + Math.cos(angle) * dist;
      const cy = height / 2 + Math.sin(angle) * dist * 0.75;
      list.push({
        id: i,
        x: Math.max(30, Math.min(width - 30, cx)),
        y: Math.max(30, Math.min(height - 30, cy)),
        radius: 6 + (i % 3) * 2,
        baseColor: colors[i % colors.length],
      });
    }
    return list;
  }, [width, height, nodeCount]);

  // Edges between nearby nodes
  const edges: Edge[] = useMemo(() => {
    const list: Edge[] = [];
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 140) {
          list.push({ from: i, to: j, weight: Math.max(0.2, 1 - dist / 140) });
        }
      }
    }
    return list;
  }, [nodes]);

  return (
    <div
      style={{
        width,
        height,
        position: "relative",
        borderRadius: 14,
        overflow: "hidden",
        backgroundColor: "#100220",
        border: "1.5px solid #7B2CBF",
        boxShadow: "0 0 24px rgba(123, 44, 191, 0.3)",
      }}
    >
      <svg width={width} height={height} style={{ position: "absolute", top: 0, left: 0 }}>
        <defs>
          <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF2A85" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#100220" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Synaptic Axon Connections */}
        {edges.map((e, idx) => {
          const n1 = nodes[e.from];
          const n2 = nodes[e.to];
          const pulsePhase = (frame * 0.05 + idx * 0.3) % 1;
          const px = n1.x + (n2.x - n1.x) * pulsePhase;
          const py = n1.y + (n2.y - n1.y) * pulsePhase;

          return (
            <g key={idx}>
              <line
                x1={n1.x}
                y1={n1.y}
                x2={n2.x}
                y2={n2.y}
                stroke="#5A189A"
                strokeWidth={e.weight * 2.2}
                strokeOpacity={0.65}
              />
              {/* Traveling Action Potential Packet */}
              <circle
                cx={px}
                cy={py}
                r={3.2}
                fill="#FF2A85"
                filter="drop-shadow(0px 0px 4px #FF2A85)"
              />
            </g>
          );
        })}

        {/* Neurons */}
        {nodes.map((node) => {
          const pulse = Math.sin(frame * 0.1 + node.id) * 0.25;
          const r = node.radius * (1 + pulse);
          return (
            <g key={node.id}>
              {/* Outer halo */}
              <circle
                cx={node.x}
                cy={node.y}
                r={r * 2.2}
                fill={node.baseColor}
                opacity={0.18 + pulse * 0.1}
              />
              {/* Core neuron */}
              <circle
                cx={node.x}
                cy={node.y}
                r={r}
                fill={node.baseColor}
                stroke="#FFFFFF"
                strokeWidth={1.5}
                filter={`drop-shadow(0px 0px 6px ${node.baseColor})`}
              />
            </g>
          );
        })}
      </svg>

      {/* Floating HUD Indicator */}
      <div
        style={{
          position: "absolute",
          top: 10,
          left: 12,
          fontSize: 10,
          fontFamily: "monospace",
          color: "#E0AAFF",
          backgroundColor: "rgba(30, 4, 52, 0.75)",
          padding: "3px 8px",
          borderRadius: 6,
          border: "1px solid #9D4EDD",
        }}
      >
        ● DYNAMIC SYNAPTIC MESH • {nodes.length} NEURONS • {edges.length} AXONS
      </div>
    </div>
  );
};
