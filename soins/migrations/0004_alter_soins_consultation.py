# Generated by Django 5.1.3 on 2025-01-01 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_alter_consultation_certificat_and_more'),
        ('soins', '0003_alter_soins_infirmier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soins',
            name='consultation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='soins', to='consultations.consultation'),
        ),
    ]