import React from "react";
import { AbsoluteFill, Audio, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ChoreographySentence } from "../types/choreography";
import choreographyData from "../data/MASTER_CHOREOGRAPHY_MAP.json";
import { FloatingDustParticles } from "./FloatingDustParticles";
import { AudioWaveformVisualizer } from "./AudioWaveformVisualizer";
import { CyberSubtitles } from "./CyberSubtitles";
import subtitleData from "../data/subtitles.json";

// Import all 3D pedagogical visualizers
import { ChalkboardVectorBranch } from "./ChalkboardVectorBranch";
import { TensorCube3D } from "./TensorCube3D";
import { CompanyLogoBanner } from "./CompanyLogoBanner";
import { DatacenterVisualizer } from "./DatacenterVisualizer";
import { ResearcherPortraitCard } from "./ResearcherPortraitCard";
import { RealPaperHighlighter } from "./RealPaperHighlighter";
import { CodeTerminal } from "./CodeTerminal";
import { MathFormulaCard } from "./MathFormulaCard";
import { BiologicalNeocortexCard } from "./BiologicalNeocortexCard";
import { STDPSynapseCard } from "./STDPSynapseCard";
import { SynapticNetwork } from "./SynapticNetwork";
import { AttentionHeatmap } from "./AttentionHeatmap";
import { AnimatedLossChart } from "./AnimatedLossChart";
import { SystolicHardwareGrid } from "./SystolicHardwareGrid";
import { MemristorCrossbar3D } from "./MemristorCrossbar3D";
import { EigenvalueCollapseBar } from "./EigenvalueCollapseBar";
import { LifelongMemoryPipeline } from "./LifelongMemoryPipeline";

interface MasterContinuousDirectorProps {
  chapterNum: number;
  chapterTitle: string;
  chapterSubtitle: string;
  sceneKey: keyof typeof subtitleData;
  audioFile: string;
}

const allSentences = (choreographyData as { sentences: ChoreographySentence[] }).sentences;

export const MasterContinuousDirector: React.FC<MasterContinuousDirectorProps> = ({
  chapterNum,
  chapterTitle,
  chapterSubtitle,
  sceneKey,
  audioFile,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Filter sentences for this chapter
  const chapterSentences = allSentences.filter((s) => s.chapter_num === chapterNum);

  // Find active sentence
  let activeSentence = chapterSentences[0];
  for (let i = 0; i < chapterSentences.length; i++) {
    const s = chapterSentences[i];
    if (frame >= s.start_frame && frame <= s.end_frame) {
      activeSentence = s;
      break;
    } else if (frame > s.end_frame) {
      activeSentence = s;
    }
  }

  // Sentence-relative frame calculations
  const relFrame = Math.max(0, frame - activeSentence.start_frame);
  const sentenceDuration = Math.max(1, activeSentence.end_frame - activeSentence.start_frame);
  const sentenceProgress = Math.min(1, relFrame / sentenceDuration);

  // Sub-second cycle (30 frames = 1 second)
  const currentSec = relFrame / 30;
  const subSec = currentSec - Math.floor(currentSec); // 0.0 to 1.0 within every single second

  // Sub-second phase detection:
  // 0.00 - 0.15: anticipation
  // 0.15 - 0.40: primary action
  // 0.40 - 0.70: propagation
  // 0.70 - 0.90: emphasis
  // 0.90 - 1.00: settle/bridge
  const isAnticipation = subSec < 0.15;
  const isPrimaryAction = subSec >= 0.15 && subSec < 0.40;
  const isPropagation = subSec >= 0.40 && subSec < 0.70;
  const isEmphasis = subSec >= 0.70 && subSec < 0.90;
  const isSettle = subSec >= 0.90;

  // Kinetic pulse multiplier
  const pulseFactor = isEmphasis ? 1.08 : isAnticipation ? 0.97 : 1.0;
  const actionGlow = isEmphasis ? "#FF2A85" : isPropagation ? "#00F0FF" : "#C77DFF";

  // Dynamic Camera Tilt based on camera_motion
  const camYaw = Math.sin((frame * 0.015) % (Math.PI * 2)) * 4;
  const camPitch = Math.cos((frame * 0.012) % (Math.PI * 2)) * 2;
  const camScale = interpolate(sentenceProgress, [0, 0.5, 1], [0.98, 1.02, 1.0], {
    extrapolateRight: "clamp",
  });

  // Background Grid motion
  const gridOffsetY = (frame * 0.6) % 40;

  // Active verb styling
  const verbUpper = (activeSentence.visual_verb || "ANALYZE").toUpperCase();

  return (
    <AbsoluteFill style={{ backgroundColor: "#06010F", overflow: "hidden" }}>
      {/* 1. CONTINUOUS 3D CAUSAL BACKGROUND ENVIRONMENT */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage: `
            linear-gradient(rgba(123, 44, 191, 0.14) 1px, transparent 1px),
            linear-gradient(90deg, rgba(123, 44, 191, 0.14) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
          backgroundPosition: `0px ${gridOffsetY}px`,
          pointerEvents: "none",
        }}
      >
        {/* Dynamic Nebulae responding to current visual verb */}
        <div
          style={{
            position: "absolute",
            top: "8%",
            left: "12%",
            width: 580,
            height: 580,
            borderRadius: "50%",
            background: isEmphasis
              ? "radial-gradient(circle, rgba(255, 42, 133, 0.22) 0%, transparent 70%)"
              : "radial-gradient(circle, rgba(123, 44, 191, 0.16) 0%, transparent 70%)",
            filter: "blur(60px)",
            transition: "all 0.3s ease",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: "8%",
            right: "12%",
            width: 620,
            height: 620,
            borderRadius: "50%",
            background: isPropagation
              ? "radial-gradient(circle, rgba(0, 240, 255, 0.18) 0%, transparent 70%)"
              : "radial-gradient(circle, rgba(90, 247, 142, 0.14) 0%, transparent 70%)",
            filter: "blur(70px)",
          }}
        />
        <FloatingDustParticles count={36} />
      </div>

      {/* Audio Tracks */}
      <Audio src={staticFile(audioFile)} />
      <Audio src={staticFile("audio_natural/ambient_bed.wav")} volume={0.05} loop />

      {/* 2. CINEMATIC HEADER WITH LIVE TELEMETRY CHIP */}
      <div
        style={{
          position: "absolute",
          top: 14,
          left: 32,
          right: 32,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          zIndex: 40,
        }}
      >
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span
              style={{
                padding: "3px 8px",
                backgroundColor: "#FF2A85",
                color: "#FFFFFF",
                borderRadius: 4,
                fontSize: 10,
                fontWeight: 900,
                letterSpacing: 1.5,
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              CHAPTER {String(chapterNum).padStart(2, "0")}
            </span>
            <span
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: 0.6,
                fontFamily: "'Cinzel', serif, -apple-system",
                textShadow: "0 0 14px rgba(255, 42, 133, 0.5)",
              }}
            >
              {chapterTitle}
            </span>
          </div>
          <div
            style={{
              fontSize: 10.5,
              color: "#C77DFF",
              marginTop: 3,
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            {chapterSubtitle}
          </div>
        </div>

        {/* Live Hardware Telemetry */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            backgroundColor: "rgba(18, 2, 34, 0.85)",
            border: "1px solid rgba(199, 125, 255, 0.3)",
            padding: "5px 12px",
            borderRadius: 6,
            fontSize: 9.5,
            color: "#E0AAFF",
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              backgroundColor: isEmphasis ? "#FF2A85" : "#5AF78E",
              boxShadow: `0 0 8px ${isEmphasis ? "#FF2A85" : "#5AF78E"}`,
            }}
          />
          <span>4K MASTERCLASS • 30 FPS • H100 SXM5</span>
          <span>|</span>
          <span style={{ color: "#5AF78E" }}>
            FRAME {frame} ({((frame / 30)).toFixed(1)}s)
          </span>
        </div>
      </div>

      {/* 3. DYNAMIC PEDAGOGICAL DIRECTOR ACTION HUD */}
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 32,
          right: 32,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 35,
          backgroundColor: "rgba(12, 1, 24, 0.92)",
          border: `1.5px solid ${actionGlow}`,
          borderRadius: 8,
          padding: "6px 14px",
          boxShadow: `0 0 20px ${actionGlow}44`,
          backdropFilter: "blur(6px)",
          fontFamily: "'JetBrains Mono', monospace",
        }}
      >
        {/* Left: Active Visual Verb & Action */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span
            style={{
              backgroundColor: actionGlow,
              color: "#000000",
              fontWeight: 900,
              fontSize: 10,
              padding: "2px 7px",
              borderRadius: 4,
              letterSpacing: 1,
            }}
          >
            VERB: {verbUpper}
          </span>
          <span style={{ fontSize: 11, color: "#FFFFFF", fontWeight: 700 }}>
            {activeSentence.semantic_action.replace(/_/g, " ").toUpperCase()}
          </span>
          <span style={{ fontSize: 9.5, color: "#C77DFF" }}>
            → {activeSentence.visual_consequence}
          </span>
        </div>

        {/* Right: Live Mathematical Equation */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            backgroundColor: "rgba(0, 0, 0, 0.6)",
            border: "1px solid rgba(199, 125, 255, 0.25)",
            padding: "3px 10px",
            borderRadius: 5,
          }}
        >
          <span style={{ fontSize: 9, color: "#8E7DBE" }}>EQUATION:</span>
          <span
            style={{
              fontSize: 11,
              fontWeight: 800,
              color: isEmphasis ? "#FF2A85" : "#00F0FF",
              textShadow: `0 0 8px ${actionGlow}`,
            }}
          >
            {activeSentence.equation_state || "W_inference = W_0"}
          </span>
        </div>
      </div>

      {/* 4. MAIN DENSE 3D PEDAGOGICAL STAGE */}
      <div
        style={{
          position: "absolute",
          top: 104,
          left: 32,
          right: 32,
          bottom: 50,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 24,
          zIndex: 20,
          transform: `perspective(1200px) rotateX(${camPitch}deg) rotateY(${camYaw}deg) scale(${camScale * pulseFactor})`,
          transition: "transform 0.1s ease-out",
        }}
      >
        {/* Render Primary & Secondary Objects Based on Sentence Choreography */}
        {renderPedagogicalStage(activeSentence, relFrame, chapterNum)}
      </div>

      {/* 5. FOOTER TELEMETRY & AUDIO WAVEFORM */}
      <div
        style={{
          position: "absolute",
          bottom: 6,
          left: 32,
          right: 32,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 30,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            fontSize: 9.5,
            color: "#8E7DBE",
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          <span>CHOREOGRAPHY: 1-SEC RHYTHM</span>
          <span>•</span>
          <span style={{ color: "#FF2A85" }}>
            SUB-SEC: {subSec < 0.15 ? "ANTICIPATION" : subSec < 0.4 ? "ACTION" : subSec < 0.7 ? "PROPAGATION" : subSec < 0.9 ? "EMPHASIS" : "SETTLE"}
          </span>
          <span>•</span>
          <span style={{ color: "#5AF78E" }}>SENTENCE {activeSentence.sentence_index_in_chapter} / {chapterSentences.length}</span>
        </div>
        <AudioWaveformVisualizer barCount={36} height={20} />
      </div>

      {/* 6. CLEAN, UNOBTRUSIVE CYBER SUBTITLES (Synchronized with Whisper) */}
      <CyberSubtitles sceneKey={sceneKey} />
    </AbsoluteFill>
  );
};

// ==============================================================================
// STAGE RENDERER: DYNAMICALLY CONSTRUCTS PEDAGOGICAL 3D SCENE PER SENTENCE
// ==============================================================================
function renderPedagogicalStage(sentence: ChoreographySentence, relFrame: number, chapterNum: number) {
  const pObj = (sentence.primary_object || "").toLowerCase();
  const verb = (sentence.visual_verb || "").toLowerCase();
  const text = (sentence.spoken_text || "").toLowerCase();

  // STAGE A: Frontier Models, Convergence, or Roadmap Radial Branch
  if (
    pObj.includes("branch") ||
    pObj.includes("radial") ||
    text.includes("gpt-4") ||
    text.includes("claude") ||
    text.includes("frontier") ||
    text.includes("theorem") ||
    verb === "branch" ||
    verb === "converge"
  ) {
    const targets = chapterNum === 1
      ? [
          { id: "gpt4", title: "GPT-6 Astra", subtitle: "OpenAI • Frontier MoE", color: "#FF2A85", logoSrc: "assets/real_world/logos/openai_logo.svg", badge: "TRANSFORMER" },
          { id: "claude", title: "Claude 5.5 Sonnet", subtitle: "Anthropic • Transformer", color: "#C77DFF", logoSrc: "assets/real_world/logos/anthropic_logo.svg", badge: "TRANSFORMER" },
          { id: "gemini", title: "Gemini 4 Pro", subtitle: "Google DeepMind", color: "#9D4EDD", logoSrc: "assets/real_world/logos/google_logo.svg", badge: "TRANSFORMER" },
          { id: "llama", title: "Llama 5", subtitle: "Meta Open Weights", color: "#0081FB", logoSrc: "assets/real_world/logos/meta_logo.svg", badge: "TRANSFORMER" },
          { id: "mythos", title: "Mythos", subtitle: "Frontier Lab • Reasoning", color: "#5AF78E", logoSrc: "assets/real_world/logos/openai_logo.svg", badge: "TRANSFORMER" },
        ]
      : [
          { id: "t1", title: "Theorem 1: Rank Collapse", subtitle: "Lyapunov SVD Decay (Rank → 1)", color: "#FF2A85", badge: "OJA TRAP" },
          { id: "t2", title: "Theorem 2: Routing Bounds", subtitle: "Moore Bound Graph Latency", color: "#C77DFF", badge: "O(1) VS O(log N)" },
          { id: "t3", title: "Theorem 3: Hardware Barrier", subtitle: "Dense Systolic vs Sparse Pointer", color: "#5AF78E", badge: "MEMORY WALL" },
        ];

    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <ChalkboardVectorBranch
          sourceTitle={chapterNum === 1 ? "FRONTIER AI MONOLITH" : "3 MASTER THEOREMS"}
          sourceBadge="SHARED TRANSFORMER ENGINE"
          targets={targets}
          startFrame={0}
          width={640}
          height={390}
        />
        <div style={{ display: "flex", flexDirection: "column", gap: 14, alignItems: "center" }}>
          <TensorCube3D size={130} label="TRANSFORMER" subLabel="MONOLITH CORE" color="#FF2A85" speed={1.2} />
          <div
            style={{
              backgroundColor: "rgba(18, 2, 34, 0.9)",
              border: "1.5px solid #FF2A85",
              borderRadius: 8,
              padding: "6px 14px",
              fontSize: 10,
              color: "#FFFFFF",
              fontFamily: "'JetBrains Mono', monospace",
              textAlign: "center",
            }}
          >
            <div>ARCHITECTURAL INVARIANCE</div>
            <div style={{ color: "#FF2A85", fontWeight: 900, fontSize: 13, marginTop: 2 }}>dW/dt = 0.000</div>
          </div>
        </div>
      </div>
    );
  }

  // STAGE B: Datacenter Supercomputer, Power Grid, or Hardware Lottery
  if (
    pObj.includes("datacenter") ||
    pObj.includes("hardware") ||
    pObj.includes("supercomputer") ||
    pObj.includes("systolic") ||
    text.includes("electrical grids") ||
    text.includes("megawatts") ||
    text.includes("h100") ||
    text.includes("gpu") ||
    text.includes("hardware lottery") ||
    verb === "lock" ||
    chapterNum === 7
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <DatacenterVisualizer
          supercomputerName="NVIDIA DGX SUPERPOD (42.8 MW)"
          gpuCount="32,768 H100 SXM5"
          powerDraw="42.8 MW Cluster Load"
          bandwidth="3.35 TB/s HBM3"
          width={530}
          height={390}
        />
        <SystolicHardwareGrid width={520} height={390} />
      </div>
    );
  }

  // STAGE C: Frozen Weights, Lifelong Memory Pipeline, or Residual Highway
  if (
    pObj.includes("freeze") ||
    pObj.includes("cryo") ||
    pObj.includes("pipeline") ||
    pObj.includes("highway") ||
    text.includes("frozen") ||
    text.includes("crystalline monolith") ||
    text.includes("pre-training concludes") ||
    verb === "freeze"
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <LifelongMemoryPipeline
          activeStage={relFrame > 40 ? 2 : 1}
          isFrozen={relFrame > 20}
          width={540}
          height={390}
        />
        <MathFormulaCard
          title="The Frozen Invariance Law"
          formula="W_{inference} = W_0 \implies \frac{dW}{dt} = 0"
          terms={[
            { symbol: "W_0", label: "Fixed parameters in GPU HBM", color: "#FF2A85" },
            { symbol: "dW/dt", label: "Zero synaptic plasticity during inference", color: "#C77DFF" },
            { symbol: "G(V, E)", label: "Static topology invariance: G_{inf} = G_{init}", color: "#5AF78E" },
          ]}
          conclusion="No new synapses sprout; no connections prune. The silicon monolith is locked."
          width={490}
        />
      </div>
    );
  }

  // STAGE D: Biological Brain, Neocortex, or STDP Synaptic Cleft
  if (
    pObj.includes("brain") ||
    pObj.includes("neocortex") ||
    pObj.includes("stdp") ||
    pObj.includes("synapse") ||
    text.includes("biological") ||
    text.includes("86 billion") ||
    text.includes("20 watts") ||
    text.includes("dendritic") ||
    verb === "sprout" ||
    chapterNum === 2
  ) {
    if (text.includes("stdp") || text.includes("spike") || text.includes("timing") || text.includes("hebb")) {
      return (
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          <STDPSynapseCard width={520} height={390} />
          <SynapticNetwork width={510} height={390} nodeCount={24} />
        </div>
      );
    }
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <BiologicalNeocortexCard width={520} height={390} />
        <SynapticNetwork width={510} height={390} nodeCount={26} />
      </div>
    );
  }

  // STAGE E: Academic Evidence, Papers & Research Citations
  if (
    pObj.includes("paper") ||
    text.includes("vaswani") ||
    text.includes("gaier") ||
    text.includes("hasani") ||
    text.includes("chen") ||
    text.includes("hooker") ||
    text.includes("von oswald") ||
    text.includes("sara hooker") ||
    text.includes("attention is all you need")
  ) {
    let paperImg = "assets/real_world/papers/paper_attention-01.png";
    let paperTitle = "Attention Is All You Need";
    let paperAuthors = "Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin";
    let paperVenue = "NeurIPS 2017 • 120,000+ Citations";
    let paperHighlight = "MULTI-HEAD SELF-ATTENTION PRIMITIVE";

    if (text.includes("gaier") || text.includes("weight agnostic")) {
      paperImg = "assets/real_world/papers/paper_wann-01.png";
      paperTitle = "Weight Agnostic Neural Networks";
      paperAuthors = "Adam Gaier & David Ha (Google Brain)";
      paperVenue = "NeurIPS 2019";
      paperHighlight = "TOPOLOGY OVER WEIGHTS ENCODES TASK BIAS";
    } else if (text.includes("liquid") || text.includes("hasani")) {
      paperImg = "assets/real_world/papers/paper_liquid-01.png";
      paperTitle = "Liquid Time-Constant Networks";
      paperAuthors = "Ramin Hasani, Mathias Lechner, Alexander Amini, Daniela Rus";
      paperVenue = "MIT CSAIL / AAAI";
      paperHighlight = "CONTINUOUS DYNAMICS & ADAPTIVE TIME CONSTANTS";
    } else if (text.includes("neural ode") || text.includes("chen")) {
      paperImg = "assets/real_world/papers/paper_neural_ode-01.png";
      paperTitle = "Neural Ordinary Differential Equations";
      paperAuthors = "Ricky T. Q. Chen, Yulia Rubanova, Jesse Bettencourt, David Duvenaud";
      paperVenue = "NeurIPS 2018 Best Paper Award";
      paperHighlight = "CONTINUOUS DEPTH VECTOR FIELDS";
    } else if (text.includes("hardware lottery") || text.includes("hooker")) {
      paperImg = "assets/real_world/papers/paper_hardware_lottery-01.png";
      paperTitle = "The Hardware Lottery";
      paperAuthors = "Sara Hooker (Google Brain / Cohere For AI)";
      paperVenue = "Communications of the ACM";
      paperHighlight = "IDEAS SUCCEED WHEN THEY MATCH DOMINANT ACCELERATORS";
    } else if (text.includes("von oswald") || text.includes("in-context")) {
      paperImg = "assets/real_world/papers/paper_in_context-01.png";
      paperTitle = "Transformers Learn In-Context by Gradient Descent";
      paperAuthors = "Johannes von Oswald, Eyvind Niklasson, Ettore Randazzo et al.";
      paperVenue = "ICML 2023 Outstanding Paper";
      paperHighlight = "FORWARD ATTENTION SIMULATES META-OPTIMIZATION";
    }

    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <RealPaperHighlighter
          imageSrc={paperImg}
          title={paperTitle}
          authors={paperAuthors}
          venue={paperVenue}
          highlights={[{ top: 22, left: 10, width: 80, height: 6, label: paperHighlight }]}
          width={530}
          height={390}
          startFrame={0}
        />
        <CodeTerminal
          filename="forward_attention_projection.py"
          codeLines={[
            "# Multi-Head Self-Attention Projection Primitive",
            "def self_attention(Q, K, V, d_k):",
            "    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)",
            "    attn_weights = F.softmax(scores, dim=-1)",
            "    return torch.matmul(attn_weights, V) # O(1) Path Length",
          ]}
          outputLines={[
            ">> [TENSOR] Q @ K.T computed: Instantaneous all-to-all metric routing.",
            ">> [COMPLEXITY] Constant depth: 1 layer bridges 100k tokens.",
            ">> [INVARIANCE] Weights W remain fixed in torch.inference_mode().",
          ]}
          startFrame={0}
          width={510}
          height={390}
        />
      </div>
    );
  }

  // STAGE F: Scientist Portrait & Code Terminal
  if (
    text.includes("hebb") ||
    text.includes("hassabis") ||
    text.includes("sutskever") ||
    text.includes("lecun") ||
    text.includes("olah")
  ) {
    let researcherName = "Demis Hassabis";
    let researcherRole = "CEO & Co-Founder";
    let researcherInst = "Google DeepMind • Nobel Laureate 2024";
    let researcherPhoto = "assets/real_world/researchers/demis_hassabis.jpg";
    let researcherQuote = "The biological brain is our ultimate existence proof of general intelligence. But building artificial systems requires understanding the computational principles, not slavishly copying biology.";
    let quoteHighlight = "understanding the computational principles, not slavishly copying biology";

    if (text.includes("hebb")) {
      researcherName = "Donald O. Hebb";
      researcherRole = "Author of The Organization of Behavior";
      researcherInst = "McGill University (1949)";
      researcherPhoto = "assets/real_world/researchers/donald_hebb.jpg";
      researcherQuote = "Neurons that fire together wire together. The foundational postulate of localized synaptic plasticity.";
      quoteHighlight = "fire together wire together";
    }

    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <ResearcherPortraitCard
          name={researcherName}
          role={researcherRole}
          institution={researcherInst}
          photoSrc={researcherPhoto}
          quote={researcherQuote}
          highlightText={quoteHighlight}
          startFrame={0}
          width={520}
        />
        <CodeTerminal
          filename="plasticity_engine.py"
          codeLines={[
            "# Continuous Localized Synaptic Update Dynamics",
            "def localized_hebbian_step(w, x, y, eta=0.01):",
            "    delta_w = eta * torch.outer(y, x)",
            "    return w + delta_w # Correlated reinforcement",
          ]}
          outputLines={[
            ">> [EVENT] Action potentials synchronized across pre/post terminals.",
            ">> [BIOLOGY] NMDA calcium channel opened; dendritic spine reinforced.",
          ]}
          startFrame={0}
          width={510}
          height={390}
        />
      </div>
    );
  }

  // STAGE G: Theorem 1 (Eigenvalue Rank Collapse / Oja Trap)
  if (
    pObj.includes("rank") ||
    pObj.includes("collapse") ||
    pObj.includes("oja") ||
    pObj.includes("eigenvalue") ||
    verb === "collapse" ||
    chapterNum === 5
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <EigenvalueCollapseBar width={530} height={390} />
        <AnimatedLossChart
          title="Empirical Rank Collapse & Loss Trajectory"
          lineColor="#FF2A85"
          width={510}
          height={390}
        />
      </div>
    );
  }

  // STAGE H: Theorem 2 (Routing Bounds, Moore Bound, Attention Matrix)
  if (
    pObj.includes("routing") ||
    pObj.includes("moore") ||
    pObj.includes("expressivity") ||
    chapterNum === 6
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <AttentionHeatmap width={520} height={390} />
        <SynapticNetwork width={510} height={390} nodeCount={24} />
      </div>
    );
  }

  // STAGE I: Benchmark Diagnostics (Chapter 8: 92.3% vs 7.7%)
  if (
    pObj.includes("benchmark") ||
    text.includes("associative recall") ||
    text.includes("92%") ||
    text.includes("7.7%") ||
    chapterNum === 8
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <AnimatedLossChart
          title="Controlled In-Context Recall: Transformer (92.3%) vs Rewiring (7.7%)"
          lineColor="#00F0FF"
          width={530}
          height={390}
        />
        <AttentionHeatmap width={510} height={390} />
      </div>
    );
  }

  // STAGE J: Frontier Labs & Neuromorphic Memristor Crossbars (Chapter 9 & 10)
  if (
    pObj.includes("memristor") ||
    pObj.includes("crossbar") ||
    pObj.includes("kan") ||
    pObj.includes("deepseek") ||
    chapterNum === 9 ||
    chapterNum === 10
  ) {
    return (
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        <MemristorCrossbar3D width={530} height={390} />
        <CompanyLogoBanner
          logos={[
            { name: "DeepSeek", logoSrc: "assets/real_world/logos/openai_logo.svg", color: "#5AF78E", model: "DeepSeek-V3", params: "MLA + MoE" },
            { name: "Google DeepMind", logoSrc: "assets/real_world/logos/google_deepmind_logo.png", color: "#C77DFF", model: "Gemini 4", params: "Meta-Plasticity" },
            { name: "Anthropic", logoSrc: "assets/real_world/logos/anthropic_logo.svg", color: "#FF2A85", model: "Claude 5.5", params: "Induction Heads" },
            { name: "NVIDIA", logoSrc: "assets/real_world/logos/nvidia_logo.svg", color: "#76B900", model: "Blackwell", params: "NVLink Cluster" },
          ]}
          width={510}
        />
      </div>
    );
  }

  // DEFAULT DENSE FALLBACK: Tensor Cube + Synaptic Network
  return (
    <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
      <TensorCube3D size={140} label="NEURAL MATRIX" subLabel="ACTIVE CAUSAL FLOW" color="#FF2A85" speed={1.4} />
      <SynapticNetwork width={540} height={390} nodeCount={24} />
    </div>
  );
}
