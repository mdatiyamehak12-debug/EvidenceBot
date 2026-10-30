# EvidenceBot - Push to GitHub Utility Script
param (
    [Parameter(Mandatory=$false)]
    [string]$RepoUrl
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "            EVIDENCEBOT: UPLOAD TO GITHUB                   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (-not $RepoUrl) {
    $RepoUrl = Read-Host "Please enter your GitHub repository URL (e.g., https://github.com/username/EvidenceBot.git)"
}

if (-not $RepoUrl) {
    Write-Host "Error: No repository URL provided. Aborting." -ForegroundColor Red
    exit 1
}

# Clean any existing origin remote
git remote remove origin 2>$null

# Add new remote
Write-Host "Linking repository to $RepoUrl..." -ForegroundColor Yellow
git remote add origin $RepoUrl
git branch -M main

# Push to GitHub
Write-Host "Pushing project files to GitHub..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Your EvidenceBot project is now live on GitHub:" -ForegroundColor Green
    Write-Host "👉 $RepoUrl" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️ Push encountered an issue. Please verify your credentials or permissions." -ForegroundColor Yellow
}
