BClassPitch

Simple impress.js pitch deck for BClass (BClass — Pitch Deck). This repository contains a single-page HTML presentation built with impress.js and custom styles/assets.

Quick upload to GitHub

Option A — GitHub CLI (recommended):
1. Install GitHub CLI (gh) and authenticate: gh auth login
2. Create and push the repo:
   gh repo create BClassPitch --public --source=. --remote=origin --push

Option B — Git commands:
1. git init
2. git add .
3. git commit -m "Initial commit - BClass pitch deck"
4. Create a repository on GitHub named "BClassPitch" and copy the repository URL.
5. git remote add origin <REPO_URL>
6. git branch -M main
7. git push -u origin main

Project structure

- index.html        — main presentation file (impress.js)
- Assets/           — images, fonts and other static assets

Notes

- The presentation includes local font files (Assets/fonts). Keep those files when publishing.
- Use the GitHub CLI command above to create the remote and push in one step.

License

This project is licensed under the MIT License (see LICENSE).