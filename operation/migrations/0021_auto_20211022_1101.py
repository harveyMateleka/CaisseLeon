# Generated by Django 3.0 on 2021-10-22 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0020_auto_20211021_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='droit',
            options={'permissions': (('entree', 'Onglet Entrée'), ('entreemodi', 'Onglet Modifier Entrée'), ('entreesup', 'Onglet Supprimer Entrée'), ('sortiemodi', 'Onglet Modifier Sortie'), ('sortiesup', 'Onglet Supprimer Sortie'), ('superviseur', 'Etat Besoins Superviseur'), ('validation', 'Validation Etat Besoins'), ('regularisa', 'Onglet Régularisation'), ('soldephysi', 'Onglet Solde Physique'), ('sortie', 'Onglet Sortie'), ('categorie', 'Onglet Référentiel'), ('rapport', 'Onglet Rapport'), ('exportation', 'Onglet Exportation'))},
        ),
        migrations.AddField(
            model_name='caisse',
            name='etatbesoin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='operation.EtatBesoin'),
        ),
    ]
