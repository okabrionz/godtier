# God Tier Prompts ⚡

**Daily god-tier AI prompts — generated, ranked, and published every day.**

One best prompt published daily at **7 AM WIB** (UTC+7). Works with GPT-4o, Claude 3.5, Gemini 2.0, and every LLM.

---

## 🌐 Live Site

**GitHub Pages:**

```
https://okabrionz.github.io/godtier/
```

*(Custom domain: godtier.store — not configured yet. Default GitHub Pages domain shown above.)*

---

## 🚀 How It Works

1. **Generate** — Each day, the system generates 10 prompt candidates via HuggingFace Inference API (free tier) or OpenAI
2. **Rank** — Each candidate scored on clarity, specificity, structure, and usefulness (10-point scale)
3. **Publish** — Top 10 prompts automatically committed to this repo via GitHub Actions
4. **Deploy** — Hugo builds the site and GitHub Pages deploys it

> VS Code integration available — see [God Tier Prompts VS Code Extension](https://github.com/okabrionz/god-tier-prompts-vscode-extension)

---

## 🏗️ Architecture

```
godtier/
├── .github/workflows/
│   └── daily-publish.yml     # Cron scheduler (daily 7 AM WIB = 0 AM UTC)
├── content/
│   ├── prompts/2026/          # Auto-generated daily prompts (10/day)
│   ├── builder/index.md       # Interactive prompt builder page
│   └── about/index.md
├── themes/godtier/
│   ├── layouts/               # Templates (home, list, single, taxonomy, builder)
│   └── assets/
│       ├── css/main.css       # OKLCH dark theme CSS (18KB)
│       └── fonts/             # Space Grotesk + Sora + JetBrains Mono
├── scripts/
│   └── generate_and_publish.py  # AI prompt generator + ranker (10/day)
├── hugo.yaml                  # Hugo config (v0.165)
├── README.md                  # This file
└── SETUP.md                   # Full setup guide (secrets, pages, troubleshooting)
```

---

## 🎨 Design System

- **Display font:** Space Grotesk (characterful, techy)  
- **Body font:** Sora  
- **Code font:** JetBrains Mono  
- **Palette:** Dark #0a0a0d + Red #ff2b4f + Amber #ffb020 (OKLCH-toned)  
- **Signature:** Interactive "prompt terminal" in hero with typing animation  
- **Pages:** Homepage (terminal hero + prompt cards), Prompt Builder (7-step form + live preview), Categories/Tags grid

---

## 🔧 Setup

### Prerequisites

- [Hugo](https://gohugo.io) (v0.165+, extended) — for local dev only
- Python 3.11+ — for the generator script
- [HuggingFace Inference API token](https://huggingface.co/settings/tokens) — free tier, or OpenAI API key

### Local Development

```bash
# Clone
git clone https://github.com/okabrionz/god-tier-prompts.git
cd god-tier-prompts

# Install Python deps
pip install requests pyyaml

# Set API token
export HF_TOKEN="hf_xxxxxxxx"   # or export OPENAI_API_KEY="sk-xxx"

# Generate a prompt manually
python scripts/generate_and_publish.py

# Preview site
hugo server --buildDrafts
```

### GitHub Actions Setup

1. **Create a new GitHub repo** (e.g., `god-tier-prompts`)
2. **Push this code:**

   ```bash
   cd god-tier-prompts
   git remote add origin https://github.com/YOUR_USERNAME/god-tier-prompts.git
   git push -u origin main
   ```

3. **Add API secrets** — Go to **Settings → Secrets and variables → Actions** and add:
   - `HF_TOKEN` — your [HuggingFace Inference API token](https://huggingface.co/settings/tokens) (free tier works)
   - or `OPENAI_API_KEY` — your OpenAI API key (fallback)

4. **Enable GitHub Pages** — Go to **Settings → Pages** and set:
   - Source: **GitHub Actions**
   - Branch: `main`
   - **Do not add a custom domain** (using GitHub Pages default domain)

5. **Run the workflow manually** — Go to **Actions → Daily Prompt Publish → Run workflow**

6. **Wait for deployment** — GitHub Pages builds automatically within ~2 minutes

The workflow runs daily at **0 AM UTC (7 AM WIB)**. It will:
- Generate 10 prompt candidates via HF Inference API
- Rank them on clarity, specificity, structure, usefulness
- Publish the top 10 as `content/prompts/2026/`
- Build the Hugo site and deploy to GitHub Pages

---

## 📊 Workflow Output

After each run, check the commit message for:

```
🤖 10 daily prompts (10 published, best: God Tier Coding Prompt: ... 9.x/10)
```

Check the deployed site:

```
https://okabrionz.github.io/godtier/prompts/2026/
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Workflow fails at "Generate" | Verify `HF_TOKEN` is valid in `Settings → Secrets` |
| Pages shows 404 | Ensure Pages source = `GitHub Actions` + branch `main` |
| Archive/v1 baseline commit appears | Old commit still in history — ignore, deploy uses latest |
| Lower case deletion of `cname`? | If you see `cname: godtier.store` in workflow, it was added by mistake — check the latest commit |

---

## 📄 License

MIT — free to use, modify, and deploy. Credit `okabrionz` if you reuse the code.
