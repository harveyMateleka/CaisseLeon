from django.contrib import admin
from .models import *

admin.site.register(Fournisseur)
admin.site.register(Tbl_banque)
admin.site.register(Pays)
admin.site.register(Mode_paie)

# Register your models here.
