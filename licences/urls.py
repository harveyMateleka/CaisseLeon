from django.urls import path
from . import views

from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from .views import *

urlpatterns = [
    path('declaration/', views.declaration,name='declaration'),
    path('declaration/connexe', views.connexe,name='connexe'),
    path('decla/getconex/<str:con>', views.getconnexe),
    path('decla/getdetailprod/<str:prod>', views.getdetailprod),
    path('declaration/afficher/<str:ddebut>/<str:dfin>', views.afficherapport),
    path('declaration/ligne_print/<str:code>',views.ligne_print),
    # path('declaration/afficherextrai/<str:ddebut>/<str:dfin>/<str:num>', views.afficherextrai),
    path('declaration/afficherextrai/<str:ddebut>/<str:num>', views.afficherextrai),
    path('declaration/print/<str:ddebut>/<str:dfin>', views.printrapport),
    path('declaration/deletecon/',views.delconnexe,name="delconnexe"),
    path('declaration/delproduit/',views.delproduit,name="delproduit"),
    path('declaration/afficheDeclaration/',views.afficheDeclaration,name="afficheDeclaration"),
    path('declaration/rapportlicence/',views.rapportlicence,name="rapportlicence"),
    path('declaration/save_detail/',views.save_detail,name="detail_prod"),
    path('declaration/create_paiement/',views.save_paiement,name="paie_licence"),
    path('decla/printextrait/<str:ddebut>/<str:num>', views.printextrait),
    path('declaration/paiement/',views.view_paiement,name="view_paiement"),
    path('declaration/consultation/',views.getdeclaration,name="consultation"),
    path('declaration/charge_paie/', views.getAll_paie,name="charge_paie"),
    path('declaration/deletepaie/', views.delete_paiement,name="deletepaie"),
    path('declaration/valide_licence/',views.valide_licence,name="valide_licence"),
    path('declaration/update_licence/',views.update_licence,name="update_licence"),
    path('declaration/delete_licence/',views.delete_licence,name="delete_licence"),
    path('declaration/rapport_extrais/',views.rapport_extrais,name="rapport_extrais"),
    path('declaration/detail_produit/',views.view_produit,name="index_produit"),
    
]

