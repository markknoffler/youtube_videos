import React, { useMemo } from "react";
import { useCurrentFrame } from "remotion";

interface Particle {
  id: number;
  baseX: number;
  baseY: number;
  size: number;
  color: string;
  speed: number;
  amplitude: number;
  phase: number;
}

export const FloatingDustParticles: React.FC<{ count?: number }> = ({ count = 35 }) => {
  const frame = useCurrentFrame();

  const particles: Particle[] = useMemo(() => {
    const colors = ["#FF2A85", "#C77DFF", "#E0AAFF", "#9D4EDD", "#FF70A6"];
    const list: Particle[] = [];
    for (let i = 0; i < count; i++) {
      list.push({
        id: i,
        baseX: (i * 37) % 1280,
        baseY: (i * 53) % 720,
        size: 2 + (i % 4) * 1.5,
        color: colors[i % colors.length],
        speed: 0.2 + (i % 3) * 0.15,
        amplitude: 15 + (i % 5) * 8,
        phase: (i * 0.7) % (Math.PI * 2),
      });
    }
    return list;
  }, [count]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: 1280,
        height: 720,
        pointerEvents: "none",
        overflow: "hidden",
        zIndex: 1,
      }}
    >
      {particles.map((p) => {
        const yOffset = ((frame * p.speed + p.baseY) % 760) - 20;
        const xOffset = p.baseX + Math.sin(frame * 0.04 + p.phase) * p.amplitude;
        const opacity = 0.3 + 0.4 * Math.sin(frame * 0.06 + p.phase);

        return (
          <div
            key={p.id}
            style={{
              position: "absolute",
              left: xOffset,
              top: yOffset,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              backgroundColor: p.color,
              boxShadow: `0 0 ${p.size * 3}px ${p.color}`,
              opacity,
            }}
          />
        );
      })}
    </div>
  );
};
