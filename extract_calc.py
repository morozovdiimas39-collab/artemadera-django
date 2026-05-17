from pathlib import Path

text = Path("restoration_block.html").read_text()
marker = '<div class="mt-20 lg:mt-32">'
idx = text.index(marker)
end = text.index("</div></div></section>", idx)
calc = text[idx:end]
out = (
    "{% load static %}\n"
    '<section id="quiz" class="py-20 lg:py-32 relative overflow-hidden">\n'
    ' <div class="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">\n'
    f"{calc}\n"
    " </div>\n"
    "</section>\n"
)
Path("templates/includes/home_calculator_section.html").write_text(out)
print("ok", len(out))
