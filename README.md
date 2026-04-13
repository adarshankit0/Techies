# 🚀 Techies – Developers Collaboration Platform

Techies is a full-stack web application designed to help developers connect, collaborate, and learn together. The platform provides an interactive environment where users can create study rooms, share posts, send friend requests, and stay updated through a notification system.

This project aims to modernize collaborative learning by offering a centralized space for discussions, knowledge sharing, and networking among developers.

---

## 🌟 Key Features

### 👥 User Authentication

* Secure login and registration system
* Email-based authentication
* User profile with avatar and bio

### 📚 Study Rooms

* Create and join topic-based study rooms
* Add room descriptions and categories
* Real-time discussions inside rooms

### 💬 Messaging System

* Users can send messages inside rooms
* Tracks recent activities
* Displays participants in each room

### 📝 Posts & Feed

* Create posts with text and images
* View posts from all users in a feed
* Media upload support

### 🤝 Friend System

* Send and receive friend requests
* Accept or reject requests
* Maintain a personal friends list

### 🔔 Notifications System

* Get notified for friend requests
* Dynamic notification counter (badge)
* Central notification page

### 📩 Contact System

* Users can submit queries via contact form
* Data stored in database and visible in admin panel

---

## 🛠️ Technologies Used

### 🎨 Frontend

* HTML5
* CSS3
* JavaScript

### ⚙️ Backend

* Python
* Django Framework

### 🗄️ Database

* SQLite (default Django database)

### 📦 Additional Tools

* Django ORM
* Bootstrap (for UI styling)
* Git & GitHub (version control)

---

## 📁 Project Structure

```
Techies/
│
├── base/               # Main application logic
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # Uploaded files (images)
├── studygate/          # Project settings
├── manage.py           # Entry point of Django project
└── db.sqlite3          # Database file
```

---

## ▶️ How to Run the Project

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd Techies
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Start Server

```bash
python manage.py runserver
```

### 7️⃣ Open in Browser

```
http://127.0.0.1:8000/
```

---

## 🔐 Admin Panel Access

To access admin panel:

```bash
python manage.py createsuperuser
```

Then open:

```
http://127.0.0.1:8000/admin/
```

---

## 🎯 Future Enhancements

* Real-time chat using WebSockets
* Like & comment system on posts
* Advanced notification system
* Profile customization
* Mobile app version

---

## 📌 Conclusion

Techies provides a collaborative platform where developers can interact, learn, and grow together. It integrates multiple features like study rooms, posts, friendships, and notifications into a single unified system, making it a powerful tool for developer communities.

---

## 👨‍💻 Author

Adarsh Priyadarshi

---

⭐ If you like this project, feel free to star the repository and contribute!
