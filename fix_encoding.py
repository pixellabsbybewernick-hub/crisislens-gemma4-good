from pathlib import Path

p = Path("app.py")
s = p.read_text(encoding="utf-8")

replacements = {
    "\u00f0\u0178\u201d\u00ad": "",
    "\u00f0\u0178": "",
    "\u00e2\u2020\u2019": "->",
    "\u00e2\u20ac\u201d": "-",
    "\u00e2\u20ac\u201c": "-",
    "\u00e2\u20ac\u2122": "'",
    "\u00e2\u20ac\u0153": '"',
    "\u00e2\u20ac\u009d": '"',
    "â†’": "->",
    "â€”": "-",
    "â€“": "-",
    "ðŸ”­": "",
}

for old, new in replacements.items():
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
