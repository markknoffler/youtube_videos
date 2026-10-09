import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface ResearcherPortraitCardProps {
  name: string;
  role: string;
  institution: string;
  photoSrc?: string;
  logoSrc?: string;
  quote?: string;
  highlightText?: string;
  startFrame?: number;
  width?: number;
}

export const ResearcherPortraitCard: React.FC<ResearcherPortraitCardProps> = ({
  name,
  role,
  institution,
  photoSrc = "assets/real_world/researchers/demis_hassabis.jpg",
  logoSrc,
  quote,
  highlightText,
  startFrame = 0,
  width = 500,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const safePhotoSrc = photoSrc || "assets/real_world/researchers/demis_hassabis.jpg";

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({
    frame: relFrame,
    fps,
    config: { damping: 14, stiffness: 180 },
  });

  const borderPulse = interpolate(Math.sin(relFrame * 0.1), [-1, 1], [0.4, 0.9]);

  return (
    <div
      style={{
        width,
        backgroundColor: "rgba(14, 2, 28, 0.94)",
        border: `1.5px solid rgba(255, 42, 133, ${borderPulse})`,
        borderRadius: 14,
        padding: "16px 20px",
        boxShadow: "0 0 32px rgba(255, 42, 133, 0.35), 0 10px 30px rgba(0, 0, 0, 0.7)",
        display: "flex",
        flexDirection: "column",
        gap: 12,
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      {/* Header: Researcher Info & Portrait */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          {/* Portrait Circle */}
          <div
            style={{
              width: 58,
              height: 58,
              borderRadius: "50%",
              overflow: "hidden",
              border: "2px solid #FF2A85",
              boxShadow: "0 0 16px rgba(255, 42, 133, 0.7)",
              flexShrink: 0,
            }}
          >
            <img
              src={staticFile(safePhotoSrc)}
              alt={name}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
              }}
            />
          </div>

          <div>
            <div style={{ fontSize: 14, fontWeight: 900, color: "#FFFFFF" }}>{name}</div>
            <div style={{ fontSize: 9.5, color: "#C77DFF" }}>{role}</div>
            <div style={{ fontSize: 9, color: "#E0AAFF" }}>{institution}</div>
          </div>
        </div>

        {/* Company/Institution Logo */}
        {logoSrc && (
          <div
            style={{
              backgroundColor: "rgba(255, 255, 255, 0.96)",
              border: "1px solid rgba(255, 42, 133, 0.5)",
              borderRadius: 6,
              padding: "3px 8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: 28,
              boxShadow: "0 2px 8px rgba(0, 0, 0, 0.5)",
            }}
          >
            <img
              src={staticFile(logoSrc)}
              alt="Lab Logo"
              style={{
                height: 18,
                maxWidth: 64,
                objectFit: "contain",
              }}
            />
          </div>
        )}
      </div>

      {/* Kinetic Pull Quote */}
      {quote && (
        <div
          style={{
            position: "relative",
            backgroundColor: "rgba(25, 3, 45, 0.8)",
            borderLeft: "3px solid #5AF78E",
            borderRadius: "0 8px 8px 0",
            padding: "10px 14px",
            fontSize: 10.5,
            lineHeight: 1.45,
            color: "#E0AAFF",
            fontStyle: "italic",
          }}
        >
          <span style={{ color: "#5AF78E", fontWeight: 900, fontSize: 13, marginRight: 4 }}>"</span>
          {highlightText ? (
            <>
              {quote.split(highlightText)[0]}
              <span
                style={{
                  color: "#FF2A85",
                  fontWeight: 900,
                  backgroundColor: "rgba(255, 42, 133, 0.2)",
                  padding: "1px 4px",
                  borderRadius: 3,
                  boxShadow: "0 0 10px rgba(255, 42, 133, 0.4)",
                }}
              >
                {highlightText}
              </span>
              {quote.split(highlightText)[1]}
            </>
          ) : (
            quote
          )}
          <span style={{ color: "#5AF78E", fontWeight: 900, fontSize: 13, marginLeft: 4 }}>"</span>
        </div>
      )}

      {/* Scientific Authority Telemetry Footer */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 8.5,
          color: "#8E7DBE",
          borderTop: "1px dashed rgba(199, 125, 255, 0.25)",
          paddingTop: 6,
        }}
      >
        <span style={{ color: "#5AF78E" }}>● PRIMARY SCIENTIFIC CITATION</span>
        <span>PEER RECOGNITION ARCHIVE</span>
      </div>
    </div>
  );
};
