# Generated by Django 4.2.2 on 2023-06-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upload", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadfiledetails",
            name="user_id",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
