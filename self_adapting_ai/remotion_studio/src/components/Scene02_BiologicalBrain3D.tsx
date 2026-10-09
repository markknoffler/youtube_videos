import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene02_BiologicalBrain3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // STAGE TIMINGS (Narrative synchronization for Chapter 2)
  // "In biology, there is no separation between the processor and the memory." (0-80)
  // "Every synapse is both computing and storing information simultaneously." (80-160)
  // "They wire together locally, physically growing connections based on usage." (160-240)

  // 1. Biological Brain setup
  const pulseScale = spring({ frame: frame - 10, fps, config: { damping: 10 }, from: 0, to: 1 });
  const pulseOpacity = interpolate(frame, [10, 40], [0, 0.4], { extrapolateRight: "clamp" });

  // 2. Compute and Store simultaneously (split nodes)
  const computeOpacity = interpolate(frame, [80, 100], [0, 1], { extrapolateRight: "clamp" });
  const storeOpacity = interpolate(frame, [110, 130], [0, 1], { extrapolateRight: "clamp" });
  const mergeProgression = spring({ frame: frame - 140, fps, config: { damping: 14 }, from: 0, to: 1 });

  // 3. Physical wiring growth
  const wiringProgression = spring({ frame: frame - 160, fps, config: { damping: 20 }, from: 0, to: 1 });
  
  const cx = 410, cy = 260;
  const nodes = [
    { x: cx - 120, y: cy - 60 },
    { x: cx + 140, y: cy - 80 },
    { x: cx - 40, y: cy + 100 },
    { x: cx + 80, y: cy + 60 }
  ];

  return (
    <div style={{ position: "relative", width: 820, height: 520, fontFamily: "'JetBrains Mono', monospace" }}>
      
      {/* Background Pulse representing organic compute */}
      <svg style={{ position: "absolute", width: "100%", height: "100%" }}>
        <circle cx={cx} cy={cy} r={200 * pulseScale} fill="none" stroke="#5AF78E" strokeWidth="2" opacity={pulseOpacity} />
        <circle cx={cx} cy={cy} r={(200 * pulseScale) - (frame % 40)} fill="none" stroke="#5AF78E" strokeWidth="1" opacity={pulseOpacity * 0.5} />
      </svg>

      {/* Nodes displaying Compute and Store split, then merging */}
      <div style={{ position: "absolute", left: cx - 50, top: cy - 180, textAlign: "center", color: "#FFF", width: 100 }}>
         {frame < 80 ? null : (
           <>
             <div style={{ color: "#00F0FF", opacity: computeOpacity - mergeProgression, position: "absolute", left: -40 + mergeProgression*40 }}>COMPUTE</div>
             <div style={{ color: "#FF2A85", opacity: storeOpacity - mergeProgression, position: "absolute", left: 60 - mergeProgression*40 }}>STORE</div>
             <div style={{ color: "#5AF78E", opacity: mergeProgression, position: "absolute", left: 10 }}>UNIFIED</div>
           </>
         )}
      </div>

      <svg style={{ position: "absolute", width: "100%", height: "100%" }}>
        {/* Physical Wiring Growth */}
        {nodes.map((node, i) => {
          if (i === 0) return null; // Connect everything to node 0 for simplicity
          const prev = nodes[0];
          
          const lineX = prev.x + (node.x - prev.x) * wiringProgression;
          const lineY = prev.y + (node.y - prev.y) * wiringProgression;

          return (
            <g key={i}>
              <line x1={prev.x} y1={prev.y} x2={lineX} y2={lineY} stroke="#5AF78E" strokeWidth="3" opacity={wiringProgression} />
              <circle cx={node.x} cy={node.y} r="8" fill="#5AF78E" opacity={wiringProgression} />
            </g>
          );
        })}
        {/* Central Node */}
        <circle cx={nodes[0].x} cy={nodes[0].y} r="12" fill="#5AF78E" opacity={pulseOpacity} />
      </svg>

    </div>
  );
};
