#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "templates" / "shlifovka.html"
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
markers = (
    "REMOVED_QUIZ",
    "lucide-house w-6 h-6 text-amber-400",
    'disabled:opacity-50 ">Далее<!-- -->',
)
new_lines = [ln for ln in lines if not any(m in ln for m in markers)]
path.write_text("".join(new_lines), encoding="utf-8")
print("lines", len(lines), "->", len(new_lines))
