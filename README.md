🚀 Techies – Social + Coding Ecosystem
💻 CodeTechies by Techies – Learn • Code • Compete • Connect










🌐 About Techies

Techies is a full-stack Django-based platform that combines:

👉 Social Networking
👉 AI Interaction
👉 Competitive Coding System (CodeTechies)

It is designed as a complete ecosystem where users can:

Connect with people 🌍
Share knowledge 💬
Solve coding problems 💻
Compete on leaderboard 🏆
Earn certificates 🎓
💻 CodeTechies by Techies (Core Feature)

CodeTechies is the coding engine inside Techies that provides:

🚀 What it Includes:
🧠 Coding Problems System
⚡ Online Code Execution (Judge API)
🧪 Real Testcase-based Evaluation
🏆 Score System
📊 Leaderboard Ranking
🎓 Certificate Generation
📈 Submission Tracking

👉 This makes Techies not just social, but skill-driven & competitive

🧠 Core Features
🔹 1. Social Platform
Chat rooms & discussions
Friend system
Notifications
Profile management
Post sharing system
🔹 2. AI Integration
AI-powered interaction page
Smart query handling
🔹 3. CodeTechies (Coding Platform)
💻 Online Code Editor
Multi-language support:
Python 🐍
C++ ⚙️
C
Java ☕
JavaScript 🌐
⚡ Run vs Submit System
Action	Purpose
▶ Run	Execute code with custom input
🚀 Submit	Evaluate code using hidden testcases
🧪 Real Judge System

✔ Each problem has multiple testcases
✔ Code runs against all testcases
✔ Output is matched with expected results

👉 Supports different logic, different code styles
👉 Works like real platforms (LeetCode / Codeforces)

🏆 Scoring System
Based on number of testcases passed
Dynamic scoring system
Score = (Passed Testcases / Total Testcases) × Problem Points
📊 Submission Tracking

Each submission stores:

User code
Output
Score
Status (Attempted / Completed)
Timestamp
🥇 Leaderboard System
Auto-updated ranking
Based on total user score
Competitive environment
🎓 Certificate System
Certificate	Condition
Participation	Attempted but not fully correct
Completion	All testcases passed

👉 Certificates are automatically generated after submission

🛠️ Tech Stack
🔹 Backend
Django (Python)
SQLite (Development)
🔹 Frontend
HTML
CSS
JavaScript
🔹 External API
Judge0 API (Code Execution Engine)
📁 Project Structure
Techies/
│
├── base/                 # Social features
├── codetechies/          # Coding system (CodeTechies)
├── static/               # CSS, JS, Images
├── templates/            # HTML Templates
├── studygate/            # Main Django project
├── manage.py
├── requirements.txt
└── README.md
⚙️ Setup & Installation
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/Techies.git
cd Techies
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Admin User
python manage.py createsuperuser
6️⃣ Run Server
python manage.py runserver

👉 Open in browser:

http://127.0.0.1:8000/
🧪 Adding Coding Testcases (Important)
🔹 Fast Method (Django Shell)
python manage.py shell
from codetechies.models import Problem, TestCase

p = Problem.objects.get(title="Sum Two Numbers")

TestCase.objects.create(problem=p, input_data="10 20", expected_output="30")
TestCase.objects.create(problem=p, input_data="5 5", expected_output="10")
TestCase.objects.create(problem=p, input_data="1 2", expected_output="3")
⚠️ Important Notes
db.sqlite3 is excluded from GitHub
__pycache__ ignored via .gitignore
Secure API handling implemented
Judge system supports real-world coding logic
🚀 Future Enhancements
Monaco Editor (VS Code-like editor)
Code highlighting
Time & memory constraints
Contest system
Docker sandbox execution
AI-assisted coding hints
Badges & achievements system
👨‍💻 Author

Adarsh Priyadarshi

Full-stack developer (Django)
Passionate about building scalable platforms
Focused on real-world problem solving
⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork it
🚀 Contribute