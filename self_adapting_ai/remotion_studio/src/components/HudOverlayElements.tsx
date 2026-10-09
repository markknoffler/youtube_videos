import React from "react";
import { useCurrentFrame } from "remotion";

export const HudOverlayElements: React.FC = () => {
  const frame = useCurrentFrame();

  // Rotating radar angle
  const radarAngle = (frame * 2.5) % 360;
  // Streaming hex addresses
  const hexValues = [
    "0x7F01A4B0", "0x7F01A4C4", "0x7F01A4D8", "0x7F01A4EC",
    "0x8A12BC00", "0x8A12BC14", "0x8A12BC28", "0x8A12BC3C",
  ];
  const activeHexIndex = Math.floor(frame / 6) % hexValues.length;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 15,
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      {/* Corner Bracket Top-Left */}
      <svg
        style={{ position: "absolute", top: 18, left: 18, width: 36, height: 36 }}
        viewBox="0 0 36 36"
      >
        <path d="M 0 16 L 0 0 L 16 0" fill="none" stroke="#FF2A85" strokeWidth="2.5" />
        <circle cx="4" cy="4" r="2" fill="#FF2A85" />
      </svg>

      {/* Corner Bracket Top-Right */}
      <svg
        style={{ position: "absolute", top: 18, right: 18, width: 36, height: 36 }}
        viewBox="0 0 36 36"
      >
        <path d="M 20 0 L 36 0 L 36 16" fill="none" stroke="#FF2A85" strokeWidth="2.5" />
        <circle cx="32" cy="4" r="2" fill="#FF2A85" />
      </svg>

      {/* Corner Bracket Bottom-Left */}
      <svg
        style={{ position: "absolute", bottom: 18, left: 18, width: 36, height: 36 }}
        viewBox="0 0 36 36"
      >
        <path d="M 0 20 L 0 36 L 16 36" fill="none" stroke="#FF2A85" strokeWidth="2.5" />
        <circle cx="4" cy="32" r="2" fill="#FF2A85" />
      </svg>

      {/* Corner Bracket Bottom-Right */}
      <svg
        style={{ position: "absolute", bottom: 18, right: 18, width: 36, height: 36 }}
        viewBox="0 0 36 36"
      >
        <path d="M 20 36 L 36 36 L 36 20" fill="none" stroke="#FF2A85" strokeWidth="2.5" />
        <circle cx="32" cy="32" r="2" fill="#FF2A85" />
      </svg>

      {/* Top Left Live Telemetry Widget */}
      <div
        style={{
          position: "absolute",
          top: 66,
          left: 42,
          display: "flex",
          flexDirection: "column",
          gap: 3,
          backgroundColor: "rgba(18, 1, 32, 0.7)",
          border: "1px solid rgba(199, 125, 255, 0.25)",
          borderRadius: 6,
          padding: "6px 10px",
          backdropFilter: "blur(6px)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 9, color: "#C77DFF" }}>
          <span
            style={{
              width: 5,
              height: 5,
              borderRadius: "50%",
              backgroundColor: frame % 20 < 10 ? "#FF2A85" : "transparent",
            }}
          />
          <span>STREAM_ADDR: {hexValues[activeHexIndex]}</span>
        </div>
        <div style={{ fontSize: 8.5, color: "#E0AAFF", opacity: 0.8 }}>
          SYS_TICK: {String(frame).padStart(5, "0")} | LATENCY: {(1.12 + Math.sin(frame * 0.1) * 0.08).toFixed(2)}ms
        </div>
      </div>

      {/* Top Right Mini Radar Scope */}
      <div
        style={{
          position: "absolute",
          top: 66,
          right: 42,
          width: 54,
          height: 54,
          borderRadius: "50%",
          border: "1px solid rgba(255, 42, 133, 0.4)",
          backgroundColor: "rgba(15, 1, 28, 0.65)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        {/* Inner concentric ring */}
        <div
          style={{
            position: "absolute",
            width: 32,
            height: 32,
            borderRadius: "50%",
            border: "1px dashed rgba(199, 125, 255, 0.35)",
          }}
        />
        {/* Crosshairs */}
        <div style={{ position: "absolute", width: "100%", height: 1, backgroundColor: "rgba(199, 125, 255, 0.25)" }} />
        <div style={{ position: "absolute", height: "100%", width: 1, backgroundColor: "rgba(199, 125, 255, 0.25)" }} />
        {/* Rotating sweep */}
        <div
          style={{
            position: "absolute",
            width: "50%",
            height: 2,
            top: "50%",
            left: "50%",
            transformOrigin: "0 0",
            transform: `rotate(${radarAngle}deg)`,
            background: "linear-gradient(90deg, #FF2A85 0%, transparent 100%)",
            boxShadow: "0 0 6px #FF2A85",
          }}
        />
        {/* Blinking detected blip */}
        <div
          style={{
            position: "absolute",
            top: 14,
            right: 14,
            width: 3,
            height: 3,
            borderRadius: "50%",
            backgroundColor: "#FF2A85",
            boxShadow: "0 0 5px #FF2A85",
            opacity: frame % 30 < 15 ? 1 : 0.2,
          }}
        />
      </div>

      {/* Bottom Floating Coordinate Grid Markers */}
      <div
        style={{
          position: "absolute",
          bottom: 46,
          left: 42,
          display: "flex",
          gap: 16,
          fontSize: 8.5,
          color: "#9D4EDD",
          letterSpacing: 0.5,
        }}
      >
        <span>COORD: [{(Math.sin(frame * 0.02) * 12).toFixed(3)}, {(Math.cos(frame * 0.02) * 12).toFixed(3)}, +0.841]</span>
        <span>•</span>
        <span>MANIFOLD: DIM-4096</span>
        <span>•</span>
        <span style={{ color: "#FF2A85" }}>ENTROPY: {(1.412 + Math.sin(frame * 0.05) * 0.05).toFixed(3)} nats</span>
      </div>
    </div>
  );
};
