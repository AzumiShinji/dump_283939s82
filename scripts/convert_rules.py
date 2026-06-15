import json
from pathlib import Path

SRC = Path("rules.json")
DST_YAML = Path("generated/proxy_rules.yaml")
DST_LIST = Path("generated/proxy_rules.list")

def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))

    result: set[str] = set()

    for rule in data.get("rules", []):
        for domain in rule.get("domain_suffix", []):
            domain = domain.strip().lower()
            if not domain:
                continue
            if domain.startswith("."):
                domain = domain[1:]
            result.add(domain)

    domains = sorted(result)

    DST_YAML.parent.mkdir(parents=True, exist_ok=True)

    yaml_lines = ["payload:"] + [f"  - DOMAIN-SUFFIX,{d}" for d in domains]
    DST_YAML.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")

    list_lines = [f"DOMAIN-SUFFIX,{d}" for d in domains]
    DST_LIST.write_text("\n".join(list_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()