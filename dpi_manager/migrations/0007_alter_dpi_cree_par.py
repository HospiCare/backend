# Generated by Django 5.1.3 on 2024-12-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi_manager', '0006_alter_dpi_medecin_traitant_delete_medecin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpi',
            name='cree_par',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
