"""Gera o banner do perfil em tema claro e escuro."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

TEMAS = {
    "dark": dict(bg="#0F1B2D", grid="#1C2D44", panel="#152538", stroke="#2C4461",
                 text="#EAF0F7", muted="#8DA2BB", amber="#FFB547", sky="#7CC6FE", done="#6FD3A5"),
    "light": dict(bg="#F4F7FB", grid="#E3EAF3", panel="#FFFFFF", stroke="#C8D4E3",
                  text="#0F1B2D", muted="#52667E", amber="#C77C00", sky="#1D6FB8", done="#1E9E6A"),
}


def e(s):
    return escape(s)


def css(t):
    return f"""<style>
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .t{{fill:{t['text']}}} .m{{fill:{t['muted']}}}
  </style>"""


# ------------------------------------------------------------------ banner
def banner(nome_tema):
    t = TEMAS[nome_tema]
    W, H = 1200, 300

    # nós do grafo: (id, rótulo, x, y, largura)
    nos = {
        "voce": ("você", 660, 150, 76),
        "gw": ("pyêtro", 790, 150, 96),
        "spring": ("spring boot", 950, 80, 120),
        "fast": ("fastapi", 950, 150, 120),
        "rag": ("rag + llm", 950, 220, 120),
        "pg": ("postgresql", 1110, 115, 112),
        "chroma": ("chromadb", 1110, 220, 112),
    }
    h = 34

    def dir_(k):
        _, x, y, w = nos[k]
        return x + w / 2, y

    def esq(k):
        _, x, y, w = nos[k]
        return x - w / 2, y

    def curva(a, b):
        (x1, y1), (x2, y2) = a, b
        mx = (x1 + x2) / 2
        return f"C {mx} {y1} {mx} {y2} {x2} {y2}"

    arestas = [("voce", "gw"), ("gw", "spring"), ("gw", "fast"), ("gw", "rag"),
               ("spring", "pg"), ("fast", "pg"), ("rag", "chroma")]
    linhas = "".join(
        f'<path d="M {dir_(a)[0]} {dir_(a)[1]} {curva(dir_(a), esq(b))}" fill="none" '
        f'stroke="{t["stroke"]}" stroke-width="1.5"/>'
        for a, b in arestas)

    # rotas completas percorridas pelos pacotes (passam por trás dos nós)
    def rota(*ks):
        d = f"M {esq(ks[0])[0]} {esq(ks[0])[1]}"
        for i, k in enumerate(ks):
            d += f" L {dir_(k)[0]} {dir_(k)[1]}"
            if i + 1 < len(ks):
                d += " " + curva(dir_(k), esq(ks[i + 1]))
        return d

    rotas = [rota("voce", "gw", "spring", "pg"),
             rota("voce", "gw", "fast", "pg"),
             rota("voce", "gw", "rag", "chroma")]
    pacotes = ""
    for i, r in enumerate(rotas):
        for j in range(2):
            atraso = i * 1.1 + j * 3.3
            pacotes += (
                f'<circle r="4" opacity="0" fill="{t["amber"]}">'
                f'<animateMotion dur="3.3s" begin="{atraso}s" repeatCount="indefinite" '
                f'path="{r}" keyTimes="0;1" calcMode="linear"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" '
                f'dur="3.3s" begin="{atraso}s" repeatCount="indefinite"/></circle>')

    caixas = ""
    for k, (rot, x, y, w) in nos.items():
        destaque = k == "gw"
        stroke = t["amber"] if destaque else t["stroke"]
        caixas += (
            f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="7" '
            f'fill="{t["panel"]}" stroke="{stroke}" stroke-width="{1.8 if destaque else 1.2}"/>'
            f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" class="mono {"t" if destaque else "m"}" '
            f'font-size="13" font-weight="{600 if destaque else 400}">{e(rot)}</text>')

    grade = (f'<pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<circle cx="1" cy="1" r="1" fill="{t["grid"]}"/></pattern>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
  aria-label="Pyêtro Augusto Malaquias, desenvolvedor back-end em Java e Python">
  <defs>{grade}</defs>
  {css(t)}
  <rect width="{W}" height="{H}" rx="14" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
  <text x="64" y="118" class="sans t" font-size="54" font-weight="800" letter-spacing="-1.2">Pyêtro Augusto</text>
  <text x="64" y="176" class="sans t" font-size="54" font-weight="800" letter-spacing="-1.2">Malaquias</text>
  <text x="66" y="222" class="sans m" font-size="20">Back-end em Java e Python</text>
  <text x="66" y="250" class="sans m" font-size="20">Ciência da Computação na UFLA</text>
  <g>{linhas}</g>
  <g>{pacotes}</g>
  <g>{caixas}</g>
  <text x="1166" y="280" text-anchor="end" class="mono m" font-size="12">GET /pyetro  200 OK</text>
</svg>"""


for tema in TEMAS:
    (OUT / f"banner-{tema}.svg").write_text(banner(tema), encoding="utf-8")
print("ok")
