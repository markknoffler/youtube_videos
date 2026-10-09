import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Sentence9_ParadoxVortex: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame: frame - 4250, fps, config: { damping: 14 } });

  // Rotating gimbal rings
  const ring1Angle = (frame * 1.5) % 360;
  const ring2Angle = (-frame * 2.0) % 360;
  const ring3Angle = (frame * 1.0) % 360;

  return (
    <div
      style={{
        position: "relative",
        width: 860,
        height: 520,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${Math.max(0.01, entrance)})`,
        fontFamily: "'JetBrains Mono', monospace",
        flexDirection: "column",
        gap: 16,
      }}
    >
      {/* 3D Concentric Gimbal Ring System */}
      <div
        style={{
          position: "relative",
          width: 340,
          height: 340,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          perspective: 1000,
        }}
      >
        {/* Ring 1 (Hot Pink) */}
        <div
          style={{
            position: "absolute",
            width: 320,
            height: 320,
            borderRadius: "50%",
            border: "2px dashed #FF2A85",
            boxShadow: "0 0 20px rgba(255, 42, 133, 0.4)",
            transform: `rotateX(60deg) rotateZ(${ring1Angle}deg)`,
            transformStyle: "preserve-3d",
          }}
        />

        {/* Ring 2 (Lavender) */}
        <div
          style={{
            position: "absolute",
            width: 250,
            height: 250,
            borderRadius: "50%",
            border: "2px solid #C77DFF",
            boxShadow: "0 0 16px rgba(199, 125, 255, 0.4)",
            transform: `rotateY(55deg) rotateZ(${ring2Angle}deg)`,
            transformStyle: "preserve-3d",
          }}
        />

        {/* Ring 3 (Deep Purple) */}
        <div
          style={{
            position: "absolute",
            width: 180,
            height: 180,
            borderRadius: "50%",
            border: "2.5px dotted #9D4EDD",
            boxShadow: "0 0 14px rgba(157, 78, 221, 0.5)",
            transform: `rotateX(45deg) rotateY(45deg) rotateZ(${ring3Angle}deg)`,
            transformStyle: "preserve-3d",
          }}
        />

        {/* Swirling Vortex Dust Particles */}
        <svg
          style={{ position: "absolute", width: "100%", height: "100%", pointerEvents: "none" }}
          viewBox="0 0 340 340"
        >
          {Array.from({ length: 24 }).map((_, p) => {
            const angle = ((p * 15 + frame * 3) * Math.PI) / 180;
            const radius = 40 + ((p * 10 + frame * 2) % 120);
            const cx = 170 + Math.cos(angle) * radius;
            const cy = 170 + Math.sin(angle) * (radius * 0.7);

            return (
              <circle
                key={p}
                cx={cx}
                cy={cy}
                r="2.5"
                fill="#FF2A85"
                filter="drop-shadow(0 0 6px #FF2A85)"
              />
            );
          })}
        </svg>

        {/* Center Giant Holographic 3D Question Glyph */}
        <div
          style={{
            fontSize: 100,
            fontWeight: 900,
            color: "#FFFFFF",
            textShadow: "0 0 30px #FF2A85, 0 0 60px #7B2CBF",
            zIndex: 10,
            transform: `rotateY(${Math.sin(frame * 0.05) * 20}deg)`,
          }}
        >
          ?
        </div>
      </div>

      {/* Kinetic Climax Typography */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 6,
          zIndex: 12,
        }}
      >
        <div
          style={{
            fontSize: 14,
            fontWeight: 900,
            color: "#FF2A85",
            letterSpacing: 2,
            textShadow: "0 0 16px #FF2A85",
          }}
        >
          THE ARCHITECTURAL PARADOX
        </div>
        <div
          style={{
            fontSize: 12,
            color: "#E0AAFF",
            backgroundColor: "rgba(18, 1, 32, 0.9)",
            border: "1px solid #7B2CBF",
            padding: "6px 20px",
            borderRadius: 8,
            boxShadow: "0 0 20px rgba(123, 44, 191, 0.4)",
          }}
        >
          WHY CANNOT OUR REASONING MACHINES REWIRE THEIR SILICON ANATOMY?
        </div>
      </div>
    </div>
  );
};
