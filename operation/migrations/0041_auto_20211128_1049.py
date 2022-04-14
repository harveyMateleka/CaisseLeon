# Generated by Django 3.0 on 2021-11-28 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0040_auto_20211127_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='droit',
            options={'permissions': (('entree', 'Onglet Entrée'), ('entreeajout', 'Onglet Ajout Entrée'), ('entreemodi', 'Onglet Modifier Entrée'), ('entreesup', 'Onglet Supprimer Entrée'), ('sortieajout', 'Onglet Ajout Sortie'), ('sortiemodi', 'Onglet Modifier Sortie'), ('sortiesup', 'Onglet Supprimer Sortie'), ('superviseur', 'Etat Besoins Superviseur'), ('validation', 'Validation Etat Besoins'), ('regularisa', 'Onglet Régularisation'), ('soldephysi', 'Onglet Solde Physique'), ('soldephysiajout', 'Onglet Ajout Solde Physique'), ('soldephysimodi', 'Onglet Modifier Solde Physique'), ('soldephysisup', 'Onglet Supprimer Solde Physique'), ('sortie', 'Onglet Sortie'), ('categorie', 'Onglet Référentiel'), ('rapport', 'Onglet Rapport'), ('exportation', 'Onglet Exportation'), ('signature', 'Onglet Signature'), ('etatbesoin', 'Etat Besoins'), ('dashboard', 'Dashboard'), ('caissep', 'Voir Rapport toute Caisse'))},
        ),
        migrations.CreateModel(
            name='cloture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('datemvt', models.DateTimeField(db_column='DateMvt', unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
