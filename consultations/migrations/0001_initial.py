# Generated by Django 5.1.4 on 2024-12-23 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dpi_manager', '0006_alter_dpi_medecin_traitant_delete_medecin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_demande', models.DateTimeField(auto_now_add=True)),
                ('date_fin', models.DateTimeField()),
                ('motif', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Frais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_echeance', models.DateTimeField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('antecedants', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('certificat', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.certificat')),
                ('dpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='dpi_manager.dpi')),
                ('frais', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.frais')),
                ('resume', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.resume')),
            ],
        ),
    ]
