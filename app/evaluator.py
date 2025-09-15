import os, json, datetime, re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is missing. Set it in .env or environment.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=API_KEY)

EVAL_PROMPT = """
You are an expert Excel interviewer. Evaluate the candidate’s answer.
Always return STRICT JSON only. No text outside JSON.

Question: {question}
Answer: {answer}

Expected Answer Description:
{expected_answer_description}

Evaluation Criteria:
{evaluation_criteria}

Return JSON with this schema ONLY:
{{
  "score": number (0-5),
  "rationale": "string"
}}
"""

def _extract_json(raw: str) -> dict:
    raw = (raw or "").strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    m = re.search(r"\{.*\}", raw, re.S)
    if m:
        return json.loads(m.group(0))
    raise ValueError("Model did not return valid JSON.")

def evaluate_answer(q: dict, answer: str) -> dict:
    if not answer or not answer.strip():
        return {"score": 0.0, "rationale": "No answer provided."}
    prompt = EVAL_PROMPT.format(
        question=q.get("question",""),
        answer=answer,
        expected_answer_description=q.get("expected_answer_description",""),
        evaluation_criteria=q.get("evaluation_criteria","")
    )
    try:
        resp = llm.invoke(prompt)
        data = _extract_json(resp.content)
        score = data.get("score", 0)
        try:
            score = float(score)
        except Exception:
            score = 0.0
        return {"score": round(score,1), "rationale": data.get("rationale","")}
    except Exception as e:
        return {"score": 0.0, "rationale": f"⚠️ Evaluation failed: {str(e)}"}

def save_logs(transcript_text: str, feedback_text: str) -> str:
    os.makedirs("logs/transcripts", exist_ok=True)
    os.makedirs("logs/reports", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"logs/transcripts/{ts}_transcript.txt","w",encoding="utf-8") as f:
        f.write(transcript_text)
    with open(f"logs/reports/{ts}_feedback.txt","w",encoding="utf-8") as f:
        f.write(feedback_text)
    return ts
