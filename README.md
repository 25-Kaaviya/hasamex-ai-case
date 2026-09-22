# 🤖 European Robotic Surgery Insights

**Hasamex AI Engineer Technical Case Submission**

A Streamlit application that analyzes expert interview transcripts using **Google Gemini AI** to generate evidence-based insights, extract timestamped quotes, compare expert opinions, and answer questions across multiple transcripts.

## Features

* **Interview Guide Answers** – Generates structured answers for predefined interview questions using transcript evidence.
* **Exact Quotes & Timestamps** – Extracts supporting quotes with timestamps from each transcript.
* **Common Themes & Disagreements** – Compares all expert interviews to identify shared insights and differing opinions.
* **Ask Anything** – Allows users to ask natural language questions across all transcripts.
* **Clean Dashboard UI** – Professional tab-based Streamlit interface optimized for demonstration.

## Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **python-dotenv**

  
## 🚀 Live Demo
Live Application: https://hasamex-ai-case.onrender.com/

## Project Structure

```text
hasamex-ai-case/
│── app.py
│── requirements.txt
│── .env                 # Local only (not committed)
│── transcripts/
│   ├── Transcript_1_France.txt
│   ├── Transcript_2_Germany.txt
│   └── Transcript_3_UK.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/25-Kaaviya/hasamex-ai-case.git
cd hasamex-ai-case
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configure API Key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

## Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## Application Workflow

1. Load the three expert interview transcripts.
2. Select an interview guide question.
3. Generate AI-powered answers using transcript evidence.
4. View exact supporting quotes with timestamps.
5. Compare common themes and disagreements.
6. Ask custom questions across all transcripts.

## Engineering Approach

* Transcript-based evidence retrieval.
* AI-powered summarization using Google Gemini.
* Timestamp preservation for traceability.
* Structured prompts for consistent outputs.
* Modular Streamlit interface for usability.

## Future Improvements

* FAISS-based Retrieval-Augmented Generation (RAG) for faster responses.
* Clickable timestamp navigation.
* Transcript chunking for improved retrieval accuracy.
* Export insights as PDF or Excel reports.

## Author

**Kaavya M**

GitHub: https://github.com/25-Kaaviya
