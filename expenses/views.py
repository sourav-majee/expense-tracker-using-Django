import csv
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Category, Expense
from .serializers import (
    CategorySerializer, ExpenseSerializer,
    RegisterSerializer, UserSerializer,
)


# ── Auth Views ────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """POST /api/auth/register/  — create a new account"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """POST /api/auth/login/  — { username, password }"""
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response({"error": "Invalid username or password."}, status=400)


@api_view(["POST"])
def logout_view(request):
    """POST /api/auth/logout/"""
    logout(request)
    return Response({"message": "Logged out successfully."})


@api_view(["GET"])
def me_view(request):
    """GET /api/auth/me/  — returns current user or 401"""
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    return Response({"error": "Not authenticated."}, status=401)


# ── Categories ────────────────────────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """GET /api/categories/"""
    queryset             = Category.objects.all()
    serializer_class     = CategorySerializer
    permission_classes   = [IsAuthenticated]


# ── Expenses ──────────────────────────────────────────────────────────────────

class ExpenseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/expenses/  — list current user's expenses
    POST /api/expenses/  — create expense for current user
    """
    serializer_class   = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Expense.objects.select_related("category").filter(user=self.request.user)

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(note__icontains=search))

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)

        month = self.request.query_params.get("month")
        if month:
            try:
                year, mon = map(int, month.split("-"))
                qs = qs.filter(date__year=year, date__month=mon)
            except ValueError:
                pass

        return qs

    def perform_create(self, serializer):
        # Automatically attach logged-in user
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PUT / PATCH / DELETE /api/expenses/<id>/"""
    serializer_class   = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own expenses
        return Expense.objects.select_related("category").filter(user=self.request.user)


# ── Stats ─────────────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stats_view(request):
    """GET /api/stats/?month=YYYY-MM"""
    month = request.query_params.get("month") or date.today().strftime("%Y-%m")

    try:
        year, mon = map(int, month.split("-"))
    except ValueError:
        return Response({"error": "Invalid month format. Use YYYY-MM."}, status=400)

    base_qs    = Expense.objects.filter(user=request.user)
    monthly_qs = base_qs.filter(date__year=year, date__month=mon)
    total      = monthly_qs.aggregate(total=Sum("amount"))["total"] or 0

    # By category
    by_category = []
    for cat in Category.objects.all():
        cat_total = monthly_qs.filter(category=cat).aggregate(t=Sum("amount"))["t"] or 0
        by_category.append({
            "id": cat.id, "name": cat.name,
            "color": cat.color, "icon": cat.icon,
            "total": float(cat_total),
        })
    by_category.sort(key=lambda x: x["total"], reverse=True)

    # Daily trend (last 30 days)
    thirty_days_ago = date.today() - timedelta(days=30)
    daily_qs = (
        base_qs.filter(date__gte=thirty_days_ago)
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )
    daily = [{"date": str(r["date"]), "total": float(r["total"])} for r in daily_qs]

    return Response({"total": float(total), "by_category": by_category, "daily": daily})


# ── CSV Export ────────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_csv(request):
    """
    GET /api/expenses/export/
    Optional filters: ?month=YYYY-MM  ?category=<id>
    Downloads a .csv file of matching expenses.
    """
    qs = Expense.objects.select_related("category").filter(user=request.user)

    month = request.query_params.get("month")
    if month:
        try:
            year, mon = map(int, month.split("-"))
            qs = qs.filter(date__year=year, date__month=mon)
        except ValueError:
            pass

    category = request.query_params.get("category")
    if category:
        qs = qs.filter(category_id=category)

    # Build the HTTP response with CSV content type
    filename = f"expenses_{month or 'all'}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Header row
    writer.writerow(["ID", "Title", "Amount (₹)", "Category", "Date", "Note", "Created At"])

    # Data rows
    for exp in qs:
        writer.writerow([
            exp.id,
            exp.title,
            exp.amount,
            exp.category.name if exp.category else "Uncategorised",
            exp.date.strftime("%Y-%m-%d"),
            exp.note,
            exp.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    return response


