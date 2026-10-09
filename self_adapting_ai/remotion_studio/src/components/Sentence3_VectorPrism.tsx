import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Sentence3_VectorPrism: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // "Instead of words, it sees vectors." (0-60)
  // "A word like 'king' becomes a coordinate..." (60-120)
  // "...and 'queen' is just a geometrical step away." (120-180)
  // "It is taking language and turning it into physics." (180-240)

  // Axes drawing
  const axisLength = spring({ frame: frame - 10, fps, config: { damping: 15 }, from: 0, to: 300 });
  const gridOpacity = interpolate(frame, [10, 40], [0, 0.3], { extrapolateRight: "clamp" });

  // Word 1: KING
  const kingAppear = frame > 60;
  const kingScale = spring({ frame: frame - 60, fps, config: { damping: 12 } });
  const kingVecLen = spring({ frame: frame - 70, fps, config: { damping: 12 }, from: 0, to: 1 });

  // Word 2: QUEEN
  const queenAppear = frame > 120;
  const queenScale = spring({ frame: frame - 120, fps, config: { damping: 12 } });
  const queenVecLen = spring({ frame: frame - 130, fps, config: { damping: 12 }, from: 0, to: 1 });

  // Vector subtraction step
  const stepProgression = spring({ frame: frame - 150, fps, config: { damping: 15 }, from: 0, to: 1 });

  // Physics grid pulse
  const pulseRadius = spring({ frame: frame - 180, fps, config: { damping: 20 }, from: 0, to: 500 });
  const physicsOpacity = interpolate(frame, [180, 200], [0, 1], { extrapolateRight: "clamp" });

  // Coordinates
  const cx = 410, cy = 400; // Origin (bottom center)
  const kx = 250, ky = 150; // King pos
  const qx = 550, ky_q = 150; // Queen pos

  return (
    <div style={{ position: "relative", width: 820, height: 520, fontFamily: "'JetBrains Mono', monospace", backgroundColor: "#05000A" }}>
      
      {/* 3D Coordinate Grid */}
      <svg style={{ position: "absolute", width: "100%", height: "100%", opacity: gridOpacity }}>
        <path d={`M ${cx} ${cy} L ${cx} ${cy - axisLength}`} stroke="#9D4EDD" strokeWidth="2" />
        <path d={`M ${cx} ${cy} L ${cx + axisLength * 0.8} ${cy - axisLength * 0.3}`} stroke="#9D4EDD" strokeWidth="2" />
        <path d={`M ${cx} ${cy} L ${cx - axisLength * 0.8} ${cy - axisLength * 0.3}`} stroke="#9D4EDD" strokeWidth="2" />
      </svg>

      {/* Physics Pulse */}
      {frame > 180 && (
         <svg style={{ position: "absolute", width: "100%", height: "100%", opacity: physicsOpacity }}>
           <circle cx={cx} cy={cy - 150} r={pulseRadius} fill="none" stroke="#FF2A85" strokeWidth="3" opacity="0.4" />
           <circle cx={cx} cy={cy - 150} r={pulseRadius * 0.8} fill="none" stroke="#FF2A85" strokeWidth="1" opacity="0.6" />
           <text x={cx} y={cy - 150} fill="#FF2A85" fontSize="32" fontWeight="900" textAnchor="middle" opacity="0.3">PHYSICS LATENT SPACE</text>
         </svg>
      )}

      {/* Vectors and Words */}
      <svg style={{ position: "absolute", width: "100%", height: "100%" }}>
        {kingAppear && (
          <g>
            <line x1={cx} y1={cy} x2={cx + (kx - cx) * kingVecLen} y2={cy + (ky - cy) * kingVecLen} stroke="#00F0FF" strokeWidth="4" />
            <circle cx={cx + (kx - cx) * kingVecLen} cy={cy + (ky - cy) * kingVecLen} r="6" fill="#00F0FF" />
          </g>
        )}
        
        {queenAppear && (
          <g>
            <line x1={cx} y1={cy} x2={cx + (qx - cx) * queenVecLen} y2={cy + (ky_q - cy) * queenVecLen} stroke="#FF0055" strokeWidth="4" />
            <circle cx={cx + (qx - cx) * queenVecLen} cy={cy + (ky_q - cy) * queenVecLen} r="6" fill="#FF0055" />
          </g>
        )}

        {/* The Geometrical Step */}
        {frame > 150 && (
          <g>
            <line x1={kx} y1={ky} x2={kx + (qx - kx) * stepProgression} y2={ky + (ky_q - ky) * stepProgression} stroke="#FFF" strokeWidth="3" strokeDasharray="6 6" />
            {stepProgression === 1 && (
              <polygon points={`${qx},${ky_q} ${qx-10},${ky_q-5} ${qx-10},${ky_q+5}`} fill="#FFF" />
            )}
            <text x={(kx + qx)/2} y={ky - 15} fill="#FFF" fontSize="14" opacity={stepProgression}>+ [ FEMALE ]</text>
          </g>
        )}
      </svg>

      {/* HTML Labels */}
      {kingAppear && (
        <div style={{ position: "absolute", left: kx - 40, top: ky - 40, transform: `scale(${kingScale})`, backgroundColor: "rgba(0, 240, 255, 0.1)", padding: "4px 8px", border: "1px solid #00F0FF", borderRadius: 4, color: "#00F0FF", fontSize: 14, fontWeight: "bold" }}>
          [KING]
        </div>
      )}
      
      {queenAppear && (
        <div style={{ position: "absolute", left: qx - 40, top: ky_q - 40, transform: `scale(${queenScale})`, backgroundColor: "rgba(255, 0, 85, 0.1)", padding: "4px 8px", border: "1px solid #FF0055", borderRadius: 4, color: "#FF0055", fontSize: 14, fontWeight: "bold" }}>
          [QUEEN]
        </div>
      )}
    </div>
  );
};
