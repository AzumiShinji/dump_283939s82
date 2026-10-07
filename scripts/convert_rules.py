import json
from pathlib import Path

SRC = Path("rules.json")
GROUP_DIR = Path("generated")

def write_all(stem: str, domains: list[str]) -> None:
    """Write <stem>.yaml (Clash), <stem>.list (Shadowrocket) and <stem>.json (sing-box source)."""
    GROUP_DIR.mkdir(parents=True, exist_ok=True)
    (GROUP_DIR / f"{stem}.yaml").write_text(
        "\n".join(["payload:"] + [f"  - DOMAIN-SUFFIX,{d}" for d in domains]) + "\n",
        encoding="utf-8",
    )
    (GROUP_DIR / f"{stem}.list").write_text(
        "\n".join(f"DOMAIN-SUFFIX,{d}" for d in domains) + "\n", encoding="utf-8"
    )
    # compiled to .srs in CI: sing-box rule-set compile <stem>.json
    (GROUP_DIR / f"{stem}.json").write_text(
        json.dumps({"version": 3, "rules": [{"domain_suffix": domains}]}, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))

    result: set[str] = set()
    groups: dict[str, set[str]] = {}

    for rule in data.get("rules", []):
        name = rule.get("name")
        for domain in rule.get("domain_suffix", []):
            domain = domain.strip().lower()
            if not domain:
                continue
            if domain.startswith("."):
                domain = domain[1:]
            if name:
                groups.setdefault(name, set()).add(domain)
            else:
                result.add(domain)

    write_all("proxy_rules", sorted(result))

    # Named groups (e.g. "ai") go to their own <name>_rules.* files and are
    # excluded from proxy_rules.*, which holds only the unnamed (general) rules.
    for name, group in groups.items():
        write_all(f"{name}_rules", sorted(group))


if __name__ == "__main__":
    main()