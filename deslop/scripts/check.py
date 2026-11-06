#!/usr/bin/env python3
"""Mechanical pre-pass for the deslop skill.

Finds candidates that a script can spot reliably and a model can miss:
chatbot artefacts, placeholders, likely chat phrases, didactic asides,
Spanish capitalisation and punctuation, badly spaced dialogue dashes,
clear calques, dash density, mixed quotation marks and clusters of stock
AI vocabulary or translationese.

Every hit is a candidate, not a verdict. The skill's rules decide what to
do, and the script cannot see context: a chat phrase may be addressed to
the email's recipient, a capitalised day may be part of a name.

Usage:
    python3 -I check.py draft.txt [--lang es|en]
    cat draft.txt | python3 -I check.py - [--lang es|en]

Standard library only. Reads the text, prints a report, changes nothing.
"""

from __future__ import annotations

import argparse
import re
import sys

ARTEFACTS = [
    r"utm_source=(?:chatgpt\.com|openai)",
    r"\boaicite\b",
    r"\bcontentReference\b",
    r"turn\d+(?:search|news|view|file)\d+",
    r"\battributableIndex\b",
]

PLACEHOLDERS = [
    r"\[(?:your|tu|su|insert|insertar|nombre|name|fecha|date|cifra|figure|company|empresa|link|enlace)[^\]]{0,40}\]",
    r"\bXX\s?%",
    r"\blorem ipsum\b",
    r"\b(?:Empresa|Company|Persona|Person|Cliente|Client|Producto|Product)\s+[XYZ]\b",
]

CHAT_PHRASES = {
    "es": [
        r"¡claro!", r"¡por supuesto!", r"excelente pregunta", r"aquí tienes", r"espero que te (?:sea|sirva)",
        r"¿quieres que", r"¿te gustaría", r"¿prefieres que", r"si quieres,? puedo", r"no dudes en",
        r"dime si necesitas", r"como (?:modelo de lenguaje|ia)\b", r"según mi última actualización",
        r"hasta la fecha de mi conocimiento",
    ],
    "en": [
        r"\bcertainly!", r"\bof course!", r"great question", r"\bhere's (?:a|the|an|your)\b",
        r"\bhere is (?:a|the|an|your)\b", r"i hope this helps", r"would you like", r"\bwant me to",
        r"\bshall i\b", r"do you want me to", r"let me know if", r"feel free to", r"as an ai\b",
        r"as of my last (?:training|knowledge)", r"knowledge cutoff",
    ],
}

ASIDES = {
    "es": [
        r"\bes importante (?:señalar|tener en cuenta|destacar|mencionar|recordar)\b",
        r"\bcabe (?:destacar|mencionar|señalar)\b", r"\bconviene recordar\b",
        r"^\s*en (?:resumen|conclusión|definitiva)\b",
    ],
    "en": [
        r"\bit is (?:important|worth) (?:to note|noting|mentioning)\b", r"\bit should be noted\b",
        r"\bit's (?:important|worth) (?:to note|noting|mentioning)\b",
        r"^\s*in (?:summary|conclusion)\b",
    ],
}

AI_WORDS = {
    "es": [
        "crucial", "fundamental", "esencial", "potenciar", "potenciando", "fomentar", "fomentando",
        "impulsar", "impulsando", "optimizar", "abordar", "profundizar", "sumergirse", "sumérgete",
        "sumerjámonos", "destacar", "resaltar", "subrayar", "panorama", "ecosistema", "entramado",
        "holístico", "sinergia", "vibrante", "fascinante", "apasionante", "sinfín", "desbloquear",
        "empoderar", "además", "asimismo", "imprescindible", "inolvidable",
    ],
    "en": [
        "additionally", "crucial", "enduring", "interplay", "intricate", "meticulous", "pivotal",
        "seamless", "tapestry", "testament", "vibrant", "breathtaking", "nestled",
        r"bolster(?:s|ed|ing)?", r"delv(?:e|es|ed|ing)", r"empower(?:s|ed|ing)?", r"enhanc(?:e|es|ed|ing)",
        r"foster(?:s|ed|ing)?", r"garner(?:s|ed|ing)?", r"showcas(?:e|es|ed|ing)", r"underscor(?:e|es|ed|ing)",
        r"key (?:role|factor|element|part)", r"(?:digital|evolving|competitive|cultural) landscape",
    ],
}

AI_PATTERNS_ES = [
    r"\b(?:factor|elemento|papel|punto|momento|pieza|aspecto) clave\b",
    r"\brealiz(?:ar|a|an|ó|aron|ará|arán|ado|ada|ando)\b",
    r"\bllev(?:ar|a|ó|ará) a cabo\b",
    r"\ba nivel de\b",
    r"\b(?:fue|fueron|será|serán|es|son|ha sido|han sido)\s+[a-záéíóúñ]+(?:ado|ada|ido|ida)s?\s+por\b",
]

DAYS_ES = {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"}
MONTHS_DAYS_ES = (
    "Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Setiembre|Octubre|Noviembre|Diciembre|"
    "Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo"
)
LOWER_WORDS_ES = "De|Del|La|Las|El|Los|Y|E|O|U|En|Con|Para|Por|A|Al|Sin|Sobre|Entre"
UPPER = "A-ZÁÉÍÓÚÑ"


def detect_lang(text: str) -> str:
    es_hits = len(re.findall(r"\b(?:el|la|los|las|que|de|y|en|un|una|es|por|con|para)\b", text, re.I))
    en_hits = len(re.findall(r"\b(?:the|and|of|to|is|that|for|with|on|an|you|it)\b", text, re.I))
    if re.search(r"[ñ¿¡áéíóú]", text, re.I):
        es_hits += 5
    return "es" if es_hits >= en_hits else "en"


def excerpt(line: str, start: int, end: int, pad: int = 25) -> str:
    a = max(0, start - pad)
    b = min(len(line), end + pad)
    return ("…" if a else "") + line[a:b].strip() + ("…" if b < len(line) else "")


def paragraphs_with_lines(text: str) -> list[tuple[int, str]]:
    """Split into paragraphs and return (first line number, paragraph)."""
    out = []
    pos = 0
    for m in re.finditer(r"\n[ \t]*\n", text + "\n\n"):
        para = text[pos:m.start()]
        if para.strip():
            lead = len(para) - len(para.lstrip("\n"))
            out.append((text.count("\n", 0, pos + lead) + 1, para))
        pos = m.end()
    return out


def is_heading(lines: list[str], i: int) -> bool:
    s = lines[i].strip()
    if re.match(r"(?:#{1,6}\s|(?:Subject|Asunto)\s*:)", s):
        return True
    alone = (i == 0 or not lines[i - 1].strip()) and (i + 1 >= len(lines) or not lines[i + 1].strip())
    return alone and 0 < len(s.split()) <= 8 and not re.search(r"[.!?…:;,]$", s) and not s.startswith("—")


def check(text: str, lang: str) -> list[tuple[int, str, str]]:
    hits: set[tuple[int, str, str]] = set()
    text = text.replace("\r\n", "\n")
    norm = text.replace("’", "'")
    lines = norm.split("\n")

    def add(n: int, code: str, msg: str) -> None:
        hits.add((n, code, msg))

    greeting = re.compile(r"^\s*(?:hi|hello|dear|hey|hola|estimad[oa]s?|buen[oa]s)\b", re.I)
    seen_greeting = False
    for n, line in enumerate(lines, 1):
        for pat in ARTEFACTS:
            for m in re.finditer(pat, line):
                add(n, "R5", f"chatbot artefact: {excerpt(line, m.start(), m.end())}")
        if re.match(r"\s*(?:Subject|Asunto)\s*:", line) and seen_greeting:
            add(n, "R5", "subject line inside the body of the message")
        if greeting.match(line):
            seen_greeting = True
        for pat in PLACEHOLDERS:
            for m in re.finditer(pat, line, re.I if "Empresa" not in pat else 0):
                add(n, "R4", f"placeholder: {m.group(0)}")
        for pat in CHAT_PHRASES[lang]:
            for m in re.finditer(pat, line, re.I):
                add(n, "R1/R2?", f"chat phrase, check who 'you' is: {excerpt(line, m.start(), m.end())}")
        for pat in ASIDES[lang]:
            for m in re.finditer(pat, line, re.I):
                add(n, "E21", f"didactic aside or summary: {excerpt(line, m.start(), m.end())}")

        if lang != "es":
            continue

        for m in re.finditer(rf"\b({MONTHS_DAYS_ES})\b", line):
            before = line[: m.start()].rstrip()
            after = line[m.end():]
            if re.match(rf"\s+(?:de\s+)?[{UPPER}]", after):
                continue  # Viernes Santo, Domingo García, Lunes de Pascua
            if re.search(rf"[{UPPER}][\wáéíóúñ]*\s+(?:de|del)$", before):
                continue  # Plaza de Mayo, Avenida de Marzo
            is_day = m.group(1) in DAYS_ES
            context = (r"(?:el|los|este|próximo|cada|todos los|un|del)$" if is_day
                       else r"(?:de|del|en|desde|hasta|para|a|finales de|principios de|mediados de)$")
            if re.search(context, before, re.I) or re.match(r"\s*\d", after):
                add(n, "N1", f"month or day in capitals: {excerpt(line, m.start(), m.end())}")
        for m in re.finditer(rf"[{UPPER}][\wáéíóúñ]+(?:\s+(?:{LOWER_WORDS_ES}|[{UPPER}][\wáéíóúñ]+))+", line):
            span = m.group(0)
            lowers = re.findall(rf"\b(?:{LOWER_WORDS_ES})\b", span)
            if len(lowers) >= 2:
                add(n, "N1", f"articles or prepositions in capitals: {span}")

        if line.lstrip().startswith("—"):
            for m in re.finditer(r"—\s+[a-záéíóúñ]+\b|[a-záéíóúñ.,]\s+—(?=[.,;:\s]|$)", line):
                add(n, "N3", f"dialogue raya with a space inside: {excerpt(line, m.start(), m.end())}")
        else:
            for m in re.finditer(r"\w\s—\s\w", line):
                add(n, "N3/E8", f"spaced raya outside dialogue: {excerpt(line, m.start(), m.end())}")
            rest = re.sub(r"—[^\s—][^—\n]*?[^\s—]—", "", line)
            rest = re.sub(r"\w\s—\s\w", "", rest)
            if "—" in rest:
                add(n, "N3", f"inciso raya without its closing raya: {line.strip()[:70]}")
        calques = (r"\b(?:tomar|tomó|tomará|toma|toman|tomaron|tomarán) lugar\b|\bhac(?:er|e|en) sentido\b"
                   r"|\baplicar (?:a|para) (?:un|el|este|ese) puesto\b")
        for m in re.finditer(calques, line, re.I):
            add(n, "N4", f"calque: {excerpt(line, m.start(), m.end())}")
        for m in re.finditer(r"\beventualmente\b", line, re.I):
            add(n, "N4?", f"check meaning: 'eventualmente' means 'possibly', not 'finally': {excerpt(line, m.start(), m.end())}")
        for m in re.finditer(r"\b[a-záéíóúñ]+-(?:calidad|plazo|nivel)\b", line, re.I):
            add(n, "N5", f"hyphenated compound: {m.group(0)}")

    for start, para in paragraphs_with_lines(norm):
        if lang == "es":
            flat = re.sub(r"https?://\S+", "", para.replace("\n", " ")).replace("...", "…")
            quote_rx = r"«([^»]*)»|“([^”]*)”|\"([^\"]*)\""
            pieces = ["".join(g for g in m.groups() if g) for m in re.finditer(quote_rx, flat)]
            pieces.append(re.sub(quote_rx, " ", flat))
            for piece in pieces:
                for sentence in re.split(r"(?<=[.!?])\s+", piece):
                    if "?" in sentence and "¿" not in sentence:
                        add(start, "N2", f"missing ¿: {sentence.strip()[:70]}")
                    if "!" in sentence and "¡" not in sentence:
                        add(start, "N2", f"missing ¡: {sentence.strip()[:70]}")
        counts: dict[str, int] = {}
        patterns = [rf"\b{re.escape(w)}\b" if w.isalpha() else rf"\b{w}\b" for w in AI_WORDS[lang]]
        if lang == "es":
            patterns += AI_PATTERNS_ES
        for pat in patterns:
            for m in re.finditer(pat, para, re.I):
                counts[m.group(0).lower()] = counts.get(m.group(0).lower(), 0) + 1
        total = sum(counts.values())
        if total >= 3:
            listed = ", ".join(f"{w} ×{c}" if c > 1 else w for w, c in sorted(counts.items()))
            add(start, "E10", f"{total} stock or translated words in one paragraph: {listed}")

    body = [l for i, l in enumerate(lines) if not is_heading(lines, i)]
    connectors = 0
    for l in body:
        if l.lstrip().startswith("—"):
            continue
        pairs = len(re.findall(r"—[^\s—][^—\n]*?[^\s—]—", l)) if lang == "es" else 0
        connectors += max(0, l.count("—") - 2 * pairs)
        connectors += len(re.findall(r"\s–\s", l)) + len(re.findall(r"\s--\s", l))
    if connectors:
        noun = "connector" if connectors == 1 else "connectors"
        msg = f"{connectors} dash {noun} outside dialogue and headings"
        if connectors >= 3:
            words = max(1, len(re.findall(r"\w+", norm)))
            msg += f" ({connectors / words * 1000:.1f} per 1,000 words)"
        add(0, "E8", msg)

    styles = {
        "« »": r"«[^»\n]*»",
        "“ ”": r"“[^”\n]*”",
        "‘ ’": r"‘[^’\n]*’",
        '" "': r"\"[^\"\n]*\"",
        "' '": r"(?:(?<=^)|(?<=[\s(]))'[^'\n]{2,}?'(?=[\s.,;:!?)]|$)",
    }
    spans = []
    for name, rx in styles.items():
        for m in re.finditer(rx, text, re.M):
            spans.append((m.start(), m.end(), name))
    top_level: dict[str, int] = {}
    for s, e, name in spans:
        if not any(s2 < s and e <= e2 for s2, e2, _ in spans):
            top_level[name] = top_level.get(name, 0) + 1
    if len(top_level) > 1:
        add(0, "N2", "mixed quotation marks at the same level: "
            + ", ".join(f"{k} ×{v}" for k, v in sorted(top_level.items())))

    if re.search(r"(?m)^\s*(?:#{1,6}\s|\*\*[^*]+\*\*\s*:)", text) or "**" in text:
        add(0, "R5?", "Markdown found: remove it if the target format is plain text")

    return sorted(hits, key=lambda h: (h[0], h[1], h[2]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical pre-pass for deslop.")
    parser.add_argument("path", help="file to check, or - for stdin")
    parser.add_argument("--lang", choices=["es", "en"], help="language of the text (auto-detected if omitted)")
    args = parser.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
    else:
        with open(args.path, encoding="utf-8") as f:
            text = f.read()

    lang = args.lang or detect_lang(text)
    hits = check(text, lang)
    if not args.lang:
        other = "en" if lang == "es" else "es"
        es_w = len(re.findall(r"\b(?:el|la|los|las|que|de|y|en|una|es|por|con|para)\b", text, re.I))
        en_w = len(re.findall(r"\b(?:the|and|of|to|is|that|for|with|on|an|you|it)\b", text, re.I))
        if min(es_w, en_w) >= 5 and min(es_w, en_w) / max(es_w, en_w) > 0.3:
            print(f"Note: the text looks mixed. Run again with --lang {other} for the other language's passages.")
    print(f"deslop check · language: {lang} · {len(hits)} candidate(s)")
    print("Candidates only: apply the skill's rules before changing anything.")
    for n, code, msg in hits:
        where = f"line {n}" if n else "whole text"
        print(f"- {where} · {code} · {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
