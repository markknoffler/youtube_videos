import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface CodeTerminalProps {
  filename?: string;
  codeLines: string[];
  outputLines?: string[];
  typingSpeed?: number; // characters per frame
  startFrame?: number;
  width?: number | string;
  height?: number | string;
  showTelemetry?: boolean;
}

export const CodeTerminal: React.FC<CodeTerminalProps> = ({
  filename = "research_model.py",
  codeLines,
  outputLines = [],
  typingSpeed = 1.6,
  startFrame = 0,
  width = 620,
  height = 360,
  showTelemetry = true,
}) => {
  const frame = useCurrentFrame();
  const relFrame = Math.max(0, frame - startFrame);

  // Total characters across all lines
  const fullText = codeLines.join("\n");
  const totalChars = fullText.length;

  // Calculate visible characters based on frame
  const visibleCharCount = Math.min(
    totalChars,
    Math.floor(relFrame * typingSpeed)
  );

  const visibleText = fullText.slice(0, visibleCharCount);
  const currentLines = visibleText.split("\n");

  // Output reveals after code finishes typing
  const typingFinishedFrame = Math.ceil(totalChars / typingSpeed);
  const showOutput = relFrame > typingFinishedFrame;
  const outputProgress = interpolate(
    relFrame,
    [typingFinishedFrame, typingFinishedFrame + 40],
    [0, outputLines.length],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const visibleOutputLines = outputLines.slice(0, Math.floor(outputProgress));

  // Dynamic spinner for active execution
  const spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
  const spinnerChar = spinners[Math.floor(frame / 4) % spinners.length];

  // Dynamic GPU metrics
  const vramUsage = (72.4 + Math.sin(frame * 0.05) * 1.8).toFixed(1);
  const gpuPower = (345 + Math.sin(frame * 0.07) * 12).toFixed(0);

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "#120224",
        borderRadius: 14,
        border: "1.5px solid #9D4EDD",
        boxShadow: "0 12px 36px rgba(157, 78, 221, 0.25), 0 0 16px rgba(255, 42, 133, 0.15)",
        fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        backdropFilter: "blur(12px)",
        boxSizing: "border-box",
      }}
    >
      {/* Terminal Title Bar */}
      <div
        style={{
          height: 34,
          backgroundColor: "#1F0438",
          borderBottom: "1px solid #7B2CBF",
          display: "flex",
          alignItems: "center",
          padding: "0 14px",
          gap: 8,
          justifyContent: "space-between",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", gap: 7, alignItems: "center" }}>
          <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#FF5F56" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#FFBD2E" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#27C93F" }} />
        </div>
        <div style={{ fontSize: 12, color: "#E0AAFF", fontWeight: 600, letterSpacing: 0.5 }}>
          {filename}
        </div>
        <div style={{ fontSize: 10, color: "#9D4EDD", fontWeight: 500 }}>
          UTF-8 • Python 3.12
        </div>
      </div>

      {/* Code Editor Body */}
      <div
        style={{
          flex: 1,
          padding: "12px 14px",
          fontSize: 12.5,
          lineHeight: "1.5",
          color: "#FFFFFF",
          overflowY: "hidden",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          boxSizing: "border-box",
        }}
      >
        {currentLines.map((line, idx) => {
          // Syntax highlighting tokens
          const isComment = line.trim().startsWith("#");
          const isKeyword =
            line.includes("def ") ||
            line.includes("class ") ||
            line.includes("import ") ||
            line.includes("return ");

          let formattedLine: React.ReactNode = line;
          if (isComment) {
            formattedLine = <span style={{ color: "#8E7DBE", fontStyle: "italic" }}>{line}</span>;
          } else if (isKeyword) {
            formattedLine = (
              <span>
                {line.split(" ").map((word, wIdx) => {
                  const kw = ["import", "from", "class", "def", "return", "self", "torch", "nn"].includes(
                    word
                  );
                  return (
                    <span key={wIdx} style={{ color: kw ? "#FF2A85" : "#E0AAFF", fontWeight: kw ? 700 : 400 }}>
                      {word}{" "}
                    </span>
                  );
                })}
              </span>
            );
          } else {
            formattedLine = <span style={{ color: "#E0AAFF" }}>{line}</span>;
          }

          const isLastLine = idx === currentLines.length - 1;
          const showCursor = isLastLine && frame % 16 < 8;

          return (
            <div key={idx} style={{ display: "flex", gap: 10 }}>
              <span style={{ color: "#5A189A", minWidth: 20, textAlign: "right", userSelect: "none" }}>
                {idx + 1}
              </span>
              <span>
                {formattedLine}
                {showCursor && (
                  <span
                    style={{
                      display: "inline-block",
                      width: 7,
                      height: 14,
                      backgroundColor: "#FF2A85",
                      marginLeft: 2,
                      verticalAlign: "middle",
                      boxShadow: "0 0 8px #FF2A85",
                    }}
                  />
                )}
              </span>
            </div>
          );
        })}

        {/* Live Output Log */}
        {showOutput && visibleOutputLines.length > 0 && (
          <div
            style={{
              marginTop: 10,
              paddingTop: 8,
              borderTop: "1px dashed #7B2CBF",
              fontSize: 11,
              fontFamily: "monospace",
            }}
          >
            {visibleOutputLines.map((out, oIdx) => (
              <div
                key={oIdx}
                style={{
                  color: out.includes("ERROR")
                    ? "#FF2A85"
                    : out.includes("FAIL")
                    ? "#FF2A85"
                    : "#5AF78E",
                  margin: "2px 0",
                  display: "flex",
                  gap: 6,
                  alignItems: "center",
                }}
              >
                <span>{spinnerChar}</span>
                <span>{out}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Live Telemetry Footer */}
      {showTelemetry && (
        <div
          style={{
            height: 24,
            backgroundColor: "#0D0218",
            borderTop: "1px solid #3C096C",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 12px",
            fontSize: 9.5,
            color: "#C77DFF",
            flexShrink: 0,
          }}
        >
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", backgroundColor: "#5AF78E", boxShadow: "0 0 6px #5AF78E" }} />
            <span>GPU 0: NVIDIA H100 SXM5</span>
          </div>
          <div style={{ display: "flex", gap: 12 }}>
            <span>PWR: {gpuPower}W</span>
            <span>VRAM: {vramUsage}/80GB (90.5%)</span>
            <span>UTIL: 96%</span>
          </div>
        </div>
      )}
    </div>
  );
};
