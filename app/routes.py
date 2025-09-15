import os, json
from flask import Blueprint, render_template, request, redirect, url_for, session
from .evaluator import evaluate_answer, save_logs

bp = Blueprint("core", __name__)

def load_questions():
    with open(os.path.join("data","excel_questions.json"), "r", encoding="utf-8") as f:
        return json.load(f)

@bp.route("/", methods=["GET","POST"])
def intro():
    session.clear()
    session["answers"] = {}
    session["evaluations"] = {}
    session["idx"] = 0
    questions = load_questions()
    session["total"] = len(questions)
    if request.method == "POST":
        return redirect(url_for("core.question"))
    return render_template("intro.html", total=len(questions))

@bp.route("/question", methods=["GET","POST"])
def question():
    questions = load_questions()
    idx = session.get("idx", 0)
    total = len(questions)
    if idx >= total:
        return redirect(url_for("core.summary"))
    q = questions[idx]

    if request.method == "POST":
        ans = request.form.get("answer","").strip()
        session["answers"][q["id"]] = ans
        ev = evaluate_answer(q, ans)
        session["evaluations"][q["id"]] = ev
        session["idx"] = idx + 1
        return redirect(url_for("core.question"))

    progress = int((idx/total)*100) if total else 0
    return render_template("question.html", q=q, qnum=idx+1, total=total, progress=progress)

@bp.route("/summary", methods=["GET"])
def summary():
    questions = load_questions()
    answers = session.get("answers", {})
    evaluations = session.get("evaluations", {})
    scored = [evaluations.get(q["id"], {"score":0}) for q in questions]
    scores = [float(s.get("score",0)) for s in scored]
    avg = round(sum(scores)/len(scores), 1) if scores else 0.0

    if avg >= 4.0:
        band, alert = "Excellent", "success"
    elif avg >= 3.0:
        band, alert = "Competent", "info"
    else:
        band, alert = "Needs Improvement", "warning"

    transcript_lines = []
    feedback_lines = []
    for q in questions:
        ans = answers.get(q["id"], "")
        ev = evaluations.get(q["id"], {"score":0, "rationale":""})
        transcript_lines.append(f"Q: {q['question']}\nA: {ans}\nScore: {ev.get('score',0)}\n")
        feedback_lines.append(f"- {q['id']}: {ev.get('rationale','')}")

    transcript_text = "\n".join(transcript_lines)
    feedback_text = f"Overall: {avg}/5 ({band})\n" + "\n".join(feedback_lines)
    ts = save_logs(transcript_text, feedback_text)

    return render_template("summary.html",
        questions=questions, answers=answers, evaluations=evaluations,
        avg=avg, band=band, alert=alert, ts=ts)
