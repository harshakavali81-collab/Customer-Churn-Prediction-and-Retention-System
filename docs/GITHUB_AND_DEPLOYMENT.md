# GitHub and deployment

Published source: https://github.com/harshakavali81-collab/Customer-Churn-Prediction-and-Retention-System
Public app hosting is not yet completed. The instructions below are retained for making a separate copy.
## GitHub upload (Windows)
Your project folder is ready to commit. The source repository above contains the project. Use the steps below only to publish a separate copy.
1. Visit https://github.com/new while signed in as your intended account.
2. Name: `customer-churn-retention`. Choose visibility and create an empty repository (no auto README, license or gitignore).
3. In the extracted project's VS Code terminal, run:
```powershell
git init
git branch -M main
git add .
git commit -m "Build reproducible customer churn and retention demo"
git remote add origin https://github.com/harshakavali81-collab/customer-churn-retention.git
git push -u origin main
```
Git may ask you to authenticate or set your name/email. Use your actual Git identity; never paste a password into a script. If using another account, replace the repository URL. These commands assume a new directory with no remote.

Alternatively run `publish_github.ps1` after installing GitHub CLI and signing in with `gh auth login`. It creates a PRIVATE repo by default and pushes it; review visibility before sharing. The script is included, not executed here.

## Local deployment
```bash
python -m streamlit run app.py
```

## Docker
```bash
docker build -t churn-retention .
docker run --rm -p 8501:8501 churn-retention
```
Docker configuration is provided but not built in this environment.

## Streamlit Community Cloud
Once GitHub upload is complete, sign in to https://share.streamlit.io/ with GitHub, create an app from the repository's `main` branch, and set `app.py` as the entrypoint. Select Python 3.11 or 3.12 in advanced settings. Dependencies are in requirements.txt and model/data files are committed. Verify all three pages after deploy. This authenticated hosting step is not completed in this package.

Official deployment instructions checked on 2026-09-30:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started

## CI
The included GitHub Actions workflow installs dependencies, rebuilds the synthetic pipeline and runs tests on Python 3.11. The local tests have been run; hosted CI runs only after pushing. Pin transitive dependencies with a lock file for a longer-lived production release.
