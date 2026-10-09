import React from "react";
import { useCurrentFrame } from "remotion";

interface TensorCube3DProps {
  size?: number;
  label?: string;
  speed?: number;
  color?: string;
  glowColor?: string;
  subLabel?: string;
}

export const TensorCube3D: React.FC<TensorCube3DProps> = ({
  size = 140,
  label = "TENSOR [d×d]",
  speed = 1,
  color = "#FF2A85",
  glowColor = "rgba(255, 42, 133, 0.4)",
  subLabel = "4096×4096",
}) => {
  const frame = useCurrentFrame();
  const half = size / 2;

  // 3D rotation angles
  const rotX = 25 + Math.sin(frame * 0.02 * speed) * 15;
  const rotY = (frame * 0.8 * speed) % 360;
  const rotZ = Math.sin(frame * 0.015 * speed) * 8;

  const faceStyle: React.CSSProperties = {
    position: "absolute",
    width: size,
    height: size,
    backgroundColor: "rgba(22, 2, 40, 0.6)",
    border: `1.5px solid ${color}`,
    boxShadow: `0 0 16px ${glowColor}, inset 0 0 14px ${glowColor}`,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontSize: size * 0.08,
    fontFamily: "'JetBrains Mono', monospace",
    color: "#FFFFFF",
    fontWeight: 700,
    boxSizing: "border-box",
    backfaceVisibility: "visible",
  };

  return (
    <div
      style={{
        width: size,
        height: size,
        perspective: 900,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: size,
          height: size,
          position: "relative",
          transformStyle: "preserve-3d",
          transform: `rotateX(${rotX}deg) rotateY(${rotY}deg) rotateZ(${rotZ}deg)`,
        }}
      >
        {/* Front Face */}
        <div style={{ ...faceStyle, transform: `translateZ(${half}px)` }}>
          <div style={{ fontSize: size * 0.09, color, textShadow: `0 0 8px ${color}` }}>{label}</div>
          <div style={{ fontSize: size * 0.065, color: "#C77DFF", marginTop: 4 }}>{subLabel}</div>
          {/* Internal matrix dots */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 6, marginTop: 8 }}>
            {Array.from({ length: 9 }).map((_, i) => (
              <div
                key={i}
                style={{
                  width: 4,
                  height: 4,
                  borderRadius: "50%",
                  backgroundColor: (frame + i * 5) % 30 < 15 ? color : "#7B2CBF",
                  boxShadow: `0 0 4px ${color}`,
                }}
              />
            ))}
          </div>
        </div>

        {/* Back Face */}
        <div style={{ ...faceStyle, transform: `rotateY(180deg) translateZ(${half}px)` }}>
          <span style={{ color: "#E0AAFF", fontSize: size * 0.07 }}>DIM: R^{size}</span>
        </div>

        {/* Right Face */}
        <div style={{ ...faceStyle, transform: `rotateY(90deg) translateZ(${half}px)` }}>
          <span style={{ color, fontSize: size * 0.07 }}>DENSE_TENSOR</span>
        </div>

        {/* Left Face */}
        <div style={{ ...faceStyle, transform: `rotateY(-90deg) translateZ(${half}px)` }}>
          <span style={{ color: "#C77DFF", fontSize: size * 0.07 }}>W_PARAM</span>
        </div>

        {/* Top Face */}
        <div style={{ ...faceStyle, transform: `rotateX(90deg) translateZ(${half}px)` }}>
          <div
            style={{
              width: "70%",
              height: "70%",
              border: `1px dashed ${color}`,
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: size * 0.06,
              color: "#FFFFFF",
            }}
          >
            ∇W
          </div>
        </div>

        {/* Bottom Face */}
        <div style={{ ...faceStyle, transform: `rotateX(-90deg) translateZ(${half}px)` }}>
          <span style={{ color: "#7B2CBF", fontSize: size * 0.06 }}>STATIC_LATTICE</span>
        </div>
      </div>
    </div>
  );
};
