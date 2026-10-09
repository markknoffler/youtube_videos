import React from "react";
import { spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface LogoItem {
  name: string;
  logoSrc?: string;
  logo?: string;
  model?: string;
  params?: string;
  metric?: string;
  color?: string;
}

interface CompanyLogoBannerProps {
  logos?: LogoItem[];
  startFrame?: number;
  width?: number;
  height?: number;
}

const DEFAULT_LOGOS: LogoItem[] = [
  { name: "OpenAI", logoSrc: "assets/real_world/logos/openai_logo.svg", model: "GPT-6 Astra", params: "Frontier MoE" },
  { name: "Anthropic", logoSrc: "assets/real_world/logos/anthropic_logo.svg", model: "Claude 5.5", params: "Transformer" },
  { name: "Google DeepMind", logoSrc: "assets/real_world/logos/google_deepmind_logo.png", model: "Gemini 4", params: "Multimodal" },
  { name: "Meta", logoSrc: "assets/real_world/logos/meta_logo.svg", model: "Llama 5", params: "Dense Foundation" },
  { name: "Frontier Reasoning", logoSrc: "assets/real_world/logos/openai_logo.svg", model: "Mythos", params: "Latent Reasoning" },
];

export const CompanyLogoBanner: React.FC<CompanyLogoBannerProps> = ({
  logos = DEFAULT_LOGOS,
  startFrame = 0,
  width = 680,
  height,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - startFrame);
  const scale = spring({
    frame: relFrame,
    fps,
    config: { damping: 14, stiffness: 190 },
  });

  const safeLogos = Array.isArray(logos) && logos.length > 0 ? logos : DEFAULT_LOGOS;

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(16, 2, 30, 0.92)",
        border: "1.5px solid #FF2A85",
        borderRadius: 12,
        padding: "12px 18px",
        boxShadow: "0 0 24px rgba(255, 42, 133, 0.3)",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        transform: `scale(${scale})`,
        fontFamily: "'JetBrains Mono', monospace",
        boxSizing: "border-box",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: 11, fontWeight: 800, color: "#FFFFFF" }}>
          FRONTIER AI LAB CONVERGENCE
        </div>
        <div style={{ fontSize: 9, color: "#5AF78E", fontWeight: 700 }}>
          ● UNIFIED MONOLITH PARADIGM
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, justifyContent: "space-around" }}>
        {safeLogos.map((item, idx) => {
          const itemSpring = spring({
            frame: Math.max(0, relFrame - idx * 6),
            fps,
            config: { damping: 12 },
          });

          const logoPath = item.logoSrc || item.logo || "assets/real_world/logos/openai_logo.svg";
          const modelText = item.model || item.name || "FRONTIER";
          const paramText = item.params || item.metric || "TRANSFORMER";

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 6,
                backgroundColor: "rgba(25, 3, 45, 0.8)",
                border: "1px solid rgba(199, 125, 255, 0.3)",
                borderRadius: 8,
                padding: "8px 12px",
                transform: `scale(${itemSpring})`,
                flex: 1,
              }}
            >
              <div
                style={{
                  height: 32,
                  width: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: "rgba(255, 255, 255, 0.96)",
                  borderRadius: 6,
                  padding: "3px 6px",
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.4)",
                  boxSizing: "border-box",
                }}
              >
                <img
                  src={staticFile(logoPath)}
                  alt={item.name}
                  style={{
                    maxHeight: 24,
                    maxWidth: 72,
                    objectFit: "contain",
                  }}
                />
              </div>

              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: 10, fontWeight: 800, color: "#FFFFFF" }}>{modelText}</div>
                <div style={{ fontSize: 8.5, color: "#FF2A85", fontWeight: 700 }}>{paramText}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
