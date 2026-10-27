#!/usr/bin/env python3
"""Download JMdict English and look up Japanese or English terms.

Source: EDRDG JMdict, CC BY-SA 4.0.
This script uses the Python standard library only.
"""
import argparse
import gzip
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

URL = "https://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz"
CACHE = Path(__file__).resolve().parent / "cache" / "JMdict_e.gz"

def download(force=False):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    if force or not CACHE.exists():
        print("Downloading JMdict English from EDRDG...")
        request = urllib.request.Request(URL, headers={"User-Agent": "Japanese-Learning-Dictionary/1.0"})
        with urllib.request.urlopen(request, timeout=120) as response, CACHE.open("wb") as output:
            import shutil
            shutil.copyfileobj(response, output)
    return CACHE

def records(path):
    with gzip.open(path, "rb") as stream:
        for _, elem in ET.iterparse(stream, events=("end",)):
            if elem.tag != "entry":
                continue
            written = [x.text for x in elem.findall("./k_ele/keb") if x.text]
            readings = [x.text for x in elem.findall("./r_ele/reb") if x.text]
            meanings = []
            for sense in elem.findall("./sense"):
                for gloss in sense.findall("gloss"):
                    if gloss.text and gloss.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "eng") == "eng":
                        meanings.append(gloss.text)
            if meanings:
                yield {"japanese": written or readings, "readings": readings, "english": meanings}
            elem.clear()

def matches(entry, query, direction):
    q = query.casefold()
    if direction in ("auto", "jp"):
        if any(query in s for s in entry["japanese"] + entry["readings"]):
            return True
    if direction in ("auto", "en"):
        if any(re.search(r"(?<!\\w)" + re.escape(q) + r"(?!\\w)", m.casefold()) for m in entry["english"]):
            return True
    return False

def main():
    p = argparse.ArgumentParser(description="English/Japanese JMdict lookup")
    p.add_argument("query", help="Japanese word, kana reading, or English term")
    p.add_argument("--direction", choices=("auto", "en", "jp"), default="auto")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--refresh", action="store_true", help="Download latest JMdict")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.limit < 1:
        p.error("--limit must be positive")
    result = []
    for entry in records(download(a.refresh)):
        if matches(entry, a.query, a.direction):
            result.append(entry)
            if len(result) >= a.limit:
                break
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result:
            print(" / ".join(item["japanese"]), "[" + ", ".join(item["readings"]) + "]")
            print("  " + "; ".join(item["english"][:8]))
        if not result:
            print("No matches. Try a shorter term or another reading.")

if __name__ == "__main__":
    main()
