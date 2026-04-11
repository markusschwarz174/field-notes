# Co-Authoring Prozess V2

Erstellt: 2026-04-12 | Basierend auf Learnings aus Blog Teil 01

---

## Kernprinzip

KI fragt, Markus liefert die Worte. Nicht umgekehrt.

Original-Prompts und Markus' eigene Saetze sind das Skelett — KI baut drumherum, nicht darueber.

---

## Phase 0: THEMA & QUELLEN

| Schritt | Wer | Output |
|---|---|---|
| Thema waehlen | Markus oder KI | z.B. "Teil 02: Bloom als Universalwerkzeug" |
| Chats/Quellen suchen via META_INDEX | KI | Liste der relevanten Dokumente |
| KI stellt Material vor (Kurzuebersicht) | KI | 1-Seiter: Was steht in den Chats? |

---

## Phase 1: INTERVIEW (ersetzt den alten v1-Draft)

| Schritt | Wer | Output |
|---|---|---|
| KI fuehrt Interview mit Markus | KI fragt, Markus antwortet | Transkript mit Markus' eigenen Worten |
| Fragen: Motive, Beweggruende, was soll rein, was war der Kipppunkt? | KI | |
| KI identifiziert Kern-Saetze aus dem Interview | KI | 5-8 Saetze die "Markus klingen" |
| Markus validiert Kern-Saetze | Markus | "Ja, das bin ich" / "Nein, so meine ich das nicht" |

**Warum:** v1 in Teil 01 war schlecht weil KI aus dem Chat-Material geraten hat, was Markus wichtig ist. Das Interview fragt ihn direkt.

---

## Phase 2: DREHBUCH (ersetzt den alten Struktur-Entwurf)

| Schritt | Wer | Output |
|---|---|---|
| KI schlaegt Drehbuch vor (Abschnitte, Bogen) | KI | Struktur mit 5-8 Kapitel-Titeln |
| Markus sichtet Original-Chat | Markus | Markiert: welche Prompts rein, welche Screenshots |
| Markus ergaenzt Drehbuch | Markus | "Hier fehlt X, das ist mir wichtig" |

---

## Phase 3: DRAFT (v1 = schon naeher dran)

| Schritt | Wer | Output |
|---|---|---|
| KI schreibt Draft basierend auf: Interview + Kern-Saetze + Drehbuch + Original-Prompts | KI | v1 als .docx |

### Regeln fuer den Draft

- Original-Prompts **woertlich uebernehmen**, nicht umschreiben
- Kern-Saetze aus Interview **einbauen**, nicht ersetzen
- Wo KI unsicher ist: `[TODO-HUM]` statt raten
- Arbeitsformat ist **.docx** bis near-final
- .md erst bei Konvertierung fuer Git/Publikation

---

## Phase 4: ITERATION (v1 → v3, max. 3 Runden)

| Runde | Was passiert |
|---|---|
| v1 → v2 | Markus liest, markiert: "Das bin ich" / "Das bin ich nicht" / "Hier fehlt was" |
| v2 → v3 | KI ueberarbeitet nur markierte Stellen. Kein Neuschreiben. |
| v3 | Markus uebernimmt (Veredelung). Ab hier ist es sein Text. |

---

## Phase 5: REVIEW + RELEASE

Gemaess `release_checkliste.md`:
- Block 1: Sprache
- Block 2: Stil
- Block 3: Inhalt & Glaubwuerdigkeit
- Block 4: Quellen & Literatur
- Block 5: Meta-Analyse
- Block 6: Zielgruppe
- Block 7: Release-Gate

---

## Vergleich: Alt vs. Neu

| Alt (Teil 01) | Neu (ab Teil 02) |
|---|---|
| KI liest Chat → fasst zusammen → schreibt v1 | KI fuehrt Interview → Markus liefert die Worte → KI baut daraus v1 |
| v1 war KI-Sprache, Markus musste zurueck zum Original | v1 enthaelt Markus' eigene Saetze + Original-Prompts |
| .md ab v1 | .docx bis near-final, .md erst fuer Git |
| 8 Versionen bis near-final | Ziel: 3-4 Versionen |
| KI raet was wichtig ist | KI fragt was wichtig ist |
| Struktur-Vorschlag ohne Drehbuch | Drehbuch mit Markus-Input vor dem Draft |
