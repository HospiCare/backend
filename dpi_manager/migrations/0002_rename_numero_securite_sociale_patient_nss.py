# Generated by Django 5.1.3 on 2024-12-21 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpi_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='numero_securite_sociale',
            new_name='NSS',
        ),
    ]
