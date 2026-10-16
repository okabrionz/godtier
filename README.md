# God Tier Prompts ⚡

**Daily god-tier AI prompts — generated, ranked, and published every day.**

One best prompt, published at 8 AM WIB. Works with GPT-4o, Claude 3.5, Gemini 2.0, and every LLM.

## 🌐 Live Site

**[godtier.store](https://godtier.store)** (set up GitHub Pages + CNAME)

## 🚀 How It Works

1. **Generate** — Each day, the system generates 5 prompt candidates via HuggingFace Inference API (free tier) or OpenAI
2. **Rank** — Each candidate scored on clarity, specificity, structure, and usefulness (10-point scale)
3. **Publish** — The highest-scoring prompt is automatically committed to this repo via GitHub Actions
4. **Deploy** — Hugo builds the site and GitHub Pages deploys it

## 🏗️ Architecture

```
god-tier-prompts/
├── content/
│   ├── prompts/           # Auto-generated daily prompts (YYYY/slug.md)
│   └── about/             # Static about page
├── themes/godtier/        # Custom dark theme (red accent)
│   ├── layouts/           # Templates (home, list, single, taxonomy)
│   └── assets/css/        # OKLCH dark theme CSS
├── scripts/
│   └── generate_and_publish.py  # AI prompt generator + ranker
├── .github/workflows/
│   └── daily-publish.yml  # Cron scheduler (daily 8 AM WIB)
├── hugo.yaml              # Hugo config
└── README.md
```

## 🔧 Setup

### Prerequisites

- [Hugo](https://gohugo.io) (v0.165+) — local dev only
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
   - Branch: `main` (or whichever branch)
5. **Run the workflow manually** — Go to **Actions → Daily Prompt Publish → Run workflow**
6. **Set up domain** (optional) — Go to **Settings → Pages → Custom domain** and enter `godtier.store`, then update your DNS with the GitHub Pages CNAME

The workflow runs daily at **1 AM UTC (8 AM WIB)**. It will:
- Generate 5 prompt candidates via HF Inference API
- Rank them on clarity, specificity, structure, usefulness
- Publish the best one as `content/prompts/YYYY/slug.md`
- Build Hugo and deploy to GitHub Pages

### Customization

| Variable | Default | Description |
|----------|---------|-------------|
| `CANDIDATES` | 5 | Number of prompt candidates per day |
| `OUTPUT_DIR` | `content/prompts` | Where markdown files are written |
| `HF_TOKEN` | — | HuggingFace Inference API token |
| `OPENAI_API_KEY` | — | OpenAI API key (fallback) |

## 📄 License

MIT — do whatever you want.

---

Built by [okabrionz](https://superkilat.com) — web dev & agentic AI studio, Tasikmalaya.
