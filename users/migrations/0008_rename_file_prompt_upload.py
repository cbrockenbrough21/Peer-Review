# Generated by Django 4.2.16 on 2024-11-01 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_prompt_promptresponse"),
    ]

    operations = [
        migrations.RenameField(
            model_name="prompt",
            old_name="file",
            new_name="upload",
        ),
    ]