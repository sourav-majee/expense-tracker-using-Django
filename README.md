# 💰 Ledger — Expense Tracker

Ledger is a personal expense tracking web application built with **Django** and **vanilla JavaScript**.
It allows users to manage daily expenses, visualize spending patterns, and export data easily.

---

## 🌟 Features

* 🔐 **User Authentication** — Register, login, and logout functionality
* 🎭 **Guest Mode** — Use the application without creating an account (data stored temporarily in the browser)
* 📊 **Dashboard Analytics** — View monthly totals, top spending category, and a 30-day spending chart
* 💳 **Expense Management** — Add, edit, and delete expenses
* 🗂️ **Default Categories** — Food, Transport, Shopping, Health, Bills, Entertainment, Other
* 🔍 **Search & Filter** — Filter expenses by keyword, category, or month
* ⬇️ **CSV Export** — Download expense data as a spreadsheet
* 🌙 **Dark / Light Theme** — Toggle theme with saved preference
* 👤 **User-specific Data** — Each user can access only their own expenses
* 🛡️ **Django Admin Panel** — Manage users, expenses, and categories via `/admin/`

---

## 🛠 Tech Stack

**Backend**

* Django
* Django REST Framework

**Frontend**

* HTML
* CSS
* Vanilla JavaScript

**Database**

* PostgreSQL (local or production)

**Deployment**

* Render

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/sourav-majee/expense-tracker-using-Django.git
cd expense-tracker-using-Django
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

Windows

```bash
venv\Scripts\activate
```

Mac / Linux

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create PostgreSQL database

```sql
CREATE DATABASE expense_tracker;
```

---

### 5. Create a `.env` file in the project root

```env
SECRET_KEY=django-insecure-change-me
DEBUG=True
DB_NAME=expense_tracker
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

---

### 6. Apply database migrations

```bash
python manage.py migrate
```

---

### 7. Create an admin user

```bash
python manage.py createsuperuser
```

---

### 8. Run the development server

```bash
python manage.py runserver 8001
```

Open your browser and visit:

```
http://localhost:8001
```


## 👤 Author

**Sourav Majee**

GitHub
https://github.com/sourav-majee

## 🚀 Live Demo

https://expense-tracker-using-django-piwc.onrender.com
