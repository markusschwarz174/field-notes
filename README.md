# Field Notes — Publish Repo

> **Verbindlich ab:** 2026-06-16 (`D_260616_02_P6_P8_PIPELINE` in `FIELD_NOTES_DRAFT/DECISIONS_LOG.md`).
> **Editorial Workspace:** `../FIELD_NOTES_DRAFT/` (DOCX-Iterationen, Sources, Marker, WIP — **nicht versioniert**).
> **Publish Repo:** dieses Verzeichnis (nur fertige `.md` + `meta.yaml` + `img/`).

Markus Schwarz' Werkstattbericht: AI im Unterricht. Serialisiertes Entwicklungstagebuch (Juli 2025 – Januar 2026), retrospektiv erzaehlt, Sixth-Sense-Rahmen.

## Struktur

```
field-notes_git/
├── _config.yml                          # Jekyll-Konfiguration
├── _data/
│   └── series.yaml                      # Series-Index + cross_themen closed_list
├── _includes/                           # Jekyll-Partials (geplant)
├── _layouts/
│   └── note.html                        # Per-Note Layout
├── _archive/
│   └── v7_pre_refactor_260616/          # alte teil_01-Inhalte + stilprofil (2026-06-16 archiviert)
├── <NN>_<slug>/                         # ein Folder pro Note (von W_P8a_CONVERSATION_TRANSFORMER generiert)
│   ├── index.md                         # Body mit Frontmatter aus DOSSIER
│   ├── meta.yaml                        # erweiterte Metadaten
│   └── img/                             # WebP-optimiert
├── .github/
│   └── workflows/
│       └── pages.yml                    # Auto-Deploy zu gh-pages
└── README.md
```

## Pipeline

DOCX-Drafts und Iterationen leben im `FIELD_NOTES_DRAFT/`-Workspace (nicht versioniert, siehe `.gitignore`). Sobald eine Note P5-LASTCALL GO erreicht, geht sie durch:

1. **P6a** (Editorial, deutsch) — `W_P6a_MARKER_STRIP_DELETER` + `W_P6a_FRONTMATTER_READER` → `V6.50_HUMAN_FINAL_GER.docx`
2. **P8** LAUNCH (nach HITL „LAUNCH") — `W_P8a_CONVERSATION_TRANSFORMER` (DOCX→MD+img) + `W_P8b_GIT_LOCAL_CREATER` + `W_P8c_GIT_PUSH_LAUNCHER`
3. **GitHub Actions** → Jekyll-Build → live auf GitHub Pages

Detail-Spec: `FIELD_NOTES_DRAFT/0_C_CONVENTION/C_OPS_P6_RELEASE.md` + `C_OPS_P8_LAUNCH.md`.

## .gitignore

DOCX, PDF, PPTX, OS-Files (Thumbs.db, .DS_Store) bleiben draussen — Drafts leben im DRAFT-Workspace.

## Lizenz

CC-BY 4.0 (Saison-Bundle ueber Zenodo bei Saison-Ende, `AGENT_PUSHER §8` P9).

## Repo-Geschichte

- 2026-06-16: Restructure auf neue Per-Note-Folder-Struktur (`D_260616_02`). Alte `teil_01/`-Inhalte + `stilprofil/` ins `_archive/v7_pre_refactor_260616/` bewegt.
- Vorher (April 2026): erster `teil_01/`-Aufschlag mit v7-Vorschlaegen, archiviert.

## Autor

Markus Schwarz
