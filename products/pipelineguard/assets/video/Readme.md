# PipelineGuard – Video Copy & Demo Assets

This directory stores the official product demo materials for PipelineGuard.

## Purpose
Demonstrates zero-trust CI/CD enforcement and scoring as part of the GuardSuite Pipeline pillar.

## Contents
- `video.yml` — Copy specification for the product video.
- `demo/plan_bad.json` — Triggers 1–2 deterministic pipeline violations.
- `demo/plan_guard.json` — Optional plan for deeper analysis.
- `repro_notes.md` — Full reproduction metadata.

## Deterministic Video Rules
- demo plans must remain unchanged after recording.
- Output hash must match expected value.
- Fixed terminal preset must be used.
- Duration target: 8–12 seconds.

## Recording Command
