# Generated by Django 4.2.3 on 2023-08-08 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="modified_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
