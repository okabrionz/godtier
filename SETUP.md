# Setup God Tier Prompts — GitHub Secrets + Pages

## 1. Setup Secrets

Buka: `https://github.com/okabrionz/godtier/settings/secrets/actions`

Klik **"New repository secret"** untuk masing-masing:

| Nama Secret | Value | Cara Dapat |
|-------------|-------|------------|
| `HF_TOKEN` | HuggingFace API token | https://huggingface.co/settings/tokens → New token (role: read) |
| `OPENAI_API_KEY` | OpenAI API key | https://platform.openai.com/api-keys → Create new secret key |

> OpenAI optional — kalau kosong, script fallback ke HF saja. Tapi kalau dua-duanya kosong, workflow gagal.

---

## 2. Aktifkan GitHub Pages

Buka: `https://github.com/okabrionz/godtier/settings/pages`

- **Source**: `Deploy from a branch`
- **Branch**: `main` / `/(root)`
- Klik **Save**

Tunggu 1-2 menit. Site akan live di `https://okabrionz.github.io/godtier/`.

Untuk custom domain `godtier.store`:
- Tambahkan file `CNAME` di root repo berisi `godtier.store`
- Tambahkan DNS record di domain registrar

---

## 3. Setup Custom Domain (godtier.store)

### a. File CNAME di repo
```bash
echo "godtier.store" > CNAME
git add CNAME && git commit -m "Add CNAME for custom domain"
git push
```

### b. DNS Record
```
Type:   CNAME
Name:   @ atau godtier
Value:  okabrionz.github.io
TTL:    300
```

### c. Enforce HTTPS
Di Settings → Pages → centang **"Enforce HTTPS"** setelah DNS propagate.

---

## 4. Test Workflow Manual

Buka: `https://github.com/okabrionz/godtier/actions`

1. Klik **"Daily Prompt Publish"** di sidebar kiri
2. Klik **"Run workflow"** → tombol hijau
3. Tunggu 2-5 menit

Kalau sukses:
- 10 file baru di `content/prompts/2026/`
- Commit: `🤖 10 daily prompts (10 published, best: ... 9.x/10)`
- Deploy otomatis

---

## 5. Verifikasi Schedule

Cron `0 0 * * *` = **7:00 AM WIB** setiap hari.

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Workflow gagal di step "Generate" | Cek `HF_TOKEN` valid di hf.co/settings/tokens |
| Deploy 404 | Pages source = `main` branch, bukan `gh-pages` |
| Custom domain tidak resolve | DNS propagate 5-30 menit. Cek `dig godtier.store` |
| Build error di Hugo | Version harus `0.165.0` (match local) |
| Pages tidak update | Clear cache browser |

---

## Struktur Repo

```
godtier/
├── .github/workflows/daily-publish.yml    # CI/CD: 7 AM WIB daily
├── content/prompts/2026/*.md              # 10 prompts/hari
├── scripts/generate_and_publish.py        # LLM generate + rank + publish
├── themes/godtier/                        # Hugo theme
└── CNAME                                  # godtier.store
```
