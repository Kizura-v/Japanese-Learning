# English ↔ Japanese Dictionary

This folder adds a **searchable dictionary integration** using **JMdict**, the Electronic Dictionary Research and Development Group's Japanese–English lexical database.

## Quick start

Requires Python 3 and internet access for the first download.

```bash
python3 dictionary/lookup.py 食べる
python3 dictionary/lookup.py たべる --direction jp
python3 dictionary/lookup.py greenhouse --direction en
python3 dictionary/lookup.py help --direction en --limit 25
python3 dictionary/lookup.py 引っ張る --json
python3 dictionary/lookup.py 食べる --refresh
```

The first lookup downloads the English-only compressed JMdict data into `dictionary/cache/`. Subsequent lookups reuse the local file. `--refresh` downloads a newer version. The source file is **not committed to this repository** because it is large and changes frequently.

**Dictionary entries do not automatically contain Romanji.** JMdict provides Japanese written forms, kana readings, and English definitions; Romanji must be generated or verified separately. Results may contain uncommon, technical, or multiple senses; select the appropriate one before adding a term to the curated learning workbook. English lookup is substring-based and may produce broad results.

## How this fits the project

- **Dictionary:** broad lookup of Japanese spellings, readings, and English senses.
- **Google Sheets:** curated practical vocabulary, concrete English examples, usage explanations, and register.
- **E-R-K daily training:** build and speak natural sentences; do not memorize every dictionary sense as equally common.

The study tab format remains **Eng | Romanji | Hiragana | Japanese | Examples | Group | Usage | Register**.

## Source, attribution, and licence

**JMdict/EDICT:** Copyright © Electronic Dictionary Research and Development Group (EDRDG) and its contributors.

> These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence.

- Official project: https://www.edrdg.org/wiki/JMdict-EDICT_Dictionary_Project.html
- Official download: https://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz
- Licence terms: https://www.edrdg.org/edrdg/newlic.html
- Licence: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)

Any distributed derived dictionary data must preserve the required attribution and applicable share-alike terms. The script in this folder is original integration code; it does not claim ownership of JMdict entries.

**Note:** This is a Python command-line lookup, not yet a browser-based dictionary page. It has been committed and read back, but not executed against the full live JMdict download in this environment.
