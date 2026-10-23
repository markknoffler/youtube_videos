import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";
import { CyberSubtitles } from "../components/CyberSubtitles";

// The 10 Bespoke 3D Pedagogical Mathematical Blackboards
import { Scene01_MonolithBlackboard } from "../components/Scene01_MonolithBlackboard";
import { Scene02_BiologicalBlackboard } from "../components/Scene02_BiologicalBlackboard";
import { Scene03_SelfOrganizingBlackboard } from "../components/Scene03_SelfOrganizingBlackboard";
import { Scene04_ParadoxBlackboard } from "../components/Scene04_ParadoxBlackboard";
import { Scene05_Theorem1Blackboard } from "../components/Scene05_Theorem1Blackboard";
import { Scene06_Theorem2Blackboard } from "../components/Scene06_Theorem2Blackboard";
import { Scene07_Theorem3Blackboard } from "../components/Scene07_Theorem3Blackboard";
import { Scene08_BenchmarkBlackboard } from "../components/Scene08_BenchmarkBlackboard";
import { Scene09_FrontierBlackboard } from "../components/Scene09_FrontierBlackboard";
import { Scene10_SynthesisBlackboard } from "../components/Scene10_SynthesisBlackboard";

export interface SceneProps {
  voiceType?: "cloned" | "standard";
}

// ==============================================================================
// 10 CONTINUOUS 3D PEDAGOGICAL MASTERCLASS CHAPTERS (BESPOKE MATHEMATICAL BLACKBOARDS)
// Supports Dual-Audio Pipeline: 'cloned' (User's Voice) & 'standard' (Studio Deep Voice)
// ==============================================================================

export const Scene01_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene01_TheMonolith_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene01_MonolithBlackboard />
    <CyberSubtitles sceneKey="Scene01" />
  </AbsoluteFill>
);

export const Scene02_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene02_TheBiologicalDream_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene02_BiologicalBlackboard />
    <CyberSubtitles sceneKey="Scene02" />
  </AbsoluteFill>
);

export const Scene03_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene03_TheSelfOrganizingHypothesis_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene03_SelfOrganizingBlackboard />
    <CyberSubtitles sceneKey="Scene03" />
  </AbsoluteFill>
);

export const Scene04_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene04_TheParadox_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene04_ParadoxBlackboard />
    <CyberSubtitles sceneKey="Scene04" />
  </AbsoluteFill>
);

export const Scene05_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene05_Theorem1_RankCollapse_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene05_Theorem1Blackboard />
    <CyberSubtitles sceneKey="Scene05" />
  </AbsoluteFill>
);

export const Scene06_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene06_Theorem2_RoutingBounds_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene06_Theorem2Blackboard />
    <CyberSubtitles sceneKey="Scene06" />
  </AbsoluteFill>
);

export const Scene07_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene07_Theorem3_HardwareBarrier_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene07_Theorem3Blackboard />
    <CyberSubtitles sceneKey="Scene07" />
  </AbsoluteFill>
);

export const Scene08_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene08_EmpiricalBenchmarks_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene08_BenchmarkBlackboard />
    <CyberSubtitles sceneKey="Scene08" />
  </AbsoluteFill>
);

export const Scene09_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene09_FrontierLabs_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene09_FrontierBlackboard />
    <CyberSubtitles sceneKey="Scene09" />
  </AbsoluteFill>
);

export const Scene10_Composition: React.FC<SceneProps> = ({ voiceType = "cloned" }) => (
  <AbsoluteFill style={{ backgroundColor: "#06010F" }}>
    <Audio src={staticFile(`audio_${voiceType}/Scene10_The10YearFrontier_${voiceType}.wav`)} />
    <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.035} loop />
    <Scene10_SynthesisBlackboard />
    <CyberSubtitles sceneKey="Scene10" />
  </AbsoluteFill>
);
