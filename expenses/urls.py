from django.urls import path
from expenses import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────
    path("auth/register/", views.register_view, name="auth-register"),
    path("auth/login/",    views.login_view,    name="auth-login"),
    path("auth/logout/",   views.logout_view,   name="auth-logout"),
    path("auth/me/",       views.me_view,        name="auth-me"),

    # ── Categories ────────────────────────────────
    path("categories/",    views.CategoryListView.as_view(), name="category-list"),

    # ── Expenses ──────────────────────────────────
    path("expenses/",          views.ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/export/",   views.export_csv,                      name="expense-export"),
    path("expenses/<int:pk>/", views.ExpenseDetailView.as_view(),     name="expense-detail"),

    # ── Stats ─────────────────────────────────────
    path("stats/",         views.stats_view, name="stats"),
]
