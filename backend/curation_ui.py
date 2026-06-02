#!/usr/bin/env python3
"""
China AI Health — Curation UI (Streamlit)
==========================================
You open http://localhost:5000, see today's ~30-40 AI-translated articles,
check the ones you want to publish, and confirm.
Saves selected_YYYY-MM-DD.json for publish.py to use.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg

CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")

st.set_page_config(
    page_title="China AI Health — Daily Curation",
    page_icon="📋",
    layout="wide",
)

PROCESSED_FILE = os.path.join(cfg.PROCESSED_DIR, f"processed_{TODAY}.json")
SELECTED_FILE = os.path.join(cfg.SELECTED_DIR, f"selected_{TODAY}.json")

TAG_COLORS = {
    "AI-diagnosis": ("AI Diagnosis", "#0071e3"),
    "AI-drug-discovery": ("AI Drug Discovery", "#5856d6"),
    "AI-medical-device": ("AI Medical Device", "#ff6b35"),
    "Regulation": ("Regulation", "#34c759"),
    "Funding": ("Funding", "#af52de"),
    "Exhibition": ("Exhibition", "#ff9500"),
    "AI-genomics": ("AI Genomics", "#30d158"),
    "AI-robotics": ("AI Robotics", "#ff2d55"),
    "Digital-health": ("Digital Health", "#5e5ce6"),
    "Policy": ("Policy", "#64d2ff"),
}


def tag_display(tag, score):
    label, color = TAG_COLORS.get(tag, (tag, "#888"))
    return f'<span style="background:{color}22;color:{color};padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;margin-right:4px">{label}</span>'


def score_color(qs):
    if qs >= 80:
        return "#30d158"
    elif qs >= 60:
        return "#ff9500"
    else:
        return "#ff3b30"


def main():
    st.title("China AI Health — Daily Curation")
    st.caption(f"📅 {TODAY}  |  source: processed_{TODAY}.json")

    # Load data
    if not os.path.exists(PROCESSED_FILE):
        st.error(f"❌ No processed file found: {PROCESSED_FILE}")
        st.error("Run: python crawl.py && python translate.py  first.")
        return

    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    st.success(f"✅ Loaded {len(articles)} AI-translated candidates")

    # Target count
    TARGET = st.slider("How many articles to select:", 5, 20, 10)

    # Sidebar stats
    st.sidebar.header("📊 Stats")
    st.sidebar.metric("Total Candidates", len(articles))

    avg_score = sum(a.get("quality_score", 0) for a in articles) / max(len(articles), 1)
    st.sidebar.metric("Avg Quality Score", f"{avg_score:.1f}")

    tag_counts = {}
    for a in articles:
        for t in (a.get("tags") or []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    st.sidebar.markdown("**By Tag:**")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        label, color = TAG_COLORS.get(tag, (tag, "#888"))
        st.sidebar.markdown(f"<span style='color:{color}'>●</span> {label}: **{count}**")

    st.divider()

    # ── Article List ────────────────────────────────
    selected_titles = []
    expanded_idx = None

    for i, art in enumerate(articles):
        qs = art.get("quality_score", 0)
        tag_list = art.get("tags") or []

        cols = st.columns([1, 12, 3])

        # Checkbox
        checked = cols[0].checkbox("", key=f"art_{i}", help=f"QS: {qs}")

        # Title + meta
        with cols[1]:
            qs_color = score_color(qs)
            tags_html = " ".join(tag_display(t, qs) for t in tag_list)
            pub = art.get("published", "")[:16] if art.get("published") else ""

            st.markdown(
                f"<span style='background:{qs_color}22;color:{qs_color};padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;margin-right:8px'>QS {qs:.0f}</span>"
                f"{tags_html}",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<b style='font-size:16px;line-height:1.3'>{art.get('en_title', art.get('title', ''))}</b>",
                unsafe_allow_html=True,
            )
            src = art.get("source", "")
            st.caption(f"  {src}  ·  {pub}  ·  [{art.get('source_authority', '?')}/10 authority]")

        # Expand button
        with cols[2]:
            if st.button("📖 Preview", key=f"expand_{i}"):
                expanded_idx = i if expanded_idx != i else None

        # Expanded content
        if expanded_idx == i:
            with st.container():
                st.markdown("**English Summary:**")
                st.info(art.get("en_summary", "N/A"))
                kp = art.get("en_key_points") or []
                if kp:
                    st.markdown("**Key Points:**")
                    for pt in kp:
                        st.markdown(f"- {pt}")

                # Original Chinese
                with st.expander("📄 Original Chinese Title + Summary"):
                    st.markdown(f"**Title:** {art.get('title', 'N/A')}")
                    st.markdown(f"**Summary:** {art.get('summary', 'N/A')[:300]}...")

                st.markdown(f"[🔗 Source URL]({art.get('url', '#')})")

        st.divider()

        if checked:
            selected_titles.append(art.get("en_title") or art.get("title"))

    # ── Confirm Section ──────────────────────────────
    st.divider()
    st.subheader(f"✏️ Selection ({len(selected_titles)} / {TARGET} selected)")

    if len(selected_titles) > 0:
        st.write(f"Selected: **{len(selected_titles)}** articles")
        if len(selected_titles) < TARGET:
            st.warning(f"⚠️  Select at least {TARGET} articles to confirm.")

    if st.button("✅ Confirm & Save Selection", type="primary", disabled=len(selected_titles) == 0):
        # Save selected articles
        selected_arts = [a for i, a in enumerate(articles) if st.session_state.get(f"art_{i}")]
        os.makedirs(cfg.SELECTED_DIR, exist_ok=True)
        with open(SELECTED_FILE, "w", encoding="utf-8") as f:
            json.dump(selected_arts, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Saved {len(selected_arts)} selected articles → {SELECTED_FILE}")
        st.balloons()

        # Show what was selected
        st.markdown("**Selected articles:**")
        for a in selected_arts:
            st.markdown(f"- {a.get('en_title', a.get('title', ''))}")

    # ── Footer ─────────────────────────────────────
    st.divider()
    st.caption(
        "Next: run `python publish.py` to generate index.html + GitHub Pages publish. "
        "Or run `python publish.py --dry-run` to preview first."
    )


if __name__ == "__main__":
    main()