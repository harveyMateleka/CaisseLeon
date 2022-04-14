# Generated by Django 3.0 on 2021-12-28 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0047_delai'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='droit',
            options={'permissions': (('entree', 'Onglet Entrée'), ('entreeajout', 'Onglet Ajout Entrée'), ('entreemodi', 'Onglet Modifier Entrée'), ('entreesup', 'Onglet Supprimer Entrée'), ('sortieajout', 'Onglet Ajout Sortie'), ('sortiemodi', 'Onglet Modifier Sortie'), ('sortiesup', 'Onglet Supprimer Sortie'), ('superviseur', 'Etat Besoins Superviseur'), ('validation', 'Validation Etat Besoins'), ('regularisa', 'Onglet Régularisation'), ('soldephysi', 'Onglet Solde Physique'), ('soldephysiajout', 'Onglet Ajout Solde Physique'), ('soldephysimodi', 'Onglet Modifier Solde Physique'), ('soldephysisup', 'Onglet Supprimer Solde Physique'), ('sortie', 'Onglet Sortie'), ('categorie', 'Onglet Référentiel'), ('rapport', 'Onglet Rapport'), ('exportation', 'Onglet Exportation'), ('signature', 'Onglet Signature'), ('etatbesoin', 'Etat Besoins'), ('dashboard', 'Dashboard'), ('delai', 'Delai Etat Besoin'), ('caissep', 'Voir Rapport toute Caisse'))},
        ),
    ]
