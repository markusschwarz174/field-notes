"""backfill_seo_meta.py — Einmaliger SEO-Backfill fuer 8 Live-Notes.

Decision: D_260715_SEO_BASISHYGIENE (FIELD_NOTES_DRAFT).

Was:
- Setzt Jekyll-Front-Matter `--- ---` an den Datei-Anfang (damit jekyll-sitemap
  die Seite als Page erkennt und in sitemap.xml aufnimmt).
- Fuegt canonical + Open Graph + Twitter Card + JSON-LD (Article + Person) in
  den <head> ein, direkt nach dem bestehenden <meta name="author">-Tag.
- Extrahiert title + description aus der bestehenden HTML.
- Slug = Ordner-Name unter notes/.
- OG-Image: sucht heroes/hero_<slug>_*.png oder hero_<NN>.png; Fallback = globales
  Storyline-Backdrop.

Idempotent: erkennt existierenden `<link rel="canonical"` und ueberspringt Datei.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

SITE_URL = "https://markusschwarz174.github.io/field-notes"
REPO_ROOT = Path(__file__).resolve().parent.parent
OG_DEFAULT = f"{SITE_URL}/assets/storyline_fieldnotes_bg_260714.png"

# Notes im Publish-Repo. Reihenfolge = numerische Reihe wo verfuegbar.
NOTES = [
    # (slug, section_hint_for_og_image_search)
    ("neugierde", "01"),
    ("unterrichtsidee", "02"),
    ("unterrichtsentwurf-vision", "02"),  # legacy-redirect slug
    ("wald", "08"),
    ("schablonen", "10"),
    ("lets-yaml", "04"),
    ("datenbanken", "11"),
    ("p7-translation", None),
]


def find_og_image(slug: str, note_dir: Path, nr_hint: str | None) -> str:
    """Sucht ein passendes Hero-Bild fuer OG. Prioritaet:
    1) notes/<slug>/heroes/hero_<slug>_*.png
    2) heroes/hero_<slug>_*.png im globalen heroes/
    3) heroes/hero_<nr_hint>.png im globalen heroes/
    4) OG_DEFAULT (Landing-Backdrop)
    """
    global_heroes = REPO_ROOT / "heroes"
    local_heroes = note_dir / "heroes"

    # p7-translation hat sein Hero im Note-Root
    if slug == "p7-translation":
        cand = note_dir / "hero_p7_translation_260714.png"
        if cand.exists():
            return f"{SITE_URL}/{slug}/{cand.name}"

    # (1) note-lokal
    if local_heroes.exists():
        for f in sorted(local_heroes.iterdir()):
            n = f.name.lower()
            if n.startswith(f"hero_{slug}") and n.endswith((".png", ".webp", ".jpg", ".jpeg")):
                return f"{SITE_URL}/notes/{slug}/heroes/{f.name}"

    # (2) globales heroes/ mit slug
    if global_heroes.exists():
        for f in sorted(global_heroes.iterdir()):
            n = f.name.lower()
            if slug in n and n.endswith((".png", ".webp", ".jpg", ".jpeg")):
                return f"{SITE_URL}/heroes/{f.name}"

    # (3) globales heroes/ mit nr_hint (hero_08.png etc.)
    if nr_hint and global_heroes.exists():
        cand = global_heroes / f"hero_{nr_hint}.png"
        if cand.exists():
            return f"{SITE_URL}/heroes/{cand.name}"

    return OG_DEFAULT


def extract_title_desc(html: str) -> tuple[str, str]:
    m_title = re.search(r"<title>(.*?)</title>", html, flags=re.DOTALL | re.IGNORECASE)
    title = m_title.group(1).strip() if m_title else "Field Notes"
    m_desc = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        html,
        flags=re.IGNORECASE,
    )
    desc = m_desc.group(1).strip() if m_desc else ""
    # HTML-Entities in title auf & zurueck (kein Escape-Doppel)
    title = title.replace("&amp;", "&")
    return title, desc


def build_meta_block(slug: str, title: str, desc: str, og_image: str) -> str:
    canonical = f"{SITE_URL}/p7-translation/" if slug == "p7-translation" else f"{SITE_URL}/notes/{slug}/"
    # Escape doppelte Quotes in Werten (safety)
    t = title.replace('"', "&quot;")
    d = desc.replace('"', "&quot;").replace("\n", " ").strip()
    json_title = json.dumps(title, ensure_ascii=False)
    json_desc = json.dumps(desc, ensure_ascii=False)
    return f"""<link rel="canonical" href="{canonical}">
<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Field Notes — Markus Schwarz">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="de_CH">
<meta property="article:author" content="Markus Schwarz">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og_image}">
<!-- JSON-LD: Article + Person (Google Knowledge Graph Signal) -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "headline": {json_title},
      "description": {json_desc},
      "inLanguage": "de-CH",
      "url": "{canonical}",
      "image": "{og_image}",
      "author": {{
        "@type": "Person",
        "name": "Markus Schwarz",
        "url": "{SITE_URL}/"
      }},
      "publisher": {{
        "@type": "Person",
        "name": "Markus Schwarz",
        "url": "{SITE_URL}/"
      }},
      "isPartOf": {{
        "@type": "CreativeWorkSeries",
        "name": "Field Notes — KI & Unterricht",
        "url": "{SITE_URL}/"
      }}
    }},
    {{
      "@type": "Person",
      "name": "Markus Schwarz",
      "url": "{SITE_URL}/",
      "sameAs": [
        "https://github.com/markusschwarz174"
      ],
      "description": "Lehrer, Autor der Field-Notes-Reihe zu AI im Unterricht."
    }}
  ]
}}
</script>"""


FRONTMATTER = "---\n---\n"


def patch_file(html_path: Path, slug: str, nr_hint: str | None) -> tuple[bool, str]:
    text = html_path.read_text(encoding="utf-8")
    if 'rel="canonical"' in text:
        return False, "skip: already has canonical"

    title, desc = extract_title_desc(text)
    og_image = find_og_image(slug, html_path.parent, nr_hint)
    meta_block = build_meta_block(slug, title, desc, og_image)

    # Front-Matter voranstellen (nur wenn noch keins da ist)
    if not text.startswith("---"):
        text = FRONTMATTER + text

    # Meta-Block nach <meta name="author"...>-Zeile einfuegen.
    # Fallback: nach <meta name="viewport"...>.
    author_re = re.compile(r'(<meta\s+name="author"[^>]*>\s*\n)', flags=re.IGNORECASE)
    viewport_re = re.compile(r'(<meta\s+name="viewport"[^>]*>\s*\n)', flags=re.IGNORECASE)

    if author_re.search(text):
        text = author_re.sub(r"\1" + meta_block + "\n", text, count=1)
    elif viewport_re.search(text):
        text = viewport_re.sub(r"\1" + meta_block + "\n", text, count=1)
    else:
        return False, "no anchor for meta insertion"

    html_path.write_text(text, encoding="utf-8")
    return True, f"patched · og={og_image.split('/')[-1]}"


def patch_landing(landing_path: Path) -> tuple[bool, str]:
    """Landing (root index.html): kleiner Meta-Block ohne Article-JSON-LD."""
    text = landing_path.read_text(encoding="utf-8")
    if 'rel="canonical"' in text:
        return False, "skip: already has canonical"

    title, desc = extract_title_desc(text)
    og_image = OG_DEFAULT
    canonical = f"{SITE_URL}/"
    t = title.replace('"', "&quot;")
    d = desc.replace('"', "&quot;").replace("\n", " ").strip()
    block = f"""<link rel="canonical" href="{canonical}">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Field Notes — Markus Schwarz">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="de_CH">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og_image}">
<!-- JSON-LD: WebSite + Person -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebSite",
      "name": "Field Notes — Markus Schwarz",
      "url": "{canonical}",
      "inLanguage": "de-CH",
      "author": {{
        "@type": "Person",
        "name": "Markus Schwarz",
        "url": "{canonical}"
      }}
    }},
    {{
      "@type": "Person",
      "name": "Markus Schwarz",
      "url": "{canonical}",
      "sameAs": [
        "https://github.com/markusschwarz174"
      ],
      "description": "Lehrer, Autor der Field-Notes-Reihe zu AI im Unterricht."
    }}
  ]
}}
</script>"""

    if not text.startswith("---"):
        text = FRONTMATTER + text

    desc_re = re.compile(r'(<meta\s+name="description"[^>]*>\s*\n)', flags=re.IGNORECASE)
    if desc_re.search(text):
        text = desc_re.sub(r"\1" + block + "\n", text, count=1)
    else:
        return False, "no anchor for meta insertion on landing"

    landing_path.write_text(text, encoding="utf-8")
    return True, "landing patched"


def main() -> int:
    print(f"REPO_ROOT = {REPO_ROOT}")
    ok, skip, fail = 0, 0, 0

    # Landing zuerst
    landing = REPO_ROOT / "index.html"
    if landing.exists():
        did, msg = patch_landing(landing)
        print(f"[landing] {msg}")
        if did:
            ok += 1
        elif "skip" in msg:
            skip += 1
        else:
            fail += 1

    # 8 Notes
    for slug, nr_hint in NOTES:
        p = REPO_ROOT / "notes" / slug / "index.html"
        if slug == "p7-translation":
            p = REPO_ROOT / "p7-translation" / "index.html"
        if not p.exists():
            print(f"[{slug}] MISSING: {p}")
            fail += 1
            continue
        did, msg = patch_file(p, slug, nr_hint)
        print(f"[{slug}] {msg}")
        if did:
            ok += 1
        elif "skip" in msg:
            skip += 1
        else:
            fail += 1

    print(f"\nDone. ok={ok} skip={skip} fail={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
