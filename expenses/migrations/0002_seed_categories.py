from django.db import migrations

DEFAULT_CATEGORIES = [
    ("Food & Dining",    "#f59e0b", "🍔"),
    ("Transport",        "#3b82f6", "🚗"),
    ("Shopping",         "#ec4899", "🛍️"),
    ("Entertainment",    "#8b5cf6", "🎬"),
    ("Health",           "#10b981", "💊"),
    ("Bills & Utilities","#ef4444", "⚡"),
    ("Other",            "#6b7280", "📦"),
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("expenses", "Category")
    for name, color, icon in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={"color": color, "icon": icon})


def unseed_categories(apps, schema_editor):
    Category = apps.get_model("expenses", "Category")
    Category.objects.filter(name__in=[c[0] for c in DEFAULT_CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=unseed_categories),
    ]
