import re
from pathlib import Path

SRC = Path("profile-summary-card-output/radical")
DST = Path("profile-summary-card-output/dendzyhype")

COLORS = [
    ('stroke="#141321"', 'stroke="#3a1a0c"'),
    ("#141321", "#0f0806"),
    ("#fe428e", "#ff7a1a"),
    ("#a9fef7", "#ffd9c2"),
    ("#f8d847", "#ffb020"),
    ("#ae81ff", "#ff5a16"),
]

BG_RECT = re.compile(r'<rect x="1" y="1" rx="5" ry="5"[^>]*></rect>')
TITLE = "font-size: 22px; fill: #ff7a1a;"
VIEWBOX = re.compile(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"')

DEFS = """<defs>
<linearGradient id="cBg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0F0806"/><stop offset="0.5" stop-color="#180B07"/><stop offset="1" stop-color="#0B0504"/>
</linearGradient>
<radialGradient id="cGlow1" cx="0.15" cy="0.1" r="0.7">
<stop offset="0" stop-color="#FF5A16" stop-opacity="0.26"/><stop offset="1" stop-color="#FF5A16" stop-opacity="0"/>
</radialGradient>
<radialGradient id="cGlow2" cx="0.92" cy="0.95" r="0.65">
<stop offset="0" stop-color="#FF2200" stop-opacity="0.32"/><stop offset="1" stop-color="#FF2200" stop-opacity="0"/>
</radialGradient>
<linearGradient id="cBar" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FFC46B"/><stop offset="0.5" stop-color="#FF5A16"/><stop offset="1" stop-color="#C1121F"/>
</linearGradient>
<linearGradient id="cBorder" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#FF5A16" stop-opacity="0.55"/><stop offset="1" stop-color="#C1121F" stop-opacity="0.25"/>
</linearGradient>
<linearGradient id="cTitle" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="100" y2="0" spreadMethod="repeat">
<stop offset="0" stop-color="#FF7A1A"/><stop offset="0.25" stop-color="#FFF0C9"/><stop offset="0.5" stop-color="#FFA033"/><stop offset="0.75" stop-color="#FF2A00"/><stop offset="1" stop-color="#FF7A1A"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="100 0" dur="2.5s" repeatCount="indefinite"/>
</linearGradient>
<pattern id="cGrid" width="20" height="20" patternUnits="userSpaceOnUse">
<path d="M20 0H0V20" fill="none" stroke="#FF6A1A" stroke-opacity="0.07"/>
</pattern>
<clipPath id="cClip"><rect x="1" y="1" width="{w}" height="{h}" rx="5" ry="5"/></clipPath>
</defs>
<g clip-path="url(#cClip)">
<rect x="1" y="1" width="{w}" height="{h}" fill="url(#cBg)"/>
<rect x="1" y="1" width="{w}" height="{h}" fill="url(#cGrid)"/>
<rect x="1" y="1" width="{w}" height="{h}" fill="url(#cGlow1)"/>
<rect x="1" y="1" width="{w}" height="{h}" fill="url(#cGlow2)"/>
<rect x="1" y="1" width="3" height="{h}" fill="url(#cBar)"/>
</g>
<rect x="1" y="1" width="{w}" height="{h}" rx="5" ry="5" fill="none" stroke="url(#cBorder)" stroke-width="1"/>"""

W, H = 400, 186
RESIZE = (
    ('width="340" height="200" viewBox="0 0 340 200"', f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"'),
    ('<text x="30" y="40" class="gpsc-item"', '<text x="30" y="36" class="gpsc-item"'),
    ('<g transform="translate(0,40)">', '<g transform="translate(0,32)">'),
    ('x="130" y=', 'x="150" y='),
    ('<g transform="translate(220,20)">', '<g transform="translate(275,20)">'),
    ('translate( 230, 80 )', 'translate( 310, 80 )'),
)
RESIZE_CARDS = {"3-stats.svg", "2-most-commit-language.svg"}
ROW_CARDS = ("3-stats.svg", "2-most-commit-language.svg")
ROW_GAP = 16


def restyle(text, name=""):
    if name in RESIZE_CARDS:
        for old, new in RESIZE:
            text = text.replace(old, new)
    for old, new in COLORS:
        text = text.replace(old, new)
    m = VIEWBOX.search(text)
    width, height = (float(m.group(1)), float(m.group(2))) if m else (340.0, 200.0)
    layers = DEFS.format(w=f"{width - 2:g}", h=f"{height - 2:g}")
    text, n = BG_RECT.subn(lambda _: layers, text, count=1)
    if n:
        text = text.replace(TITLE, "font-size: 22px; fill: url(#cTitle);")
    return text


def build_row():
    root = re.compile(r"<svg[^>]*>")
    parts = []
    x = 0
    for name in ROW_CARDS:
        text = (DST / name).read_text(encoding="utf-8")
        parts.append(
            root.sub(
                f'<svg x="{x}" y="0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
                text,
                count=1,
            )
        )
        x += W + ROW_GAP
    total = x - ROW_GAP
    row = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{H}" '
        f'viewBox="0 0 {total} {H}">' + "".join(parts) + "</svg>"
    )
    (DST / "stats-row.svg").write_text(row, encoding="utf-8")


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for svg in sorted(SRC.glob("*.svg")):
        out = restyle(svg.read_text(encoding="utf-8"), svg.name)
        (DST / svg.name).write_text(out, encoding="utf-8")
    build_row()


if __name__ == "__main__":
    main()
