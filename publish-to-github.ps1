$ErrorActionPreference = "Stop"

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoName,

    [string]$Description = "Backup of my Codex skills",

    [switch]$Public
)

if (-not $env:GITHUB_TOKEN) {
    throw "Set GITHUB_TOKEN first. Example: `$env:GITHUB_TOKEN='ghp_...'"
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$headers = @{
    "Accept" = "application/vnd.github+json"
    "Authorization" = "Bearer $env:GITHUB_TOKEN"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent" = "codex-skills-backup"
}

function Invoke-GitHubJson {
    param(
        [string]$Method,
        [string]$Uri,
        $Body = $null
    )

    $args = @{
        Method = $Method
        Uri = $Uri
        Headers = $headers
    }

    if ($null -ne $Body) {
        $args.Body = ($Body | ConvertTo-Json -Depth 20)
        $args.ContentType = "application/json"
    }

    Invoke-RestMethod @args
}

$owner = (Invoke-GitHubJson -Method Get -Uri "https://api.github.com/user").login

try {
    $repo = Invoke-GitHubJson -Method Post -Uri "https://api.github.com/user/repos" -Body @{
        name = $RepoName
        description = $Description
        private = (-not $Public.IsPresent)
        auto_init = $false
    }
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 422) {
        $repo = Invoke-GitHubJson -Method Get -Uri "https://api.github.com/repos/$owner/$RepoName"
    } else {
        throw
    }
}

$skipDirs = @(".git")
$files = Get-ChildItem -Path $repoRoot -Recurse -File -Force | Where-Object {
    $relative = Resolve-Path -LiteralPath $_.FullName -Relative
    -not ($skipDirs | Where-Object { $relative -like ".\$_\*" })
}

foreach ($file in $files) {
    $relative = [System.IO.Path]::GetRelativePath($repoRoot, $file.FullName).Replace("\", "/")
    if ($relative -eq "publish-to-github.ps1") {
        continue
    }

    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [Convert]::ToBase64String($bytes)
    $encodedPath = ($relative -split "/" | ForEach-Object { [System.Uri]::EscapeDataString($_) }) -join "/"
    $uri = "https://api.github.com/repos/$owner/$RepoName/contents/$encodedPath"

    $body = @{
        message = "Add $relative"
        content = $content
    }

    try {
        $existing = Invoke-GitHubJson -Method Get -Uri $uri
        if ($existing.sha) {
            $body.sha = $existing.sha
        }
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 404) {
            throw
        }
    }

    Invoke-GitHubJson -Method Put -Uri $uri -Body $body | Out-Null
    Write-Host "Uploaded $relative"
}

Write-Host ""
Write-Host "Repository ready: $($repo.html_url)"

