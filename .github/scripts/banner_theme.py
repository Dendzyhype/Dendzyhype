"""Recolor the generated profile cards to match the banner palette.

Reads the built-in `radical` theme output and writes recolored copies
to profile-summary-card-output/dendzyhype/.
"""
from pathlib import Path

SRC = Path("profile-summary-card-output/radical")
DST = Path("profile-summary-card-output/dendzyhype")

# order matters: border first, because it shares its color with the background
REPLACEMENTS = [
    ('stroke="#141321"', 'stroke="#3a1a0c"'),   # border
    ("#141321", "#0f0806"),                      # background
    ("#fe428e", "#ff7a1a"),                      # title
    ("#a9fef7", "#ffd9c2"),                      # text
    ("#f8d847", "#ffb020"),                      # icons
    ("#ae81ff", "#ff5a16"),                      # chart bars
]


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for svg in sorted(SRC.glob("*.svg")):
        text = svg.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        (DST / svg.name).write_text(text, encoding="utf-8")
        print(f"themed {svg.name}")


if __name__ == "__main__":
    main()
