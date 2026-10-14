#!/usr/bin/env python3
"""Pubblica soltanto una banca dati con manifest e SHA-256 verificati."""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ZIP = Path("ViaLibera_Feed_Aggiornamenti.zip")
EXPECTED = {"AM": 2035, "AB": 7106, "SUP": 3456, "CQC": 5528, "CAP": 514}
PREFIX = "https://raw.githubusercontent.com/matteofronzi199076-dev/ViaLibera-Quiz-Updates/main/"
MAX_UNCOMPRESSED = 25_000_000

def invalid(message):
    raise ValueError(message)

def main():
    if not ZIP.is_file():
        invalid(f"Archivio assente: carica {ZIP.name} nella radice del repository.")
    if ZIP.stat().st_size > 15_000_000:
        invalid("ZIP troppo grande.")
    payloads = {}
    with zipfile.ZipFile(ZIP) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            invalid("ZIP con nomi duplicati.")
        required = {"manifest.json"} | {bank + ".json" for bank in EXPECTED}
        if not required.issubset(names):
            invalid("Mancano manifest.json o uno dei cinque JSON.")
        if sum(entry.file_size for entry in z.infolist()) > MAX_UNCOMPRESSED:
            invalid("Contenuto non compresso troppo grande.")
        for name in required:
            if z.getinfo(name).file_size > 12_000_000:
                invalid(f"File troppo grande: {name}")
            payloads[name] = z.read(name)

    meta = json.loads(payloads["manifest.json"].decode("utf-8"))
    if meta.get("schema") != 1 or set(meta.get("banks", {})) != set(EXPECTED):
        invalid("Formato del manifest non valido o banche incomplete.")
    for bank, count in EXPECTED.items():
        name = bank + ".json"
        raw = payloads[name]
        item = meta["banks"][bank]
        if item.get("url") != PREFIX + name:
            invalid(f"Indirizzo non corrispondente al repository per {bank}.")
        digest = hashlib.sha256(raw).hexdigest()
        if item.get("sha256") != digest:
            invalid(f"SHA-256 errato per {bank}.")
        if item.get("count") != count:
            invalid(f"Conteggio atteso errato in manifest: {bank}.")
        body = json.loads(raw.decode("utf-8"))
        if body.get("bank") != bank:
            invalid(f"Identificativo banca non valido: {bank}.")
        questions = body.get("questions")
        figures = body.get("figures")
        if not isinstance(questions, list) or len(questions) != count:
            invalid(f"Numero domande errato: {bank}.")
        if not isinstance(figures, dict):
            invalid(f"Figure mancanti o malformate: {bank}.")
        for key, value in figures.items():
            if not isinstance(key, str) or not isinstance(value, str) or not re.match(r"^data:image/(webp|png|jpeg);base64,[A-Za-z0-9+/=]+$", value):
                invalid(f"Immagine non valida in {bank}.")
        ids = set()
        for q in questions:
            if not isinstance(q, dict) or not isinstance(q.get("id"), str) or q["id"] in ids:
                invalid(f"Quesito duplicato o senza ID in {bank}.")
            ids.add(q["id"])
            if not isinstance(q.get("question"), str) or len(q["question"].strip()) < 6:
                invalid(f"Testo domanda invalido: {bank}, {q['id']}")
            if bank == "CAP":
                opts = q.get("options")
                if not isinstance(opts, list) or len(opts) != 3 or any(not isinstance(x, str) or not x.strip() for x in opts):
                    invalid(f"Opzioni CAP malformate: {q['id']}")
                if type(q.get("answer")) is not int or not 0 <= q["answer"] < len(opts):
                    invalid(f"Risposta CAP malformata: {q['id']}")
            elif type(q.get("answer")) is not bool:
                invalid(f"Risposta V/F non valida: {bank}, {q['id']}")
            if q.get("image") and q["image"] not in figures:
                invalid(f"Figura assente: {bank}, {q['id']}")
            if bank == "CQC" and not isinstance(q.get("tipologia"), int):
                invalid(f"Tipologia CQC assente: {q['id']}")
        print(f"OK {bank}: {len(questions)} quesiti, {len(figures)} figure, SHA-256 {digest[:14]}…")

    for name, raw in payloads.items():
        Path(name).write_bytes(raw)
    print("PUBBLICAZIONE VALIDATA: tutti i cinque JSON e il manifest sono pronti.")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError, zipfile.BadZipFile) as exc:
        print("ERRORE DI VALIDAZIONE:", exc, file=sys.stderr)
        sys.exit(1)
