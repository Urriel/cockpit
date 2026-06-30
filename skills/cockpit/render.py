#!/usr/bin/env python3
"""Render a cockpit JSON spec into a self-contained HTML dashboard.

The spec is *inlined* into template.html (not fetched), so the output works on
file:// and in mobile webviews where a sibling-.json fetch would be CORS-blocked.

Usage:
    python3 render.py gallery/morning-briefing.json
    python3 render.py gallery/morning-briefing.json out.html
"""
import json
import pathlib
import re
import sys

ISLAND = re.compile(
    r'(<script type="application/json" id="cockpit-data">)(.*?)(</script>)',
    re.S,
)


def render(spec_path: pathlib.Path, out_path: pathlib.Path) -> None:
    template = (pathlib.Path(__file__).parent / "template.html").read_text()
    data = spec_path.read_text()
    json.loads(data)  # validate the spec before injecting
    html = ISLAND.sub(
        lambda m: m.group(1) + "\n" + data.strip() + "\n" + m.group(3),
        template,
    )
    if "{{DATE}}" in html:
        raise SystemExit("error: data island was not replaced")
    out_path.write_text(html)
    print(f"wrote {out_path}")


def main(argv: list[str]) -> None:
    if not argv:
        raise SystemExit("usage: python3 render.py <spec.json> [out.html]")
    spec_path = pathlib.Path(argv[0])
    out_path = pathlib.Path(argv[1]) if len(argv) > 1 else spec_path.with_suffix(".html")
    render(spec_path, out_path)


if __name__ == "__main__":
    main(sys.argv[1:])
