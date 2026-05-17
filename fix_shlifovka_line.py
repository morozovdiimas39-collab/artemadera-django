from pathlib import Path
p = Path("templates/shlifovka.html")
lines = p.read_text().splitlines(keepends=True)
# Remove line 84 (index 83) if it contains quiz remnants
if len(lines) > 83 and ("quiz_srub" in lines[83] or "Калькулятор стоимости" in lines[83] or "Далее<!-- -->" in lines[83] or lines[83].strip().startswith("<span>25")):
    del lines[83]
    p.write_text("".join(lines))
    print("removed line 84")
else:
    print("line 84:", lines[83][:80] if len(lines) > 83 else "n/a")
