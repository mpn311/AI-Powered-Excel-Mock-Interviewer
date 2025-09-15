# AI-Powered Excel Mock Interviewer

# Deployed Link: https://interview.apkzube.com/

## 🚀 Project Overview
The **AI-Powered Excel Mock Interviewer** is a web-based application that simulates Excel technical interviews, evaluates candidate responses, and generates professional feedback reports.  
It helps organizations **automate and standardize Excel skill assessments**, reducing interviewer workload and improving fairness.

---

## 🌟 Key Features
- **Structured Interview Flow** → Candidate introduction, multi-turn Q&A, closing summary.  
- **Intelligent Answer Evaluation** → Google Gemini LLM (`gemini-1.5-flash-latest`) with rubric-based scoring.  
- **Agentic Behavior** → Maintains context across questions, acts like a real interviewer.  
- **Constructive Feedback Report** → Scores, rationale, and overall proficiency rating.  
- **Automated Logging** → Saves transcripts & reports with timestamps in `/logs`.  
- **Professional UI** → Flask + Bootstrap 5 with progress bar, accordions, and score cards.  

---

## 🏗️ Technical Architecture
**Flow:**
1. Candidate enters profile (name, experience).  
2. Questions loaded dynamically from `data/excel_questions.json`.  
3. Candidate answers → evaluated by Gemini LLM with expected answer + rubric.  
4. LLM outputs strict JSON `{score, rationale}`.  
5. Scores + rationale stored in session.  
6. Summary page → interactive accordion + score card.  
7. Transcript & feedback report auto-saved in `/logs`.  

---
# Technology Stack (Detailed Justification)

## 1) LLM — Google Gemini (gemini-1.5-flash-latest)
**Why this?**  
- **Cost–performance sweet spot:** Flash is optimized for speed and lower cost vs. “Pro” models, which keeps inference bills down while still handling instruction following, tool-use style prompts, and JSON outputs reliably.  
- **Great for evaluation workflows:** Consistent, fast responses are ideal for multi-turn interview flows (ask → evaluate → feedback) without user-visible lag.  
- **Structured output friendliness:** Works well with schema-guided prompts (e.g., “return valid JSON with fields: score, rubric, suggestions”), which simplifies downstream parsing.  

## 2) Framework — LangChain (Python)
**Why this?**  
- **Prompt templates & chaining:** Cleanly separates your system/role prompts from variable inputs; easy to build multi-step flows (ask → evaluate → summarize → store).  
- **State & memory:** Conversation memory (buffer/summary) avoids manual bookkeeping across turns.  
- **Structured output parsing:** `PydanticOutputParser` (or LC equivalent) to enforce JSON schemas, reducing brittle string parsing.  
- **Integrations:** Ready adapters for Gemini + easy swap if you A/B test other models later.  

## 3) Backend — Python Flask
**Why this?**  
- **Lightweight & familiar:** Minimal boilerplate; perfect for APIs that proxy LLM calls and handle uploads.  
- **Production-ready with simple stack:** Gunicorn + Nginx works well; easy to containerize.  

## 4) Frontend — Bootstrap 5
**Why this?**  
- **Fast to ship:** Grid, forms, buttons, modals out-of-the-box → you focus on core logic.  
- **Consistent & accessible:** Good default a11y and responsive behavior for dashboards and forms.  

## 5) Storage — JSON Question Bank (`excel_questions.json`)
**Why this?**  
- **Human-editable & versionable:** Non-tech stakeholders can update questions/rubrics via PRs.  
- **Zero ops:** No DB admin required for early stages.  

## 6) Logging — `/logs` folder for transcripts & feedback
**Why this?**  
- **Traceability:** Every interview run can be replayed (inputs, model outputs, score, rubric).  
- **Offline analysis:** Simple local JSONL is easy to mine for QA and model prompt improvements.  

## 7) Hosting — AWS EC2
**Why this?**  
- **Full control:** You own the box; easy to tune system dependencies (imagemagick, ffmpeg, etc. if later needed).  
- **Predictable pricing:** Good for steady loads; simpler than managed PaaS when you already know Linux basics.  

---

## 📂 Project Structure
```
excel-mock-interviewer/
│── app/
│   ├── templates/        # HTML templates (intro, question, summary, base)
│   ├── static/css/       # Stylesheets
│   ├── evaluator.py      # LLM evaluation & logging
│   └── routes.py         # Flask routes & logic
│── data/
│   └── excel_questions.json  # Question bank
│── logs/
│   ├── transcripts/      # Saved Q&A transcripts
│   └── reports/          # Saved feedback reports
│── run.py                
│── wsgi.py               
│── requirements.txt
│── README.md
```

---

## ❄️ Cold Start Strategy
Since no dataset exists initially:
1. **Bootstrapping** – Use curated `excel_questions.json` with expert-written expected answers & evaluation criteria.  
2. **Iterative Improvement** – Log transcripts & reports → review by Excel experts → refine prompts.  
3. **Dataset Building** – Collect anonymized transcripts for fine-tuning.  
4. **Future Optimization** – Fine-tune smaller LLMs  

---

## 📑 Deliverables
- ✅ Design Document & Approach Strategy (`.docx`)  
- ✅ Flask-based Proof-of-Concept app  
- ✅ Deployed version (AWS EC2)  
- ✅ Sample transcripts & feedback in `/logs`  

---

## 🚀 Future Enhancements
- Skill-wise analytics dashboard (charts).  
- Adaptive questioning (difficulty adjustment).  
 
---

👨‍💻 **Author:** [Milan Nagvadiya]  
