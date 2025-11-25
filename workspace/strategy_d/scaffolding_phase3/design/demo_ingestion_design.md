# Demo Ingestion Design — Strategy-D Phase 3

This document defines how real demo plans will be introduced later in a safe,
non-breaking manner.

## Goals
- Preserve existing placeholders until real plans are ready.
- Ensure demos do not break normal CLI runs.
- Establish file naming rules for future demo ingestion.
- Support stable snapshot hashes for reproducible video capture.

## Ingestion Rules
1. plan_bad.json must represent the minimal failing Terraform plan for the product.
2. plan_guard.json must represent an enriched plan containing:
   - drift
   - waste
   - posture findings
   - metadata sufficient for demo triggers
3. All ingestion must preserve LF line endings.
4. No ingestion should modify demo_version.yml unless demo content changes.
5. Real demo plans must never live outside the product tree.

## Expected Future Flow (Phase 4+)
- Ingestion validation script
- Snapshot generation script
- Plan hash computation
- Output hash computation
- CLI “demo-mode” contract

No implementations created here — design only.
