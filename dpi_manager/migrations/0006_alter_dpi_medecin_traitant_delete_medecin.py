# Generated by Django 5.1.3 on 2024-12-21 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi_manager', '0005_dpi_qr_code'),
        ('users', '0004_medecin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpi',
            name='medecin_traitant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dossiers', to='users.medecin'),
        ),
        migrations.DeleteModel(
            name='Medecin',
        ),
    ]