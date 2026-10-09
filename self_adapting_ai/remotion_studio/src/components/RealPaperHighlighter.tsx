import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface HighlightBox {
  top: number; // percentage from top (e.g. 35)
  left: number; // percentage from left (e.g. 15)
  width: number; // percentage width (e.g. 70)
  height: number; // percentage height (e.g. 8)
  label?: string;
  color?: string;
  delayFrame?: number; // relative delay
}

interface RealPaperHighlighterProps {
  imageSrc?: string;
  title?: string;
  authors?: string;
  venue?: string;
  highlights?: HighlightBox[];
  startFrame?: number;
  width?: number;
  height?: number;
}

export const RealPaperHighlighter: React.FC<RealPaperHighlighterProps> = ({
  imageSrc = "assets/real_world/papers/paper_attention-01.png",
  title = "Attention Is All You Need",
  authors = "Vaswani et al.",
  venue = "NeurIPS 2017",
  highlights = [
    {
      top: 32,
      left: 12,
      width: 76,
      height: 7,
      label: "O(1) CONSTANT PATH LENGTH ATTENTION",
      color: "#FF2A85",
      delayFrame: 15,
    },
  ],
  startFrame = 0,
  width = 540,
  height = 420,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const safeImageSrc = imageSrc || "assets/real_world/papers/paper_attention-01.png";

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({
    frame: relFrame,
    fps,
    config: { damping: 15, stiffness: 180 },
  });

  const scanlineY = (relFrame * 2.5) % 100;

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(10, 1, 20, 0.95)",
        border: "1.5px solid #FF2A85",
        borderRadius: 12,
        boxShadow: "0 0 30px rgba(255, 42, 133, 0.35), 0 14px 40px rgba(0, 0, 0, 0.8)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        position: "relative",
        boxSizing: "border-box",
      }}
    >
      {/* Header Bar */}
      <div
        style={{
          padding: "7px 12px",
          backgroundColor: "rgba(22, 2, 40, 0.9)",
          borderBottom: "1px solid rgba(255, 42, 133, 0.35)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 3,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              padding: "2px 6px",
              backgroundColor: "#FF2A85",
              color: "#FFFFFF",
              borderRadius: 3,
              fontSize: 8.5,
              fontWeight: 900,
            }}
          >
            PEER-REVIEWED EVIDENCE
          </span>
          <span style={{ fontSize: 11, fontWeight: 800, color: "#FFFFFF", letterSpacing: 0.4 }}>
            {title}
          </span>
        </div>
        <span style={{ fontSize: 9, color: "#C77DFF" }}>{venue}</span>
      </div>

      {/* Authors Citation Subtitle */}
      <div
        style={{
          padding: "3px 12px",
          backgroundColor: "rgba(15, 1, 30, 0.7)",
          borderBottom: "1px solid rgba(199, 125, 255, 0.15)",
          fontSize: 8.5,
          color: "#8E7DBE",
          zIndex: 3,
        }}
      >
        {authors}
      </div>

      {/* Main Paper Viewport */}
      <div
        style={{
          position: "relative",
          flex: 1,
          overflow: "hidden",
          backgroundColor: "#0d021a",
        }}
      >
        {/* Actual High-Res Paper Document Image */}
        <img
          src={staticFile(safeImageSrc)}
          alt={title}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            objectPosition: "top center",
            filter: "contrast(1.08) brightness(0.96)",
          }}
        />

        {/* Animated Laser Scanline */}
        <div
          style={{
            position: "absolute",
            top: `${scanlineY}%`,
            left: 0,
            right: 0,
            height: 2,
            background: "linear-gradient(90deg, transparent, #FF2A85, #00F0FF, transparent)",
            boxShadow: "0 0 12px #FF2A85",
            pointerEvents: "none",
            opacity: 0.6,
          }}
        />

        {/* Dynamic SVG Highlighter Overlays */}
        {highlights.map((h, i) => {
          const delay = h.delayFrame || 10 * (i + 1);
          const hFrame = Math.max(0, relFrame - delay);

          const widthProgress = interpolate(hFrame, [0, 25], [0, 100], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          const glowColor = h.color || (i % 2 === 0 ? "#FF2A85" : "#00F0FF");

          if (hFrame <= 0) return null;

          return (
            <div
              key={i}
              style={{
                position: "absolute",
                top: `${h.top}%`,
                left: `${h.left}%`,
                width: `${h.width}%`,
                height: `${h.height}%`,
                pointerEvents: "none",
              }}
            >
              <div
                style={{
                  width: `${widthProgress}%`,
                  height: "100%",
                  backgroundColor: `${glowColor}33`,
                  border: `1.5px solid ${glowColor}`,
                  borderRadius: 3,
                  boxShadow: `0 0 16px ${glowColor}88, inset 0 0 8px ${glowColor}44`,
                  boxSizing: "border-box",
                  transition: "width 0.1s linear",
                }}
              />

              {h.label && widthProgress > 80 && (
                <div
                  style={{
                    position: "absolute",
                    top: -18,
                    left: 0,
                    backgroundColor: glowColor,
                    color: "#000000",
                    fontSize: 8,
                    fontWeight: 900,
                    padding: "1px 5px",
                    borderRadius: 3,
                    letterSpacing: 0.6,
                    whiteSpace: "nowrap",
                    boxShadow: `0 0 8px ${glowColor}`,
                  }}
                >
                  {h.label}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer Status Bar */}
      <div
        style={{
          padding: "4px 12px",
          backgroundColor: "rgba(18, 2, 34, 0.95)",
          borderTop: "1px solid rgba(255, 42, 133, 0.25)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 8.5,
          color: "#E0AAFF",
        }}
      >
        <span style={{ color: "#5AF78E" }}>● VERIFIED CITATION ARCHIVE</span>
        <span>LATENT EMBEDDING: SECTION 3.2</span>
      </div>
    </div>
  );
};
