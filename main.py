import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rapidfuzz import fuzz
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

DEPARTMENTS = {
    "technical": {
        "name": "Technical Support",
        "email": os.getenv("TECH_EMAIL"),
        "keywords": [
            "error", "issue", "not working", "slow", "crash",
            "bug", "failure", "glitch", "problem", "broken"
        ]
    },
    "billing": {
        "name": "Billing Department",
        "email": os.getenv("BILLING_EMAIL"),
        "keywords": [
            "invoice", "payment", "subscription", "price", "fees",
            "charge", "refund", "billing", "cost", "plan"
        ]
    },
    "general": {
        "name": "General Support",
        "email": os.getenv("SUPPORT_EMAIL"),
        "keywords": [
            "help", "question", "information", "inquiry", "support"
        ]
    }
}

THRESHOLD = 65

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

with open("data.json", "r", encoding="utf-8") as f:
    kb = json.load(f)


def get_answer(user_question):
    best_score = 0
    best_answer = None

    for item in kb:
        score = fuzz.ratio(user_question, item["question"])
        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score >= THRESHOLD:
        return {"status": "found", "answer": best_answer, "score": best_score}
    else:
        return {"status": "not_found", "answer": None, "score": best_score}


def detect_department(user_question):
    user_question = user_question.lower()

    for dept_key, dept_info in DEPARTMENTS.items():
        for keyword in dept_info["keywords"]:
            if keyword in user_question:
                return dept_key

    return "general"  # ✅ FIXED


def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        logging.info(f"Mail sent to {to_email} | Subject: {subject}")
        print("📧 Email sent successfully")

    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        print(f"❌ Email send failed: {e}")


def save_json(filename, entry):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def manual_redirect(user_question, score):
    dept_key = detect_department(user_question)

    # ✅ SAFE FALLBACK (no crash ever)
    dept = DEPARTMENTS.get(dept_key, DEPARTMENTS["general"])

    print(f"📌 Redirecting to {dept['name']}")

    subject = "A new question needs review"
    body = f"""
Hello,

A question was received from a user that the system could not automatically answer.

📝 Question: {user_question}
📊 Match Score: {score:.1f}%
🕐 Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Please follow up with the user.

Thank you,
Smart Responder System
"""

    send_email(dept["email"], subject, body)

    save_json("redirects.json", {
        "question": user_question,
        "score": score,
        "department": dept_key,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    logging.info(f"Redirected to {dept_key} | Question: {user_question}")


def auto_responder(user_question):
    result = get_answer(user_question)

    if result["status"] == "found":
        print(f"\n✅ Automatic Answer (Confidence: {result['score']:.1f}%):")
        print(f"👉 {result['answer']}\n")
        logging.info(f"Answered automatically | Score: {result['score']:.1f}")

    else:
        print(f"\n❓ I couldn't understand your question (Confidence: {result['score']:.1f}%)")

        manual_redirect(user_question, result["score"])

        save_json("unanswered.json", {
            "question": user_question,
            "score": result["score"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


print("🤖 Smart Responder System - Type a question or 'exit' to leave")
print("=" * 50)

while True:
    user_input = input("\nYour question: ").strip()

    if user_input.lower() in ["exit", "done", "quit", "bye"]:
        print("👋 Bye!")
        logging.info("System stopped by user")
        break

    if not user_input:
        print("⚠️ Please type a question!")
        continue

    auto_responder(user_input)