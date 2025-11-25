# ComputeScan – Video Copy & Demo Assets

This folder houses the official ComputeScan demo video materials and deterministic test plans.

## Purpose
The ComputeScan video demonstrates instant detection of GPU and inference waste in Terraform plans.

## Contents
- `video.yml` — Copy for the short demo video.
- `demo/plan_bad.json` — Minimal plan showing GPU waste.
- `demo/plan_guard.json` — Optional advanced plan for deeper findings.
- `repro_notes.md` — All parameters required to reproduce the video exactly.

## Deterministic Video Rules
- `plan_bad.json` is immutable after v1.0 recording.
- Output hash must match the expected value.
- Fixed terminal preset required (see reproduction notes).
- Target duration: 8–12 seconds.

## Recording Command
