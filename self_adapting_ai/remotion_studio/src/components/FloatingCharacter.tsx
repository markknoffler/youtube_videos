import React from "react";
import { interpolate, staticFile, useCurrentFrame } from "remotion";

interface FloatingCharacterProps {
  imageSrc: string;
  name: string;
  role: string;
  size?: number;
  flip?: boolean;
}

export const FloatingCharacter: React.FC<FloatingCharacterProps> = ({
  imageSrc,
  name,
  role,
  size = 280,
  flip = false,
}) => {
  const frame = useCurrentFrame();

  // Floating bobbing motion
  const bobbing = Math.sin(frame * 0.08) * 8;
  const rotation = Math.sin(frame * 0.04) * 1.5;

  // Holographic ring rotation
  const ringRotate = (frame * 1.2) % 360;

  // Scale in smoothly
  const scale = interpolate(frame, [0, 15], [0.95, 1], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [0, 5], [0.8, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "relative",
        width: size,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        transform: `translateY(${bobbing}px) rotate(${rotation}deg) scale(${scale}) ${flip ? "scaleX(-1)" : ""}`,
        opacity,
        transition: "transform 0.1s ease-out",
      }}
    >
      {/* Holographic Glowing Reticle Behind Avatar */}
      <div
        style={{
          position: "absolute",
          top: size * 0.1,
          width: size * 1.1,
          height: size * 1.1,
          borderRadius: "50%",
          border: "1.5px dashed rgba(255, 42, 133, 0.45)",
          boxShadow: "0 0 32px rgba(157, 78, 221, 0.3)",
          transform: `rotate(${ringRotate}deg)`,
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: size * 0.18,
          width: size * 0.95,
          height: size * 0.95,
          borderRadius: "50%",
          border: "1px solid rgba(199, 125, 255, 0.3)",
          transform: `rotate(${-ringRotate * 0.7}deg)`,
          pointerEvents: "none",
        }}
      />

      {/* Character Image in Rounded Container */}
      <div
        style={{
          width: size,
          height: size * 1.25,
          borderRadius: 20,
          overflow: "hidden",
          border: "2px solid #FF2A85",
          boxShadow: "0 0 30px rgba(255, 42, 133, 0.4), inset 0 0 20px rgba(123, 44, 191, 0.5)",
          backgroundColor: "#0D021A",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <img
          src={staticFile(imageSrc)}
          alt={name}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>

      {/* Character Nameplate Badge */}
      <div
        style={{
          marginTop: -16,
          zIndex: 2,
          backgroundColor: "#1D0433",
          border: "1.5px solid #C77DFF",
          borderRadius: 10,
          padding: "6px 14px",
          textAlign: "center",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.8)",
          transform: flip ? "scaleX(-1)" : "none",
        }}
      >
        <div style={{ fontSize: 13, fontWeight: 800, color: "#FFFFFF", letterSpacing: 0.5 }}>
          {name}
        </div>
        <div style={{ fontSize: 10, color: "#E0AAFF", fontWeight: 500 }}>
          {role}
        </div>
      </div>
    </div>
  );
};
