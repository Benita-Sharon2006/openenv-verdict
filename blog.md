# VERDICT: Training an AI Attorney with OpenEnv

This is my first blog post. Before describing my problem statement, I need to say that I don't know a damn thing about Reinforcement Learning or LLMs. I started this hackathon despite the odds, and now I'm typing this in the middle of it, waiting for my code to finish running on Google Colab.

## The Problem

LLMs can answer legal questions — but they can't manage 8 simultaneous cases under pressure, protect threatened witnesses, counter surprise motions from opposing counsel, and keep clients happy all at once. This is a real capability gap that exists in every legal AI deployment today. **VERDICT** is the first open RL environment designed to close it.

It may not be necessary right now, but in the near future it will be — and I'm willing to bet on that.

## What VERDICT Does

VERDICT places an AI agent in the role of lead attorney at a law firm facing a corporate crisis. Every episode, the agent must manage 6 interconnected systems simultaneously:

- **Case Management** — real deadlines, priority triage across 8 cases
- **Evidence Locker** — forged documents to detect, chain of custody to repair
- **Witness Protection** — threatened witnesses cannot testify until protected
- **Courtroom** — surprise motions from opposing counsel to counter
- **Firm Operations** — client trust, media sentiment, settlements
- **Advanced Forensics** — DNA and digital evidence lab

Every decision cascades. A missed filing deadline tanks the firm's reputation. An unprotected witness cannot testify and the case collapses. A weak motion drops jury sentiment. The agent must learn to prioritise correctly under pressure — with 20 available actions and a 12-dimensional reward signal.

## Training

We trained Qwen2.5-1.5B-Instruct using GRPO with Unsloth on 200 episodes across 3 difficulty levels. Training ran for 100 steps on a T4 GPU.

## Results

The agent improved from a reward of **0.326 → 0.550** — a 68% improvement in 100 steps. It learned to protect threatened witnesses before preparing them, analyze evidence before calling witnesses, and file motions with strong legal arguments.

![Reward Curve](reward_curve.png)

## Why This Matters

VERDICT will not solve cases faster than humans today. It cannot reason about actual case law or make moral judgments. But the point is not to replace lawyers — it is to create a training environment where future AI systems can practice legal decision-making the same way chess engines practiced chess.

Right now, no such public training environment exists. VERDICT is that first step.

## Links

- HuggingFace Space: https://huggingface.co/spaces/BenitaSharon/openenv-verdict
- GitHub: https://github.com/Benita-Sharon2006/openenv-verdict
- Colab Notebook: https://colab.research.google.com/drive/1DN-MkNoK2dfpEbKpJYYu11ONL6Adx308