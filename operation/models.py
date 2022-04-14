from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimespantedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Zone(TimespantedModel):
    libelle = models.CharField(max_length=150,unique=True)
    def __str__(self):
        return self.libelle

class Delai(TimespantedModel):
    heure = models.TimeField()
    def __str__(self):
        return str(self.heure)

class Location(TimespantedModel):
    libelle = models.CharField(max_length=150)
    compte = models.CharField(max_length=50)
    typemvt = models.CharField(db_column='TypeMvt', max_length=1,null=True,blank=True)

class Taux(TimespantedModel):
    taux = models.FloatField()


class Departement(TimespantedModel):
    libelle = models.CharField(max_length=150)
    def __str__(self):
        return self.libelle

cat = (
        ('S', 'Sortie'),
        ('E', 'Entrée'),
 )


class Superviseur(TimespantedModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    departement = models.ForeignKey(Departement,on_delete=models.SET_NULL,related_name="superviseurdata", null=True,blank=True)

class Affectation(TimespantedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='userzone',
    )
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

etat = (
        ('R', 'Rejet'),
        ('N', 'Normal'),
        ('C', 'Caisse'),#ca par chez le caissier
        ('A', 'Admin'), #ca par chez le valideur(kas)
        ('V', 'Verificateur'),#ca par chez le verificateur(tshenda)
 )

class EtatBesoin(TimespantedModel):
    datemvt = models.DateField()
    demandeur = models.CharField(max_length=100)
    motif = models.TextField()
    devise = models.CharField(max_length=10)
    superviseur = models.ForeignKey(Superviseur, models.PROTECT)
    userAdmi = models.ForeignKey(User, models.PROTECT, related_name="adminuser", null=True, blank=True)
    etat = models.CharField(max_length=1,choices=etat,default='N')

class Caisse(TimespantedModel):
    datemvt = models.DateTimeField(db_column='DateMvt')
    refdoc = models.CharField(db_column='RefDoc', max_length=100)
    montant = models.FloatField(db_column='Montant')
    taux = models.FloatField(db_column='Taux')
    operation = models.CharField( max_length=1,choices=cat,null=True,blank=True)
    lettre = models.CharField( max_length=200,null=True,blank=True)
    devise = models.CharField(db_column='Devise', max_length=10)
    motif = models.TextField(db_column='Motif')
    location = models.ForeignKey(Location, models.PROTECT)#referenciel
    departement = models.ForeignKey(Departement, models.PROTECT)
    etatbesoin = models.ForeignKey(EtatBesoin, models.PROTECT,null=True,blank=True)
    user = models.ForeignKey(User, models.PROTECT)

    demandeurboss = models.CharField(max_length=100,null=True,blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)



class EtatBesoinImage(TimespantedModel):
    caisse = models.ForeignKey(Caisse, models.SET_NULL,null=True,blank=True)
    imagebs = models.TextField()

class UserImage(TimespantedModel):
    user = models.ForeignKey(User, models.SET_NULL,related_name="imageuser",null=True,blank=True)
    imagebs = models.TextField()


class Signature(TimespantedModel):
    user = models.ForeignKey(User, models.SET_NULL,null=True,blank=True)
    txt = models.TextField('Mot de passe')
    delai=models.DateTimeField()
    etat=models.BooleanField(default=False)

    class Meta:
        verbose_name='Cle de validation'
        verbose_name_plural='Cle de validation'

class DetailEtatBesoin(TimespantedModel):
    prix = models.FloatField()
    item = models.TextField()
    qte = models.FloatField()
    etatbesoin = models.ForeignKey(EtatBesoin, models.PROTECT)

class FactureEtatBesoin(TimespantedModel):
    prix = models.FloatField()
    datemvt = models.DateTimeField(db_column='DateMvt')
    description = models.CharField(max_length=255,null=True,blank=True)
    facture = models.CharField(max_length=20,null=True,blank=True)
    fournisseur = models.CharField(max_length=255,null=True,blank=True)
    etatbesoin = models.ForeignKey(EtatBesoin, models.PROTECT)



class Solde(TimespantedModel):
    datemvt = models.DateTimeField(db_column='DateMvt',unique=True)
    deviseusd = models.FloatField()
    devisecfa = models.FloatField()
    devisecdf = models.FloatField()
    deviseeuro = models.FloatField()
    user = models.ForeignKey(User, models.PROTECT)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

class cloture(TimespantedModel):
    datemvt = models.DateField(db_column='DateMvt')
    user = models.ForeignKey(User, models.PROTECT)
    etat=models.BooleanField(default=False)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)


class Societe(TimespantedModel):
    nom = models.CharField(max_length=100)
    sigle = models.CharField(max_length=15)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    idetat = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    


class Droit(models.Model):
    class Meta:
        permissions = (

            ('entree', 'Onglet Entrée'),
                # enfant
                ('entreeajout', 'Onglet Ajout Entrée'),
                ('entreemodi', 'Onglet Modifier Entrée'),
                ('entreesup', 'Onglet Supprimer Entrée'),
                # enfant
            ('sortieajout', 'Onglet Ajout Sortie'),
            ('sortiemodi', 'Onglet Modifier Sortie'),
            ('sortiesup', 'Onglet Supprimer Sortie'),
                # enfant
                # enfant
            ('superviseur', 'Etat Besoins Superviseur'),
                # enfant
                # enfant
            ('validation', 'Validation Etat Besoins'),
                # enfant
                # enfant
            ('regularisa', 'Onglet Régularisation'),
                # enfant
                # enfant
            ('soldephysi', 'Onglet Solde Physique'),
                # enfant
                ('soldephysiajout', 'Onglet Ajout Solde Physique'),
                ('soldephysimodi', 'Onglet Modifier Solde Physique'),
                ('soldephysisup', 'Onglet Supprimer Solde Physique'),
                # enfant
            ('sortie', 'Onglet Sortie'),
                # enfant
                # enfant
            ('categorie', 'Onglet Référentiel'),
                # enfant
                # enfant
            ('rapport', 'Onglet Rapport'),
                # enfant

                # enfant
            ('exportation', 'Onglet Exportation'),
                # enfant
                # enfant
            ('signature', 'Onglet Signature'),
                # enfant
                # enfant
            ('etatbesoin', 'Etat Besoins'),
                 #enfant
                 #enfant

            ('dashboard', 'Dashboard'),
            #('delai', 'Delai Etat Besoin'),
            ('caissep', 'Voir Rapport toute Caisse'),
            )



# update operation_caisse set operation=(select TypeMvt from operation_location where operation_location.id=operation_caisse.location_id)
# where location_id =(select operation_location.id from operation_location where operation_location.id=operation_caisse.location_id)