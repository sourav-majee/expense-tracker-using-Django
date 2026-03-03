from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id",    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name",  models.CharField(max_length=100, unique=True)),
                ("color", models.CharField(default="#6366f1", max_length=20)),
                ("icon",  models.CharField(default="💰", max_length=50)),
            ],
            options={"verbose_name_plural": "Categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id",         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title",      models.CharField(max_length=200)),
                ("amount",     models.DecimalField(decimal_places=2, max_digits=10)),
                ("date",       models.DateField()),
                ("note",       models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category",   models.ForeignKey(
                                blank=True, null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="expenses",
                                to="expenses.category",
                               )),
            ],
            options={"ordering": ["-date", "-created_at"]},
        ),
    ]
