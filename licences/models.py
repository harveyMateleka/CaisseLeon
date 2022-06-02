from django.db import models
from django.db.models.base import Model

# Create your models here.
class Tbl_banque(models.Model):
    name_banque=models.CharField(max_length=60)

    def __str__(self):
        return self.name_banque

class Pays(models.Model):
    name_pays=models.CharField(max_length=70)

    def __str__(self):
        return self.name_pays

class Fournisseur(models.Model):
    name_four=models.CharField(max_length=100)
    adresse=models.TextField()
    email_four=models.CharField(max_length=50)
    telfour=models.CharField(max_length=20, unique=True)
    fax_four=models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.name_four

class Declaration(models.Model):
    code_typ_decl=models.CharField(max_length=10,null=True,blank=True)
    banque=models.ForeignKey(Tbl_banque,on_delete=models.SET_NULL,null=True,blank=True)
    s_typ_decl=models.CharField(max_length=4,null=True,blank=True)
    num_valid=models.CharField(max_length=25,unique=True,null=False)
    poste=models.CharField(max_length=50,null=True,blank=True)
    cod_pays=models.ForeignKey(Pays,on_delete=models.SET_NULL,null=True,blank=True)
    name_four=models.ForeignKey(Fournisseur,on_delete=models.SET_NULL,null=True,blank=True)
    montantdecl=models.FloatField()
    mode_paie=models.CharField(max_length=20,null=True,blank=True)
    contact_ben=models.CharField(max_length=20,null=True,blank=True)
    monnaie=models.CharField(max_length=10,null=True,blank=True)
    mode_trans=models.CharField(max_length=20,null=True,blank=True)
    num_fac=models.CharField(max_length=15,unique=True,null=False)
    date_fac=models.DateField(null=True,blank=True)
    date_valid=models.DateField(null=True,blank=True)
    montpay=models.FloatField(null=True,blank=True)
    datfin=models.DateField(null=True,blank=True)
    datop=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.num_valid
        
    def __iter__(self):
        return self

class Element_conx(models.Model):
    type_element=models.CharField(max_length=20)
    mont_elem=models.FloatField()
    id_declaration=models.ForeignKey(Declaration,on_delete=models.SET_NULL,null=True,blank=True)
    num_valid=models.CharField(max_length=25,null=True,blank=True)

    def __str__(self):
        return self.type_element

class Mode_paie(models.Model):
    libelle=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.libelle

class Ligne_declarate(models.Model):
    tarif=models.CharField(max_length=20,unique=True)
    designation=models.TextField()
    qtefour=models.FloatField()
    unit=models.CharField(max_length=30,blank=True)
    prix=models.FloatField()
    id_declaration=models.ForeignKey(Declaration,on_delete=models.SET_NULL,null=True,blank=True)
    num_valid=models.CharField(max_length=25,null=True,blank=True)

    def __str__(self):
        return self.designation
class Paiedeclaration(models.Model):
    datepaie=models.DateField(auto_now_add=True)
    id_declaration=models.ForeignKey(Declaration,on_delete=models.SET_NULL,null=True,blank=True)
    montpaie=models.FloatField()
    numfact=models.CharField(max_length=20, unique=True,null=True,blank=True)
    name_ordre=models.CharField(max_length=30,null=True,blank=True)
    name_ordrepaie=models.CharField(max_length=30,null=True,blank=True)
    code_mode=models.ForeignKey(Mode_paie,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.montpaie

class Mvt_rapport(models.Model):
    numlicence=models.CharField(max_length=25,null=True,blank=True)
    codep=models.CharField(max_length=40,null=True,blank=True)
    report=models.FloatField(default=0)
    montantlice=models.FloatField(default=0)
    montantp=models.FloatField(default=0)
    monnaie=models.CharField(max_length=5,null=True,blank=True)
    datvalid=models.DateField()











