# Generated by Django 5.1.3 on 2024-12-29 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilan', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilanbiologique',
            name='graphique',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bilanbiologique',
            name='result',
            field=models.TextField(blank=True, null=True),
        ),
    ]
