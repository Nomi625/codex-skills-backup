$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$destRoot = Join-Path $HOME ".codex\skills"

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

$exclude = @(".git", ".github")
Get-ChildItem -Force -Path $repoRoot | Where-Object {
    $_.PSIsContainer -and
    ($exclude -notcontains $_.Name) -and
    (Test-Path (Join-Path $_.FullName "SKILL.md") -or $_.Name -eq "_shared")
} | ForEach-Object {
    $dest = Join-Path $destRoot $_.Name
    Copy-Item -Recurse -Force -LiteralPath $_.FullName -Destination $dest
    Write-Host "Installed $($_.Name) -> $dest"
}

Write-Host ""
Write-Host "Done. Restart Codex to load updated skills."

