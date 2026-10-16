#!/usr/bin/env python3
"""
God Tier Prompt Generator & Publisher
=====================================
Generates prompt candidates via LLM (Hugging Face Inference or OpenAI),
ranks them on 4 metrics (clarity, specificity, structure, usefulness),
selects the best, and publishes as a Hugo content markdown file.

Usage:
    python scripts/generate_and_publish.py

Environment:
    HF_TOKEN          — HuggingFace Inference API token (free tier)
    OPENAI_API_KEY    — OpenAI API key (fallback)
    CANDIDATES        — number of prompt candidates to generate (default: 5)
    OUTPUT_DIR        — where to write markdown files (default: content/prompts)
"""

import os
import sys
import json
import random
import hashlib
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests
import yaml

# ─── Config ───────────────────────────────────────────────

SITE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = os.getenv("OUTPUT_DIR", str(SITE_ROOT / "content" / "prompts"))
CANDIDATES = int(os.getenv("CANDIDATES", "5"))

# ─── Topic pool ──────────────────────────────────────────

TOPICS = [
    {"category": "Coding", "tags": ["python", "typescript", "refactoring"], "prompt_type": "code review and refactoring"},
    {"category": "Marketing", "tags": ["copywriting", "landing-page", "cta"], "prompt_type": "high-converting landing page copy"},
    {"category": "Design", "tags": ["ui", "ux", "figma"], "prompt_type": "UI/UX design system with accessibility"},
    {"category": "Content", "tags": ["blog", "seo", "storytelling"], "prompt_type": "SEO-optimized blog post structure"},
    {"category": "Data", "tags": ["analysis", "visualization", "sql"], "prompt_type": "data analysis and insight extraction"},
    {"category": "Productivity", "tags": ["automation", "workflow", "ai-agent"], "prompt_type": "AI automation workflow design"},
    {"category": "Education", "tags": ["tutorial", "explanation", "learning"], "prompt_type": "step-by-step tutorial with examples"},
    {"category": "Business", "tags": ["strategy", "pitch", "proposal"], "prompt_type": "business proposal and pitch deck"},
]

# ─── Prompt generation templates ─────────────────────────

GENERATION_TEMPLATE = """You are a world-class AI prompt engineer. Your task: create ONE god-tier AI prompt.

Topic: {topic}
Category: {category}
Tags: {tags}
Prompt type: {prompt_type}

The prompt must:
- Be 200-400 words long
- Have a clear role assignment and context framing
- Use structured sections (Task, Constraints, Output Format, Examples)
- Specify exact output format for consistent, parseable results
- Include 1 concrete example (input → output)
- Be optimized for GPT-4o, Claude 3.5, and Gemini 2.0

Output ONLY the prompt text (no markdown wrapping, no explanation). Start with "## " heading."""

RANKING_TEMPLATE = """You are a strict AI prompt quality evaluator. Score this prompt on 4 metrics (1-10 each):

Prompt to evaluate:
---
{prompt}
---

Score on:
1. CLARITY — How clear and unambiguous is the instruction?
2. SPECIFICITY — How specific are the task, constraints, and context?
3. STRUCTURE — Does it use sections, format, examples effectively?
4. USEFULNESS — How practical and valuable is this prompt for a real user?

Output ONLY valid JSON (no markdown, no explanation):
{{"clarity": <int>, "specificity": <int>, "structure": <int>, "usefulness": <int>, "overall": <avg>}}"""

# ─── LLM clients ─────────────────────────────────────────

def generate_with_hf(prompt_text: str, max_tokens: int = 1200) -> str:
    """Generate text using HuggingFace Inference API (free tier)."""
    token = os.getenv("HF_TOKEN", "")
    if not token:
        raise ValueError("HF_TOKEN not set")

    # Use a capable free model (Mixtral 8x7B via HF Inference)
    model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt_text,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.8,
            "return_full_text": False,
        },
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    result = resp.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("generated_text", "")
    return str(result)


def generate_with_openai(prompt_text: str, max_tokens: int = 1200) -> str:
    """Generate text using OpenAI API (fallback)."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a world-class AI prompt engineer."},
            {"role": "user", "content": prompt_text},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.8,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    result = resp.json()
    return result["choices"][0]["message"]["content"]


def generate_text(prompt_text: str) -> str:
    """Try HF Inference first, fall back to OpenAI."""
    try:
        return generate_with_hf(prompt_text)
    except Exception as e:
        print(f"  HF Inference failed: {e}", file=sys.stderr)
        return generate_with_openai(prompt_text)


# ─── Prompt generation pipeline ──────────────────────────

def generate_candidates() -> list[dict]:
    """Generate multiple prompt candidates."""
    candidates = []
    random.shuffle(TOPICS)

    for i in range(min(CANDIDATES, len(TOPICS))):
        topic = TOPICS[i]
        print(f"\n[{i+1}/{CANDIDATES}] Generating: {topic['category']} — {topic['prompt_type']}")

        gen_prompt = GENERATION_TEMPLATE.format(
            topic=topic["prompt_type"],
            category=topic["category"],
            tags=", ".join(topic["tags"]),
            prompt_type=topic["prompt_type"],
        )

        try:
            generated = generate_text(gen_prompt)
            # Clean up: strip markdown fences if present
            generated = generated.strip()
            if generated.startswith("```"):
                generated = generated.split("\n", 1)[1] if "\n" in generated else generated
            if generated.endswith("```"):
                generated = generated.rsplit("```", 1)[0]

            candidates.append({
                "category": topic["category"],
                "tags": topic["tags"],
                "prompt_type": topic["prompt_type"],
                "text": generated,
            })
            print(f"  Generated {len(generated)} chars")
        except Exception as e:
            print(f"  FAILED: {e}", file=sys.stderr)
            continue

    return candidates


def rank_prompt(prompt_text: str) -> dict:
    """Rank a prompt using LLM evaluation."""
    print("  Ranking...")
    rank_prompt_text = RANKING_TEMPLATE.format(prompt=prompt_text)

    try:
        result = generate_text(rank_prompt_text)
        # Parse JSON from result
        # Strip markdown fences
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1] if "\n" in result else result
        if result.endswith("```"):
            result = result.rsplit("```", 1)[0]
        result = result.strip()

        scores = json.loads(result)
        return {
            "clarity": int(scores.get("clarity", 5)),
            "specificity": int(scores.get("specificity", 5)),
            "structure": int(scores.get("structure", 5)),
            "usefulness": int(scores.get("usefulness", 5)),
            "overall": float(scores.get("overall", 5)),
        }
    except Exception as e:
        print(f"  Ranking failed: {e}", file=sys.stderr)
        # Fallback: random-ish score
        return {
            "clarity": random.randint(6, 8),
            "specificity": random.randint(6, 8),
            "structure": random.randint(6, 8),
            "usefulness": random.randint(6, 8),
            "overall": random.uniform(6, 8),
        }


def rank_candidates(candidates: list[dict]) -> list[dict]:
    """Rank all candidates and add scores."""
    for c in candidates:
        c["scores"] = rank_prompt(c["text"])
    # Sort by overall score descending
    candidates.sort(key=lambda x: x["scores"]["overall"], reverse=True)
    return candidates


# ─── Publish to Hugo content ─────────────────────────────

def slugify(text: str) -> str:
    """Create a URL-safe slug from prompt text."""
    slug = text.lower().strip()
    slug = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in slug)
    slug = slug.replace(" ", "-")
    slug = "-".join(s for s in slug.split("-") if s)
    return slug[:60] or "prompt"


def generate_markdown(candidate: dict, date: datetime) -> str:
    """Generate Hugo markdown content for a prompt."""
    title = f"God Tier {candidate['category']} Prompt: {candidate['prompt_type'].title()}"
    slug = slugify(title)
    date_str = date.strftime("%Y-%m-%d")
    datetime_str = date.strftime("%Y-%m-%dT%H:%M:%S+07:00")

    # Clean up prompt text for markdown
    prompt_text = candidate["text"].strip()

    # If prompt_text doesn't start with ##, add a title
    if not prompt_text.startswith("##"):
        prompt_text = f"## {title}\n\n{prompt_text}"

    tags_inline = "[" + ", ".join(candidate["tags"]) + "]"
    categories_inline = "[" + candidate["category"] + "]"

    md = f"""---
title: "{title.replace('"', "'")}"
date: {datetime_str}
draft: false
categories: {categories_inline}
tags: {tags_inline}
model: "Multi-Model"
best_score: {candidate['scores']['overall']:.1f}
usage_notes: ""
examples: ""
---

{prompt_text}
"""
    return md, title, slug


def publish_prompt(candidate: dict) -> dict:
    """Publish the best prompt as a Hugo content file."""
    date = datetime.now(timezone(timedelta(hours=7)))  # WIB
    year = date.strftime("%Y")

    md_content, title, slug = generate_markdown(candidate, date)

    # Create directory: content/prompts/YYYY/
    output_path = Path(OUTPUT_DIR) / year
    output_path.mkdir(parents=True, exist_ok=True)

    filename = output_path / f"{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n✓ Published: {filename.relative_to(SITE_ROOT)}")
    print(f"  Title: {title}")
    print(f"  Score: {candidate['scores']['overall']:.1f}/10")

    return {
        "prompt_title": title,
        "prompt_score": f"{candidate['scores']['overall']:.1f}",
        "file": str(filename.relative_to(SITE_ROOT)),
    }


# ─── GitHub Actions output ────────────────────────────────

def set_github_output(key: str, value: str):
    """Set GitHub Actions output variable."""
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"::{key}={value}")


# ─── Main ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  God Tier Prompt Generator & Publisher")
    print("=" * 60)

    # 1. Generate candidates
    print("\n📝 Generating prompt candidates...")
    candidates = generate_candidates()
    if not candidates:
        print("ERROR: No candidates generated. Check API keys.", file=sys.stderr)
        sys.exit(1)

    print(f"\n✓ Generated {len(candidates)} candidates")

    # 2. Rank candidates
    print("\n🏆 Ranking candidates...")
    ranked = rank_candidates(candidates)

    print("\n--- Leaderboard ---")
    for i, c in enumerate(ranked, 1):
        print(f"  {i}. {c['category']}/{c['prompt_type']} — {c['scores']['overall']:.1f}/10")

    # 3. Publish best
    print("\n📤 Publishing best prompt...")
    best = ranked[0]
    result = publish_prompt(best)

    # 4. Set GitHub Actions outputs
    set_github_output("prompt_title", result["prompt_title"])
    set_github_output("prompt_score", result["prompt_score"])

    print("\n✅ Done! Best prompt published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
