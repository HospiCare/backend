# Generated by Django 5.1.4 on 2024-12-21 20:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi_manager', '0003_alter_dpi_patient_remove_medecin_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medecin_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
