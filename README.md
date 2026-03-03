# 💰 Ledger — Django Expense Tracker

> Django 5 · Django REST Framework · PostgreSQL · Vanilla HTML/CSS/JS

---

## 📁 Project Structure

```
expense-tracker-django/
│
├── manage.py                        ← Django CLI entry point
│
├── expense_tracker/                 ← Django PROJECT (config)
│   ├── __init__.py
│   ├── settings.py                  ← All settings (DB, apps, CORS...)
│   ├── urls.py                      ← Root URL dispatcher
│   └── wsgi.py
│
├── expenses/                        ← Django APP (all logic)
│   ├── models.py                    ← ORM: Category, Expense
│   ├── serializers.py               ← DRF serializers (JSON ↔ Model)
│   ├── views.py                     ← API views + stats logic
│   ├── urls.py                      ← App-level URL patterns
│   ├── admin.py                     ← Django admin config
│   └── migrations/
│       ├── 0001_initial.py          ← Creates tables
│       └── 0002_seed_categories.py  ← Seeds 7 default categories
│
├── frontend/
│   └── index.html                   ← Full SPA (no build step)
│
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Run

### 1. Create the PostgreSQL database

```sql
-- In psql or pgAdmin
CREATE DATABASE expense_tracker;
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env — set your DB_PASSWORD (and SECRET_KEY for production)
```

### 4. Run migrations (creates tables + seeds categories)

```bash
python manage.py migrate
```

### 5. Create a superuser (for the Admin panel)

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

| URL                          | What it does                    |
|------------------------------|---------------------------------|
| http://localhost:8000/       | Frontend SPA                    |
| http://localhost:8000/admin/ | Django Admin (free dashboard)   |
| http://localhost:8000/api/   | REST API                        |

---

## 🔌 REST API Reference

| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| GET    | `/api/categories/`     | List all categories                |
| GET    | `/api/expenses/`       | List expenses (filterable)         |
| POST   | `/api/expenses/`       | Create new expense                 |
| GET    | `/api/expenses/<id>/`  | Get single expense                 |
| PUT    | `/api/expenses/<id>/`  | Full update                        |
| PATCH  | `/api/expenses/<id>/`  | Partial update                     |
| DELETE | `/api/expenses/<id>/`  | Delete expense                     |
| GET    | `/api/stats/`          | Dashboard stats + chart data       |

### Query params for `GET /api/expenses/`
```
?search=coffee         keyword in title or note
?category=2            filter by category ID
?month=2024-03         filter by YYYY-MM
```

### Query params for `GET /api/stats/`
```
?month=2024-03         defaults to current month
```

---

## 🗄️ Models

```python
class Category(models.Model):
    name  = CharField(max_length=100, unique=True)
    color = CharField(max_length=20)   # hex color, e.g. "#f59e0b"
    icon  = CharField(max_length=50)   # emoji, e.g. "🍔"

class Expense(models.Model):
    title      = CharField(max_length=200)
    amount     = DecimalField(max_digits=10, decimal_places=2)
    category   = ForeignKey(Category, on_delete=SET_NULL, null=True)
    date       = DateField()
    note       = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

---

## 🔑 Key Django Concepts Used

| Concept | Where |
|---|---|
| `models.Model` | `expenses/models.py` — defines DB tables |
| `ModelSerializer` | `expenses/serializers.py` — JSON conversion |
| `ListCreateAPIView` | `expenses/views.py` — GET list + POST |
| `RetrieveUpdateDestroyAPIView` | `expenses/views.py` — GET/PUT/DELETE single |
| `@api_view` | `expenses/views.py` — custom stats endpoint |
| `migrations` | `expenses/migrations/` — versioned DB changes |
| `admin.site.register` | `expenses/admin.py` — free admin panel |
| `CORS` | `settings.py` — allow frontend requests |

---

## 🚀 Next Steps to Level Up

```bash
# Add JWT authentication
pip install djangorestframework-simplejwt

# Add filtering library
pip install django-filter

# Export CSV
# Add a view that returns HttpResponse with content_type='text/csv'

# Dockerize
# Add Dockerfile + docker-compose.yml with postgres service
```
