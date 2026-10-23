import React from "react";
import { Composition } from "remotion";
import { MasterclassFullTimeline, SCENE_DURATIONS } from "./Composition";
import {
  Scene01_Composition,
  Scene02_Composition,
  Scene03_Composition,
  Scene04_Composition,
  Scene05_Composition,
  Scene06_Composition,
  Scene07_Composition,
  Scene08_Composition,
  Scene09_Composition,
  Scene10_Composition,
} from "./scenes/MasterScenes";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ================================================================== */}
      {/* 25-MINUTE FULL MASTERCLASSES (45,000 frames @ 30 FPS = 25:00.00)  */}
      {/* ================================================================== */}
      <Composition
        id="Masterclass-ClonedVoice"
        component={MasterclassFullTimeline}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={45000}
        fps={30}
        width={1280}
        height={720}
      />

      <Composition
        id="Masterclass-StandardVoice"
        component={MasterclassFullTimeline}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={45000}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Default legacy ID for backward compatibility */}
      <Composition
        id="Masterclass-25Min"
        component={MasterclassFullTimeline}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={45000}
        fps={30}
        width={1280}
        height={720}
      />

      {/* ================================================================== */}
      {/* INDIVIDUAL CHAPTER COMPOSITIONS (CLONED VOICE)                     */}
      {/* ================================================================== */}
      <Composition
        id="Chapter01-TheMonolith-Cloned"
        component={Scene01_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene01}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter02-TheBiologicalDream-Cloned"
        component={Scene02_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene02}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter03-SelfOrganizingHypothesis-Cloned"
        component={Scene03_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene03}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter04-TheParadox-Cloned"
        component={Scene04_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene04}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter05-Theorem1-RankCollapse-Cloned"
        component={Scene05_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene05}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter06-Theorem2-RoutingBounds-Cloned"
        component={Scene06_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene06}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter07-Theorem3-HardwareBarrier-Cloned"
        component={Scene07_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene07}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter08-EmpiricalBenchmarks-Cloned"
        component={Scene08_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene08}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter09-FrontierLabs-Cloned"
        component={Scene09_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene09}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter10-The10YearFrontier-Cloned"
        component={Scene10_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene10}
        fps={30}
        width={1280}
        height={720}
      />

      {/* ================================================================== */}
      {/* INDIVIDUAL CHAPTER COMPOSITIONS (STANDARD VOICE)                   */}
      {/* ================================================================== */}
      <Composition
        id="Chapter01-TheMonolith-Standard"
        component={Scene01_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene01}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter02-TheBiologicalDream-Standard"
        component={Scene02_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene02}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter03-SelfOrganizingHypothesis-Standard"
        component={Scene03_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene03}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter04-TheParadox-Standard"
        component={Scene04_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene04}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter05-Theorem1-RankCollapse-Standard"
        component={Scene05_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene05}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter06-Theorem2-RoutingBounds-Standard"
        component={Scene06_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene06}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter07-Theorem3-HardwareBarrier-Standard"
        component={Scene07_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene07}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter08-EmpiricalBenchmarks-Standard"
        component={Scene08_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene08}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter09-FrontierLabs-Standard"
        component={Scene09_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene09}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter10-The10YearFrontier-Standard"
        component={Scene10_Composition}
        defaultProps={{ voiceType: "standard" as const }}
        durationInFrames={SCENE_DURATIONS.Scene10}
        fps={30}
        width={1280}
        height={720}
      />

      {/* ================================================================== */}
      {/* LEGACY COMPOSITIONS (FOR BACKWARD COMPATIBILITY)                    */}
      {/* ================================================================== */}
      <Composition
        id="Chapter01-TheMonolith"
        component={Scene01_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene01}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter02-TheBiologicalDream"
        component={Scene02_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene02}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter03-SelfOrganizingHypothesis"
        component={Scene03_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene03}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter04-TheParadox"
        component={Scene04_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene04}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter05-Theorem1-RankCollapse"
        component={Scene05_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene05}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter06-Theorem2-RoutingBounds"
        component={Scene06_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene06}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter07-Theorem3-HardwareBarrier"
        component={Scene07_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene07}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter08-EmpiricalBenchmarks"
        component={Scene08_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene08}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter09-FrontierLabs"
        component={Scene09_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene09}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="Chapter10-The10YearFrontier"
        component={Scene10_Composition}
        defaultProps={{ voiceType: "cloned" as const }}
        durationInFrames={SCENE_DURATIONS.Scene10}
        fps={30}
        width={1280}
        height={720}
      />
    </>
  );
};
