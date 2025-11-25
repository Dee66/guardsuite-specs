# VectorGuard – Video Copy & Demo Assets

This folder contains the video script, demo inputs, and deterministic reproduction notes for the VectorGuard video.

## Purpose
The VectorGuard demo showcases zero-trust vector infrastructure enforcement and the scoring model.

## Contents
- `video.yml` — Copy used in the product demo video.
- `demo/plan_bad.json` — Trigger minimal but meaningful IAM drift.
- `demo/plan_guard.json` — Used for advanced Guard behavior.
- `repro_notes.md` — Terminal + output hash for deterministic re-recording.

## Deterministic Video Rules
- No modifications to demo plans after release.
- Output snapshot must match expected hash.
- Use the same terminal preset for all GuardSuite videos.
- Duration target: 8–12 seconds.

## Recording Command
