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
      {/* Complete 25-Minute Masterclass (45,000 frames @ 30 FPS = 25:00.00) */}
      <Composition
        id="Masterclass-25Min"
        component={MasterclassFullTimeline}
        durationInFrames={45000}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 01: The Monolith */}
      <Composition
        id="Chapter01-TheMonolith"
        component={Scene01_Composition}
        durationInFrames={SCENE_DURATIONS.Scene01}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 02: The Biological Dream */}
      <Composition
        id="Chapter02-TheBiologicalDream"
        component={Scene02_Composition}
        durationInFrames={SCENE_DURATIONS.Scene02}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 03: Self-Organizing Hypothesis */}
      <Composition
        id="Chapter03-SelfOrganizingHypothesis"
        component={Scene03_Composition}
        durationInFrames={SCENE_DURATIONS.Scene03}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 04: The Paradox */}
      <Composition
        id="Chapter04-TheParadox"
        component={Scene04_Composition}
        durationInFrames={SCENE_DURATIONS.Scene04}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 05: Theorem 1 Rank Collapse */}
      <Composition
        id="Chapter05-Theorem1-RankCollapse"
        component={Scene05_Composition}
        durationInFrames={SCENE_DURATIONS.Scene05}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 06: Theorem 2 Routing Bounds */}
      <Composition
        id="Chapter06-Theorem2-RoutingBounds"
        component={Scene06_Composition}
        durationInFrames={SCENE_DURATIONS.Scene06}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 07: Theorem 3 Hardware Barrier */}
      <Composition
        id="Chapter07-Theorem3-HardwareBarrier"
        component={Scene07_Composition}
        durationInFrames={SCENE_DURATIONS.Scene07}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 08: Empirical Benchmarks */}
      <Composition
        id="Chapter08-EmpiricalBenchmarks"
        component={Scene08_Composition}
        durationInFrames={SCENE_DURATIONS.Scene08}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 09: Frontier Labs */}
      <Composition
        id="Chapter09-FrontierLabs"
        component={Scene09_Composition}
        durationInFrames={SCENE_DURATIONS.Scene09}
        fps={30}
        width={1280}
        height={720}
      />

      {/* Chapter 10: The 10-Year Frontier */}
      <Composition
        id="Chapter10-The10YearFrontier"
        component={Scene10_Composition}
        durationInFrames={SCENE_DURATIONS.Scene10}
        fps={30}
        width={1280}
        height={720}
      />
    </>
  );
};
