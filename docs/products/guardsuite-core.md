

# GuardSuite Core (v2.0.0)

Canonical libraries, schemas, and CLI glue that power every GuardSuite pillar with deterministic parsing, validation, and renderer utilities.


## Overview
GuardSuite Core is the shared runtime, schema bundle, and CLI harness that all
GuardSuite scanners, blueprints, and governance tooling depend on. It contains
canonical JSON schemas, deterministic loader utilities, registry management for
FixPack packs, and the GuardScore contract definitions. Every pillar consumes
this package to guarantee consistent plan ingestion, issue serialization, and
doc/template rendering. GuardSuite Core is versioned alongside the pillars and
enforces strict backwards compatibility windows so downstream products can
adopt new schema features confidently.


## Features


### CORE-FEAT-010 — Canonical Schema Bundle
- Severity: **N/A**
- Description: Ships JSON Schema + Python contracts for every pillar.

### CORE-FEAT-020 — Deterministic Loader
- Severity: **N/A**
- Description: Shared plan/YAML ingestion with strict limits.

### CORE-FEAT-030 — FixPack Registry
- Severity: **N/A**
- Description: Registers remediation snippets and metadata for paid products.

### CORE-FEAT-040 — Template + Renderer SDK
- Severity: **N/A**
- Description: Jinja + Markdown renderer utilities for docs and snapshots.



## FixPack (sample)


	


_FixPack metadata will be published when remediation snippets are available._


## Marketing
Powering every GuardSuite scanner, blueprint, and dashboard.

Get a quick GuardScore — /playground

> Snapshot generated from guardsuite-specs at commit `unknown`.