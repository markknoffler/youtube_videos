import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface BranchTarget {
  id: string;
  title: string;
  subtitle: string;
  value?: string;
  color: string;
  logoSrc?: string;
  badge?: string;
  highlightFrame?: number; // relative frame to highlight
}

interface ChalkboardVectorBranchProps {
  sourceTitle: string;
  sourceBadge?: string;
  targets: BranchTarget[];
  startFrame?: number;
  width?: number;
  height?: number;
  activeIndex?: number; // optionally force active branch
}

export const ChalkboardVectorBranch: React.FC<ChalkboardVectorBranchProps> = ({
  sourceTitle,
  sourceBadge = "ROOT PARADIGM",
  targets,
  startFrame = 0,
  width = 720,
  height = 420,
  activeIndex,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);

  // Entrance spring of source node
  const sourceEntrance = spring({
    frame: relFrame,
    fps,
    config: { damping: 14, stiffness: 180 },
  });

  // Source center coordinate
  const sourceX = 140;
  const sourceY = height / 2;

  // Compute active branch index based on time if not manually passed
  const autoActiveIndex =
    activeIndex !== undefined
      ? activeIndex
      : Math.floor(interpolate(relFrame, [30, 240], [0, targets.length], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }));

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        backgroundColor: "rgba(14, 2, 28, 0.94)",
        border: "1.5px solid #FF2A85",
        borderRadius: 14,
        boxShadow: "0 0 35px rgba(255, 42, 133, 0.35)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      {/* Background Chalkboard Grid Lines */}
      <svg
        style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}
        viewBox={`0 0 ${width} ${height}`}
      >
        <defs>
          <linearGradient id="vectorGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#FF2A85" />
            <stop offset="100%" stopColor="#5AF78E" />
          </linearGradient>
        </defs>

        {/* Faint coordinate grid lines */}
        {Array.from({ length: 9 }).map((_, i) => (
          <line
            key={`grid-x-${i}`}
            x1={i * 90}
            y1={0}
            x2={i * 90}
            y2={height}
            stroke="rgba(199, 125, 255, 0.08)"
            strokeWidth="1"
          />
        ))}
        {Array.from({ length: 6 }).map((_, j) => (
          <line
            key={`grid-y-${j}`}
            x1={0}
            y1={j * 75}
            x2={width}
            y2={j * 75}
            stroke="rgba(199, 125, 255, 0.08)"
            strokeWidth="1"
          />
        ))}

        {/* Vector conduits shooting from source to targets */}
        {targets.map((target, idx) => {
          const targetY =
            targets.length === 1
              ? height / 2
              : 60 + idx * ((height - 120) / (targets.length - 1));
          const targetX = width - 200;

          const branchDelay = idx * 15;
          const branchProgress = interpolate(
            relFrame,
            [branchDelay, branchDelay + 25],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          // Quadratic bezier curve from source to target
          const midX = (sourceX + targetX) / 2;
          const pathD = `M ${sourceX + 60} ${sourceY} Q ${midX} ${targetY} ${targetX - 10} ${targetY}`;

          const isActive = idx === autoActiveIndex || autoActiveIndex >= targets.length;

          return (
            <g key={target.id}>
              {/* Conduit Path with strokeDashoffset draw animation */}
              <path
                d={pathD}
                fill="none"
                stroke={isActive ? target.color : "rgba(199, 125, 255, 0.25)"}
                strokeWidth={isActive ? 3 : 1.5}
                strokeDasharray="400"
                strokeDashoffset={400 * (1 - branchProgress)}
                filter={isActive ? `drop-shadow(0 0 8px ${target.color})` : undefined}
              />

              {/* Traveling light particle along conduit */}
              {branchProgress > 0 && (
                <circle
                  cx={sourceX + 60 + (targetX - sourceX - 70) * ((relFrame * 0.03 + idx * 0.3) % 1)}
                  cy={sourceY + (targetY - sourceY) * ((relFrame * 0.03 + idx * 0.3) % 1)}
                  r={3.5}
                  fill={target.color}
                  filter={`drop-shadow(0 0 6px ${target.color})`}
                />
              )}
            </g>
          );
        })}
      </svg>

      {/* LEFT: Source Node */}
      <div
        style={{
          position: "absolute",
          left: sourceX - 70,
          top: sourceY - 50,
          width: 140,
          backgroundColor: "rgba(25, 3, 45, 0.95)",
          border: "2px solid #FF2A85",
          borderRadius: 10,
          padding: "10px 12px",
          textAlign: "center",
          boxShadow: "0 0 25px rgba(255, 42, 133, 0.5)",
          transform: `scale(${sourceEntrance})`,
          zIndex: 5,
        }}
      >
        <span
          style={{
            fontSize: 8,
            backgroundColor: "#FF2A85",
            color: "#FFFFFF",
            padding: "2px 6px",
            borderRadius: 3,
            fontWeight: 800,
            display: "inline-block",
            marginBottom: 6,
          }}
        >
          {sourceBadge}
        </span>
        <div style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF", lineHeight: 1.3 }}>
          {sourceTitle}
        </div>
      </div>

      {/* RIGHT: Blasting Target Nodes */}
      {targets.map((target, idx) => {
        const targetY =
          targets.length === 1
            ? height / 2
            : 60 + idx * ((height - 120) / (targets.length - 1));
        const targetX = width - 200;

        const branchDelay = idx * 15;
        const targetScale = spring({
          frame: Math.max(0, relFrame - branchDelay - 10),
          fps,
          config: { damping: 14, stiffness: 200 },
        });

        const isActive = idx === autoActiveIndex || autoActiveIndex >= targets.length;

        return (
          <div
            key={target.id}
            style={{
              position: "absolute",
              left: targetX,
              top: targetY - 32,
              width: 175,
              backgroundColor: isActive ? "rgba(35, 4, 65, 0.98)" : "rgba(18, 2, 32, 0.85)",
              border: `1.5px solid ${isActive ? target.color : "rgba(199, 125, 255, 0.3)"}`,
              borderRadius: 8,
              padding: "7px 10px",
              boxShadow: isActive ? `0 0 20px ${target.color}66` : "none",
              transform: `scale(${targetScale})`,
              display: "flex",
              alignItems: "center",
              gap: 8,
              zIndex: 5,
              boxSizing: "border-box",
            }}
          >
            {target.logoSrc && (
              <div
                style={{
                  width: 28,
                  height: 28,
                  backgroundColor: "#FFFFFF",
                  borderRadius: 4,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                  padding: 2,
                }}
              >
                <img
                  src={staticFile(target.logoSrc)}
                  alt={target.title}
                  style={{ maxHeight: 22, maxWidth: 24, objectFit: "contain" }}
                />
              </div>
            )}

            <div style={{ minWidth: 0, flex: 1 }}>
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 900,
                  color: isActive ? "#FFFFFF" : "#E0AAFF",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {target.title}
              </div>
              <div
                style={{
                  fontSize: 8,
                  color: isActive ? target.color : "#9D4EDD",
                  fontWeight: 700,
                }}
              >
                {target.subtitle}
              </div>
              {target.value && (
                <div style={{ fontSize: 7.5, color: "#5AF78E", fontWeight: 800 }}>
                  {target.value}
                </div>
              )}
            </div>
          </div>
        );
      })}

      {/* Top Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 8,
          left: 12,
          right: 12,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 8.5,
          color: "#E0AAFF",
          borderBottom: "1px solid rgba(199, 125, 255, 0.2)",
          paddingBottom: 4,
        }}
      >
        <span>VECTOR DIVERGENCE MANIFOLD</span>
        <span style={{ color: "#5AF78E", fontWeight: 800 }}>● DYNAMIC BRANCHING ACTIVE</span>
      </div>
    </div>
  );
};
