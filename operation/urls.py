from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from .views import *
app_name='operation'
urlpatterns = [
    path('', home,name='home'),

    path('mvt', mvt,name='mvt'),
    path('signature', signature,name='signature'),
    path('etatbs', etatbs,name='etatbs'),
    path('fac', fac,name='fac'),
    path('solde', solde,name='solde'),
    path('cloturee', cloturee,name='cloture'),
    path('getsolde', getsolde,name='getsolde'),
    path('regularisation', regularisation,name='regularisation'),
    path('rap', rap,name='rap'),
    path('service', service,name='service'),
    path('synthese', synthese,name='synthese'),
    path('rapgen', rapgen,name='rapgen'),
    path('rapgenfou', rapgenfou,name='rapgenfou'),
    path('raplistbesoin', raplistbesoin,name='raplistbesoin'),
    path('raplistentree', raplistentree,name='raplistentree'),
    path('raplistbonvalide', raplistbonvalide,name='raplistbonvalide'),
    path('rapetatbs', rapetatbs,name='rapetatbs'),
    path('rapetatbesoinjus', rapetatbesoinjus,name='rapetatbesoinjus'),
    path('listmvt', listmvt,name='listmvt'),
    path('exportation', exportation,name='exportation'),

    path('categorie', categorie,name='categorie'),
    path('getcategorie', getcategorie,name='getcategorie'),
    path('deletecategorie', deletecategorie,name='deletecategorie'),

    path('deletemvt', deletemvt,name='deletemvt'),
    path('pdfetat', pdfetat,name='pdfetat'),
    path('deletesolde', deletesolde,name='deletesolde'),

    path('getmvt', getmvt,name='getmvt'),
    path('getmvtcompta', getmvtcompta,name='getmvtcompta'),
    path('getbesoin', getbesoin,name='getbesoin'),
    path('getbesoinfacture', getbesoinfacture,name='getbesoinfacture'),
    path('getetatbs', getetatbs,name='getetatbs'),
    path('getmvtnormal', getmvtnormal,name='getmvtnormal'),
    path('getsignature', getsignature,name='getsignature'),
    path('deletefacturebesoin', deletefacturebesoin,name='deletefacturebesoin'),
    path('deletesignature', deletesignature,name='deletesignature'),







]
