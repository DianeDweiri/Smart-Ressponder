# 🤖 Smart Responder System

An intelligent automated response system that answers user questions using fuzzy matching and routes unanswered queries to the appropriate department via email.

---

## 🚀 Features

- ✅ Automatic question answering using fuzzy matching (RapidFuzz)
- 📊 Confidence scoring for each response
- 📩 Email redirection for unanswered questions
- 🧠 Keyword-based department detection
- 📝 Logging system for tracking activity
- 📂 JSON storage for unanswered and redirected queries

---

## 🛠️ Technologies Used

- Python
- RapidFuzz
- SMTP (Email Automation)
- python-dotenv
- JSON

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/dianedweiri/smart-responder.git
cd smart-responder
2. Install dependencies
pip install rapidfuzz python-dotenv
3. Create .env file
EMAIL=your_email@gmail.com
PASSWORD=your_app_password

TECH_EMAIL=tech@company.com
BILLING_EMAIL=billing@company.com
SUPPORT_EMAIL=support@company.com

⚠️ If you're using Gmail, make sure to use an App Password instead of your normal password.

4. Add your knowledge base

Create a file called data.json:

[
  {
    "question": "How do I reset my password?",
    "answer": "Click on 'Forgot Password' on the login page."
  }
]
▶️ How to Run
python main.py

Then type your question in the terminal.

🧠 How It Works
User enters a question
System compares it with stored questions using fuzzy matching
If confidence ≥ threshold → returns answer
If not:
Detects department using keywords
Sends an email notification
Logs the question for later improvement
📂 Output Files
app.log → system logs
unanswered.json → unanswered questions
redirects.json → redirected queries
🔥 Future Improvements
Replace keyword detection with ML/NLP model
Auto-learn from unanswered questions
Build API using FastAPI
Add web interface/dashboard
Support Arabic + English inputs
👨‍💻 Author

Diane Dweiri
GitHub: https://github.com/dianedweiri
