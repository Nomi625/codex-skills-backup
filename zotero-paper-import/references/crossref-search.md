# Crossref Search Notes

Use Crossref when the user provides partial paper citations.

Search pattern:

```powershell
$q = 'Luo 2022 Chemical Engineering Journal Battery thermal management systems phase change material comprehensive review'
$url = 'https://api.crossref.org/works?query.bibliographic=' + [uri]::EscapeDataString($q) + '&rows=5'
curl.exe -L -s $url
```

Inspect `message.items[]`:

- `score`
- `DOI`
- first author family
- `container-title`
- `published.date-parts` or `issued.date-parts`
- `title`

Treat a match as high confidence only when title intent, journal, year, and author family all align. If the best result has the wrong first author or year, mark it unresolved instead of importing.
