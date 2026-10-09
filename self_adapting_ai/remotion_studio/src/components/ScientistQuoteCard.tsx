import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface ScientistQuoteCardProps {
  scientistName: string;
  role: string;
  institution: string;
  avatarSrc?: string;
  quoteText: string;
  highlightPhrase?: string;
  startFrame?: number;
  width?: number;
}

export const ScientistQuoteCard: React.FC<ScientistQuoteCardProps> = ({
  scientistName,
  role,
  institution,
  avatarSrc,
  quoteText,
  highlightPhrase,
  startFrame = 0,
  width = 620,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({ frame: relFrame, fps, config: { damping: 14 } });

  return (
    <div
      style={{
        width,
        backgroundColor: "rgba(18, 1, 32, 0.9)",
        border: "2px solid #C77DFF",
        borderRadius: 14,
        padding: "16px 20px",
        boxShadow: "0 0 30px rgba(199, 125, 255, 0.35)",
        display: "flex",
        flexDirection: "column",
        gap: 12,
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      {/* Top Scientist Profile Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {avatarSrc ? (
            <img
              src={avatarSrc}
              alt={scientistName}
              style={{
                width: 48,
                height: 48,
                borderRadius: "50%",
                border: "2px solid #FF2A85",
                boxShadow: "0 0 10px #FF2A85",
                objectFit: "cover",
              }}
            />
          ) : (
            <div
              style={{
                width: 44,
                height: 44,
                borderRadius: "50%",
                backgroundColor: "#2B0145",
                border: "2px solid #FF2A85",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 18,
                color: "#FFFFFF",
                fontWeight: 900,
              }}
            >
              {scientistName.charAt(0)}
            </div>
          )}
          <div>
            <div style={{ fontSize: 13, fontWeight: 900, color: "#FFFFFF" }}>{scientistName}</div>
            <div style={{ fontSize: 9.5, color: "#C77DFF" }}>{role}</div>
          </div>
        </div>

        {/* Institution Badge */}
        <div
          style={{
            padding: "4px 10px",
            backgroundColor: "#200133",
            border: "1px solid #FF2A85",
            borderRadius: 6,
            fontSize: 9.5,
            color: "#FF2A85",
            fontWeight: 800,
          }}
        >
          {institution}
        </div>
      </div>

      {/* Quote Body */}
      <div
        style={{
          position: "relative",
          backgroundColor: "rgba(10, 0, 18, 0.85)",
          borderLeft: "3px solid #FF2A85",
          padding: "10px 14px",
          borderRadius: "0 8px 8px 0",
          fontSize: 11.5,
          color: "#FFFFFF",
          lineHeight: 1.5,
        }}
      >
        <span style={{ fontSize: 18, color: "#FF2A85", fontWeight: 900, marginRight: 4 }}>“</span>
        {highlightPhrase ? (
          <>
            {quoteText.split(highlightPhrase)[0]}
            <span style={{ color: "#FF2A85", fontWeight: 900, textShadow: "0 0 8px #FF2A85" }}>
              {highlightPhrase}
            </span>
            {quoteText.split(highlightPhrase)[1]}
          </>
        ) : (
          quoteText
        )}
        <span style={{ fontSize: 18, color: "#FF2A85", fontWeight: 900, marginLeft: 4 }}>”</span>
      </div>

      {/* Footer Status */}
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 8.5, color: "#E0AAFF" }}>
        <span>FRONTIER COGNITIVE CONSENSUS</span>
        <span style={{ color: "#5AF78E" }}>● VERIFIED PRIMARY SOURCE</span>
      </div>
    </div>
  );
};
