import os
import re
from pathlib import Path
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from google import genai

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="European Robotic Surgery Insights",
    page_icon="🤖",
    layout="wide"
)

# Change this to the model that appeared in check_models.py
GEMINI_MODEL = "gemini-3.5-flash-lite"

# =========================
# LOAD API KEY
# =========================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================
# LOAD TRANSCRIPTS
# =========================
TRANSCRIPT_FOLDER = Path("transcripts")

def load_transcripts():
    data = {}

    if TRANSCRIPT_FOLDER.exists():
        for file in sorted(TRANSCRIPT_FOLDER.glob("*.txt")):
            data[file.stem] = file.read_text(encoding="utf-8")

    return data

transcripts = load_transcripts()

# =========================
# EXTRACT TIMESTAMP QUOTES
# =========================
timestamp_pattern = r"^\d{2}:\d{2}$"

def extract_quotes(text):

    quotes = []
    current_time = "Unknown"

    for line in text.splitlines():

        line = line.strip()

        if re.match(timestamp_pattern, line):
            current_time = line

        elif ":" in line and len(line) > 15:
            quotes.append((current_time, line))

    return quotes

# =========================
# GEMINI FUNCTION
# =========================
def ask_gemini(prompt):

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Gemini Error:\n\n{e}"

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📂 Loaded Transcripts")

if transcripts:
    for name in transcripts:
        st.sidebar.success(name)
else:
    st.sidebar.error("No transcripts found.")

# =========================
# HEADER
# =========================
st.title("🤖 European Robotic Surgery Insights")
st.caption("Hasamex AI Engineer Technical Case")

c1, c2, c3 = st.columns(3)

c1.metric("Experts", len(transcripts))
c2.metric("Markets", "France • Germany • UK")
c3.metric("Interview Questions", "6")

st.divider()

# =========================
# TABS
# =========================
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

Instructions:
- Answer separately for France, Germany and the UK.
- Use ONLY transcript evidence.
- Include an exact supporting quote.
- Include the timestamp.
- Do not invent information.

France:
{transcripts.get("Transcript_1_France", "")}

Germany:
{transcripts.get("Transcript_2_Germany", "")}

UK:
{transcripts.get("Transcript_3_UK", "")}
"""

        with st.spinner("Generating answer..."):
            st.markdown(ask_gemini(prompt))

# =====================================================
# TAB 2
# =====================================================
with tab2:

    st.header("Exact Quotes with Timestamps")

    for name, text in transcripts.items():

        with st.expander(name):

            quotes = extract_quotes(text)

            for t, q in quotes:
                st.markdown(f"**{t}**")
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

- Bullet points

## Disagreements

- Bullet points

Mention which expert supports each point.

Use only transcript evidence.

France:
{transcripts.get("Transcript_1_France", "")}

Germany:
{transcripts.get("Transcript_2_Germany", "")}

UK:
{transcripts.get("Transcript_3_UK", "")}
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
Answer the user's question using ONLY these transcripts.

Question:
{question}

Requirements:
- Mention which expert said it.
- Include exact quotes.
- Include timestamps.
- Do not invent information.

France:
{transcripts.get("Transcript_1_France", "")}

Germany:
{transcripts.get("Transcript_2_Germany", "")}

UK:
{transcripts.get("Transcript_3_UK", "")}
"""

        with st.spinner("Searching transcripts..."):
            st.markdown(ask_gemini(prompt))

# =========================
# FOOTER
# =========================
st.divider()
st.caption("Built with Streamlit + Gemini for the Hasamex AI Engineer Case Study.")