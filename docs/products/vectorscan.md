

# VectorScan (v2.0.0)

Free, deterministic Terraform plan scanner for vector databases, embedding pipelines, and RAG-like architectures.


## Overview
VectorScan provides fast, deterministic governance and security scanning
for vector-serving infrastructure, embedding storage, and RAG
configuration patterns. It emits canonical schema–aligned output,
integrates seamlessly with Playground, and feeds GuardScore and
GuardBoard for scoring and reporting. VectorScan is the top-of-funnel
entry point into the GuardSuite ecosystem.


## Features


### VEC-FEAT-001 — Public Endpoint Detection
- Severity: **N/A**
- Description: Detects vector indices exposed to global CIDRs.

### VEC-FEAT-004 — Embedding Storage Encryption Check
- Severity: **N/A**
- Description: Flags storage lacking encryption-at-rest.

### VEC-FEAT-020 — IAM Wildcard Detection
- Severity: **N/A**
- Description: Detects IAM roles with unsafe vector path wildcards.

### VEC-FEAT-030 — Retrieval Pipeline Configuration Safety
- Severity: **N/A**
- Description: Detects missing filters, PII omissions, or risky retrieval params.



## FixPack (sample)


	


_FixPack metadata will be published when remediation snippets are available._


## Marketing
Secure your vector stack with instant, deterministic scans.

Get a quick GuardScore — /playground

> Snapshot generated from guardsuite-specs at commit `unknown`.