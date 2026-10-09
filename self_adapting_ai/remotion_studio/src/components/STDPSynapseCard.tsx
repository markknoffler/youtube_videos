import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const STDPSynapseCard: React.FC<{
  width?: number;
  height?: number;
  startFrame?: number;
}> = ({ width = 500, height = 420, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const entrance = spring({ frame: relFrame, fps, config: { damping: 14 } });

  // Delta t millisecond cycle (-40ms to +40ms)
  const deltaT = ((relFrame % 120) - 60) * 0.8;
  const isLTP = deltaT > 0;
  // Synaptic weight delta based on STDP exponential
  const deltaW = isLTP ? 0.85 * Math.exp(-deltaT / 15) : -0.65 * Math.exp(deltaT / 20);
  const cleftWidth = isLTP ? 14 + deltaW * 8 : 14;

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(18, 1, 32, 0.92)",
        border: "1.5px solid #FF2A85",
        borderRadius: 14,
        padding: "16px 18px",
        boxShadow: "0 0 28px rgba(255, 42, 133, 0.3)",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        alignItems: "center",
        transform: `scale(${entrance})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      <div style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, fontWeight: 900, color: "#FFFFFF" }}>SYNAPTIC CLEFT BIOMECHANICS</span>
        <span
          style={{
            fontSize: 8.5,
            color: isLTP ? "#5AF78E" : "#FF2A85",
            fontWeight: 800,
            border: `1px solid ${isLTP ? "#5AF78E" : "#FF2A85"}`,
            padding: "2px 6px",
            borderRadius: 4,
          }}
        >
          {isLTP ? "LTP POTENTIATION (+Δw)" : "LTD DEPRESSION (-Δw)"}
        </span>
      </div>

      {/* Synaptic Cleft Graphic */}
      <div
        style={{
          position: "relative",
          width: "100%",
          height: 240,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg style={{ width: "100%", height: "100%" }} viewBox="0 0 440 240">
          {/* Presynaptic Terminal */}
          <path
            d="M 20 50 Q 80 50 140 70 Q 180 90 190 120 Q 180 150 140 170 Q 80 190 20 190 Z"
            fill="rgba(123, 44, 191, 0.4)"
            stroke="#9D4EDD"
            strokeWidth="2"
          />
          {/* Postsynaptic Spine */}
          <path
            d={`M ${260 + cleftWidth} 60 Q ${230 + cleftWidth} 90 ${230 + cleftWidth} 120 Q ${230 + cleftWidth} 150 ${260 + cleftWidth} 180 L 420 180 L 420 60 Z`}
            fill="rgba(255, 42, 133, 0.3)"
            stroke="#FF2A85"
            strokeWidth="2"
          />

          {/* Neurotransmitter Vesicles traveling across cleft */}
          {Array.from({ length: 14 }).map((_, v) => {
            const vx = 160 + ((relFrame * 2 + v * 20) % (60 + cleftWidth));
            const vy = 90 + ((v * 17) % 60);
            return (
              <circle
                key={v}
                cx={vx}
                cy={vy}
                r="3.5"
                fill={isLTP ? "#5AF78E" : "#FF5EAA"}
                filter="drop-shadow(0 0 4px #5AF78E)"
              />
            );
          })}
        </svg>

        {/* Real-time Delta t Badge */}
        <div
          style={{
            position: "absolute",
            top: 6,
            backgroundColor: "#160128",
            border: "1px solid #7B2CBF",
            borderRadius: 6,
            padding: "4px 10px",
            fontSize: 9,
            color: "#E0AAFF",
          }}
        >
          SPIKE DELAY Δt = {deltaT > 0 ? `+${deltaT.toFixed(1)}` : deltaT.toFixed(1)} ms
        </div>
      </div>

      {/* Dynamic Weight Update Readout */}
      <div
        style={{
          width: "100%",
          backgroundColor: "#160128",
          padding: "8px 12px",
          borderRadius: 8,
          border: "1px solid #7B2CBF",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 10,
        }}
      >
        <span style={{ color: "#E0AAFF" }}>PLASTICITY RULE (STDP):</span>
        <span style={{ color: isLTP ? "#5AF78E" : "#FF2A85", fontWeight: 800 }}>
          Δw = {deltaW > 0 ? `+${deltaW.toFixed(3)}` : deltaW.toFixed(3)}
        </span>
      </div>
    </div>
  );
};
