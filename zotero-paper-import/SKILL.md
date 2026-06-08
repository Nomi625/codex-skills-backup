---
name: zotero-paper-import
description: Use when the user wants papers, DOI lists, article titles, Markdown literature tables, RIS/BibTeX files, or PDFs added to a local Zotero library, especially from Chinese academic writing notes or partially specified paper lists.
---

# Zotero Paper Import

## Overview

Import papers conservatively: confirm identifiers first, use Zotero-supported import paths, and never write directly to `zotero.sqlite`.

## Workflow

1. Read the user's source file with the correct encoding, usually UTF-8 for Chinese Markdown.
2. Extract explicit DOI/URL/title data. If entries are only "author, year, journal + topic", resolve metadata through Crossref or targeted web search before importing.
3. Classify confidence:
   - High: DOI confirmed and title/journal/year match the source row.
   - Medium: title and journal match but author/year differ slightly; ask or mark for review.
   - Low: search results are ambiguous; do not import as a real paper.
4. Generate `RIS` or `BibTeX` from confirmed metadata. Prefer RIS for Zotero desktop imports.
5. Start Zotero if needed and import the file. Do not edit the SQLite database directly.
6. Verify by checking Zotero UI state, database modified time, Local API if enabled, or user-visible imported collection. Be explicit about unresolved papers and PDF limits.

## Local Zotero Checks

Use these checks on Windows:

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'zotero' }
Test-NetConnection -ComputerName 127.0.0.1 -Port 23119
curl.exe -s -X POST http://127.0.0.1:23119/connector/ping -H "Content-Type: application/json" -H "Zotero-Connector-API-Version: 3" -d "{}"
```

If Zotero is not running:

```powershell
Start-Process -FilePath 'C:\Program Files\Zotero\zotero.exe' -WindowStyle Hidden
```

Connector `/connector/detect` can identify translators, but `/connector/saveItems` may return `500` for DOI-only saves in automation. When this happens, switch to RIS import instead of retrying blindly.

## RIS Generation

Use `scripts/make_ris_from_dois.py` when the input DOI list is known:

```powershell
python scripts\make_ris_from_dois.py --doi-file dois.txt --output papers.ris
```

The script uses Crossref JSON and writes RIS with title, authors, journal, year, DOI, URL, volume/issue/pages when available.

For source Markdown without DOI values, search Crossref with `query.bibliographic` and inspect top results. Do not import an item unless the title, journal, year, and author family agree with the user's source.

## Importing Into Zotero

Preferred import path:

```powershell
Start-Process -FilePath 'C:\path\to\papers.ris'
```

If Windows file association does not open Zotero:

```powershell
& 'C:\Program Files\Zotero\zotero.exe' 'C:\path\to\papers.ris'
```

If Zotero shows an import dialog, the user may need to confirm. Report this clearly instead of claiming completion.

## PDFs

Importing metadata is not the same as downloading full-text PDFs. Zotero can only attach PDFs when:

- the item is open access,
- the user's institution/proxy/session grants access,
- the publisher translator exposes the PDF, or
- the user has a local PDF to attach.

For "download papers to Zotero", first import metadata and then try Zotero's "Find Available PDF" flow where possible. Never use questionable sources or bypass publisher access controls.

## Common Pitfalls

- Chinese Markdown may display as mojibake if PowerShell omits `-Encoding UTF8`.
- Do not trust vague rows like `Chen et al., 2022, Applied Thermal Engineering` without title/DOI confirmation.
- Do not directly write Zotero's SQLite database; it may be locked and direct writes can corrupt the library.
- Local API at `/api/...` may return `Local API is not enabled`; use RIS import unless the user has enabled it.
- Record unresolved entries separately so the user can correct titles or provide DOI values.
