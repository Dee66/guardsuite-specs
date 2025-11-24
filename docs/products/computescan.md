

# ComputeScan (v2.0.0)

Free, deterministic scanner for GPU and compute waste, cost risk, and misconfiguration.


## Overview
ComputeScan analyzes Terraform plans and compute-heavy deployment manifests to
detect GPU provisioning waste, incorrect instance sizing, idle or orphaned GPUs,
and cost-risk patterns. It is deterministic, offline-capable, and designed to
serve as the top-of-funnel scanner in the GuardSuite compute pillar.


## Features


### CMP-FEAT-001 — Idle GPU Detection
- Severity: **N/A**
- Description: Detect GPU resources that are provisioned but show no usage indicators in config.

### CMP-FEAT-010 — Oversized Instance Detection
- Severity: **N/A**
- Description: Identify instances that are likely overprovisioned relative to workload hints.

### CMP-FEAT-020 — Autoscaling Risk Detection
- Severity: **N/A**
- Description: Detect autoscaling policies that may lead to runaway costs or instability.

### CMP-FEAT-030 — Spot/Preemptible Misuse
- Severity: **N/A**
- Description: Flags risky spot instance configurations or absence of fallbacks.



## FixPack (sample)


	


_FixPack metadata will be published when remediation snippets are available._


## Marketing
Detect GPU waste and cut cloud spend before it ships.

Get a quick GuardScore — /playground

> Snapshot generated from guardsuite-specs at commit `ada9477f7404f20ae367f703bc304917be627e58`.