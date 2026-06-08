#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def first(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def date_year(item):
    for key in ("published-print", "published-online", "published", "issued"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def clean(value):
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def fetch_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    result = subprocess.run(
        ["curl.exe", "-L", "-sS", url],
        text=True,
        capture_output=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl failed for {doi}")
    data = json.loads(result.stdout)
    return data["message"]


def item_to_ris(item, fallback_doi):
    lines = ["TY  - JOUR"]
    title = first(item.get("title"))
    if title:
        lines.append(f"T1  - {clean(title)}")
    for author in item.get("author", []):
        family = author.get("family", "")
        given = author.get("given", "")
        name = f"{family}, {given}".strip(", ")
        if name:
            lines.append(f"AU  - {clean(name)}")
    journal = first(item.get("container-title"))
    if journal:
        lines.append(f"JO  - {clean(journal)}")
        lines.append(f"JF  - {clean(journal)}")
    for ris_key, crossref_key in (("VL", "volume"), ("IS", "issue"), ("SP", "page")):
        if item.get(crossref_key):
            lines.append(f"{ris_key}  - {clean(item[crossref_key])}")
    year = date_year(item)
    if year:
        lines.append(f"PY  - {year}")
    issn = first(item.get("ISSN"))
    if issn:
        lines.append(f"SN  - {clean(issn)}")
    doi = item.get("DOI", fallback_doi)
    lines.append(f"DO  - {clean(doi)}")
    lines.append(f"UR  - https://doi.org/{clean(doi)}")
    abstract = item.get("abstract")
    if abstract:
        lines.append(f"AB  - {clean(abstract)}")
    lines.append("ER  -")
    return "\n".join(lines)


def read_dois(path):
    values = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(line.replace("https://doi.org/", "").replace("http://doi.org/", ""))
    return values


def main():
    parser = argparse.ArgumentParser(description="Build a Zotero-importable RIS file from DOI values.")
    parser.add_argument("--doi-file", required=True, help="UTF-8 text file with one DOI per line")
    parser.add_argument("--output", required=True, help="Output RIS path")
    args = parser.parse_args()

    records = []
    failures = []
    for doi in read_dois(args.doi_file):
        try:
            item = fetch_crossref(doi)
            records.append(item_to_ris(item, doi))
            print(f"ok {doi}", file=sys.stderr)
        except Exception as exc:
            failures.append((doi, str(exc)))
            print(f"failed {doi}: {exc}", file=sys.stderr)

    Path(args.output).write_text("\n\n".join(records) + "\n", encoding="utf-8")
    if failures:
        print("\nUnresolved DOI values:", file=sys.stderr)
        for doi, reason in failures:
            print(f"- {doi}: {reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
