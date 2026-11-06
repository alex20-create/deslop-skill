# deslop

A Claude skill that cleans AI-generated drafts in English and Spanish so they can be used as the writer's own text. It removes chat residue, deals with invented or unsupported content, fixes spelling and style-guide errors, and tones down stock AI habits only where they repeat or say nothing.

It keeps what the writer chose: the language variety (British or American English, Spanish from Spain or Latin America), the tone, the genre and the register.

## What it does

The skill works in four groups, in order of priority.

| Group | What it covers | What it does |
|---|---|---|
| R | Chat residue and machine artefacts: "Certainly!", "¡Claro!", "I hope this helps", placeholders such as `[Your Name]`, tracking codes such as `utm_source=chatgpt.com` | Removes them. Placeholders stay visible and are listed for you to fill. |
| I | Invented and unsupported content: figures, dates, awards, quotes, unnamed experts, guesses that fill a gap | With your notes or brief: corrects contradictions with your data, removes unsupported claims that would matter if wrong, and lists what the draft left out. Without a source: lists every specific for you to check and removes only guesses and unnamed authority. |
| N | Spelling and style-guide errors: capitalised months in Spanish, missing ¿ ¡, badly formed dialogue dashes, clear calques | Corrects and lists them. Inside dialogue or a deliberate voice it only lists them. |
| E | Style habits: not-X-but-Y contrasts, empty closers, triads by default, stock vocabulary, inflated significance | Acts only when the habit repeats as a mould or the element says nothing, with the smallest possible edit. |

It distinguishes what the model said to you from what the draft says to its reader. "I hope this helps" at the end of a chat reply goes; the same words in an email you are sending to a colleague stay.

### Two levels

- **Cleanup** (default): groups R, I and N in full, and only clear cases from group E.
- **Deep**: ask for a deep pass ("deep", "full pass", "a fondo") to go through group E pattern by pattern.

### Genre and voice

In fiction, scripts, synopses, advertising, speeches and social posts, fragments, triads and strong closers are legitimate tools. The skill leaves them alone unless they repeat or are empty, and in fiction it lists possible deliberate choices instead of changing them. If you give it a sample of your own writing, it uses the sample to decide between options.

### What you get back

1. The final text.
2. The changes, grouped by R, I, N and E, each quoting what triggered it.
3. A "to check" list: unverified claims, removed claims, interpretations, placeholders, unjustified mixes of variety or register, and doubtful facts. The skill never changes a doubtful fact on its own.

## Install

### Claude Code

Copy the `deslop/` folder of this repository into your skills folder:

```bash
git clone https://github.com/alex20-create/deslop-skill.git
mkdir -p ~/.claude/skills
cp -r deslop-skill/deslop ~/.claude/skills/
```

On Windows the skills folder is `%USERPROFILE%\.claude\skills\`. Start a new session so Claude picks up the skill.

### Claude apps

Download `deslop.skill` from the latest release and upload it in the skills section of your Claude settings. To build it yourself, run this from the repository root:

```bash
zip -r deslop.skill deslop
```

There is no hook and nothing runs on its own: the skill loads only when you ask for it.

## Use

Ask Claude to clean a draft, for example:

- "Humanize this draft: ..."
- "Limpia este borrador: ..."
- "Clean this email. Here is my brief: ..." (the brief is used as source material)
- "Deep pass on this synopsis. This is how I write: ..." (a sample of your own prose)

### Mechanical check

The skill includes `scripts/check.py`, which Claude runs first when it can run code. You can also run it yourself from the repository root:

```bash
python3 -I deslop/scripts/check.py draft.txt
python3 -I deslop/scripts/check.py draft.txt --lang es
```

It reports candidates for chat residue, placeholders, artefacts, dash density, stock vocabulary, didactic asides and mixed quotation marks in both languages, and in Spanish also capitalisation, missing ¿ ¡, raya form, clear calques and hyphenated compounds. It cannot see context: every hit is a candidate, and the skill's rules decide. It uses only the Python standard library and changes nothing.

## Files

```
deslop/                           the skill: this is the folder you install
  SKILL.md                        rules shared by both languages
  references/en.md                English watch lists, examples and norm rules
  references/es.md                Spanish watch lists, examples and norm rules
  scripts/check.py                mechanical pre-pass
  LICENSE
tools/validate.py                 repository checks (development only)
tools/fixtures/                   test texts for check.py (development only)
.github/workflows/validate.yml    runs the checks on GitHub
```

## Development

Run the repository checks before opening a pull request:

```bash
python3 tools/validate.py
```

They check the skill's frontmatter (including strict YAML when PyYAML is installed, because the Claude apps reject what Claude Code forgives), that the skill folder carries its licence, that pattern codes match across files, that no "after" example adds words its "before" does not have, that there are no stray dashes outside examples, and that `check.py` reports what it should on the test texts and stays quiet on the texts with correct usage. The same checks run on every push to `main` and on every pull request. Tested with Python 3.11, 3.12 and 3.13.

## En español

La skill limpia borradores escritos con un modelo de IA, en inglés y en español, sin cambiar la variedad (español de España o de Latinoamérica, *vosotros* o *ustedes*), el tono, el género ni el registro. Quita los restos de chat, corrige con tus datos lo que contradiga tu briefing y te avisa de lo que no puede comprobar. Corrige errores de norma (mayúsculas en meses y días, ¿ ¡, rayas de diálogo, calcos claros) y solo toca el estilo cuando un recurso se repite o está vacío. En ficción respeta los recursos que pueden ser deliberados y te los señala en lugar de cambiarlos.

Las listas y las reglas de español son criterio editorial basado en la *Ortografía de la lengua española* de la RAE y en FundéuRAE. No proceden de una guía equivalente a la de Wikipedia en inglés, que es la base de las listas inglesas.

## Credits and licence

MIT licence. See [LICENSE](LICENSE).

Based on [blader/humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT), which draws on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Some patterns are summarised in our own words from that page; its text is licensed CC BY-SA and none of it is copied here.
