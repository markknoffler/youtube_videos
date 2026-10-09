import React from "react";
import { Img, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface HolographicAssetWindowProps {
  src: string;
  title: string;
  authorBadge: string;
  highlightText?: string;
  x: number;
  y: number;
  width: number;
  height: number;
  colorTheme?: "cyan" | "magenta" | "green" | "yellow" | "purple";
  enterFrame?: number;
}

export const HolographicAssetWindow: React.FC<HolographicAssetWindowProps> = ({
  src,
  title,
  authorBadge,
  highlightText,
  x,
  y,
  width,
  height,
  colorTheme = "cyan",
  enterFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring
  const relFrame = Math.max(0, frame - enterFrame);
  const scale = spring({
    frame: relFrame,
    fps,
    config: { damping: 15, mass: 0.8 },
    from: 0.85,
    to: 1.0,
  });
  const opacity = interpolate(relFrame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const themeColors = {
    cyan: { primary: "#00F0FF", glow: "rgba(0, 240, 255, 0.25)", border: "rgba(0, 240, 255, 0.5)" },
    magenta: { primary: "#FF2A85", glow: "rgba(255, 42, 133, 0.25)", border: "rgba(255, 42, 133, 0.5)" },
    green: { primary: "#5AF78E", glow: "rgba(90, 247, 142, 0.25)", border: "rgba(90, 247, 142, 0.5)" },
    yellow: { primary: "#FFE600", glow: "rgba(255, 230, 0, 0.25)", border: "rgba(255, 230, 0, 0.5)" },
    purple: { primary: "#C77DFF", glow: "rgba(199, 125, 255, 0.25)", border: "rgba(199, 125, 255, 0.5)" },
  };

  const currentTheme = themeColors[colorTheme];

  if (opacity <= 0.01) return null;

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        height,
        transform: `scale(${scale})`,
        opacity,
        zIndex: 40,
        pointerEvents: "none",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      {/* Container Box */}
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "rgba(8, 3, 22, 0.88)",
          border: `1px solid ${currentTheme.border}`,
          borderRadius: 8,
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          boxShadow: `0 8px 32px ${currentTheme.glow}`,
          backdropFilter: "blur(12px)",
        }}
      >
        {/* Holographic Header Bar */}
        <div
          style={{
            padding: "5px 10px",
            backgroundColor: "rgba(20, 10, 40, 0.95)",
            borderBottom: `1px solid ${currentTheme.border}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <div
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                backgroundColor: currentTheme.primary,
                boxShadow: `0 0 6px ${currentTheme.primary}`,
              }}
            />
            <span
              style={{
                color: "#FFFFFF",
                fontSize: 10,
                fontWeight: 900,
                letterSpacing: 0.5,
                textTransform: "uppercase",
              }}
            >
              {title}
            </span>
          </div>

          <span
            style={{
              color: currentTheme.primary,
              fontSize: 9,
              fontWeight: 700,
              backgroundColor: "rgba(0, 0, 0, 0.4)",
              padding: "2px 6px",
              borderRadius: 3,
              border: `1px solid ${currentTheme.primary}44`,
            }}
          >
            {authorBadge}
          </span>
        </div>

        {/* Media Preview Area */}
        <div
          style={{
            flex: 1,
            position: "relative",
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "#030108",
          }}
        >
          <Img
            src={src}
            style={{
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              opacity: 0.94,
            }}
          />

          {/* Holographic Scanline Overlay */}
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.03) 50%, transparent 50%)",
              backgroundSize: "100% 4px",
              pointerEvents: "none",
            }}
          />

          {/* Highlight Badge */}
          {highlightText && (
            <div
              style={{
                position: "absolute",
                bottom: 8,
                left: 8,
                right: 8,
                backgroundColor: "rgba(0, 0, 0, 0.85)",
                border: `1px solid ${currentTheme.primary}`,
                borderRadius: 4,
                padding: "3px 8px",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <div
                style={{
                  width: 5,
                  height: 5,
                  borderRadius: "50%",
                  backgroundColor: currentTheme.primary,
                }}
              />
              <span
                style={{
                  color: "#FFFFFF",
                  fontSize: 9.5,
                  fontWeight: 800,
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {highlightText}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
