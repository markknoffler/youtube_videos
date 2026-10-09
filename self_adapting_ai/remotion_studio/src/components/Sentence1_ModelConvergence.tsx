import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { TensorCube3D } from "./TensorCube3D";

export const Sentence1_ModelConvergence: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // STAGE TIMINGS (Narrative synchronization)
  // "Take a look at the landscape..." (0 - 60)
  // "...Whether it's OpenAI's GPT-4, Anthropic's Claude..." (60 - 120)
  // "...Google's Gemini, or open-source models like LLaMA and Mistral..." (120 - 180)
  // "...there's a strange uniformity." (180 - 240)
  
  // Grid sweeping radar effect
  const radarRadius = spring({ frame: frame - 10, fps, config: { damping: 20 }, from: 0, to: 400 });

  const models = [
    { name: "GPT-6 Astra", org: "OpenAI", logo: "assets/real_world/logos/openai_logo.svg", angle: -45, color: "#FF2A85", appearFrame: 65 },
    { name: "Claude 5.5", org: "Anthropic", logo: "assets/real_world/logos/anthropic_logo.svg", angle: 45, color: "#C77DFF", appearFrame: 90 },
    { name: "Gemini 4", org: "Google", logo: "assets/real_world/logos/google_logo.svg", angle: 135, color: "#9D4EDD", appearFrame: 125 },
    { name: "Llama 5", org: "Meta", logo: "assets/real_world/logos/meta_logo.svg", angle: 225, color: "#E0AAFF", appearFrame: 155 },
  ];

  const orbitRadius = 240;

  // Center monolith appears at "strange uniformity"
  const monolithScale = spring({ frame: frame - 180, fps, config: { mass: 1, damping: 12 }, from: 0, to: 1 });
  const convPercent = Math.min(100, Math.floor(interpolate(frame, [185, 230], [0, 100], { extrapolateRight: "clamp" })));

  return (
    <div
      style={{
        position: "relative",
        width: 820,
        height: 520,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      {/* Radar sweeping grid */}
      <svg style={{ position: "absolute", width: "100%", height: "100%", pointerEvents: "none" }} viewBox="0 0 820 520">
        <circle cx="410" cy="260" r={radarRadius} fill="none" stroke="rgba(255, 42, 133, 0.1)" strokeWidth="1" />
        <circle cx="410" cy="260" r={radarRadius * 0.7} fill="none" stroke="rgba(255, 42, 133, 0.2)" strokeWidth="1" />
        <circle cx="410" cy="260" r={radarRadius * 0.4} fill="none" stroke="rgba(255, 42, 133, 0.3)" strokeWidth="1" />
        <line x1="410" y1="0" x2="410" y2="520" stroke="rgba(199, 125, 255, 0.15)" strokeWidth="1" />
        <line x1="0" y1="260" x2="820" y2="260" stroke="rgba(199, 125, 255, 0.15)" strokeWidth="1" />
        
        {/* Connection lines drawn ONLY after center monolith appears */}
        {frame >= 180 && models.map((m) => {
          const mScale = spring({ frame: frame - m.appearFrame, fps, config: { damping: 12 } });
          const currentAngle = (m.angle * Math.PI) / 180;
          const x = 410 + Math.cos(currentAngle) * orbitRadius;
          const y = 260 + Math.sin(currentAngle) * (orbitRadius * 0.65);
          
          const lineProgression = interpolate(frame, [180, 200], [0, 1], { extrapolateRight: "clamp" });
          const lineX = x + (410 - x) * lineProgression;
          const lineY = y + (260 - y) * lineProgression;

          return (
            <g key={`line-${m.name}`}>
              <line x1={x} y1={y} x2={lineX} y2={lineY} stroke={m.color} strokeWidth="2" strokeOpacity="0.8" strokeDasharray="4 4" />
              {frame > 200 && (
                <circle cx={410 + (x - 410) * ((frame * 2 % 100) / 100)} cy={260 + (y - 260) * ((frame * 2 % 100) / 100)} r="3" fill="#FFF" filter={`drop-shadow(0 0 5px ${m.color})`} />
              )}
            </g>
          );
        })}
      </svg>

      {/* Orbiting Model Nodes */}
      {models.map((m) => {
        if (frame < m.appearFrame) return null;
        
        const mScale = spring({ frame: frame - m.appearFrame, fps, config: { damping: 14 } });
        const currentAngle = (m.angle * Math.PI) / 180;
        const x = 410 + Math.cos(currentAngle) * orbitRadius - 75;
        const y = 260 + Math.sin(currentAngle) * (orbitRadius * 0.65) - 40;

        return (
          <div
            key={m.name}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: 150,
              padding: "8px 12px",
              backgroundColor: "rgba(20, 2, 38, 0.95)",
              border: `1.5px solid ${m.color}`,
              borderRadius: 8,
              boxShadow: `0 0 15px ${m.color}66`,
              transform: `scale(${mScale})`,
              display: "flex",
              flexDirection: "column",
              gap: 4,
              zIndex: 10,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 11, fontWeight: 800, color: "#FFFFFF" }}>{m.name}</span>
            </div>
            <div style={{ fontSize: 9, color: m.color, fontWeight: 600 }}>{m.org}</div>
            
            {/* Engine tag appears only when uniformity is mentioned */}
            {frame > 185 && (
               <div style={{ fontSize: 8, color: "#FFF", backgroundColor: "#FF2A85", padding: "2px 4px", borderRadius: 3, marginTop: 4, width: "fit-content" }}>
                 TRANSFORMER
               </div>
            )}
          </div>
        );
      })}

      {/* Central Transformer Monolith Core */}
      {frame >= 180 && (
        <div style={{ zIndex: 12, display: "flex", flexDirection: "column", alignItems: "center", transform: `scale(${monolithScale})` }}>
          <TensorCube3D
            size={140}
            label="TRANSFORMER"
            subLabel="SHARED ENGINE"
            color="#FF2A85"
            glowColor="rgba(255, 42, 133, 0.8)"
            speed={1.5}
          />
          <div
            style={{
              marginTop: 18,
              backgroundColor: "rgba(15, 1, 30, 0.9)",
              border: "1.5px solid #FF2A85",
              borderRadius: 4,
              padding: "6px 12px",
              boxShadow: "0 0 15px rgba(255, 42, 133, 0.5)",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 10, color: "#FFF" }}>UNIFORMITY:</span>
            <span style={{ fontSize: 12, color: "#FF2A85", fontWeight: 900 }}>{convPercent}%</span>
          </div>
        </div>
      )}
    </div>
  );
};
