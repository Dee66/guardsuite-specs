import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.bootstrap_api import get_bootstrap, regenerate_bootstrap
from api.db import load_db
from api.products import create_product
from api.validate import validate_product
from api.ci_integration import (
    ci_regenerate_all,
    ci_structural_check,
    ci_validate_products,
)

parser = argparse.ArgumentParser(prog="guard-specs-cli")

sub = parser.add_subparsers(dest="cmd")

p_list = sub.add_parser("product:list")

p_create = sub.add_parser("product:create")
p_create.add_argument("--id", required=True)
p_create.add_argument("--spec")
p_create.add_argument("--checklist")
p_create.add_argument("--instructions")

p_val = sub.add_parser("product:validate")
p_val.add_argument("--id", required=True)

p_boot = sub.add_parser("bootstrap:generate")
p_boot.add_argument("--id", required=True)

p_boot_get = sub.add_parser("bootstrap:get")
p_boot_get.add_argument("--id", required=True)

p_ci_val = sub.add_parser("ci:validate")

p_ci_boot = sub.add_parser("ci:bootstrap")

p_ci_struct = sub.add_parser("ci:structural")


def main():
    args = parser.parse_args()
    if args.cmd == "product:list":
        print(json.dumps(load_db(), indent=2))
    elif args.cmd == "product:create":
        payload = {
            "spec_yaml": args.spec or "",
            "checklist_yaml": args.checklist or "",
            "gpt_instructions_yaml": args.instructions or "",
        }
        out = create_product(args.id, payload)
        print(json.dumps(out, indent=2))
    elif args.cmd == "product:validate":
        out = validate_product(args.id)
        print(json.dumps(out, indent=2))
    elif args.cmd == "bootstrap:generate":
        out = regenerate_bootstrap(args.id)
        print(json.dumps(out, indent=2))
    elif args.cmd == "bootstrap:get":
        out = get_bootstrap(args.id)
        print(json.dumps(out, indent=2))
    elif args.cmd == "ci:validate":
        out = ci_validate_products()
        print(json.dumps(out, indent=2))
    elif args.cmd == "ci:bootstrap":
        out = ci_regenerate_all()
        print(json.dumps(out, indent=2))
    elif args.cmd == "ci:structural":
        out = ci_structural_check()
        print(json.dumps(out, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
