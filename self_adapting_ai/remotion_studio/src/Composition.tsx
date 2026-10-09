import React from "react";
import { Series } from "remotion";
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

// Duration of each scene: 4,500 frames (150.0s @ 30fps) -> 45,000 frames total (25 minutes 0 seconds)
export const SCENE_DURATIONS = {
  Scene01: 4500,
  Scene02: 4500,
  Scene03: 4500,
  Scene04: 4500,
  Scene05: 4500,
  Scene06: 4500,
  Scene07: 4500,
  Scene08: 4500,
  Scene09: 4500,
  Scene10: 4500,
};

export const MasterclassFullTimeline: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene01}>
        <Scene01_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene02}>
        <Scene02_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene03}>
        <Scene03_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene04}>
        <Scene04_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene05}>
        <Scene05_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene06}>
        <Scene06_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene07}>
        <Scene07_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene08}>
        <Scene08_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene09}>
        <Scene09_Composition />
      </Series.Sequence>
      <Series.Sequence durationInFrames={SCENE_DURATIONS.Scene10}>
        <Scene10_Composition />
      </Series.Sequence>
    </Series>
  );
};
