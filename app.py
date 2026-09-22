import os
import re
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="European Robotic Surgery Insights",
    page_icon="🤖",
    layout="wide"
)

# Hide sidebar completely
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="collapsedControl"] {display:none;}
.block-container {padding-top:2rem; max-width:1200px;}
.stButton>button {width:100%; border-radius:10px; height:45px;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD API KEY
# -------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found.")
    st.stop()

genai.configure(api_key=API_KEY)

# Render-friendly model
GEMINI_MODEL = "gemini-2.5-flash-lite"

# -------------------------
# LOAD TRANSCRIPTS
# -------------------------
TRANSCRIPT_FOLDER = Path("transcripts")

def load_transcripts():
    data = {}
    if TRANSCRIPT_FOLDER.exists():
        for file in sorted(TRANSCRIPT_FOLDER.glob("*.txt")):
            data[file.stem] = file.read_text(encoding="utf-8")
    return data

transcripts = load_transcripts()

# -------------------------
# QUOTE EXTRACTION
# -------------------------
timestamp_pattern = r"^\d{2}:\d{2}$"

def extract_quotes(text):
    quotes = []
    current = "Unknown"

    for line in text.splitlines():
        line = line.strip()

        if re.match(timestamp_pattern, line):
            current = line
        elif ":" in line and len(line) > 15:
            quotes.append((current, line))

    return quotes

# -------------------------
# GEMINI FUNCTION
# -------------------------
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        return "No response."

    except Exception as e:
        return f"❌ Gemini Error: {e}"

# -------------------------
# HEADER
# -------------------------
st.title("🤖 European Robotic Surgery Insights")
st.caption("Hasamex AI Engineer Technical Case")

c1, c2, c3 = st.columns(3)

c1.metric("Experts", len(transcripts))
c2.metric("Markets", "France • Germany • UK")
c3.metric("Interview Questions", "6")

st.divider()

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Interview Guide",
    "Quotes",
    "Themes",
    "Ask Anything"
])

# =====================================================
# TAB 1
# =====================================================
with tab1:

    st.header("Interview Guide Answers")

    questions = [
        "1. Current adoption of robotic surgery",
        "2. Main barriers to adoption",
        "3. Importance of hospital budgets and ROI",
        "4. Importance of surgeon training and clinical outcomes",
        "5. Expected adoption trend over the next 3–5 years",
        "6. Typical hospital purchasing timeline"
    ]

    selected = st.selectbox("Choose a question", questions)

    if st.button("Generate Answer"):

        prompt = f"""
You are analysing expert interview transcripts.

Question:
{selected}

Answer separately for France, Germany and the UK.

Requirements:
- Use ONLY transcript evidence.
- Include an exact quote.
- Include its timestamp.
- Keep answers concise.

France:
{transcripts.get("Transcript_1_France","")}

Germany:
{transcripts.get("Transcript_2_Germany","")}

UK:
{transcripts.get("Transcript_3_UK","")}
"""

        with st.spinner("Generating answer..."):
            st.markdown(ask_gemini(prompt))

# =====================================================
# TAB 2
# =====================================================
with tab2:

    st.header("Exact Quotes with Timestamps")

    for name, text in transcripts.items():

        with st.expander(name.replace("_"," ")):

            for t, q in extract_quotes(text):
                st.markdown(f"**⏱ {t}**")
                st.write(q)

# =====================================================
# TAB 3
# =====================================================
with tab3:

    st.header("Common Themes & Disagreements")

    if st.button("Compare Experts"):

        prompt = f"""
Compare all three experts.

Return:

## Common Themes

- bullet points

## Disagreements

- bullet points

Mention which expert supports each point.

Use ONLY transcript evidence.

France:
{transcripts.get("Transcript_1_France","")}

Germany:
{transcripts.get("Transcript_2_Germany","")}

UK:
{transcripts.get("Transcript_3_UK","")}
"""

        with st.spinner("Comparing experts..."):
            st.markdown(ask_gemini(prompt))

# =====================================================
# TAB 4
# =====================================================
with tab4:

    st.header("Ask Questions Across All Transcripts")

    question = st.text_input(
        "Example: What are the biggest barriers to adoption?"
    )

    if st.button("Ask") and question:

        prompt = f"""
Answer ONLY from these transcripts.

Question:
{question}

Requirements:
- Mention which expert said it.
- Include exact quotes.
- Include timestamps.
- Do not invent information.

France:
{transcripts.get("Transcript_1_France","")}

Germany:
{transcripts.get("Transcript_2_Germany","")}

UK:
{transcripts.get("Transcript_3_UK","")}
"""

        with st.spinner("Searching transcripts..."):
            st.markdown(ask_gemini(prompt))

# -------------------------
# FOOTER
# -------------------------
st.divider()
st.caption("Built with Streamlit + Google Gemini for the Hasamex AI Engineer Technical Case.")