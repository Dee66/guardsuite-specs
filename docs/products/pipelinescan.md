

# PipelineScan (v2.0.0)

Free CI/CD and supply-chain misconfiguration scanner for Terraform pipelines, GitHub Actions, GitLab CI, and container build workflows.


## Overview
PipelineScan provides deterministic, offline-first CI/CD and supply-chain
governance scanning for infrastructure pipelines. It detects workflow security
risks, unsafe permissions, missing integrity controls, unbounded actions,
weak artifact policies, and execution-boundary misconfigurations. It is the
entry point to the Pipeline pillar, feeding GuardScore and GuardBoard while
serving as the lightweight scanner for paste-to-scan CI/CD YAML and pipeline
manifests in Playground.


## Features


### PIPE-FEAT-001 — Workflow Permission Check
- Severity: **N/A**
- Description: Detect unsafe GitHub/GitLab permissions and overbroad scopes.

### PIPE-FEAT-005 — Signature & Integrity Validation
- Severity: **N/A**
- Description: Flags missing artifact signatures or provenance metadata.

### PIPE-FEAT-010 — Unsafe Trigger Detection
- Severity: **N/A**
- Description: Detects risky triggers such as unprotected pull_request events.

### PIPE-FEAT-020 — Secret Handling Safety
- Severity: **N/A**
- Description: Detects unsafe secret usage or missing restricted contexts.

### PIPE-FEAT-030 — Runner Security Checks
- Severity: **N/A**
- Description: Identifies weak runner isolation or unbounded self-hosted runners.



## FixPack (sample)


	


_FixPack metadata will be published when remediation snippets are available._


## Marketing
Secure your CI/CD pipeline before it reaches production.

Get a quick GuardScore — /playground

> Snapshot generated from guardsuite-specs at commit `unknown`.