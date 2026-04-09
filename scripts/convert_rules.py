import json
from pathlib import Path

SRC = Path("rules.json")
DST = Path("generated/proxy_rules.yaml")

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

    lines = ["payload:"]
    for domain in sorted(result):
        lines.append(f"  - DOMAIN-SUFFIX,{domain}")

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()