import React from "react";
import { staticFile, useCurrentFrame } from "remotion";

interface PaperSpotlightProps {
  imageSrc: string;
  title: string;
  authors: string;
  year: string;
  keyFinding: string;
  arxivId?: string;
  width?: number;
}

export const PaperSpotlight: React.FC<PaperSpotlightProps> = ({
  imageSrc,
  title,
  authors,
  year,
  keyFinding,
  arxivId,
  width = 560,
}) => {
  const frame = useCurrentFrame();

  // Scanning laser beam across the paper screenshot
  const scanY = (frame * 1.5) % 180;

  // Subtle breathing glow
  const glow = 16 + Math.sin(frame * 0.08) * 8;

  return (
    <div
      style={{
        width,
        backgroundColor: "rgba(22, 3, 38, 0.85)",
        borderRadius: 14,
        border: "1.5px solid #FF2A85",
        boxShadow: `0 8px 32px rgba(255, 42, 133, 0.25), 0 0 ${glow}px rgba(199, 125, 255, 0.2)`,
        padding: "16px 18px",
        display: "flex",
        flexDirection: "column",
        gap: 12,
        backdropFilter: "blur(14px)",
        boxSizing: "border-box",
      }}
    >
      {/* Header with arXiv badge */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              padding: "3px 8px",
              backgroundColor: "#7B2CBF",
              color: "#FFFFFF",
              borderRadius: 4,
              fontSize: 10,
              fontWeight: 800,
              letterSpacing: 0.8,
            }}
          >
            SEMINAL RESEARCH
          </span>
          {arxivId && (
            <span style={{ fontSize: 11, color: "#C77DFF", fontFamily: "monospace" }}>
              arXiv:{arxivId}
            </span>
          )}
        </div>
        <span style={{ fontSize: 11, color: "#FF2A85", fontWeight: 700, fontFamily: "monospace" }}>
          {year}
        </span>
      </div>

      {/* Main Content: Screenshot + Text */}
      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        {/* Paper Screenshot with Laser Scan */}
        <div
          style={{
            position: "relative",
            width: 170,
            height: 105,
            borderRadius: 8,
            overflow: "hidden",
            border: "1.5px solid #9D4EDD",
            flexShrink: 0,
            boxShadow: "0 4px 16px rgba(0,0,0,0.5)",
          }}
        >
          <img
            src={staticFile(imageSrc)}
            alt={title}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
          {/* Animated Laser Scanning Line */}
          <div
            style={{
              position: "absolute",
              top: scanY,
              left: 0,
              right: 0,
              height: 2,
              backgroundColor: "#FF2A85",
              boxShadow: "0 0 8px #FF2A85, 0 0 16px #FF2A85",
            }}
          />
        </div>

        {/* Paper Details */}
        <div style={{ display: "flex", flexDirection: "column", gap: 4, flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#FFFFFF",
              lineHeight: 1.3,
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {title}
          </div>
          <div style={{ fontSize: 11, color: "#C77DFF", fontWeight: 500 }}>
            {authors}
          </div>
          <div
            style={{
              fontSize: 11.5,
              color: "#E0AAFF",
              lineHeight: 1.4,
              marginTop: 4,
              backgroundColor: "rgba(43, 6, 75, 0.6)",
              padding: "6px 10px",
              borderRadius: 6,
              borderLeft: "3px solid #FF2A85",
            }}
          >
            <b>Key Finding:</b> {keyFinding}
          </div>
        </div>
      </div>
    </div>
  );
};
