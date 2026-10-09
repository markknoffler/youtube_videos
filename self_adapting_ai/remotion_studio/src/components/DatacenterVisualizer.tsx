import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface DatacenterVisualizerProps {
  imageSrc?: string;
  title?: string;
  facility?: string;
  powerMW?: number;
  flopTera?: number;
  gpuCount?: string;
  powerDraw?: string;
  bandwidth?: string;
  supercomputerName?: string;
  startFrame?: number;
  width?: number;
  height?: number;
}

export const DatacenterVisualizer: React.FC<DatacenterVisualizerProps> = ({
  imageSrc = "assets/real_world/datacenters/datacenter_supercomputer.jpg",
  title = "NVIDIA DGX SUPERPOD",
  facility = "Frontier Training Cluster",
  powerMW = 42.8,
  flopTera = 45000,
  supercomputerName,
  gpuCount = "32,768 H100 SXM5",
  powerDraw,
  startFrame = 0,
  width = 540,
  height = 420,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const displayTitle = supercomputerName || title;

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({
    frame: relFrame,
    fps,
    config: { damping: 15, stiffness: 180 },
  });

  const livePower = (powerMW + Math.sin(frame * 0.1) * 2.3).toFixed(1);
  const liveFlops = (flopTera + Math.cos(frame * 0.15) * 14.2).toFixed(0);
  const thermalProgress = interpolate(Math.sin(frame * 0.08), [-1, 1], [62, 74]);

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(12, 2, 24, 0.95)",
        border: "1.5px solid #FF2A85",
        borderRadius: 12,
        boxShadow: "0 0 28px rgba(255, 42, 133, 0.35), 0 12px 35px rgba(0, 0, 0, 0.8)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        position: "relative",
        boxSizing: "border-box",
      }}
    >
      {/* Top Header */}
      <div
        style={{
          padding: "7px 12px",
          backgroundColor: "rgba(25, 3, 45, 0.85)",
          borderBottom: "1px solid rgba(255, 42, 133, 0.3)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 2,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
          <span
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              backgroundColor: "#5AF78E",
              boxShadow: "0 0 8px #5AF78E",
            }}
          />
          <span style={{ fontSize: 11, fontWeight: 800, color: "#FFFFFF", letterSpacing: 0.6 }}>
            {displayTitle}
          </span>
        </div>
        <span style={{ fontSize: 9.5, color: "#C77DFF" }}>{facility}</span>
      </div>

      {/* Main Image Container */}
      <div
        style={{
          flex: 1,
          position: "relative",
          overflow: "hidden",
          backgroundColor: "#05000A",
        }}
      >
        <img
          src={staticFile(imageSrc)}
          alt={displayTitle}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "contrast(1.1) brightness(0.85)",
          }}
        />

        {/* Ambient Dark Gradient */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "linear-gradient(to top, rgba(12, 2, 24, 0.95) 0%, rgba(12, 2, 24, 0.2) 50%, transparent 100%)",
            pointerEvents: "none",
          }}
        />

        {/* Overlaid Telemetry Overlay */}
        <div
          style={{
            position: "absolute",
            bottom: 8,
            left: 10,
            right: 10,
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 8,
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(15, 1, 30, 0.85)",
              border: "1px solid rgba(255, 42, 133, 0.4)",
              borderRadius: 6,
              padding: "4px 8px",
            }}
          >
            <div style={{ fontSize: 8.5, color: "#8E7DBE" }}>CLUSTER POWER</div>
            <div style={{ fontSize: 11.5, fontWeight: 900, color: "#FF2A85" }}>
              {powerDraw || `${livePower} MW`}
            </div>
          </div>

          <div
            style={{
              backgroundColor: "rgba(15, 1, 30, 0.85)",
              border: "1px solid rgba(0, 240, 255, 0.4)",
              borderRadius: 6,
              padding: "4px 8px",
            }}
          >
            <div style={{ fontSize: 8.5, color: "#8E7DBE" }}>GPU ACCELERATORS</div>
            <div style={{ fontSize: 11.5, fontWeight: 900, color: "#00F0FF" }}>
              {gpuCount}
            </div>
          </div>

          <div
            style={{
              backgroundColor: "rgba(15, 1, 30, 0.85)",
              border: "1px solid rgba(90, 247, 142, 0.4)",
              borderRadius: 6,
              padding: "4px 8px",
            }}
          >
            <div style={{ fontSize: 8.5, color: "#8E7DBE" }}>FP8 GEMM TFLOPS</div>
            <div style={{ fontSize: 11.5, fontWeight: 900, color: "#5AF78E" }}>
              {liveFlops} TFLOPS
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Thermal / Load Bar */}
      <div
        style={{
          padding: "5px 12px",
          backgroundColor: "rgba(18, 2, 34, 0.95)",
          borderTop: "1px solid rgba(199, 125, 255, 0.2)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 9,
          color: "#E0AAFF",
        }}
      >
        <span>THERMAL LOAD: {thermalProgress.toFixed(0)}°C</span>
        <div
          style={{
            width: 140,
            height: 5,
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderRadius: 3,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${thermalProgress}%`,
              height: "100%",
              backgroundColor: thermalProgress > 70 ? "#FF2A85" : "#5AF78E",
            }}
          />
        </div>
        <span>COOLING: LIQUID COOLED SXM5</span>
      </div>
    </div>
  );
};
