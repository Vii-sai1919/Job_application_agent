# Job Application Agent

A multi-agent AI system built with crewAI that automates the entire job application process — from researching a company to generating a tailored resume, cover letter, gap report, and recruiter outreach email.

Built as an AI internship project to demonstrate real-world multi-agent orchestration using crewAI, running entirely on your local machine with no data leaving your device.

---

## What It Does

Give it a company name, a role, and your resume PDF. A crew of 7 autonomous agents does the rest — sequentially, each passing context to the next.

| Agent | Task |
|---|---|
| Job Researcher | Finds the actual job posting and extracts all requirements and keywords |
| Company Analyst | Researches culture, tech stack, recent news, and talking points |
| Hire Pattern Analyst | Identifies background patterns from recently hired candidates |
| Resume Tailor | Rewrites your resume to match the JD naturally and pass ATS filters |
| Cover Letter Writer | Writes a personalised, company-specific cover letter |
| Gap Analyst | Scores your profile match and identifies gaps with concrete actions |
| Email Drafter | Drafts a cold outreach email to a recruiter under 100 words |

---

## Outputs

- Tailored resume optimised for ATS and the specific role
- Personalised cover letter referencing real company details
- Profile match score — current percentage and projected optimised percentage
- Gap report with ranked missing skills and one concrete action per gap
- Interview prep questions with talking points drawn from your own experience
- Recruiter outreach email ready to send

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | crewAI |
| LLM Backend | Ollama + llama3.2 (local, free) |
| Web Search | Serper API |
| Resume Parsing | PyMuPDF |
| Web UI | Streamlit |
| Language | Python 3.10+ |

---

## Project Structure

```
job-application-agent/
├── app.py
├── pyproject.toml
├── README.md
└── src/
    └── job_application_agent/
        ├── __init__.py
        ├── crew.py
        ├── main.py
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        └── tools/
            ├── __init__.py
            └── custom_tool.py
```

---

## Setup

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed on your machine
- A free Serper API key from [serper.dev](https://serper.dev)

### Install

```bash
git clone https://github.com/yourusername/job-application-agent.git
cd job-application-agent

python3 -m venv venv
source venv/bin/activate

pip install crewai crewai-tools pymupdf streamlit beautifulsoup4 requests python-dotenv langchain
```

### Configure

Create a `.env` file in the root folder with the following:

```
SERPER_API_KEY=your_serper_key_here
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL_NAME=llama3.2
```

### Pull the model

```bash
ollama pull llama3.2
```

### Run

```bash
# Web UI
streamlit run app.py

# Command line
python3 -m src.job_application_agent.main
```

---

## How It Works

Agents run sequentially. Each agent's output is passed as context to the next, so by the time the final agents run they have the complete research, tailored resume, and cover letter available to them.

```
Job Researcher → Company Analyst → Hire Pattern Analyst
                                          ↓
                  Email Drafter ← Gap Analyst ← Cover Letter Writer ← Resume Tailor
```

---

## Notes

- Runs 100% locally — no data leaves your machine
- No OpenAI or cloud LLM costs — uses Ollama with llama3.2
- Each full run takes 5 to 15 minutes depending on your hardware
- Tested on MacBook Air M1 8GB