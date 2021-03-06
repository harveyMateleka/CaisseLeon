# Generated by Django 3.0 on 2021-10-29 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0024_etatbesoinimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='droit',
            options={'permissions': (('entree', 'Onglet Entrée'), ('entreemodi', 'Onglet Modifier Entrée'), ('entreesup', 'Onglet Supprimer Entrée'), ('sortiemodi', 'Onglet Modifier Sortie'), ('sortiesup', 'Onglet Supprimer Sortie'), ('superviseur', 'Etat Besoins Superviseur'), ('validation', 'Validation Etat Besoins'), ('regularisa', 'Onglet Régularisation'), ('soldephysi', 'Onglet Solde Physique'), ('sortie', 'Onglet Sortie'), ('categorie', 'Onglet Référentiel'), ('rapport', 'Onglet Rapport'), ('exportation', 'Onglet Exportation'), ('signature', 'Onglet Signature'))},
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('imagebs', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
