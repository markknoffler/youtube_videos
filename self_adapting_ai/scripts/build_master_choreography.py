import json
import os
import re

subtitles_path = "self_adapting_ai/remotion_studio/src/data/subtitles.json"
with open(subtitles_path, "r") as f:
    subtitles = json.load(f)

chapter_meta = {
    "Scene01": {
        "num": 1,
        "title": "The Monolith of Deep Learning",
        "theme": "The Transformer Monopoly & The Frozen Silicon Monolith"
    },
    "Scene02": {
        "num": 2,
        "title": "The Biological Architecture & Neuromorphic Principles",
        "theme": "86 Billion Living Neurons (~20W) vs Megawatt Static Silos"
    },
    "Scene03": {
        "num": 3,
        "title": "The Self-Organizing Hypothesis & Neuroevolution",
        "theme": "Donald Hebb (1949), Oja's Rule (1982) & Weight Agnostic Topologies"
    },
    "Scene04": {
        "num": 4,
        "title": "The Modular Emergence Paradox",
        "theme": "Static Graph Rewiring vs Dynamic Content-Dependent Bilinear Metric Routing"
    },
    "Scene05": {
        "num": 5,
        "title": "Theorem 1 — Rank Collapse in Homogeneous Local Plasticity",
        "theme": "The Oja Trap: Why Local Hebbian Dynamics Collapse Subspace Rank to 1"
    },
    "Scene06": {
        "num": 6,
        "title": "Theorem 2 — Routing Expressivity Lower Bound",
        "theme": "The Moore Bound & Exponential Multi-Hop Attenuation in Sparse Biological Graphs"
    },
    "Scene07": {
        "num": 7,
        "title": "Theorem 3 — The Hardware Lottery and Credit Assignment Barrier",
        "theme": "Dense Systolic Tensor GEMM vs Sparse Memory Pointer Chasing & Exponential Gradient Variance"
    },
    "Scene08": {
        "num": 8,
        "title": "Empirical Benchmarks & Diagnostic Lab Evidence",
        "theme": "Controlled In-Context Key-Value Associative Recall: 92.3% vs 7.7% Rank Degradation"
    },
    "Scene09": {
        "num": 9,
        "title": "What Frontier Labs Discovered: Structured Routing",
        "theme": "DeepSeek-V3, Fine-Grained MoE, Multi-Head Latent Attention & In-Context Meta-Optimization"
    },
    "Scene10": {
        "num": 10,
        "title": "The 10-Year Horizon: Living Synthetic Minds",
        "theme": "Grand Synthesis: Neuromorphic Crossbars, MIT KANs, Liquid Neural ODEs & Meta-Plasticity"
    }
}

# Function to infer pedagogical choreography for each sentence
def generate_sentence_choreography(scene_key, s_idx, sent_obj, total_sentences):
    text = sent_obj["text"]
    start_sec = sent_obj["startSec"]
    end_sec = sent_obj["endSec"]
    duration = end_sec - start_sec
    s_id = f"{scene_key}_S{s_idx+1:02d}"
    t_lower = text.lower()
    chap_info = chapter_meta[scene_key]

    # Specific semantic action and primary objects based on content
    if "welcome" in t_lower or "masterclass" in t_lower:
        action = "establish_masterclass_hub"
        primary = "Central Pedagogical 3D Monolith Hub"
        secondaries = ["Chalkboard Coordinate Grid", "Telemetry Header: 4K 30FPS H100 SXM5"]
        v_verb = "construct"
        eq = "W_init ∈ R^{d_model × d_model}"
        cam_motion = "slow orbital sweep 15° to front-facing isometric"
        cam_target = "Central Monolith Origin (0,0,0)"
        trans = "elevate from floor plane [0, -100, 0] to [0, 0, 0]"
        rot = "slow yaw 0° to 12°"
        scale = "scale 0.2 to 1.0 with spring easing"
        topo = "radial coordinate axes draw out into 3D volume"
        flow = "cyan initialization pulse radiates outward"
        glow = "emissive core lights up at #C77DFF"
        consequence = "architectural coordinate volume established"
    elif "gpt-4" in t_lower or "claude" in t_lower or "gemini" in t_lower or "deepseek" in t_lower or "frontier" in t_lower:
        action = "branch_frontier_models"
        primary = "ChalkboardVectorBranch 5-Way Radial Conduits"
        secondaries = ["OpenAI, Anthropic, DeepMind, Meta, DeepSeek Target Nodes", "TensorCube3D"]
        v_verb = "branch"
        eq = "M ∈ {GPT-4o, Claude 3.5, Gemini 1.5, Llama 3.1, DeepSeek-V3}"
        cam_motion = "pull back 200 units along z-axis to frame all 5 branches"
        cam_target = "Central Radial Spline Hub"
        trans = "branches extend radially from (0,0,0) outward to 5 cardinal targets"
        rot = "fixed 0° pitch, 0° yaw"
        scale = "target model cards snap into scale 1.0 upon photon impact"
        topo = "5 laser conduits ignite with dynamic strokeDashoffset reveal"
        flow = "high-velocity photons stream along conduits into branded nodes"
        glow = "each branch illuminates in brand color (#FF2A85, #C77DFF, #9D4EDD, #0081FB, #5AF78E)"
        consequence = "frontier AI landscape framed as divergent outputs of a single core schema"
    elif "transformer" in t_lower or "2017" in t_lower or "vaswani" in t_lower:
        action = "morph_to_transformer_engine"
        primary = "Multi-Head Self-Attention Core Engine"
        secondaries = ["Vaswani 2017 Paper Inset", "Residual Highway Spline", "LayerNorm Plane"]
        v_verb = "project"
        eq = "Attention(Q,K,V) = softmax(QK^T / √d_k) V"
        cam_motion = "push in toward central attention matrix"
        cam_target = "Multi-Head Attention Projection Matrix"
        trans = "branches collapse back into unified central Transformer engine"
        rot = "pitch down 15° to expose horizontal tensor plane"
        scale = "attention matrix expands 1.2x"
        topo = "residual highway reconnects input directly to output block"
        flow = "token vector stream splits into 3 parallel streams"
        glow = "query-key-value planes illuminate in pink, purple, and emerald"
        consequence = "monolithic transformer primitive revealed as global monopoly"
    elif "query" in t_lower or "key" in t_lower or "value" in t_lower or "dot-product" in t_lower or "q/k" in t_lower:
        action = "project_qkv_subspaces"
        primary = "Projected Token Coordinate Vectors (Q, K, V)"
        secondaries = ["Bilinear Dot-Product Angle Visualizer", "Dynamic Attention Heatmap"]
        v_verb = "project"
        eq = "q_i = W_Q x_i,  k_j = W_K x_j,  v_j = W_V x_j"
        cam_motion = "dolly along trajectory of querying token x_i"
        cam_target = "Token Pair Coordinate Vector Interaction"
        trans = "q_i translates into upper coordinate manifold, k_j into lateral manifold"
        rot = "q_i and k_j rotate to expose angular cosine similarity"
        scale = "dot-product scalar expands into numeric magnitude badge"
        topo = "pairwise temporary attention filament connects token i to token j"
        flow = "affinity score pulse travels along filament"
        glow = "strongest attention score flashes at #FF2A85, weaker paths dim"
        consequence = "instantaneous metric routing calculated dynamically in token space"
    elif "frozen" in t_lower or "monolith" in t_lower or "freeze" in t_lower or "dw/dt = 0" in t_lower:
        action = "propagate_freeze_shockwave"
        primary = "Cryogenic Weight Lattice & Visual Padlocks"
        secondaries = ["LifelongMemoryPipeline", "Static Tensor Invariance Formula"]
        v_verb = "freeze"
        eq = "W_{inference} = W_0  (dW/dt = 0.000)"
        cam_motion = "rapid push-in to parameter lattice followed by hard freeze stop"
        cam_target = "Synaptic Weight Matrix Crossbar"
        trans = "cyan cryogenic shockwave sweeps from input layer to output layer"
        rot = "all oscillating weight vectors lock to fixed angle"
        scale = "iron padlock glyphs drop into position and lock"
        topo = "all dynamic synaptic weight updates clamp to zero"
        flow = "activation tokens flow through, but weight lattice remains rigidly motionless"
        glow = "ice-blue frost border surrounds parameter matrix (#00F0FF)"
        consequence = "telemetry verifies Δw_ij = 0.000: permanent silicon freeze"
    elif "biological" in t_lower or "brain" in t_lower or "20 watts" in t_lower or "neocortex" in t_lower:
        action = "contrast_biological_neocortex"
        primary = "BiologicalNeocortexCard (86B Neurons, 20W Budget)"
        secondaries = ["NVIDIA SuperPod Datacenter (100 MW)", "Metabolic Glucose Telemetry"]
        v_verb = "compare"
        eq = "P_{bio} ≈ 20W  vs  P_{cluster} ≥ 100,000,000W"
        cam_motion = "split-depth pan from datacenter megawatt racks to organic neocortex"
        cam_target = "Biological Neocortex Volume"
        trans = "organic dendritic volume pulses in midground"
        rot = "soft organic tumble 3°/sec"
        scale = "neocortex card scales up while datacenter dims to 40% opacity"
        topo = "asynchronous organic firing pathways flash non-deterministically"
        flow = "calcium and sodium action potentials propagate across synapses"
        glow = "magenta and lavender synaptic sparks (#FF2A85, #C77DFF)"
        consequence = "massive 5,000,000x energy efficiency contrast visually proven"
    elif "stdp" in t_lower or "spike" in t_lower or "synapse" in t_lower or "hebb" in t_lower:
        action = "animate_microscopic_stdp"
        primary = "STDPSynapseCard Microscopic Synaptic Cleft"
        secondaries = ["Neurotransmitter Vesicle Bursts", "Δt Millisecond Timing Curve"]
        v_verb = "route"
        eq = "Δw_{ij} = A_+ e^{-Δt/τ_+}  (LTP)  or  -A_- e^{Δt/τ_-}  (LTD)"
        cam_motion = "extreme microscopic zoom into synaptic cleft"
        cam_target = "Presynaptic Active Zone & Postsynaptic Receptors"
        trans = "presynaptic terminal aligns with postsynaptic dendritic spine"
        rot = "receptors rotate to bind incoming glutamate molecules"
        scale = "synaptic spine visibly swells (LTP) or shrinks (LTD)"
        topo = "synaptic contact area increases as connection strengthens"
        flow = "vesicles fuse with membrane and release glowing neurotransmitter dots"
        glow = "calcium influx flash through NMDA channels (#5AF78E)"
        consequence = "sub-millisecond spike timing dictates continuous physical weight adaptation"
    elif "sprout" in t_lower or "prun" in t_lower or "rewir" in t_lower or "structural" in t_lower:
        action = "sprout_and_prune_synapses"
        primary = "Dynamically Rewiring Synaptic Network"
        secondaries = ["Retracting Dendritic Spines", "Axonal Growth Cones"]
        v_verb = "sprout"
        eq = "Δw_{ij} = f_{STDP}(t_j - t_i) - λ_{prune} w_{ij}"
        cam_motion = "tracking dolly following advancing axonal growth cone"
        cam_target = "Active Axonal Growth Front"
        trans = "new axonal filaments branch toward co-active neurons"
        rot = "growth cone rotates searching for chemical gradients"
        scale = "redundant inactive edges thin and shrink to zero thickness"
        topo = "inactive edges disconnect and retract; new synaptic edges form"
        flow = "cytoskeletal actin filaments stream to edge tip"
        glow = "new synapses flash green upon forming; pruned edges desaturate"
        consequence = "structural physical topology continuously evolves without backpropagation"
    elif "wann" in t_lower or "neuroevolution" in t_lower or "neat" in t_lower or "topology" in t_lower:
        action = "simulate_topology_mutation"
        primary = "Weight Agnostic Neural Network Topology Graph"
        secondaries = ["Gaier & Ha 2019 Paper Highlighting", "Shared Weight Sweep Dial"]
        v_verb = "expand"
        eq = "Topology(G)  s.t.  W_i = w_shared  ∀ i ∈ E"
        cam_motion = "slow tilt up following ascending evolutionary generation tree"
        cam_target = "Evolving Minimal Seed Graph"
        trans = "minimal 2-node graph sprouts hidden nodes and recurrent loops"
        rot = "network graph rotates into optimal planar layout"
        scale = "shared weight dial sweeps across [-2.0, +2.0]"
        topo = "new structural bypass edges and recurrent loops inserted per generation"
        flow = "bipedal walker control signals traverse topological pathways"
        glow = "fittest topology illuminates in emerald (#5AF78E)"
        consequence = "functional behavior achieved purely through graph topology without trained weights"
    elif "oja" in t_lower or "covariance" in t_lower or "eigenvector" in t_lower or "rank collapse" in t_lower or "theorem 1" in t_lower:
        action = "simulate_theorem_1_rank_collapse"
        primary = "EigenvalueCollapseBar 16-Mode Spectral Decomposition"
        secondaries = ["1D Needle Attractor Subspace", "Oja Dynamical System Formula Card"]
        v_verb = "collapse"
        eq = "lim_{t → ∞} rank(W(t)) = 1,  dw/dt = C w - (w^T C w) w"
        cam_motion = "push down into 1D subspace axis as dimensions collapse"
        cam_target = "Dominant Eigenmode v_1 Axis"
        trans = "16 dimensional modes converge along dominant eigenvector v_1"
        rot = "weight matrix coordinate frame tilts to align with v_1"
        scale = "15 subordinate spectral bars plunge to zero; bar 1 surges to 100%"
        topo = "hyper-ellipsoid representation collapses into a single 1D needle line"
        flow = "sensory energy drains from minor axes and concentrates into v_1"
        glow = "dominant v_1 axis pulses in intense magenta (#FF2A85)"
        consequence = "effective rank collapses from 64 to 1.05; representation collapse proven"
    elif "moore" in t_lower or "routing" in t_lower or "degree" in t_lower or "latency" in t_lower or "theorem 2" in t_lower:
        action = "demonstrate_theorem_2_routing_bounds"
        primary = "Scene06 Moore Bound Graph Latency 3D Visualizer"
        secondaries = ["Token 1 to 100,000 Multi-Hop Relay", "O(1) Attention Shortcut"]
        v_verb = "attenuate"
        eq = "diam(G) ≥ ln(N)/ln(Δ) - O(1)  vs  diam(G_{Attn}) = 1"
        cam_motion = "wide dolly following multi-hop signal across tree levels"
        cam_target = "Multi-Hop Signal Propagation Frontier"
        trans = "sparse tree expands downward across 5 distinct hops"
        rot = "tree levels rotate to reveal logarithmic branching radius"
        scale = "signal pulse shrinks at each hop: 100% → 85% → 72% → 61% → 44%"
        topo = "5 sequential edges light up in sequence; attention connects in 1 direct arc"
        flow = "attenuated photon crawls through 5 hops while attention photon teleports"
        glow = "attenuated signal dims to faint purple; attention shortcut flashes emerald"
        consequence = "geometric trap exposed: physical sparse graphs cannot achieve instant routing without N^2 edges"
    elif "hardware lottery" in t_lower or "sara hooker" in t_lower or "systolic" in t_lower or "gemm" in t_lower or "theorem 3" in t_lower:
        action = "contrast_hardware_lottery_throughput"
        primary = "SystolicHardwareGrid 2D/3D Tensor Core Wavefront"
        secondaries = ["Sparse Memory Cache Miss Visualizer", "Sara Hooker Portrait"]
        v_verb = "compare"
        eq = "Arithmetic Intensity: GEMM ∝ O(d)  vs  Sparse Graph ∝ O(1)"
        cam_motion = "split camera tracking systolic dense dataflow vs stalled memory bus"
        cam_target = "NVIDIA H100 SXM5 Tensor Core Array"
        trans = "dense matrix rows slide smoothly through systolic array processing elements"
        rot = "array tilts 30° to show synchronized pipelining"
        scale = "dense throughput meter pegs at 989.4 TFLOPS; sparse stalls at 18.2 TFLOPS"
        topo = "dense bus streams at 3.35 TB/s; sparse memory bus shows 95% red stall bubbles"
        flow = "dense tensor data streams uniformly; sparse pointers jump erratically"
        glow = "tensor cores glow steady green; sparse lanes flash red warning stalls"
        consequence = "hardware lottery mathematically explains why Transformers win on silicon"
    elif "credit assignment" in t_lower or "variance" in t_lower or "backpropagation" in t_lower:
        action = "visualize_temporal_variance_explosion"
        primary = "Gradient Variance Horizon Cloud"
        secondaries = ["Exact Analytical Reverse Autodiff Arrow", "Neuromodulatory Noise Cone"]
        v_verb = "diverge"
        eq = "Var(∇_{local}) ∝ e^{Ω(T)}  vs  Var(∇_{backprop}) = 0"
        cam_motion = "pull back as variance cloud expands exponentially across horizon T"
        cam_target = "Temporal Trajectory Horizon T"
        trans = "backprop arrow travels straight back along computational graph"
        rot = "local gradient estimator vectors scatter into chaotic spherical cloud"
        scale = "variance cloud expands exponentially as T increases from 10 to 1,000"
        topo = "clean reverse autodiff graph remains deterministic; local updates drift"
        flow = "deterministic backprop photons flow in reverse; noisy particles diffuse"
        glow = "backprop line glows sharp laser green; local cloud blurs in noisy violet"
        consequence = "local learning wandering blindness proven: exponential sample complexity"
    elif "benchmark" in t_lower or "associative recall" in t_lower or "key-value" in t_lower or "92" in t_lower or "7.7" in t_lower:
        action = "execute_in_context_recall_benchmark"
        primary = "Scene08 Diagnostic Benchmark Head-to-Head Arena"
        secondaries = ["16 Key-Value Token Sequence", "AnimatedLossChart Convergence Curves"]
        v_verb = "retrieve"
        eq = "Recall(TF) = 92.3%  vs  Recall(SO-DRN) = 7.7% [Random Chance]"
        cam_motion = "center on query token [K_7], then pan to retrieval outputs"
        cam_target = "Queried Key-Value Retrieval Interface"
        trans = "query token [K_7] enters both architectures simultaneously"
        rot = "Transformer attention head aligns directly with [V_7]"
        scale = "Transformer accuracy bar rises to 92.3%; SO-DRN bar flatlines at 7.7%"
        topo = "SO-DRN pruned edges sever the path between K_7 and V_7"
        flow = "Transformer retrieves value instantly; SO-DRN signal scatters into crosstalk"
        glow = "Transformer output glows bright green (#5AF78E); SO-DRN flashes error red"
        consequence = "empirical diagnostic proves theoretical theorems: SO-DRN suffers catastrophic failure"
    elif "deepseek" in t_lower or "moe" in t_lower or "mla" in t_lower or "expert" in t_lower or "latent" in t_lower:
        action = "route_deepseek_moe_mla"
        primary = "DeepSeek-V3 MoERouter (256 Routed Experts + 2 Shared Experts)"
        secondaries = ["Multi-Head Latent Attention (MLA) Compression", "DeepSeek Technical Report"]
        v_verb = "route"
        eq = "y = ∑_{i∈Shared} E_i(x) + ∑_{k=1}^8 g_k(x) E_{idx_k}(x),  c_{KV} = W_{DKV} h_t"
        cam_motion = "dolly following incoming token through gating router to Top-8 experts"
        cam_target = "Soft Gating Probability Distribution"
        trans = "tokens pass through learned router gate and dispatch to 8 chosen experts"
        rot = "expert modules orient to receive incoming activation batch"
        scale = "256 expert bank arrays in background; 8 active experts illuminate"
        topo = "dynamic routing edges illuminate only to Top-8 experts; 2 shared always active"
        flow = "dense tensor streams dispatch at 91.2% MFU utilization"
        glow = "active experts illuminate in turquoise and violet (#00F0FF, #C77DFF)"
        consequence = "sparse modularity achieved over dense matrix banks: zero hardware penalty"
    elif "memristor" in t_lower or "crossbar" in t_lower or "analog" in t_lower or "kirchhoff" in t_lower:
        action = "animate_memristor_crossbar_plasticity"
        primary = "MemristorCrossbar3D In-Memory Computing Array"
        secondaries = ["Kirchhoff Current Summation Lines", "In-Situ Conductance Tuning Nodes"]
        v_verb = "converge"
        eq = "I_j = ∑_i V_i · G_{ij}  (0 ns von Neumann Bus Latency)"
        cam_motion = "orbit around 3D nanometer crossbar grid showing vertical/horizontal lines"
        cam_target = "Memristive Conductance Junction G_ij"
        trans = "voltage vector V applied to horizontal wordlines"
        rot = "crossbar tilts 45° isometric to expose nanoscale metal-oxide junctions"
        scale = "conductance dots expand as local voltage pulses adapt G_ij in-situ"
        topo = "currents sum physically along vertical bitlines via Kirchhoff's Current Law"
        flow = "analog electrical current streams down vertical columns instantaneously"
        glow = "active junctions glow bright yellow-orange; summation bus shines emerald"
        consequence = "von Neumann memory bottleneck eliminated: in-situ adaptation at physical limits"
    elif "kan" in t_lower or "kolmogorov" in t_lower or "spline" in t_lower or "function" in t_lower:
        action = "deform_kan_spline_edges"
        primary = "Kolmogorov-Arnold Network (KAN) Learnable Spline Edges"
        secondaries = ["MIT KAN Paper Inset", "1D B-Spline Basis Visualizer"]
        v_verb = "transform"
        eq = "f(x) = ∑_{q=1}^{2n+1} Φ_q( ∑_{p=1}^n φ_{q,p}(x_p) )"
        cam_motion = "push in toward a single edge to inspect continuous spline curve"
        cam_target = "Intra-Synaptic Learnable Function φ_{q,p}"
        trans = "static scalar weight wire morphs into a flexible continuous 1D curve"
        rot = "curve rotates in 3D to show control point coordinates"
        scale = "spline control points modulate height dynamically under gradient descent"
        topo = "nodes become simple summation hubs; computational complexity shifts to edges"
        flow = "continuous mathematical functions deform smoothly in real time"
        glow = "spline curve illuminates with gradient neon pink to cyan"
        consequence = "synapses gain intra-cellular mathematical depth without modifying network topology"
    elif "liquid" in t_lower or "ode" in t_lower or "continuous" in t_lower or "time-constant" in t_lower:
        action = "solve_liquid_neural_ode"
        primary = "Liquid Time-Constant Continuous Neural Trajectory"
        secondaries = ["Adaptive Time Constant τ(x, I)", "Continuous Vector Field"]
        v_verb = "route"
        eq = "dx(t)/dt = - [1/τ + f(x(t), I(t))] x(t) + A f(x(t), I(t))"
        cam_motion = "traveling camera gliding along continuous smooth hidden state path"
        cam_target = "Continuous Hidden State Trajectory x(t)"
        trans = "discrete step transitions smooth out into continuous fluid differential flow"
        rot = "state trajectory twists smoothly through multi-dimensional phase space"
        scale = "adaptive time constant τ expands when inputs change rapidly"
        topo = "static layer boundaries dissolve into continuous depth integration t ∈ [0, T]"
        flow = "continuous fluid particles stream along integral curves"
        glow = "smooth phase space trajectory glows in radiant lavender (#C77DFF)"
        consequence = "system adapts to arbitrary time intervals without catastrophic forgetting"
    elif "living" in t_lower or "synthesis" in t_lower or "organism" in t_lower or "future" in t_lower or "decade" in t_lower:
        action = "synthesize_living_synthetic_mind"
        primary = "Grand Emergence: The Self-Adapting Mathematical Organism"
        secondaries = ["Unified 4-Pillar Convergence Nexus", "Final Architectural Synthesis Badge"]
        v_verb = "emerge"
        eq = "Bilinear Attention ⊗ Continuous In-Memory Plasticity"
        cam_motion = "majestic pull-back revealing complete integrated living synthetic mind"
        cam_target = "Luminescent Living Cognitive Core"
        trans = "frozen silicon monolith from Chapter 1 dissolves its rigid crystalline shell"
        rot = "internal neural geometry breathes and pulses in harmonious organic cadence"
        scale = "system expands to fill full 1280x720 canvas in glorious architectural balance"
        topo = "all 4 revolutions (memristors, KAN splines, liquid ODEs, meta-plasticity) fuse"
        flow = "harmonious currents of photons and analog signals stream in perfect synchrony"
        glow = "radiant golden-emerald and magenta halo illuminating the entire workspace"
        consequence = "the paradox is resolved: intelligence is neither frozen silicon nor biological chaos, but a living mathematical organism"
    else:
        # Default tailored to chapter theme
        action = f"advance_{chap_info['num']:02d}_explanation"
        primary = f"Chapter {chap_info['num']} Pedagogical Mathematical Mechanism"
        secondaries = [f"{chap_info['title']} Dynamic Context", "Active Telemetry Stream"]
        v_verb = "route"
        eq = f"f_{{chap{chap_info['num']}}}(t) → S_{{{s_idx+1}}}"
        cam_motion = "smooth tracking dolly along explanatory trajectory"
        cam_target = "Active Pedagogical Focus"
        trans = "elements advance across chalkboard canvas"
        rot = "subtle 2° angular realignment"
        scale = "active elements pulse slightly at 1.05x"
        topo = "explanatory connections evolve with narrative cadence"
        flow = "data tokens advance through active sub-circuit"
        glow = "active nodes illuminate in chapter accent color"
        consequence = "narrative progression directly manifested in physical 3D geometry"

    # Sub-second actions based on duration and visual verb
    act_00_15 = f"anticipation: {primary} begins responding; illumination shifts toward incoming activation"
    act_15_40 = f"primary action: {v_verb} operation executes; geometry/tokens physically transition"
    act_40_70 = f"propagation: consequence travels through connected structures; {secondaries[0]} responds"
    act_70_90 = f"emphasis: target region/equation term glows with high luminance ({glow.split('(')[-1].replace(')', '') if '(' in glow else '#FF2A85'})"
    act_90_100 = f"settle/bridge: state stabilizes; mathematical telemetry updates; prepares entry state for sentence {s_idx+2}"

    entry_st = f"State inherited from sentence {s_idx} ({'initial scene state' if s_idx == 0 else 'active canvas'})"
    next_st = f"Stabilized state carrying {consequence} into sentence {s_idx+2}"

    return {
        "sentence_id": s_id,
        "chapter": f"Chapter {chap_info['num']:02d}: {chap_info['title']}",
        "chapter_num": chap_info['num'],
        "sentence_index_in_chapter": s_idx + 1,
        "start_time_sec": round(start_sec, 2),
        "end_time_sec": round(end_sec, 2),
        "duration_sec": round(duration, 2),
        "start_frame": sent_obj["startFrame"],
        "end_frame": sent_obj["endFrame"],
        "spoken_text": text,
        "semantic_action": action,
        "visual_verb": v_verb,
        "primary_object": primary,
        "secondary_objects": secondaries,
        "entry_state": entry_st,
        "action_0_00_to_0_15": act_00_15,
        "action_0_15_to_0_40": act_15_40,
        "action_0_40_to_0_70": act_40_70,
        "action_0_70_to_0_90": act_70_90,
        "action_0_90_to_1_00": act_90_100,
        "camera_motion": cam_motion,
        "camera_target": cam_target,
        "object_translation": trans,
        "object_rotation": rot,
        "object_scale": scale,
        "topology_change": topo,
        "particle_flow": flow,
        "glow_change": glow,
        "equation_state": eq,
        "label_state": f"Active Label: {primary.split()[0]} | Telemetry: Frame {sent_obj['startFrame']}-{sent_obj['endFrame']}",
        "graph_state": f"Kinetic stage synchronized to Chapter {chap_info['num']} timeline",
        "telemetry_change": f"FPS: 30 | Timestamp: {round(start_sec,1)}s | State: {action.upper()}",
        "visual_consequence": consequence,
        "next_state": next_st
    }

# Process all 10 chapters
all_sentences_choreography = []
total_sentences_count = sum(len(sents) for sents in subtitles.values())

for scene_key, sents in subtitles.items():
    for s_idx, sent_obj in enumerate(sents):
        entry = generate_sentence_choreography(scene_key, s_idx, sent_obj, total_sentences_count)
        all_sentences_choreography.append(entry)

print(f"Generated complete choreography for all {len(all_sentences_choreography)} sentences across 10 chapters.")

# Save to JSON
json_out_path = "self_adapting_ai/MASTER_CHOREOGRAPHY_MAP.json"
with open(json_out_path, "w") as f:
    json.dump({
        "metadata": {
            "title": "The Modular Emergence Paradox — 25:00 Masterclass Choreography Map",
            "total_runtime_seconds": 1500.20,
            "total_frames": 45000,
            "fps": 30,
            "total_sentences": len(all_sentences_choreography),
            "chapters_count": 10
        },
        "sentences": all_sentences_choreography
    }, f, indent=2)

print(f"Saved JSON choreography map to {json_out_path}")

# Generate Markdown Document
md_out_path = "self_adapting_ai/MASTER_CHOREOGRAPHY_MAP.md"
with open(md_out_path, "w") as f:
    f.write("# MASTER CHOREOGRAPHY MAP & STATE SPECIFICATION\n")
    f.write("## The Modular Emergence Paradox: 25:00 Continuous 3D Pedagogical Masterclass\n\n")
    f.write("- **Specification Standard**: 1,500-Second Resolution Grid with Sub-Second Choreography Rhythm\n")
    f.write("- **Choreography Schema**: 28 Mandatory Fields per Narration Beat\n")
    f.write(f"- **Total Sentences Choreographed**: {len(all_sentences_choreography)} sentences across 10 Chapters\n")
    f.write("- **Target Output**: `self_adapting_ai/output/masterclass_25min_complete.mp4`\n\n")
    f.write("---\n\n")

    current_chap = None
    for entry in all_sentences_choreography:
        if entry["chapter"] != current_chap:
            current_chap = entry["chapter"]
            f.write(f"\n## {current_chap}\n\n")

        f.write(f"### Sentence {entry['sentence_index_in_chapter']:02d}: `{entry['sentence_id']}` [{entry['start_time_sec']}s – {entry['end_time_sec']}s | Frames {entry['start_frame']} – {entry['end_frame']}]\n\n")
        f.write(f"> **Spoken Narration**: *\"{entry['spoken_text']}\"*\n\n")
        f.write(f"- **Semantic Action & Visual Verb**: `{entry['semantic_action']}` (Verb: **{entry['visual_verb'].upper()}**)\n")
        f.write(f"- **Primary Explanatory Object**: {entry['primary_object']}\n")
        f.write(f"- **Secondary Objects**: {', '.join(entry['secondary_objects'])}\n")
        f.write(f"- **Camera Direction**: {entry['camera_motion']} (Target: `{entry['camera_target']}`)\n")
        f.write(f"- **Geometry & Transforms**:\n")
        f.write(f"  - Translation: {entry['object_translation']}\n")
        f.write(f"  - Rotation: {entry['object_rotation']}\n")
        f.write(f"  - Scale: {entry['object_scale']}\n")
        f.write(f"- **Topology & Flow**:\n")
        f.write(f"  - Topology Change: {entry['topology_change']}\n")
        f.write(f"  - Particle / Activation Flow: {entry['particle_flow']}\n")
        f.write(f"  - Illumination & Glow: {entry['glow_change']}\n")
        f.write(f"- **Mathematical Equation State**: `${entry['equation_state']}$`\n")
        f.write(f"- **Sub-Second Choreography Rhythm**:\n")
        f.write(f"  - `0.00 – 0.15s`: {entry['action_0_00_to_0_15']}\n")
        f.write(f"  - `0.15 – 0.40s`: {entry['action_0_15_to_0_40']}\n")
        f.write(f"  - `0.40 – 0.70s`: {entry['action_0_40_to_0_70']}\n")
        f.write(f"  - `0.70 – 0.90s`: {entry['action_0_70_to_0_90']}\n")
        f.write(f"  - `0.90 – 1.00s`: {entry['action_0_90_to_1_00']}\n")
        f.write(f"- **Visible Explanatory Consequence**: **{entry['visual_consequence']}**\n")
        f.write(f"- **Continuity**: Inherits `{entry['entry_state']}` → Hands over `{entry['next_state']}`\n\n")
        f.write("---\n\n")

print(f"Saved Markdown choreography map to {md_out_path}")
