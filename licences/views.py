from decimal import Context
from itertools import count
from django import template
from django.shortcuts import render, resolve_url
from django.http import JsonResponse,HttpResponse
from licences.models import *
from licences.models import Paiedeclaration
from licences.models import Declaration
from operation.models import *
from .models import *
from .utils import render_to_pdf
from django.template.loader import get_template
from django.db.models import Sum, F
import datetime

def declaration(request):
    banque=Tbl_banque.objects.all().order_by('-id')
    pays=Pays.objects.all().order_by('-id')
    four=Fournisseur.objects.all().order_by('-id')
    res={
        "banque":banque,
        "pays":pays,
        "fournisseur":four,
    }
    return render(request,'declaration.html',res)

def connexe(request):
    if request.method=="POST" and request.is_ajax():
        Element_conx.objects.create(
            type_element=request.POST['frais'],
            mont_elem=request.POST['montfrais'],
            num_valid=request.POST['numvalide']
        )
        res={"success":"1"}
        return JsonResponse(res,safe=False)
def getconnexe(request,con):
    tableau={}
    result=Element_conx.objects.filter(num_valid=con).values('id','type_element','mont_elem')
    if result:
        tableau=list(result)
        data={'data':tableau}
        return JsonResponse(data,safe=False)

def getdetailprod(request,prod):
    tableau={}
    resol=Ligne_declarate.objects.filter(num_valid=prod).values('id','tarif','designation','qtefour','unit','prix')
    if resol:
        tableau=list(resol)
        data={'data':tableau}
        return JsonResponse(data,safe=False)

def save_detail(request):
    if request.method=='POST' and request.is_ajax():
       Ligne_declarate.objects.create(
           tarif=request.POST['tarif'],
           designation=request.POST['detail'],
           qtefour=request.POST['qte'],
           unit=request.POST['unite'],
           prix=request.POST['prix'],
           num_valid=request.POST['numvalidate'],

       ) 
       data={'success':'1'}
       return JsonResponse(data,safe=False)

def valide_licence(request):
     if request.method=='POST' and request.is_ajax():
        Declaration.objects.create(
            banque_id=request.POST['banque'],
            num_valid=request.POST['numvalide'],
            poste=request.POST['poste'],
            cod_pays_id=request.POST['select_pays'],
            name_four_id=request.POST['select_four'],
            montantdecl=request.POST['montant'],
            contact_ben=request.POST['banque'],
            monnaie=request.POST['devise'],
            mode_trans=request.POST['mode'],
            num_fac=request.POST['numfact'],
            date_fac=request.POST['datefac'],
            date_valid=request.POST['datevalid'],
            montpay=0,
            datfin=request.POST['datefin'],
            datop=request.POST['datop']
            

        )
        return JsonResponse({'success':'1'},safe=False)
       


def view_paiement(request):
    mode=Mode_paie.objects.all()
    context={
        "mode":mode
    }
    return render(request,'paiement.html',context)

def save_paiement(request):
    if request.method=="POST" and request.is_ajax():
        result=Declaration.objects.get(num_fac=request.POST['numvalide'])
        if result:
            montant=0.00
            paie=Paiedeclaration.objects.filter(id_declaration=result)
            if paie is None:
                 if float(request.POST['Montant']) < result.montantdecl:
                     Paiedeclaration.objects.create(
                         id_declaration_id=result.id,
                         montpaie=request.POST['Montant'],
                         numfact=request.POST['numfact'],
                         name_ordre=request.POST['charge'],
                         code_mode_id=request.POST['mode'],
                        )
                     donnees=request.POST['numvalide'] + '/' + request.POST['numfact']
                     Location.objects.create(
                        libelle=donnees,
                        compte='caisse',
                        typemvt='P'
                      )
                 result.montpay=request.POST['Montant']
                 result.save()
                 data={
                        "success":"1",
                        "msg":"données enregistrée"
                        }
                 return JsonResponse(data,safe=False)
            else :
                for ligne in paie:
                    montant += ligne.montpaie
                total= montant + float(request.POST['Montant'])

                if total <= result.montantdecl:
                    Paiedeclaration.objects.create(
                        id_declaration_id=result.id,
                        montpaie=request.POST['Montant'],
                        numfact=request.POST['numfact'],
                        name_ordre=request.POST['charge'],
                        code_mode_id=request.POST['mode']
                    )
                    donnees=request.POST['numvalide'] + '/' + request.POST['numfact']
                    Location.objects.create(
                        libelle=donnees,
                        compte='caisse',
                        typemvt='P'
                    )
                    result.montpay=total
                    result.save()
                    data={
                        "success":"1",
                        "msg":"données enregistrée"
                        }
                    return JsonResponse(data,safe=False)
                else:
                    data={
                        "success":"2",
                        "msg":"gonflement dans l'operation"
                        }
                    return JsonResponse(data,safe=False)


            
            

def delete_paiement(request):
    if request.method=="POST" and request.is_ajax():
        resol=Paiedeclaration.objects.get(pk=request.POST['id'])
        if resol:
            decl=Declaration.objects.get(id=resol.id_declaration_id)
            if decl:
                decl.montpay -= resol.montpaie
                decl.save()
            resol.delete()
            return JsonResponse({"success":"1"},safe=False)

def getall_declaration(request):
    tableau={}
    resul=Declaration.objects.all().order_by('-id')
    tableau=list(resul)
    return JsonResponse({'data':tableau},safe=False)

def getAll_paie(request):
    tableau={}
    result=Paiedeclaration.objects.all().values('id','id_declaration__monnaie','id_declaration__num_fac','datepaie','montpaie','numfact')
    tableau=list(result)
    data={'data':tableau}
    return JsonResponse(data,safe=False)

def getdeclaration(request):
    result=Declaration.objects.all().order_by('-id').values('id','num_valid','num_fac','date_fac','poste','montantdecl','monnaie','date_valid','cod_pays__name_pays','banque__name_banque','name_four__name_four','montpay','datfin')
    banque=Tbl_banque.objects.all().order_by('-id')
    pays=Pays.objects.all().order_by('-id')
    four=Fournisseur.objects.all().order_by('-id')
    res={
        "banque":banque,
        "pays":pays,
        "fournisseur":four,
        "declaration":result
    }
    return render(request,'consultationL.html',res)



def delconnexe(request):
    if request.method=="POST" and request.is_ajax():
        resul=Element_conx.objects.get(pk=request.POST['id'])
        if resul:
            varget=resul.num_valid
            montant=resul.mont_elem
            resul.delete()
            operation={
                "data":varget,
                "success":"1",
                "montant":montant
            }
            return JsonResponse(operation,safe=False)

def delproduit(request):
    if request.method=="POST" and request.is_ajax():
        resul=Ligne_declarate.objects.get(pk=request.POST['id'])
        if resul:
            varget=resul.num_valid
            montant=resul.qtefour * resul.prix
            resul.delete()
            operation={
                "data":varget,
                "success":"1",
                "montant":montant
            }
            return JsonResponse(operation,safe=False)

def rapportlicence(request):
    return render(request,'rapportgene.html')

def afficherapport(request,ddebut,dfin):
    tableau={}
    result=Declaration.objects.filter(date_fac__range=(ddebut,dfin)).values('id','num_valid','poste','montantdecl','monnaie','date_fac','cod_pays__name_pays','banque__name_banque','name_four__name_four','montpay').order_by('date_fac')
    tableau=list(result)
    data={'data':tableau}
    return JsonResponse(data,safe=False)

def rapport_extrais(request):
    return render(request,'rapportextrais.html')

def printrapport(request,ddebut,dfin):
    template=get_template('printpdf_rapport.html')
    tableau=[]
    result=Declaration.objects.filter(date_fac__range=(ddebut,dfin))
    tableau=result
    Mvt_rapport.objects.all().delete()
    for list_result in result:
        tab_data=Paiedeclaration.objects.filter(id_declaration=list_result,datepaie__range=(ddebut,dfin)).aggregate(total=Sum("montpaie")).get('total')
        if tab_data is None:
            tab_data=0
            Mvt_rapport.objects.create(
                numlicence=list_result.num_valid,
                codep=list_result.cod_pays,
                report=list_result.montpay - 0,
                montantlice=list_result.montantdecl,
                montantp=tab_data,
                monnaie=list_result.monnaie,
                datvalid=list_result.date_fac
            )
        else:
            Mvt_rapport.objects.create(
                numlicence=list_result.num_valid,
                codep=list_result.cod_pays,
                report=list_result.montpay - tab_data,
                montantlice=list_result.montantdecl,
                montantp=tab_data,
                monnaie=list_result.monnaie,
                datvalid=list_result.date_fac
            )
    database=Mvt_rapport.objects.all()        
    context={
        'data':database,
        'ddebut':datetime.datetime.strptime(ddebut,'%Y-%m-%d').strftime('%d/%m/%Y'),
        'dfin':datetime.datetime.strptime(dfin,'%Y-%m-%d').strftime('%d/%m/%Y'),
        'today':datetime.datetime.today().strftime('%d/%m/%Y')
    }
    pdf=render_to_pdf('printpdf_rapport.html',context)
    return HttpResponse(pdf,content_type='application/pdf')

def afficherextrai(request,ddebut,dfin,num):
    tableau={}
    result=Declaration.objects.get(num_fac=num)
    if result:
        resulte=Paiedeclaration.objects.filter(datepaie__range=(ddebut,dfin),id_declaration=result).values('id','datepaie','montpaie','numfact','id_declaration__monnaie','id_declaration__num_valid','id_declaration__num_fac','name_ordre')
        tableau=list(resulte)
        data={'data':tableau}
        return JsonResponse(data,safe=False)

def printextrait(request,ddebut,dfin,num):
    template=get_template('printpdf_extrait.html')
    result=Declaration.objects.get(num_fac=num)
    if result:
        resulte=Paiedeclaration.objects.filter(datepaie__range=(ddebut,dfin),id_declaration=result).values('datepaie','montpaie','numfact','id_declaration__monnaie','id_declaration__num_valid','id_declaration__num_fac','name_ordre')
        paiement=Paiedeclaration.objects.filter(datepaie__range=(ddebut,dfin),id_declaration=result).aggregate(total=Sum('montpaie')).get('total')
        if paiement is None:
            paiement=0
        context={
            'data':resulte,
            'numero':result.num_valid,
            'ddebut':datetime.datetime.strptime(ddebut,'%Y-%m-%d').strftime('%d/%m/%Y'),
            'dfin':datetime.datetime.strptime(dfin,'%Y-%m-%d').strftime('%d/%m/%Y'),
            'total':result.montpay,
            'monnaie':result.monnaie,
            'facturation':result.montantdecl,
            'paiement':paiement,
            'today':datetime.datetime.today().strftime('%d/%m/%Y')

        }
        pdf=render_to_pdf('printpdf_extrait.html',context)
        return HttpResponse(pdf,content_type='application/pdf')

def afficheDeclaration(request):
    if request.method=='POST' and request.is_ajax():
        result=Declaration.objects.filter(id=request.POST['id']).values('code_typ_decl','num_valid','poste','monnaie','mode_trans','num_fac','date_valid','date_fac','s_typ_decl','cod_pays','mode_paie','montantdecl','name_four','banque','datfin')
        #data={"donne":result}
        return JsonResponse({"done":list(result)},safe=False)
def update_licence(request):
    if request.method=='POST' and request.is_ajax():
        resul=Declaration.objects.get(pk=request.POST['idcode'])
        if resul:
            resul.code_typ_decl=request.POST['cotype']
            resul.banque_id=request.POST['banque']
            resul.s_typ_decl=request.POST['soustype']
            resul.num_valid=request.POST['numvalide']
            resul.poste=request.POST['poste']
            resul.cod_pays_id=request.POST['select_pays']
            resul.name_four_id=request.POST['select_four']
            resul.montantdecl=request.POST['montant']
            resul.contact_ben=request.POST['banque']
            resul.monnaie=request.POST['devise']
            resul.mode_trans=request.POST['mode']
            resul.num_fac=request.POST['numfact']
            resul.date_fac=request.POST['datefac']
            resul.date_valid=request.POST['datevalid']
            resul.datfin=request.POST['datfin']
            resul.save()
            return JsonResponse({"success":"1"},safe=False)

def delete_licence(request):
    if request.method=='POST' and request.is_ajax():
        resul=Declaration.objects.get(pk=request.POST['id'])
        if resul:
           ligne=Paiedeclaration.objects.all().filter(id_declaration=resul)
           prod=Ligne_declarate.objects.all().filter(num_valid=resul.num_valid)
           prod.delete()
           element=Element_conx.objects.all().filter(num_valid=resul.num_valid)
           element.delete()
           ligne.delete()
           resul.delete()
        return JsonResponse({"success":"1"},safe=False)
def ligne_print(request,code):
    template=get_template('printdecla.html')
    result=Declaration.objects.get(pk=code)
    if result:
        resu=Element_conx.objects.filter(num_valid=result.num_valid)
        nbre=resu.count()
        res=Ligne_declarate.objects.filter(num_valid=result.num_valid)
        context={
            'detail_connexe':resu,
            'detail_prod':res,
            'numerofac':result.num_fac,
            'numerovalid':result.num_valid,
            'datfac':result.date_fac,
            'datvalid':result.date_valid,
            'datvalidfin':result.datfin,
            'fournisseur':result.name_four,
            'banque':result.banque,
            'montant':result.montantdecl,
            'pays':result.cod_pays,
            'monnaie':result.monnaie,
            'poste':result.poste,
            'pays':result.cod_pays,
            'type':result.code_typ_decl,
            's_type':result.s_typ_decl,
            'dates':datetime.datetime.today().strftime('%d/%m/%Y'),
            'nbre':nbre,

        }
        pdf=render_to_pdf('printdecla.html',context)
        return HttpResponse(pdf,content_type='application/pdf')

def view_produit(request):
    return render(request,'detailproduit.html')






            


      





     
  










# Create your views here.
