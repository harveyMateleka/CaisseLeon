from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Sum, F
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import datetime
import os
from django.urls import reverse
from pyreportjasper import JasperPy
from num2words import num2words
# Create your views here.
from django.views.decorators.http import require_POST

from .models import *




def clot(request,zoneid):

    c=cloture.objects.filter(zone_id=zoneid).count()
    if c==0:
        return 1

    c=cloture.objects.filter(zone_id=zoneid,etat=False)
    if c:
        return c.last().datemvt
    else:
        return 1

@login_required
def home(request):
    mois=datetime.date.today().month
    anne=datetime.date.today().year
    if mois <=9:
        mois=str(0)+str(mois)

    periode=str(anne)+str(mois)

    listezone={}
    listdevise=["USD","CDF","EURO","CFA"]

    for z in Zone.objects.filter(id=1):
        temp={}
        temp["libelle"] = z.libelle
        for i in range(4):
            c = Caisse.objects.filter(devise=listdevise[i],zone=z, operation='E').aggregate(Sum('montant')).get(
                 'montant__sum')
            if c is None:
                c = 0
            c1 = Caisse.objects.filter(devise=listdevise[i],zone=z, operation='S').aggregate(Sum('montant')).get(
                 'montant__sum')
            if c1 is None:
                c1 = 0
            temp[listdevise[i]]=c-c1

        listezone[z.id]=temp


    context = {
        'zones':list(listezone.values())

    }



    return render(request,'operation/index.html',context)

##########################################################entree

@login_required
def fac(request):
    if request.method == 'POST':
        #imprimer__________________________

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("fac.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'bon': str(request.POST.get('bon'))},
            locale='en_US'
        )

        #imprimer__________________________
        return HttpResponse("true")

@login_required
def mvt(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    ct = clot(request, obj.zone.id)
    if ct == 1:
        return redirect(reverse('operation:home'))
    if request.method == 'POST':
        try:
            #print(request.POST)
            with transaction.atomic():
                dv=""
                numbon=0
                if request.POST.get('devise')=="CDF":
                    dv="Franc Congolais"
                elif request.POST.get('devise')=="USD":
                    dv="Dollar Américain"
                elif request.POST.get('devise')=="CFA":
                    dv="Franc CFA"
                elif request.POST.get('devise')=="EURO":
                    dv="Euro"
                lettre = str(num2words(request.POST.get('mtn'), lang='fr'))+" "+ dv
                cai=Caisse.objects.filter(id=request.POST.get('idmvt'))
                numbon=int(request.POST.get('idmvt'))
                if cai:
                    if request.POST.get('operation') == 'E':
                        if request.user.has_perm('operation.entreemodi'):
                            pass
                        else:
                            return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)

                    elif request.POST.get('operation') == 'S':
                        if request.user.has_perm('operation.sortiemodi'):
                            pass
                        else:
                            return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                    cai.update(
                        datemvt=request.POST.get('dt'),
                        montant=request.POST.get('mtn'),
                        taux=str(request.POST.get('taux')).replace(",","."),
                        devise=request.POST.get('devise'),
                        motif=request.POST.get('motif'),
                        demandeurboss=str(request.POST.get('demandeur')).upper(),
                        lettre=lettre,
                        departement_id=request.POST.get('location'),
                        location_id=request.POST.get('referentiel'),

                    )
                else:
                    if request.POST.get('operation')=='E':
                        if request.user.has_perm('operation.entreeajout'):
                            pass
                        else:
                            return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)

                    elif request.POST.get('operation')=='S':
                        if request.user.has_perm('operation.sortieajout'):
                            pass
                        else:
                            return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)


                    if request.POST.get('idbesoin')=='0':
                        numbon=Caisse.objects.create(
                            datemvt=request.POST.get('dt'),
                            refdoc=str("DOC_") + str(request.POST.get('operation')) + str(
                                str(datetime.datetime.today()).replace('-', '').replace(' ', '').replace(':',
                                                                                                         '').replace(
                                    '.', '')),
                            montant=request.POST.get('mtn'),
                            taux=str(request.POST.get('taux')).replace(",", "."),
                            devise=request.POST.get('devise'),
                            motif=request.POST.get('motif'),
                            lettre=lettre,
                            operation=request.POST.get('operation'),
                            demandeurboss=str(request.POST.get('demandeur')).upper(),
                            departement_id=request.POST.get('location'),
                            location_id=request.POST.get('referentiel'),
                            user=request.user,
                            zone=obj.zone
                        )
                        numbon = numbon.id
                    else:
                        numbon=Caisse.objects.create(
                            datemvt=request.POST.get('dt'),
                            refdoc=str("DOC_")+str(request.POST.get('operation'))+str(str(datetime.datetime.today()).replace('-','').replace(' ','').replace(':','').replace('.','')),
                            montant=request.POST.get('mtn'),
                            taux=str(request.POST.get('taux')).replace(",","."),
                            devise=request.POST.get('devise'),
                            motif=request.POST.get('motif'),
                            demandeurboss=str(request.POST.get('demandeur')).upper(),
                            lettre=lettre,
                            operation=request.POST.get('operation'),
                            etatbesoin_id=request.POST.get('idbesoin'),
                            departement_id=request.POST.get('location'),
                            location_id=request.POST.get('referentiel'),
                            user=request.user,
                            zone=obj.zone

                        )
                        numbon=numbon.id
                        #############################
                        EtatBesoin.objects.filter(id=request.POST.get('idbesoin')).update(etat='V')
                    EtatBesoinImage.objects.create(
                        caisse_id=numbon,
                        imagebs=request.POST.get('sigImageData')
                    )
                        #############################
                return JsonResponse({"msg": "Opération effectuée", "id": "1", "bon": str(numbon)}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    context={
        "departements":Departement.objects.all().order_by('libelle'),
        "referentiels":Location.objects.all().order_by('libelle'),
        "libelle": request.GET.get('libelle'),
        "datemvt": ct,
        "catlibelle": request.GET.get('id'),
        "tauxchange":Taux.objects.all().order_by('-id')[:1],
    }
    return render(request,'operation/mvt.html',context)



@login_required
@require_POST
@permission_required('operation.signature',raise_exception=True)
def deletesignature(request):
    try:
        with transaction.atomic():
            UserImage.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

@login_required
@permission_required('operation.signature',raise_exception=True)
def getsignature(request):
    item=UserImage.objects.all().values("id","user__username","user_id").order_by('-id')
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)

@login_required
@permission_required('operation.signature',raise_exception=True)
def signature(request):

    if request.method == 'POST':
        try:

            with transaction.atomic():

                cai=UserImage.objects.filter(user_id=request.POST.get('utilisateur'))
                if cai:
                    cai.update(
                        imagebs=request.POST.get('sigImageData')
                    )
                else:
                    UserImage.objects.create(
                        user_id=request.POST.get('utilisateur'),
                        imagebs=request.POST.get('sigImageData')

                    )
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    context={
        "users":User.objects.all(),
        "signatureusers":UserImage.objects.all(),
            }
    return render(request,'operation/signature.html',context)



@login_required
@permission_required('operation.etatbesoin',raise_exception=True)
def getbesoin(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin__etat='V',etatbesoin__datemvt__gte=request.GET.get('dtd'),etatbesoin__datemvt__lte=request.GET.get('dtf')).values("etatbesoin__superviseur__departement__libelle","etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__superviseur__departement__libelle","etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)

@login_required
@permission_required('operation.etatbesoin',raise_exception=True)
def getbesoinfacture(request):
    item=FactureEtatBesoin.objects.filter(etatbesoin_id=request.GET.get("id")).values("id","facture","description","prix","fournisseur","datemvt__date")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)


@login_required
@permission_required('operation.etatbesoin',raise_exception=True)
def getetatbs(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin_id=request.GET.get('id'),etatbesoin__etat='V').order_by('-id')
    itemfac=FactureEtatBesoin.objects.filter(etatbesoin_id=request.GET.get('id'),etatbesoin__etat='V').order_by('-id')
    txt=""
    txtfac=0
    tot=0
    for i in item:
        txt+=f"""
        <tr class="item-row">
                             <td><div class="delete-btn"><input disabled type="text" required class="form-control text-uppercase" value="{i.item}" placeholder="Ecrivez le nom de l'article" type="text"></div></td>
                             <td><input disabled class="form-control" placeholder="Qte" required type="number" value={i.qte}></td>
                             <td><input disabled class="form-control" placeholder="Prix" required type="number" value={i.prix}></td>
                             <td><span class="">{i.qte*i.prix}</span></td>
                         </tr>
        """
        tot+=i.qte*i.prix

    for i in itemfac:
        txtfac+=i.prix


    return JsonResponse({'txtfac':txtfac,'txt':txt,'tot':tot}, safe=False)


@login_required
@permission_required('operation.etatbesoin',raise_exception=True)
def rapetatbs(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("etatbesoin.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'besoin':'{}'.format(request.POST.get('bon'))},
            locale='en_US'
        )

        return HttpResponse("true")

@login_required
@permission_required('operation.etatbesoin',raise_exception=True)
def etatbs(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():

                cai=FactureEtatBesoin.objects.filter(id=request.POST.get('id'))
                if cai:
                    if request.user.has_perm('operation.change_factureetatbesoin'):

                        cai.update(
                            datemvt=request.POST.get('dtf'),
                            prix=request.POST.get('mtn'),
                            description=request.POST.get('obs'),
                            facture=request.POST.get('fac'),
                            fournisseur=request.POST.get('fou'),

                        )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                else:
                    if request.user.has_perm('operation.add_factureetatbesoin'):

                        FactureEtatBesoin.objects.create(
                            datemvt=request.POST.get('dtf'),
                            prix=request.POST.get('mtn'),
                            description = request.POST.get('obs'),
                            facture = request.POST.get('fac'),
                            fournisseur = request.POST.get('fou'),
                            etatbesoin_id=request.POST.get('idmvt'),

                        )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    context={
       # "etatbesoin":EtatBesoin.objects.filter(etat='V').order_by('-id'),
    }
    return render(request,'operation/etatbs.html',context)


@login_required
@permission_required('operation.soldephysi',raise_exception=True)
def solde(request):

    if request.method == 'POST':
        try:
            with transaction.atomic():
                obj = get_object_or_404(Affectation, pk=request.user)
                cai=Solde.objects.filter(id=request.POST.get('iddevise'))
                if cai:
                    if request.user.has_perm('operation.soldephysimodi'):

                        cai.update(
                            datemvt=request.POST.get('dt'),
                            deviseusd=request.POST.get('deviseusd'),
                            devisecfa=request.POST.get('devisecfa'),
                            devisecdf=request.POST.get('devisecdf'),
                            deviseeuro=request.POST.get('deviseeuro'),
                            user=request.user,

                        )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                else:
                    if request.user.has_perm('operation.soldephysiajout'):

                        Solde.objects.create(
                            datemvt=request.POST.get('dt'),
                            deviseusd=request.POST.get('deviseusd'),
                            devisecfa = request.POST.get('devisecfa'),
                            devisecdf = request.POST.get('devisecdf'),
                            deviseeuro = request.POST.get('deviseeuro'),
                            user=request.user,
                            zone_id=obj.zone.id,

                        )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

    return render(request,'operation/solde.html')




@login_required
@permission_required('operation.view_cloture',raise_exception=True)
def cloturee(request):

    if request.method == 'POST':
        try:
            with transaction.atomic():

                if request.user.has_perm('operation.add_cloture'):


                    obj = get_object_or_404(Affectation, pk=request.user)

                    if request.POST.get('operation')=="0":#cloture
                        c = cloture.objects.filter(zone_id=obj.zone.id, datemvt__gte=request.POST.get('dt'))
                        if c:
                            c.update(
                                etat=True
                            )
                        else:
                            return JsonResponse(
                                {"msg": "Opération non effectuée.La date n'existe pas",
                                 "id": "0"}, safe=False)
                    elif request.POST.get('operation')=="1":#ouverture
                            c = cloture.objects.filter(zone_id=obj.zone.id, datemvt__gte=request.POST.get('dt'))
                            if c:
                                return JsonResponse({"msg": "Opération non effectuée.La date doit être superieur aux date precedentes", "id": "0"}, safe=False)
                            else:
                                cloture.objects.create(
                                    datemvt=request.POST.get('dt'),
                                    zone_id=obj.zone.id,
                                    user=request.user,

                                )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p ", "id": "0"}, safe=False)


                else:
                    return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

    obj = get_object_or_404(Affectation, pk=request.user)
    c=cloture.objects.filter(zone_id=obj.zone.id,etat=False)
    if c:
        context = {
            'datecloture':c.last().datemvt,
            'operation':0
        }

    else:
        context = {
            'datecloture': datetime.date.today(),
            'operation': 1
        }



    return render(request,'operation/cloture.html',context)


@login_required
def regularisation(request):

    if request.method == 'POST':

        try:
            with transaction.atomic():

                Caisse.objects.create(
                        datemvt=request.POST.get('dt'),
                        refdoc=str("DOC_E")+str(str(datetime.datetime.today()).replace('-','').replace(' ','').replace(':','').replace('.','')),
                        montant=request.POST.get('montantentree'),
                        taux=str(request.POST.get('taux')).replace(",","."),
                        devise=request.POST.get('deviseentree'),
                        operation='E',
                        motif=request.POST.get('motif'),
                        departement_id=request.POST.get('location'),
                        location_id=request.POST.get('referentiel'),
                        user=request.user,

                    )

                Caisse.objects.create(
                    datemvt=request.POST.get('dt'),
                    refdoc=str("DOC_S") + str(
                        str(datetime.datetime.today()).replace('-', '').replace(' ', '').replace(':', '').replace('.',
                                                                                                                  '')),
                    montant=request.POST.get('montantsortie'),
                    taux=str(request.POST.get('taux')).replace(",", "."),
                    devise=request.POST.get('devisesortie'),
                    operation='S',
                    motif=request.POST.get('motif'),
                    departement_id=request.POST.get('location'),
                    location_id=request.POST.get('referentiel'),
                    user=request.user,

                )
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    context={
        "departements":Departement.objects.all().order_by('libelle'),
        "referentiels":Location.objects.all().order_by('libelle'),
        "tauxchange":Taux.objects.all().order_by('-id')[:1],
    }
    return render(request,'operation/regularisation.html',context)

@login_required
def listmvt(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    ct=clot(request,obj.zone.id)
    if ct == 1:
        return redirect(reverse('operation:home'))

    context = {
        "departements": Departement.objects.all().order_by('libelle'),
        "libelle": request.GET.get('libelle'),
        "catlibelle": request.GET.get('id'),
        "datemvt": ct,
        "referentiels": Location.objects.all().order_by('libelle')
    }


    return render(request,'operation/listmvt.html',context)

@login_required
@permission_required('operation.exportation',raise_exception=True)
def exportation(request):
    context = {
        "departements": Departement.objects.all().order_by('libelle'),
        "libelle": request.GET.get('libelle'),
        "catlibelle": request.GET.get('id'),
        "referentiels": Location.objects.all().order_by('libelle')
    }
    return render(request,'operation/exportation.html',context)




@login_required
# @permission_required('operation.categorie',raise_exception=True)
def service(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("service.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'local':'{}'.format(request.POST.get('local')),'caisse': '{}'.format(request.POST.get('caisse')),'service': request.POST.get('service'), 'dd': '{}'.format(request.POST.get('dtd')),
                        'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")
    context={'departement':Departement.objects.all().order_by('libelle')}



    if request.user.has_perm('operation.caissep'):
        context["zones"] = Zone.objects.all().order_by('libelle')
    else:
        try:
            obj = get_object_or_404(Affectation, pk=request.user)
            context["zones"] = Zone.objects.filter(id=obj.zone.id).order_by('libelle')
        except:
            context["zones"] = None
    return render(request, 'operation/service.html',context)


@login_required
def pdfetat(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("etatbesoin.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'besoin':request.POST.get('id')},
            locale='en_US'
        )

        return HttpResponse("true")


@login_required
def rapetatbesoinjus(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("etatfac.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            #,'besoin': '{}'.format(request.POST.get('bon'))
            parameters={'local': "Léon Hôtel",'dd': '{}'.format(request.POST.get('dtd')),
                        'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")

@login_required
def synthese(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("synthese.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'local':'{}'.format(request.POST.get('local')),'caisse': '{}'.format(request.POST.get('caisse')),'dd': '{}'.format(request.POST.get('dtd')),
                        'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")
    context={'departement':Departement.objects.all().order_by('libelle')}

    if request.user.has_perm('operation.caissep'):
        context["zones"] = Zone.objects.all().order_by('libelle')
    else:
        try:
            obj = get_object_or_404(Affectation, pk=request.user)
            context["zones"] = Zone.objects.filter(id=obj.zone.id).order_by('libelle')
        except:
            context["zones"] = None
    return render(request, 'operation/synthese.html',context)

@login_required
def rap(request):

    if request.method=='POST':

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("caisse.jrxml")
       

       
        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")
        
        
        output =fn+"\media"
        
        con = {
           'driver': 'generic',
        'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
        'jdbc_url':'jdbc:jtds:sqlserver://localhost/CAISSE',
        'jdbc_dir':fn,
        'username': 'sa',
        'password': 'dev'
        }
        
        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'local':'{}'.format(request.POST.get('local')),'caisse': '{}'.format(request.POST.get('zone')),'devise':request.POST.get('caisse'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")

    context = {}

    if request.user.has_perm('operation.caissep'):
        context["zones"] = Zone.objects.all().order_by('libelle')
    else:
        try:
            obj = get_object_or_404(Affectation, pk=request.user)
            context["zones"] = Zone.objects.filter(id=obj.zone.id).order_by('libelle')
        except:
            context["zones"] = None
    return render(request,'operation/rap.html',context)


@login_required
def rapgen(request):

    if request.method=='POST':

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("caissegen.jrxml")
       

       
        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")
        
        
        output =fn+"\media"
        
        con = {
           'driver': 'generic',
        'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
        'jdbc_url':'jdbc:jtds:sqlserver://localhost/CAISSE',
        'jdbc_dir':fn,
        'username': 'sa',
        'password': 'dev'
        }
        
        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'local':'{}'.format(request.POST.get('local')),'caisse': '{}'.format(request.POST.get('caisse')),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")

    context={}

    if request.user.has_perm('operation.caissep'):
        context["zones"]=Zone.objects.all().order_by('libelle')
    else:
        try:
            obj = get_object_or_404(Affectation, pk=request.user)
            context["zones"]=Zone.objects.filter(id=obj.zone.id).order_by('libelle')
        except:
            context["zones"]=None


    return render(request,'operation/rapgen.html',context)


@login_required
def rapgenfou(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("caissegenfou.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'local':'{}'.format(request.POST.get('local')),'caisse': '{}'.format(request.POST.get('caisse')),'txt': request.POST.get('txt'), 'dd': '{}'.format(request.POST.get('dtd')),
                        'df': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )

        return HttpResponse("true")

    context = {}

    if request.user.has_perm('operation.caissep'):
        context["zones"] = Zone.objects.all().order_by('libelle')
    else:
        try:
            obj = get_object_or_404(Affectation, pk=request.user)
            context["zones"] = Zone.objects.filter(id=obj.zone.id).order_by('libelle')
        except:
            context["zones"] = None
    return render(request, 'operation/rapgenfou.html',context)


@login_required
def raplistbesoin(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if str(request.POST.get('location')).strip() == '' and str(request.POST.get('departement')).strip() == '':
            input_file = fn + "\{}".format("listetatbesoinfull.jrxml")
        else:
            input_file = fn + "\{}".format("listetatbesoin.jrxml")
        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        if str(request.POST.get('location')).strip() == '' and str(request.POST.get('departement')).strip() == '':
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'dtd': '{}'.format(request.POST.get('dtd')),
                            'dtf': '{}'.format(request.POST.get('dtf'))},
                locale='en_US'
            )
            return HttpResponse("2")
        else:
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'location': '{}'.format(request.POST.get('location')),
                            'departement': '{}'.format(request.POST.get('departement')),
                            'dtd': '{}'.format(request.POST.get('dtd')),
                            'dtf': '{}'.format(request.POST.get('dtf'))},
                locale='en_US'
            )


            return HttpResponse("1")

    context = {}
    context["departements"] = Departement.objects.all().order_by('libelle')
    context["referentiels"] = Location.objects.all().order_by('libelle')

    return render(request, 'operation/raplistbesoin.html',context)


@login_required
def raplistentree(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if str(request.POST.get('location')).strip()=='' and str(request.POST.get('departement')).strip()=='':
            input_file = fn + "\{}".format("listentreefull.jrxml")
        else:
            input_file = fn + "\{}".format("listentree.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")


        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        if str(request.POST.get('location')).strip()=='' and str(request.POST.get('departement')).strip()=='':
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'dtd': '{}'.format(request.POST.get('dtd')),
                            'dtf': '{}'.format(request.POST.get('dtf'))},
                locale='en_US'
            )
            return HttpResponse("2")
        else:
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'location': '{}'.format(request.POST.get('location')),
                            'departement': '{}'.format(request.POST.get('departement')),
                            'dtd': '{}'.format(request.POST.get('dtd')),
                            'dtf': '{}'.format(request.POST.get('dtf'))},
                locale='en_US'
            )


            return HttpResponse("1")

    context = {}
    context["departements"] = Departement.objects.all().order_by('libelle')
    context["referentiels"] = Location.objects.all().order_by('libelle')

    return render(request, 'operation/raplistentree.html',context)


@login_required
def raplistbonvalide(request):
    if request.method == 'POST':
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file=""
        if request.POST.get('id')=="1":
            if request.POST.get('service') == "":
                input_file = fn + "\{}".format("listbonvalide.jrxml")
            else:
                input_file = fn + "\{}".format("listbonvalideservice.jrxml")

        elif request.POST.get('id')=="2":
            if request.POST.get('service') == "":
                input_file = fn + "\{}".format("listbonservicefull.jrxml")
            else:
                input_file = fn + "\{}".format("listbonservice.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:jtds:sqlserver://localhost/CAISSE',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        if request.POST.get('id') == "1":
            if request.POST.get('service') == "":
                jasper.process(
                    input_file,
                    output,
                    format_list=["pdf"],
                    db_connection=con,
                    parameters={'local': 'LH', 'dd': '{}'.format(request.POST.get('dtd')),
                                'df': '{}'.format(request.POST.get('dtf'))},
                    locale='en_US')
            else:
                jasper.process(
                    input_file,
                    output,
                    format_list=["pdf"],
                    db_connection=con,
                    parameters={'local': 'LH', 'departement': '{}'.format(request.POST.get('service')), 'dd': '{}'.format(request.POST.get('dtd')),
                                'df': '{}'.format(request.POST.get('dtf'))},
                    locale='en_US')

        elif request.POST.get('id') == "2":
            if request.POST.get('service') == "":
                jasper.process(
                    input_file,
                    output,
                    format_list=["pdf"],
                    db_connection=con,
                    parameters={'local': 'LH', 'dd': '{}'.format(request.POST.get('dtd')),
                                'df': '{}'.format(request.POST.get('dtf'))},
                    locale='en_US')
            else:
                jasper.process(
                    input_file,
                    output,
                    format_list=["pdf"],
                    db_connection=con,
                    parameters={'local': 'LH', 'departement': '{}'.format(request.POST.get('service')),
                                'dd': '{}'.format(request.POST.get('dtd')),
                                'df': '{}'.format(request.POST.get('dtf'))},
                    locale='en_US')


        return HttpResponse("true")

    context={
        'services':Departement.objects.all()
    }
    return render(request, 'operation/raplistbonvalide.html',context)


##########################################################entree

@login_required
@permission_required('operation.exportation',raise_exception=True)
def getmvtcompta(request):
    item=Caisse.objects.filter(datemvt__date=request.GET.get('id')).values("id","datemvt__date","montant","refdoc","taux","devise","motif","location_id","location__libelle","location__compte","departement_id","departement__libelle","user__username")
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def getmvt(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    item=Caisse.objects.filter(operation=request.GET.get('cat'),datemvt__date=request.GET.get('id'),zone_id=obj.zone.id).values("id","datemvt__date","montant","refdoc","taux","devise","motif","location_id","location__libelle","location__compte","departement_id","departement__libelle","user__username")
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getmvtnormal(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    item=Caisse.objects.filter(operation=request.GET.get('cat'),zone_id=obj.zone.id).values("id","datemvt__date","montant","refdoc","taux","devise","motif","location_id","location__libelle","location__compte","departement_id","departement__libelle","user__username").order_by('-id')[:5]
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)


@login_required
@permission_required('operation.soldephysi',raise_exception=True)
def getsolde(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    item=Solde.objects.filter(zone_id=obj.zone.id).values("id","datemvt__date","deviseusd","devisecfa","id","devisecdf","deviseeuro").order_by('-id')
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)

##########################################################sortie
@login_required
def sortie(request):

    if request.method == 'POST':

        try:
            with transaction.atomic():

                cai=Caisse.objects.filter(id=request.POST.get('idmvt'))
                if cai:

                    cai.update(
                        datemvt=request.POST.get('dt'),
                        montant=request.POST.get('mtn'),
                        taux=str(request.POST.get('taux')).replace(",","."),
                        devise=request.POST.get('devise'),
                        motif=request.POST.get('motif'),
                        operation=request.POST.get('operation'),
                        departement_id=request.POST.get('location'),
                        location_id=request.POST.get('referentiel'),

                    )
                else:
                    Caisse.objects.create(
                        datemvt=request.POST.get('dt'),
                        refdoc=str("DOC_S")+str(str(datetime.datetime.today()).replace('-','').replace(' ','').replace(':','').replace('.','')),
                        montant=request.POST.get('mtn'),
                        operation=request.POST.get('operation'),
                        taux=str(request.POST.get('taux')).replace(",","."),
                        devise=request.POST.get('devise'),
                        motif=request.POST.get('motif'),
                        departement_id=request.POST.get('location'),
                        location_id=request.POST.get('referentiel'),
                        user=request.user,

                    )
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    context={
        "departements":Departement.objects.all().order_by('libelle'),
        "referentiels":Location.objects.all().order_by('libelle'),
        "tauxchange":Taux.objects.all().order_by('-id')[:1],
    }
    return render(request,'operation/sortie.html',context)

@login_required
def listsortie(request):
    context = {
        "departements": Departement.objects.all().order_by('libelle'),
        "libelle": "Dépenses",
        "catlibelle": "S",
        "referentiels": Location.objects.all().order_by('libelle')
    }
    return render(request,'operation/listmvt.html',context)

##########################################################sortie

@login_required
#@permission_required('operation.categorie',raise_exception=True)
def getcategorie(request):
    item=Location.objects.all().values("id","libelle","compte","typemvt")
    rec = list(item)
    return JsonResponse({'data': rec}, safe=False)

@login_required
@require_POST
#@permission_required('operation.categorie',raise_exception=True)
def deletecategorie(request):
    try:
        with transaction.atomic():
            item=Location.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

@login_required
@require_POST
def deletemvt(request):
    obj = get_object_or_404(Affectation, pk=request.user)
    try:
        with transaction.atomic():
            if request.POST.get('operation') == 'E':
                if request.user.has_perm('operation.entreesup'):
                    pass
                else:
                    return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)

            elif request.POST.get('operation') == 'S':
                if request.user.has_perm('operation.sortiesup'):
                    pass
                else:
                    return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
            item = Caisse.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


@login_required
@require_POST
@permission_required('operation.soldephysisup',raise_exception=True)
def deletesolde(request):
    try:
        with transaction.atomic():
            item = Solde.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


@login_required
@require_POST
@permission_required('operation.delete_factureetatbesoin',raise_exception=True)
def deletefacturebesoin(request):
    try:
        with transaction.atomic():
            item = FactureEtatBesoin.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

@login_required
#@permission_required('operation.categorie',raise_exception=True)
def categorie(request):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                if 'idcat' in request.POST and request.POST.get('idcat')!='':
                    cai=Location.objects.filter(id=request.POST.get('idcat'))
                    if cai:

                        cai.update(
                            libelle=request.POST.get('libelle2'),
                            #typemvt=request.POST.get('categorie2'),
                            compte=request.POST.get('compte2'),

                        )
                        return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
                    else:
                        return JsonResponse({"msg": "Opération non effectuée. Ligne inexistante", "id": "0"}, safe=False)

                else:
                    l=Location.objects.create(
                        libelle=request.POST.get('libelle'),
                        compte=request.POST.get('compte'),
                        #typemvt=request.POST.get('categorie'),

                    )
                return JsonResponse({"msg": "Opération effectuée", "id": "1","idloc":l.id}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)
    return render(request,'operation/categorie.html')





###########################################""etat besoins





