import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { TensorCube3D } from "./TensorCube3D";

export const Sentence2_ParadigmShift: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // STAGE TIMINGS
  // 0-60: "But the fundamental architecture..."
  // 60-120: "...has not actually changed."
  // 120-180: "We are simply scaling..."
  // 180-240: "...the same basic paradigm."

  // 1. Initial Monolith
  const monolithScale = spring({ frame: frame - 10, fps, config: { damping: 14 }, from: 0, to: 1 });
  
  // 2. Not actually changed - lock down overlay
  const lockOpacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: "clamp" });
  
  // 3. Scaling up - multiplier grid expands
  const scaleMult = spring({ frame: frame - 120, fps, config: { damping: 20 }, from: 1, to: 4 });
  const gridOpacity = interpolate(frame, [120, 150], [0, 0.8], { extrapolateRight: "clamp" });
  
  // 4. Same paradigm - bounding box locks
  const boxScale = spring({ frame: frame - 180, fps, config: { damping: 12 }, from: 2, to: 1 });
  const boxOpacity = interpolate(frame, [180, 200], [0, 1], { extrapolateRight: "clamp" });

  const cx = 410, cy = 260;

  return (
    <div style={{ position: "relative", width: 820, height: 520, fontFamily: "'JetBrains Mono', monospace", backgroundColor: "#020005" }}>
      
      {/* 3. SCALING GRID */}
      {frame > 120 && (
        <svg style={{ position: "absolute", width: "100%", height: "100%", opacity: gridOpacity }}>
          {Array.from({ length: 11 }).map((_, i) => (
             <line key={`v-${i}`} x1={cx + (i-5)*40*scaleMult} y1={0} x2={cx + (i-5)*40*scaleMult} y2={520} stroke="rgba(255,42,133,0.15)" strokeWidth="1" />
          ))}
          {Array.from({ length: 11 }).map((_, i) => (
             <line key={`h-${i}`} x1={0} y1={cy + (i-5)*40*scaleMult} x2={820} y2={cy + (i-5)*40*scaleMult} stroke="rgba(255,42,133,0.15)" strokeWidth="1" />
          ))}
        </svg>
      )}

      {/* 4. SAME PARADIGM BOUNDING BOX */}
      {frame > 180 && (
        <div style={{
          position: "absolute",
          left: cx - 180 * boxScale,
          top: cy - 140 * boxScale,
          width: 360 * boxScale,
          height: 280 * boxScale,
          border: "2px dashed #FF2A85",
          opacity: boxOpacity,
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-end",
          paddingBottom: 10
        }}>
           <div style={{ backgroundColor: "#FF2A85", color: "#FFF", padding: "2px 8px", fontSize: 14, fontWeight: 900 }}>PARADIGM LIMIT</div>
        </div>
      )}

      {/* 1. CENTRAL ARCHITECTURE */}
      <div style={{ position: "absolute", left: cx - 75, top: cy - 90, transform: `scale(${monolithScale})` }}>
        <TensorCube3D size={150} color="#9D4EDD" glowColor="rgba(157, 78, 221, 0.5)" speed={0.5} />
      </div>

      {/* 2. LOCK DOWN OVERLAY */}
      {frame > 60 && (
         <div style={{
            position: "absolute",
            left: cx - 40,
            top: cy - 20,
            opacity: lockOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center"
         }}>
            <svg width="80" height="40" viewBox="0 0 80 40">
               <rect x="30" y="10" width="20" height="20" fill="none" stroke="#FFF" strokeWidth="2" />
               <path d="M 35 10 V 5 C 35 0, 45 0, 45 5 V 10" fill="none" stroke="#FFF" strokeWidth="2" />
            </svg>
            <span style={{ color: "#FFF", fontSize: 12, fontWeight: "bold" }}>FROZEN</span>
         </div>
      )}
      
      {/* 3. SCALING METRIC */}
      {frame > 120 && (
         <div style={{ position: "absolute", left: cx + 100, top: cy + 100, color: "#FF2A85", fontSize: 32, fontWeight: 900 }}>
           {Math.floor(scaleMult * 100)}x
         </div>
      )}
    </div>
  );
};
