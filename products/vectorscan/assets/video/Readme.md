# VectorScan – Video Copy & Demo Assets

This folder contains the video script, demo inputs, and reproduction notes for the VectorScan product video.

## Purpose
The VectorScan demo video shows how the CLI instantly detects vector database misconfigurations with a single command.

## Contents
- `video.yml` — Copy used for the 8–12 second product video.
- `demo/plan_bad.json` — Minimal failing Terraform plan used to trigger deterministic output.
- `demo/plan_guard.json` — (Optional) Additional plan for Guard comparison.
- `repro_notes.md` — Terminal preset, theme, command, and output hash for deterministic re-recording.

## Deterministic Video Rules
- No changes may be made to `plan_bad.json` after release.
- Output must match the expected hash in `repro_notes.md`.
- Terminal preset (font, size, theme) must match reproduction notes.
- Video length target: **8–12 seconds**.

## Recording Command
