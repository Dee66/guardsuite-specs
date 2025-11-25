# Strategy-D Scaffolding Phase 3 — Overview

**Purpose:**  
Establish the design and workflow scaffolding required for future demo ingestion,
deterministic video reproduction, and CLI-based demo validation, without adding
or modifying any product content.

**This phase does NOT:**
- add demo plans
- update demo_version.yml
- touch any product directories
- update CLI logic
- modify schemas

**This phase DOES:**
- define the CLI workflow contract for future demo runs
- define how real demo files will replace placeholders later
- define ingestion and snapshot behavior
- prepare workspace notes for future Strategy-D or Strategy-E expansions

**Key Areas:**
- CLI structure for demo validation
- How to replace plan_bad.json / plan_guard.json safely
- Snapshot contract for deterministic reproduction
- Demo version bump rules (carried forward from Phase 2)
- Guard vs Scan demo behavior alignment
- Notes for video recording automation

**Next:**
When Phase 3 is sealed, Phase 4 will introduce spec-based integration
for deterministic CLI demo reproduction.
