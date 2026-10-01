$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw "Install Git first." }
if (!(Get-Command gh -ErrorAction SilentlyContinue)) { throw "Install GitHub CLI first, then run gh auth login." }
gh auth status
if ($LASTEXITCODE -ne 0) { throw "Run gh auth login first." }
if (Test-Path .git) { throw "Git already initialized. Use manual commands in docs/GITHUB_AND_DEPLOYMENT.md." }
git init
if ($LASTEXITCODE -ne 0) { throw "git init failed" }
git branch -M main
git add .
git commit -m "Build customer churn prediction and retention system"
if ($LASTEXITCODE -ne 0) { throw "Commit failed. Configure your Git identity and use the manual guide." }
gh repo create customer-churn-retention --private --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw "Upload failed. Check repository existence and account permissions." }
