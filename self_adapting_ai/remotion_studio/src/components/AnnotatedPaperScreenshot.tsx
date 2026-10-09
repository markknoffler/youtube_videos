import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface HighlightZone {
  topPercent: number;
  leftPercent: number;
  widthPercent: number;
  heightPercent: number;
  color?: string;
  noteText?: string;
  notePosition?: "top" | "bottom" | "right" | "left";
}

interface AnnotatedPaperScreenshotProps {
  imageSrc: string;
  title: string;
  authors: string;
  venue: string;
  arxivId?: string;
  highlights?: HighlightZone[];
  startFrame?: number;
  width?: number;
  height?: number;
}

export const AnnotatedPaperScreenshot: React.FC<AnnotatedPaperScreenshotProps> = ({
  imageSrc,
  title,
  authors,
  venue,
  arxivId,
  highlights = [],
  startFrame = 0,
  width = 620,
  height = 430,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({ frame: relFrame, fps, config: { damping: 14 } });

  // Fast scanning laser line across the document
  const laserY = (relFrame * 4) % (height - 60);

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        backgroundColor: "rgba(16, 2, 30, 0.9)",
        border: "2px solid #FF2A85",
        borderRadius: 14,
        boxShadow: "0 0 32px rgba(255, 42, 133, 0.35)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      {/* Top Paper Header Bar */}
      <div
        style={{
          padding: "10px 14px",
          backgroundColor: "rgba(25, 2, 45, 0.95)",
          borderBottom: "1px solid #7B2CBF",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              padding: "2px 6px",
              backgroundColor: "#FF2A85",
              color: "#FFFFFF",
              borderRadius: 4,
              fontSize: 9,
              fontWeight: 800,
            }}
          >
            PEER REVIEWED
          </span>
          <span style={{ fontSize: 11, fontWeight: 800, color: "#FFFFFF" }}>{title}</span>
        </div>
        <div style={{ fontSize: 9.5, color: "#C77DFF", display: "flex", gap: 10 }}>
          <span>{venue}</span>
          {arxivId && <span style={{ color: "#E0AAFF" }}>arXiv:{arxivId}</span>}
        </div>
      </div>

      {/* Main Document Viewport with Real Paper Screenshot */}
      <div
        style={{
          position: "relative",
          flex: 1,
          overflow: "hidden",
          backgroundColor: "#0B0116",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* Actual Paper Image */}
        <img
          src={imageSrc.startsWith("http") || imageSrc.startsWith("data:") ? imageSrc : staticFile(imageSrc)}
          alt={title}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            filter: "contrast(1.05) brightness(0.95)",
          }}
        />

        {/* Dynamic Scanning Laser Beam */}
        <div
          style={{
            position: "absolute",
            top: laserY,
            left: 0,
            right: 0,
            height: 2,
            background: "linear-gradient(90deg, transparent 0%, #FF2A85 50%, transparent 100%)",
            boxShadow: "0 0 10px #FF2A85, 0 0 20px #FF2A85",
            pointerEvents: "none",
          }}
        />

        {/* Animated Neon Highlighters & Human-Style Handwritten Annotations */}
        {highlights.map((h, idx) => {
          const highlightProgress = Math.min(
            1,
            Math.max(0, interpolate(relFrame, [15 + idx * 20, 35 + idx * 20], [0, 1]))
          );
          const color = h.color || "#FF2A85";

          return (
            <React.Fragment key={idx}>
              {/* Expanding Highlighter Box */}
              <div
                style={{
                  position: "absolute",
                  top: `${h.topPercent}%`,
                  left: `${h.leftPercent}%`,
                  width: `${h.widthPercent * highlightProgress}%`,
                  height: `${h.heightPercent}%`,
                  backgroundColor: `${color}44`,
                  borderBottom: `2px solid ${color}`,
                  boxShadow: `0 0 12px ${color}88`,
                  pointerEvents: "none",
                  transition: "width 0.1s linear",
                }}
              />

              {/* Fast Human Handwritten Note */}
              {h.noteText && highlightProgress > 0.5 && (
                <div
                  style={{
                    position: "absolute",
                    top: `${h.topPercent + (h.notePosition === "bottom" ? h.heightPercent + 2 : -12)}%`,
                    left: `${h.leftPercent + (h.notePosition === "right" ? h.widthPercent + 2 : 0)}%`,
                    fontFamily: "'Brush Script MT', 'Comic Sans MS', cursive, sans-serif",
                    fontSize: 16,
                    color: "#FFFFFF",
                    textShadow: `0 0 8px ${color}, 0 0 16px ${color}`,
                    backgroundColor: "rgba(20, 1, 35, 0.85)",
                    border: `1px solid ${color}`,
                    borderRadius: 6,
                    padding: "2px 8px",
                    transform: `rotate(${idx % 2 === 0 ? -3 : 3}deg) scale(${interpolate(highlightProgress, [0.5, 1], [0.8, 1])})`,
                    zIndex: 20,
                    whiteSpace: "nowrap",
                  }}
                >
                  ✍️ {h.noteText}
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Bottom Authorship Footer */}
      <div
        style={{
          padding: "6px 14px",
          backgroundColor: "rgba(15, 1, 28, 0.95)",
          borderTop: "1px dashed #7B2CBF",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 9,
          color: "#E0AAFF",
        }}
      >
        <span>AUTHORS: {authors}</span>
        <span style={{ color: "#FF2A85", fontWeight: 700 }}>EMPIRICAL LITERATURE VERIFICATION</span>
      </div>
    </div>
  );
};
