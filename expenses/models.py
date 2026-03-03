from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20,  default="#6366f1")
    icon  = models.CharField(max_length=50,  default="💰")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.icon} {self.name}"


class Expense(models.Model):
    # Each expense belongs to a user
    user        = models.ForeignKey(
                    User, on_delete=models.CASCADE,
                    related_name="expenses", null=True, blank=True
                  )
    title       = models.CharField(max_length=200)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    category    = models.ForeignKey(
                    Category, on_delete=models.SET_NULL,
                    null=True, blank=True, related_name="expenses"
                  )
    date        = models.DateField()
    note        = models.TextField(blank=True, default="")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} — ₹{self.amount}"
