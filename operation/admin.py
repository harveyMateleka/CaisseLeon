from django.contrib import admin
from django.conf import settings
from .utils import AESCipher
# Register your models here.
from .models import *

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("id","libelle","created_at")
    search_fields = ['libelle', ]

@admin.register(Superviseur)
class SuperviseurAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("user","departement","created_at")
    search_fields = ['user', ]

@admin.register(Taux)
class TauxAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("id","taux","created_at")
    search_fields = ['taux', ]


@admin.register(Delai)
class DelaiAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("id","heure","created_at")

    def save_model(self, request, obj, form, change):
        if change:
            return False
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("id","libelle","created_at")
    search_fields = ['libelle', ]


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("user","zone","created_at")
    search_fields = ['user', ]



@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("txt","delai","created_at")
    exclude = ("user","etat")


    def save_model(self, request, obj, form, change):
        if not change:
            s=Signature.objects.filter(etat=False)
            if s:
                return False
            aes = AESCipher(settings.SECRET_KEY[:16], 32)
            obj.txt=aes.encrypt(str(obj.txt).strip()+"_caisse_"+str(obj.delai))
            obj.user=request.user
        else:
            return False
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ("id","nom","sigle","created_at")
    search_fields = ['nom', ]
