#!/usr/bin/env python3
# COPILOT: Do not add new required fields without updating all existing products.
"""Validate GuardSuite product YAML files for required keys and structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

from jsonschema import Draft202012Validator
import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
PRODUCT_INDEX_PATH = PRODUCTS / "product_index.yml"
CANONICAL_SCHEMA_REL = "guardsuite-core/canonical_schema.json"
CANONICAL_SCHEMA_PATH = ROOT / CANONICAL_SCHEMA_REL
CANONICAL_REQUIRED_TOP_LEVEL = {
    "plan_id",
    "schema_version",
    "resources",
    "metadata",
}

REQUIRED_FIELDS = [
    "id",
    "name",
    "short_description",
    "long_description",
    "version",
    "features",
]

FUNNEL_STAGES = {"toplevel_funnel", "mid_funnel", "bottom_funnel"}
STABILITY_LEVELS = {"experimental", "beta", "ga"}
PRODUCT_TYPE_CATEGORY = {
    "free_scanner": "scan",
    "paid_blueprint": "experience",
    "experience": "experience",
    "scoring_engine": "core",
    "core": "core",
    "platform_service": "platform",
    "platform": "platform",
}
PRODUCT_VALIDATION_EXCLUSIONS = {"pillar-template", "guardsuite-template"}

SEMANTIC_DIR = ROOT / "semantic"
SEMANTIC_RULES_PATH = SEMANTIC_DIR / "semantic_rules.yml"
SEMANTIC_RULES_SCHEMA = SEMANTIC_DIR / "semantic_rules.schema.yml"
SEMANTIC_RULES_PREFIX = "Semantic rules schema failed: "
SEMANTIC_CATEGORIES_PATH = SEMANTIC_DIR / "semantic_categories.yml"
SEMANTIC_CATEGORIES_SCHEMA = SEMANTIC_DIR / "semantic_categories.schema.yml"
SEMANTIC_CATEGORIES_PREFIX = "Semantic categories schema failed: "
SEMANTIC_ENTITIES_PATH = SEMANTIC_DIR / "semantic_entities.yml"
SEMANTIC_ENTITIES_SCHEMA = SEMANTIC_DIR / "semantic_entities.schema.yml"
SEMANTIC_ENTITIES_PREFIX = "Semantic entities schema failed: "
SEMANTIC_CROSSREF_PATH = SEMANTIC_DIR / "semantic_crossref.yml"
SEMANTIC_CROSSREF_SCHEMA = SEMANTIC_DIR / "semantic_crossref.schema.yml"
SEMANTIC_CROSSREF_PREFIX = "Semantic crossref schema failed: "
SEMANTIC_REGISTRY_PATH = SEMANTIC_DIR / "semantic_registry.yml"
SEMANTIC_REGISTRY_SCHEMA = SEMANTIC_DIR / "semantic_registry.schema.yml"
SEMANTIC_REGISTRY_PREFIX = "Semantic registry schema failed: "
SEMANTIC_RULE_TEMPLATE_PATH = SEMANTIC_DIR / "semantic_rule_template.yml"
SEMANTIC_RULE_TEMPLATE_SCHEMA = SEMANTIC_DIR / "semantic_rule_template.schema.yml"
SEMANTIC_RULE_TEMPLATE_PREFIX = "Semantic rule template schema failed: "
SEMANTIC_RULE_MANIFEST_PATH = SEMANTIC_DIR / "semantic_rules_manifest.yml"
SEMANTIC_RULE_MANIFEST_SCHEMA = SEMANTIC_DIR / "semantic_rules_manifest.schema.yml"
SEMANTIC_RULE_MANIFEST_PREFIX = "Semantic rule manifest schema failed: "
SEMANTIC_INTEGRITY_PATH = SEMANTIC_DIR / "semantic_integrity.yml"
SEMANTIC_INTEGRITY_SCHEMA = SEMANTIC_DIR / "semantic_integrity.schema.yml"
SEMANTIC_INTEGRITY_PREFIX = "Semantic integrity schema failed: "
SEMANTIC_COVERAGE_PATH = SEMANTIC_DIR / "semantic_coverage.yml"
SEMANTIC_COVERAGE_SCHEMA = SEMANTIC_DIR / "semantic_coverage.schema.yml"
SEMANTIC_COVERAGE_PREFIX = "Semantic coverage schema failed: "
SEMANTIC_POLICY_PATH = SEMANTIC_DIR / "semantic_policy.yml"
SEMANTIC_POLICY_SCHEMA = SEMANTIC_DIR / "semantic_policy.schema.yml"
SEMANTIC_POLICY_PREFIX = "Semantic policy schema failed: "
SEMANTIC_SURFACE_INDEX_PATH = SEMANTIC_DIR / "semantic_surface_index.yml"
SEMANTIC_SURFACE_INDEX_SCHEMA = SEMANTIC_DIR / "semantic_surface_index.schema.yml"
SEMANTIC_SURFACE_INDEX_PREFIX = "Semantic surface index schema failed: "
SEMANTIC_SURFACE_GROUPS_PATH = SEMANTIC_DIR / "semantic_surface_groups.yml"
SEMANTIC_SURFACE_GROUPS_SCHEMA = SEMANTIC_DIR / "semantic_surface_groups.schema.yml"
SEMANTIC_SURFACE_GROUPS_PREFIX = "Semantic surface groups schema failed: "
SEMANTIC_SURFACE_MAP_PATH = SEMANTIC_DIR / "semantic_surface_map.yml"
SEMANTIC_SURFACE_MAP_SCHEMA = SEMANTIC_DIR / "semantic_surface_map.schema.yml"
SEMANTIC_SURFACE_MAP_PREFIX = "Semantic surface map schema failed: "
SEMANTIC_SURFACE_MATRIX_PATH = SEMANTIC_DIR / "semantic_surface_matrix.yml"
SEMANTIC_SURFACE_MATRIX_SCHEMA = SEMANTIC_DIR / "semantic_surface_matrix.schema.yml"
SEMANTIC_SURFACE_MATRIX_PREFIX = "Semantic surface matrix schema failed: "
SEMANTIC_SURFACE_MANIFEST_PATH = SEMANTIC_DIR / "semantic_surface_manifest.yml"
SEMANTIC_SURFACE_MANIFEST_SCHEMA = SEMANTIC_DIR / "semantic_surface_manifest.schema.yml"
SEMANTIC_SURFACE_MANIFEST_PREFIX = "Semantic surface manifest schema failed: "
SEMANTIC_GOVERNANCE_INDEX_PATH = SEMANTIC_DIR / "semantic_governance_index.yml"
SEMANTIC_GOVERNANCE_INDEX_SCHEMA = SEMANTIC_DIR / "semantic_governance_index.schema.yml"
SEMANTIC_GOVERNANCE_INDEX_PREFIX = "Semantic governance index schema failed: "
SEMANTIC_PROVENANCE_PATH = SEMANTIC_DIR / "semantic_provenance.yml"
SEMANTIC_PROVENANCE_SCHEMA = SEMANTIC_DIR / "semantic_provenance.schema.yml"
SEMANTIC_PROVENANCE_PREFIX = "Semantic provenance schema failed: "
SEMANTIC_CONFIGURATION_PATH = SEMANTIC_DIR / "semantic_configuration.yml"
SEMANTIC_CONFIGURATION_SCHEMA = SEMANTIC_DIR / "semantic_configuration.schema.yml"
SEMANTIC_CONFIGURATION_PREFIX = "Semantic configuration schema failed: "
SEMANTIC_RUNTIME_PATH = SEMANTIC_DIR / "semantic_runtime.yml"
SEMANTIC_RUNTIME_SCHEMA = SEMANTIC_DIR / "semantic_runtime.schema.yml"
SEMANTIC_RUNTIME_PREFIX = "Semantic runtime schema failed: "
SEMANTIC_RUNTIME_ENVIRONMENT_PATH = SEMANTIC_DIR / "semantic_runtime_environment.yml"
SEMANTIC_RUNTIME_ENVIRONMENT_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_environment.schema.yml"
)
SEMANTIC_RUNTIME_ENVIRONMENT_PREFIX = "Semantic runtime environment schema failed: "
SEMANTIC_RUNTIME_CAPABILITIES_PATH = SEMANTIC_DIR / "semantic_runtime_capabilities.yml"
SEMANTIC_RUNTIME_CAPABILITIES_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capabilities.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITIES_PREFIX = "Semantic runtime capabilities schema failed: "
SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capabilities_registry.yml"
)
SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capabilities_registry.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_PREFIX = (
    "Semantic runtime capabilities registry schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_MATRIX_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_matrix.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MATRIX_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_matrix.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MATRIX_PREFIX = (
    "Semantic runtime capability matrix schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_manifest.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_manifest.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_PREFIX = (
    "Semantic runtime capability manifest schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_INDEX_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_index.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_INDEX_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_index.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_INDEX_PREFIX = (
    "Semantic runtime capability index schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_MAP_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_map.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MAP_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_map.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_MAP_PREFIX = (
    "Semantic runtime capability map schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_GROUPS_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_groups.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_GROUPS_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_groups.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_GROUPS_PREFIX = (
    "Semantic runtime capability groups schema failed: "
)
SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_PATH = (
    SEMANTIC_DIR / "semantic_runtime_capability_topology.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_SCHEMA = (
    SEMANTIC_DIR / "semantic_runtime_capability_topology.schema.yml"
)
SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_PREFIX = (
    "Semantic runtime capability topology schema failed: "
)
PILLAR_TEMPLATE_SPEC_PATH = PRODUCTS / "pillar-template.yml"
PILLAR_TEMPLATE_SCHEMA_PATH = (
    ROOT / "products" / "schema" / "pillar-template.schema.yml"
)
PILLAR_TEMPLATE_SCHEMA_PREFIX = "Pillar template schema failed: "

ISSUEDICT_REQUIRED_FIELDS = (
    "id",
    "severity",
    "title",
    "description",
    "remediation_hint",
    "remediation_difficulty",
)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_semantic_rules() -> None:
    if not SEMANTIC_RULES_PATH.exists():
        raise FileNotFoundError(
            "semantic_rules.yml missing; bootstrap semantic governance"
        )
    if not SEMANTIC_RULES_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_rules.schema.yml missing; bootstrap semantic governance"
        )
    rules_payload = load_yaml(SEMANTIC_RULES_PATH)
    schema_payload = load_yaml(SEMANTIC_RULES_SCHEMA)
    validator = Draft202012Validator(schema_payload)
    errors = sorted(validator.iter_errors(rules_payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_categories() -> None:
    if not SEMANTIC_CATEGORIES_PATH.exists():
        raise FileNotFoundError(
            "semantic_categories.yml missing; bootstrap semantic taxonomy"
        )
    if not SEMANTIC_CATEGORIES_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_categories.schema.yml missing; bootstrap semantic taxonomy"
        )
    payload = load_yaml(SEMANTIC_CATEGORIES_PATH)
    schema = load_yaml(SEMANTIC_CATEGORIES_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_entities() -> None:
    if not SEMANTIC_ENTITIES_PATH.exists():
        raise FileNotFoundError(
            "semantic_entities.yml missing; bootstrap semantic entities"
        )
    if not SEMANTIC_ENTITIES_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_entities.schema.yml missing; bootstrap semantic entities"
        )
    payload = load_yaml(SEMANTIC_ENTITIES_PATH)
    schema = load_yaml(SEMANTIC_ENTITIES_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_crossref() -> None:
    if not SEMANTIC_CROSSREF_PATH.exists():
        raise FileNotFoundError(
            "semantic_crossref.yml missing; bootstrap semantic crossref"
        )
    if not SEMANTIC_CROSSREF_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_crossref.schema.yml missing; bootstrap semantic crossref"
        )
    payload = load_yaml(SEMANTIC_CROSSREF_PATH)
    schema = load_yaml(SEMANTIC_CROSSREF_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_registry() -> None:
    if not SEMANTIC_REGISTRY_PATH.exists():
        raise FileNotFoundError(
            "semantic_registry.yml missing; bootstrap semantic registry"
        )
    if not SEMANTIC_REGISTRY_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_registry.schema.yml missing; bootstrap semantic registry"
        )
    payload = load_yaml(SEMANTIC_REGISTRY_PATH)
    schema = load_yaml(SEMANTIC_REGISTRY_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_rule_template() -> None:
    if not SEMANTIC_RULE_TEMPLATE_PATH.exists():
        raise FileNotFoundError(
            "semantic_rule_template.yml missing; bootstrap semantic rule template"
        )
    if not SEMANTIC_RULE_TEMPLATE_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_rule_template.schema.yml missing; bootstrap semantic rule template"
        )
    payload = load_yaml(SEMANTIC_RULE_TEMPLATE_PATH)
    schema = load_yaml(SEMANTIC_RULE_TEMPLATE_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_rule_manifest() -> None:
    if not SEMANTIC_RULE_MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "semantic_rules_manifest.yml missing; bootstrap semantic rule manifest"
        )
    if not SEMANTIC_RULE_MANIFEST_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_rules_manifest.schema.yml missing; bootstrap semantic rule manifest"
        )
    payload = load_yaml(SEMANTIC_RULE_MANIFEST_PATH)
    schema = load_yaml(SEMANTIC_RULE_MANIFEST_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_integrity() -> None:
    if not SEMANTIC_INTEGRITY_PATH.exists():
        raise FileNotFoundError(
            "semantic_integrity.yml missing; bootstrap semantic integrity"
        )
    if not SEMANTIC_INTEGRITY_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_integrity.schema.yml missing; bootstrap semantic integrity"
        )
    payload = load_yaml(SEMANTIC_INTEGRITY_PATH)
    schema = load_yaml(SEMANTIC_INTEGRITY_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_coverage() -> None:
    if not SEMANTIC_COVERAGE_PATH.exists():
        raise FileNotFoundError(
            "semantic_coverage.yml missing; bootstrap semantic coverage"
        )
    if not SEMANTIC_COVERAGE_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_coverage.schema.yml missing; bootstrap semantic coverage"
        )
    payload = load_yaml(SEMANTIC_COVERAGE_PATH)
    schema = load_yaml(SEMANTIC_COVERAGE_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_policy() -> None:
    if not SEMANTIC_POLICY_PATH.exists():
        raise FileNotFoundError(
            "semantic_policy.yml missing; bootstrap semantic policy"
        )
    if not SEMANTIC_POLICY_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_policy.schema.yml missing; bootstrap semantic policy"
        )
    payload = load_yaml(SEMANTIC_POLICY_PATH)
    schema = load_yaml(SEMANTIC_POLICY_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_surface_index() -> None:
    if not SEMANTIC_SURFACE_INDEX_PATH.exists():
        raise FileNotFoundError(
            "semantic_surface_index.yml missing; bootstrap semantic surface index"
        )
    if not SEMANTIC_SURFACE_INDEX_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_surface_index.schema.yml missing; bootstrap semantic surface index"
        )
    payload = load_yaml(SEMANTIC_SURFACE_INDEX_PATH)
    schema = load_yaml(SEMANTIC_SURFACE_INDEX_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_surface_groups() -> None:
    if not SEMANTIC_SURFACE_GROUPS_PATH.exists():
        raise FileNotFoundError(
            "semantic_surface_groups.yml missing; bootstrap semantic surface groups"
        )
    if not SEMANTIC_SURFACE_GROUPS_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_surface_groups.schema.yml missing; bootstrap semantic surface groups"
        )
    payload = load_yaml(SEMANTIC_SURFACE_GROUPS_PATH)
    schema = load_yaml(SEMANTIC_SURFACE_GROUPS_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_surface_map() -> None:
    if not SEMANTIC_SURFACE_MAP_PATH.exists():
        raise FileNotFoundError(
            "semantic_surface_map.yml missing; bootstrap semantic surface map"
        )
    if not SEMANTIC_SURFACE_MAP_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_surface_map.schema.yml missing; bootstrap semantic surface map"
        )
    payload = load_yaml(SEMANTIC_SURFACE_MAP_PATH)
    schema = load_yaml(SEMANTIC_SURFACE_MAP_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_surface_matrix() -> None:
    if not SEMANTIC_SURFACE_MATRIX_PATH.exists():
        raise FileNotFoundError(
            "semantic_surface_matrix.yml missing; bootstrap semantic surface matrix"
        )
    if not SEMANTIC_SURFACE_MATRIX_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_surface_matrix.schema.yml missing; bootstrap semantic surface matrix"
        )
    payload = load_yaml(SEMANTIC_SURFACE_MATRIX_PATH)
    schema = load_yaml(SEMANTIC_SURFACE_MATRIX_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_surface_manifest() -> None:
    if not SEMANTIC_SURFACE_MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "semantic_surface_manifest.yml missing; bootstrap semantic surface manifest"
        )
    if not SEMANTIC_SURFACE_MANIFEST_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_surface_manifest.schema.yml missing; bootstrap semantic surface manifest"
        )
    payload = load_yaml(SEMANTIC_SURFACE_MANIFEST_PATH)
    schema = load_yaml(SEMANTIC_SURFACE_MANIFEST_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_governance_index() -> None:
    if not SEMANTIC_GOVERNANCE_INDEX_PATH.exists():
        raise FileNotFoundError(
            "semantic_governance_index.yml missing; bootstrap semantic governance index"
        )
    if not SEMANTIC_GOVERNANCE_INDEX_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_governance_index.schema.yml missing; bootstrap semantic governance index"
        )
    payload = load_yaml(SEMANTIC_GOVERNANCE_INDEX_PATH)
    schema = load_yaml(SEMANTIC_GOVERNANCE_INDEX_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_provenance() -> None:
    if not SEMANTIC_PROVENANCE_PATH.exists():
        raise FileNotFoundError(
            "semantic_provenance.yml missing; bootstrap semantic provenance"
        )
    if not SEMANTIC_PROVENANCE_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_provenance.schema.yml missing; bootstrap semantic provenance"
        )
    payload = load_yaml(SEMANTIC_PROVENANCE_PATH)
    schema = load_yaml(SEMANTIC_PROVENANCE_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_configuration() -> None:
    if not SEMANTIC_CONFIGURATION_PATH.exists():
        raise FileNotFoundError(
            "semantic_configuration.yml missing; bootstrap semantic configuration"
        )
    if not SEMANTIC_CONFIGURATION_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_configuration.schema.yml missing; bootstrap semantic configuration"
        )
    payload = load_yaml(SEMANTIC_CONFIGURATION_PATH)
    schema = load_yaml(SEMANTIC_CONFIGURATION_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime() -> None:
    if not SEMANTIC_RUNTIME_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime.yml missing; bootstrap semantic runtime"
        )
    if not SEMANTIC_RUNTIME_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime.schema.yml missing; bootstrap semantic runtime"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_environment() -> None:
    if not SEMANTIC_RUNTIME_ENVIRONMENT_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_environment.yml missing; bootstrap semantic runtime environment"
        )
    if not SEMANTIC_RUNTIME_ENVIRONMENT_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_environment.schema.yml missing; bootstrap semantic runtime environment"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_ENVIRONMENT_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_ENVIRONMENT_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capabilities() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITIES_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capabilities.yml missing; bootstrap semantic runtime capabilities"
        )
    if not SEMANTIC_RUNTIME_CAPABILITIES_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capabilities.schema.yml missing; bootstrap semantic runtime capabilities"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITIES_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITIES_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capabilities_registry() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capabilities_registry.yml missing; bootstrap semantic runtime capabilities registry"
        )
    if not SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capabilities_registry.schema.yml missing; bootstrap semantic runtime capabilities registry"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_matrix() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_MATRIX_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_matrix.yml missing; bootstrap semantic runtime capability matrix"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_MATRIX_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_matrix.schema.yml missing; bootstrap semantic runtime capability matrix"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MATRIX_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MATRIX_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_manifest() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_manifest.yml missing; bootstrap semantic runtime capability manifest"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_manifest.schema.yml missing; bootstrap semantic runtime capability manifest"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_index() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_INDEX_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_index.yml missing; bootstrap semantic runtime capability index"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_INDEX_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_index.schema.yml missing; bootstrap semantic runtime capability index"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_INDEX_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_INDEX_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_map() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_MAP_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_map.yml missing; bootstrap semantic runtime capability map"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_MAP_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_map.schema.yml missing; bootstrap semantic runtime capability map"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MAP_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_MAP_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_groups() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_GROUPS_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_groups.yml missing; bootstrap semantic runtime capability groups"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_GROUPS_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_groups.schema.yml missing; bootstrap semantic runtime capability groups"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_GROUPS_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_GROUPS_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_semantic_runtime_capability_topology() -> None:
    if not SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_PATH.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_topology.yml missing; bootstrap semantic runtime capability topology"
        )
    if not SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_SCHEMA.exists():
        raise FileNotFoundError(
            "semantic_runtime_capability_topology.schema.yml missing; bootstrap semantic runtime capability topology"
        )
    payload = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_PATH)
    schema = load_yaml(SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def _load_pillar_template() -> None:
    if not PILLAR_TEMPLATE_SPEC_PATH.exists():
        raise FileNotFoundError(
            "products/pillar-template.yml missing; bootstrap pillar template spec"
        )
    if not PILLAR_TEMPLATE_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            "products/schema/pillar-template.schema.yml missing; bootstrap pillar template schema"
        )
    payload = load_yaml(PILLAR_TEMPLATE_SPEC_PATH)
    schema = load_yaml(PILLAR_TEMPLATE_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path)
        detail = first.message
        raise ValueError(f"{location}: {detail}" if location else detail)


def load_product_index() -> Dict[str, dict]:
    if not PRODUCT_INDEX_PATH.exists():
        raise FileNotFoundError(
            "products/product_index.yml missing; run index alignment."
        )
    index_doc = load_yaml(PRODUCT_INDEX_PATH) or {}
    entries = index_doc.get("products", [])
    mapping: Dict[str, dict] = {}
    for entry in entries:
        pid = entry.get("product_id")
        if not pid:
            continue
        mapping[pid] = entry
    return mapping


def _expected_category(product_type: str | None) -> str:
    return PRODUCT_TYPE_CATEGORY.get(product_type or "", "core")


def _load_canonical_schema() -> dict:
    if not CANONICAL_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Canonical schema missing at {CANONICAL_SCHEMA_REL}; run canonical schema scaffolding"
        )
    try:
        payload = json.loads(CANONICAL_SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Canonical schema JSON invalid at {CANONICAL_SCHEMA_REL}: {exc}"
        ) from exc
    if payload.get("type") != "object":
        raise ValueError(
            "Canonical schema sanity check failed: top-level type must be 'object'"
        )
    if not isinstance(payload.get("properties"), dict):
        raise ValueError(
            "Canonical schema sanity check failed: missing properties object"
        )
    if not isinstance(payload.get("required"), list):
        raise ValueError("Canonical schema sanity check failed: missing required list")
    missing_required = CANONICAL_REQUIRED_TOP_LEVEL - set(payload.get("required", []))
    if missing_required:
        raise ValueError(
            "Canonical schema sanity check failed: required list missing keys "
            + ", ".join(sorted(missing_required))
        )
    missing_properties = CANONICAL_REQUIRED_TOP_LEVEL - set(
        payload.get("properties", {}).keys()
    )
    if missing_properties:
        raise ValueError(
            "Canonical schema sanity check failed: properties block missing keys "
            + ", ".join(sorted(missing_properties))
        )
    return payload


def _uses_canonical_schema(product: dict) -> bool:
    architecture = product.get("architecture") or {}
    return architecture.get("schema_source") == CANONICAL_SCHEMA_REL


def _validate_issue_samples(product: dict, path: Path) -> List[str]:
    errors: List[str] = []
    sample_data = product.get("sample_data") or {}
    deterministic = sample_data.get("deterministic_response") or {}
    issues = deterministic.get("issues")
    if not issues:
        return errors
    if not isinstance(issues, list):
        errors.append(
            f"{path}: sample_data.deterministic_response.issues must be a list when present"
        )
        return errors
    for idx, issue in enumerate(issues):
        if not isinstance(issue, dict):
            errors.append(
                f"{path}: issue #{idx} in sample_data.deterministic_response must be an object per #ISSUEDICT_SCHEMA"
            )
            continue
        for field in ISSUEDICT_REQUIRED_FIELDS:
            if not issue.get(field):
                errors.append(
                    f"{path}: sample_data.deterministic_response.issues[{idx}] missing '{field}' required by #ISSUEDICT_SCHEMA"
                )
    return errors


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GuardSuite product validator")
    parser.add_argument(
        "--check-canonical",
        action="store_true",
        help="Only verify canonical schema presence and structure",
    )
    parser.add_argument(
        "--product",
        dest="products",
        action="append",
        default=None,
        help="Validate only the specified product id (can be passed multiple times)",
    )
    return parser.parse_args()


def _run_canonical_check_only() -> None:
    try:
        _load_canonical_schema()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Canonical schema CI check failed: {exc}", file=sys.stderr)
        sys.exit(1)
    print("canonical_schema: OK")
    sys.exit(0)


def validate_product(
    product: dict,
    path: Path,
    index: Dict[str, dict],
    known_products: set[str],
) -> List[str]:
    errors: List[str] = []
    for field in REQUIRED_FIELDS:
        if field not in product:
            errors.append(f"{path}: missing required field '{field}'")
            continue
        if product[field] in (None, ""):
            errors.append(f"{path}: field '{field}' cannot be empty")
    features = product.get("features")
    if not isinstance(features, list):
        errors.append(f"{path}: 'features' must be a list")
    else:
        for idx, feature in enumerate(features):
            if not isinstance(feature, dict):
                errors.append(f"{path}: feature #{idx} must be an object")

    metadata = product.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{path}: metadata block missing or not an object")
    else:
        pricing_ref = metadata.get("pricing_reference")
        if not isinstance(pricing_ref, str) or not pricing_ref.startswith("pricing/"):
            errors.append(
                f"{path}: metadata.pricing_reference must point into pricing/"
            )
        funnel_stage = metadata.get("funnel_stage")
        if funnel_stage not in FUNNEL_STAGES:
            errors.append(
                f"{path}: metadata.funnel_stage must be one of {sorted(FUNNEL_STAGES)}"
            )
        ux_goals = metadata.get("ux_goals", [])
        if not isinstance(ux_goals, list) or not ux_goals:
            errors.append(f"{path}: metadata.ux_goals must be a non-empty list")

    governance = product.get("governance")
    if not isinstance(governance, dict):
        errors.append(f"{path}: governance block missing or not an object")
    else:
        for key in ("spec_version", "last_reviewed", "owner", "stability_level"):
            if not governance.get(key):
                errors.append(f"{path}: governance.{key} missing or empty")
        last_reviewed = governance.get("last_reviewed", "")
        if last_reviewed and not re.match(r"^20\d{2}-\d{2}-\d{2}$", last_reviewed):
            errors.append(
                f"{path}: governance.last_reviewed must be YYYY-MM-DD in 2000s"
            )
        stability = governance.get("stability_level")
        if stability and stability not in STABILITY_LEVELS:
            errors.append(
                f"{path}: governance.stability_level must be one of {sorted(STABILITY_LEVELS)}"
            )

    related_products = product.get("related_products")
    if related_products is None:
        errors.append(f"{path}: related_products must be defined (can be empty list)")
        related_products_list: List[str] = []
    elif not isinstance(related_products, list):
        errors.append(f"{path}: related_products must be a list")
        related_products_list = []
    else:
        related_products_list = related_products
        for rel in related_products_list:
            if rel not in known_products:
                errors.append(
                    f"{path}: related_products entry '{rel}' does not map to a known product spec"
                )

    contract_ref = product.get("contract_ref", None)
    if contract_ref is not None and not isinstance(contract_ref, str):
        errors.append(f"{path}: contract_ref must be a string or null")
    elif isinstance(contract_ref, str):
        target = ROOT / contract_ref
        if not target.exists():
            errors.append(f"{path}: contract_ref file {contract_ref} missing on disk")
        else:
            try:
                load_yaml(target)
            except yaml.YAMLError as exc:  # pragma: no cover
                errors.append(f"{path}: contract_ref YAML invalid: {exc}")

    architecture = product.get("architecture") or {}
    references = product.get("references") or {}
    product_id = product.get("id")
    index_entry = index.get(product_id)
    rel_spec_path = path.relative_to(ROOT).as_posix()
    if not index_entry:
        errors.append(f"{path}: missing entry in product_index.yml for '{product_id}'")
    else:
        if index_entry.get("spec_path") != rel_spec_path:
            errors.append(
                f"{path}: product_index spec_path mismatch (expected {rel_spec_path})"
            )
        if index_entry.get("version") != product.get("version"):
            errors.append(
                f"{path}: product_index version mismatch ({index_entry.get('version')} != {product.get('version')})"
            )
        expected_category = _expected_category(product.get("product_type"))
        if index_entry.get("category") != expected_category:
            errors.append(
                f"{path}: product_index category '{index_entry.get('category')}' != expected '{expected_category}'"
            )
        schema_path = index_entry.get("schema_path")
        if schema_path:
            schema_target = ROOT / schema_path
            if not schema_target.exists():
                errors.append(f"{path}: schema_path {schema_path} missing on disk")
        entry_contract = index_entry.get("contract_ref")
        if (entry_contract or None) != (contract_ref or None):
            errors.append(
                f"{path}: contract_ref mismatch between spec and product_index"
            )
        entry_related = sorted(index_entry.get("related_products", []))
        if sorted(related_products_list) != entry_related:
            errors.append(
                f"{path}: related_products differ from product_index definition"
            )

    uses_canonical_schema = _uses_canonical_schema(product)
    if uses_canonical_schema:
        if not references or not isinstance(references, dict):
            errors.append(
                f"{path}: references block must exist for canonical schema products"
            )
        elif references.get("canonical_schema") != CANONICAL_SCHEMA_REL:
            errors.append(
                f"{path}: references.canonical_schema must point to {CANONICAL_SCHEMA_REL} when schema_source is canonical"
            )
        required_interfaces = architecture.get("required_interfaces")
        if not isinstance(required_interfaces, list) or not required_interfaces:
            errors.append(
                f"{path}: canonical schema products must declare architecture.required_interfaces per master evaluator guidance"
            )
        else:
            for iface in required_interfaces:
                if not isinstance(iface, str) or not iface.strip():
                    errors.append(
                        f"{path}: architecture.required_interfaces entries must be non-empty strings"
                    )
        errors.extend(_validate_issue_samples(product, path))

    if product_id == "playground":
        matrix_snippet = product.get("compliance", {}).get("matrix_snippet")
        if not matrix_snippet:
            errors.append(
                f"{path}: compliance.matrix_snippet must point to traceability data"
            )
        else:
            matrix_path = ROOT / matrix_snippet
            if not matrix_path.exists():
                errors.append(
                    f"{path}: compliance matrix snippet {matrix_snippet} missing on disk"
                )
    return errors


def main() -> None:
    args = _parse_args()
    if args.check_canonical:
        _run_canonical_check_only()

    try:
        _load_canonical_schema()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Canonical schema load failed: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_rules()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RULES_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_categories()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_CATEGORIES_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_entities()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_ENTITIES_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_crossref()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_CROSSREF_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_registry()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_REGISTRY_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_rule_template()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RULE_TEMPLATE_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_rule_manifest()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RULE_MANIFEST_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_integrity()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_INTEGRITY_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_coverage()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_COVERAGE_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_policy()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_POLICY_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_surface_index()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_SURFACE_INDEX_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_surface_groups()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_SURFACE_GROUPS_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_surface_map()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_SURFACE_MAP_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_surface_matrix()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_SURFACE_MATRIX_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_surface_manifest()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_SURFACE_MANIFEST_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_governance_index()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_GOVERNANCE_INDEX_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_provenance()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_PROVENANCE_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_configuration()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_CONFIGURATION_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_environment()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_ENVIRONMENT_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capabilities()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITIES_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capabilities_registry()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITIES_REGISTRY_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_matrix()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_MATRIX_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_manifest()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_MANIFEST_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_index()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_INDEX_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_map()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_MAP_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_groups()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_GROUPS_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_semantic_runtime_capability_topology()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{SEMANTIC_RUNTIME_CAPABILITY_TOPOLOGY_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _load_pillar_template()
    except (FileNotFoundError, ValueError) as exc:
        print(f"{PILLAR_TEMPLATE_SCHEMA_PREFIX}{exc}", file=sys.stderr)
        sys.exit(1)

    product_files = sorted(
        p
        for p in PRODUCTS.glob("*.yml")
        if not p.name.endswith("_worksheet.yml")
        and p.name not in {"guardsuite_master_spec.yml", "product_index.yml"}
        and p.stem not in PRODUCT_VALIDATION_EXCLUSIONS
    )
    if not product_files:
        print("No product specs found under products/", file=sys.stderr)
        sys.exit(1)

    all_product_ids = {path.stem for path in product_files}
    requested: set[str] | None = None
    if args.products:
        requested = {prod.strip() for prod in args.products if prod and prod.strip()}
        missing = requested - all_product_ids
        if missing:
            print(
                "Product validation failed:",
                *[f" - unknown product id '{name}'" for name in sorted(missing)],
                sep="\n",
                file=sys.stderr,
            )
            sys.exit(1)
        product_files = [path for path in product_files if path.stem in requested]
        if not product_files:
            print("No matching product specs after filtering", file=sys.stderr)
            sys.exit(1)
    try:
        product_index = load_product_index()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    known_products = all_product_ids
    problems: List[str] = []
    seen_ids: set[str] = set()
    for file_path in product_files:
        product = load_yaml(file_path)
        product_id = product.get("id")
        seen_ids.add(product_id)
        problems.extend(
            validate_product(product, file_path, product_index, known_products)
        )
    missing_in_specs = (
        set(product_index.keys()) - seen_ids - PRODUCT_VALIDATION_EXCLUSIONS
    )
    if requested is not None:
        missing_in_specs &= requested
    if missing_in_specs:
        problems.append(
            "product_index.yml lists products without specs: "
            + ", ".join(sorted(missing_in_specs))
        )
    if problems:
        print("Product validation failed:")
        for issue in problems:
            print(f" - {issue}")
        sys.exit(1)
    print(
        f"Validated {len(product_files)} product spec(s) against index and metadata requirements."
    )


if __name__ == "__main__":
    main()
