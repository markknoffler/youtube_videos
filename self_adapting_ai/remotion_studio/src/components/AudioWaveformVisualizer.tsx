import React from "react";
import { useCurrentFrame } from "remotion";

interface AudioWaveformVisualizerProps {
  barCount?: number;
  height?: number;
}

export const AudioWaveformVisualizer: React.FC<AudioWaveformVisualizerProps> = ({
  barCount = 48,
  height = 36,
}) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        gap: 3,
        height,
        padding: "0 10px",
        opacity: 0.85,
      }}
    >
      {Array.from({ length: barCount }).map((_, i) => {
        // Multi-frequency organic oscillation simulating audio spectrum
        const freq1 = Math.sin(frame * 0.15 + i * 0.35);
        const freq2 = Math.cos(frame * 0.08 + i * 0.6);
        const freq3 = Math.sin(frame * 0.22 + i * 0.15);
        const rawAmp = (freq1 + freq2 + freq3 + 3) / 6; // 0 to 1
        const barHeight = Math.max(4, Math.floor(rawAmp * height));

        // Color gradient from Hot Pink to Electric Lavender
        const ratio = i / barCount;
        const color = ratio < 0.5 ? "#FF2A85" : "#C77DFF";

        return (
          <div
            key={i}
            style={{
              width: 3,
              height: barHeight,
              backgroundColor: color,
              borderRadius: 2,
              boxShadow: `0 0 6px ${color}`,
              transition: "height 0.05s ease-out",
            }}
          />
        );
      })}
    </div>
  );
};
