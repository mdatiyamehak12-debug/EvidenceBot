# EvidenceBot - Push to GitHub Utility Script
param (
    [Parameter(Mandatory=$false)]
    [string]$RepoUrl = "https://github.com/mdatiyamehak12-debug/EvidenceBot.git"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "            EVIDENCEBOT: UPLOAD TO GITHUB                   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Clean and set remote
Write-Host "Linking repository to $RepoUrl..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $RepoUrl
git branch -M main

# Push project to GitHub with force to override initial empty license/readme commit
Write-Host "Pushing EvidenceBot codebase to GitHub..." -ForegroundColor Green
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Your EvidenceBot project is now live on GitHub:" -ForegroundColor Green
    Write-Host "👉 https://github.com/mdatiyamehak12-debug/EvidenceBot" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️ If prompted by Git Credential Manager, complete the sign-in in your browser window." -ForegroundColor Yellow
}
