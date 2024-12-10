# Generated by Django 4.2.16 on 2024-11-21 23:15

from django.db import migrations

def assign_owners_to_uploads(apps, schema_editor):
    Upload = apps.get_model('users', 'Upload')
    Project = apps.get_model('users', 'Project')

    for upload in Upload.objects.filter(owner__isnull=True):
        project = upload.project
        if project and project.owner:
            upload.owner = project.owner
            upload.save()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0019_upload_owner'),
    ]

    operations = [
        migrations.RunPython(assign_owners_to_uploads),
    ]
