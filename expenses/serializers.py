from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Expense


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label="Confirm password")

    class Meta:
        model  = User
        fields = ["id", "username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["id", "username", "email"]


# ── Categories ────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ["id", "name", "color", "icon"]


# ── Expenses ──────────────────────────────────────────────────────────────────

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name",  read_only=True, default=None)
    color         = serializers.CharField(source="category.color", read_only=True, default=None)
    icon          = serializers.CharField(source="category.icon",  read_only=True, default=None)

    class Meta:
        model  = Expense
        fields = [
            "id", "title", "amount", "category", "category_name",
            "color", "icon", "date", "note", "created_at",
        ]
        read_only_fields = ["created_at"]
