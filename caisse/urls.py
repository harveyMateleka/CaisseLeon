"""caisse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path, include, reverse
from django.views.decorators.http import require_POST
from operation.models import Superviseur,EtatBesoin,DetailEtatBesoin,Signature,Delai
import datetime
from operation.utils import AESCipher
from licences import views
#@group_required('Simple')
def check(request):

    if request.user.username:
         return redirect(reverse('operation:home'))
    if request.method=='GET':
        return render(request, 'login.html')
    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        #affectation

        #affectation
        login(request, user)
        # if not request.user.is_superuser:
        #     if request.user.has_perm("caisse.superviseur"):
        #         pass
        #     else:
        #         pass
        #
        # elif
        return redirect(reverse('operation:home'))
    else:
        return redirect(reverse('check'))

def uncheck(request):
    logout(request)
    return redirect(reverse('check'))


@login_required
def etatbesoin(request):

    if request.method == 'POST':
        try:
            with transaction.atomic():
                #controleeeeeeeeeeeeeeeeeeeeeeeee
                u=Signature.objects.filter(user=request.user).order_by('-id')
                if u:
                    u=u.first()
                    alld=Signature.objects.filter(etat=False).order_by('-id')

                    if alld:
                        alld = alld.first()
                        if u.user == alld.user:
                            pass
                        else:
                            return JsonResponse(
                                {
                                    "msg": "Désolé !!!.L'heure limite de faire l'etat de besoin est expirée.Veuillez contacter le financier",
                                    "id": "0"},
                                safe=False)
                    else:
                        return JsonResponse(
                            {
                                "msg": "Désolé !!!.L'heure limite de faire l'etat de besoin est expirée.Veuillez contacter le financier",
                                "id": "0"},
                            safe=False)

                else:
                    now = datetime.datetime.now()
                    current_time = now.time()
                    d=Delai.objects.all().order_by("-id")[:1]
                    if d:
                        elapsed=0
                        h=''
                        for i in d:
                            h=i.heure
                            if i.heure >= current_time:
                                elapsed = 1
                            else:
                                elapsed = 0
                            break

                        if elapsed==0:
                            return JsonResponse(
                            {"msg": "Désolé !!!.L'heure limite de faire l'etat de besoin est " + str(h)+".Veuillez contacter le financier","id": "0"},
                            safe=False)
                    else:
                        return JsonResponse({"msg": "Erreur !!!.L'heure limite n'est pas défini","id": "0"}, safe=False)
                #controleeeeeeeeeeeeeeeeeeeeeeeee

                b=EtatBesoin.objects.filter(id=request.POST.get('idmvt'))
                if b:

                    b.update(
                        datemvt=request.POST.get('dt'),
                        devise=request.POST.get('devise'),
                        demandeur=request.POST.get('demandeur'),
                        motif=str(request.POST.get('motif')).upper()
                    )
                    #delete
                    DetailEtatBesoin.objects.filter(etatbesoin_id=request.POST.get('idmvt')).delete()
                    # delete
                    for item, qte, prix in zip(request.POST.getlist('item'), request.POST.getlist('qte'),
                                               request.POST.getlist('prix')):
                        DetailEtatBesoin.objects.create(
                            prix=prix,
                            qte=qte,
                            item=item,
                            etatbesoin_id=request.POST.get('idmvt')
                        )
                    return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
                else:
                    if request.user.username:
                        et = EtatBesoin.objects.create(
                            datemvt=request.POST.get('dt'),
                            demandeur=request.POST.get('demandeur'),
                            motif=str(request.POST.get('motif')).upper(),
                            devise=request.POST.get('devise'),
                            etat='A',
                            superviseur_id=request.POST.get('superviseur'),
                        )
                    else:

                        et=EtatBesoin.objects.create(
                            datemvt=request.POST.get('dt'),
                            demandeur=request.POST.get('demandeur'),
                            motif=str(request.POST.get('motif')).upper(),
                            devise=request.POST.get('devise'),
                            etat='A',
                            superviseur_id=request.POST.get('superviseur'),
                        )
                    for item, qte, prix in zip(request.POST.getlist('item'), request.POST.getlist('qte'),
                                               request.POST.getlist('prix')):
                        DetailEtatBesoin.objects.create(
                            prix=prix,
                            qte=qte,
                            item=item,
                            etatbesoin=et
                        )
                    return JsonResponse({"msg": "Opération effectuée", "id": "1","idetat":et.id}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


    context={
        #'dt':str(datetime.date.today()+ datetime.timedelta(days=1)),
        'dt':str(datetime.date.today()),
    }
    if request.user.username:
        context['departements']=Superviseur.objects.filter(user=request.user).order_by('departement__libelle')
    else:
        context['departements']=Superviseur.objects.all().order_by('departement__libelle')

    return render(request, 'etatbesoin.html',context)



@login_required
def profil(request):

    if request.method == 'POST':

        if request.user.is_authenticated:
            if request.POST.get("password") == request.POST.get("confirmpass"):
                userdata = User.objects.get(id=request.user.id)
                userdata.username = request.POST.get("nom")
                userdata.last_name = request.POST.get("noml")
                userdata.first_name = request.POST.get("prenom")
                userdata.email = request.POST.get("email")
                userdata.password = make_password(request.POST.get("password"))
                userdata.save()
                logout(request)
                return JsonResponse({'id': "1", "msg": "Opération effectuée"}, safe=False)
        return JsonResponse({'id': "0", "msg": "Opération non effectuée"}, safe=False)

    return render(request,'profil.html')


@login_required
@permission_required('operation.validation',raise_exception=True)
def validation(request):

    if request.method == 'POST':
        aes = AESCipher(settings.SECRET_KEY[:16], 32)
        s=Signature.objects.filter(user=request.user,etat=False)
        if s:
            s=s.first()
            a = aes.decrypt(s.txt)
            b=str(a).split("_caisse_")[0]
            dt = datetime.datetime.fromisoformat(str(a).split("_caisse_")[1])

            if s.delai.replace(tzinfo=None) > datetime.datetime.now() and dt > datetime.datetime.now():

                if b==request.POST.get('pass'):
                    return JsonResponse({'val':"true"},safe=False)
                else:
                    return JsonResponse({'val':"false",'msg':"Le Pass est incorrect"},safe=False)
            else:
                s.etat=True
                s.save()
                return JsonResponse({'val':"false",'msg':"Le délai a expiré.Veuillez changer le délai dans l'onglet << Signature >> partie de l'administration"},safe=False)
        else:
            return JsonResponse({'val':"false",'msg':"L'access Interdit!!!"},safe=False)


    #print(datetime.datetime.now())
    return render(request,'validation.html')


@login_required
@permission_required('operation.validation',raise_exception=True)
def validationfull(request):

    if request.method == 'POST':
        aes = AESCipher(settings.SECRET_KEY[:16], 32)
        s=Signature.objects.filter(user=request.user,etat=False)
        if s:
            s=s.first()
            a = aes.decrypt(s.txt)
            b=str(a).split("_caisse_")[0]
            dt = datetime.datetime.fromisoformat(str(a).split("_caisse_")[1])

            if s.delai.replace(tzinfo=None) > datetime.datetime.now() and dt > datetime.datetime.now():

                if b==request.POST.get('pass'):
                    return JsonResponse({'val':"true"},safe=False)
                else:
                    return JsonResponse({'val':"false",'msg':"Le Pass est incorrect"},safe=False)
            else:
                s.etat=True
                s.save()
                return JsonResponse({'val':"false",'msg':"Le délai a expiré.Veuillez changer le délai dans l'onglet << Signature >> partie de l'administration"},safe=False)
        else:
            return JsonResponse({'val':"false",'msg':"L'access Interdit!!!"},safe=False)


    #print(datetime.datetime.now())
    return render(request,'validationfull.html')


@login_required
@permission_required('operation.superviseur',raise_exception=True)
def superviseur(request):
    context={
        "etatbesoin":EtatBesoin.objects.filter(superviseur__user=request.user).order_by('-id'),
    }
    return render(request,'superviseur.html',context)


@login_required
@permission_required('operation.superviseur',raise_exception=True)
def getsuperviseur(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin_id=request.GET.get('id')).order_by('-id')
    txt=""
    for i in item:
        txt+=f"""
        <tr class="item-row">
                             <td><div class="delete-btn"><input type="text" required class="form-control item text-uppercase" value="{i.item}" placeholder="Ecrivez le nom de l'article" type="text">{'<a class="delete" tabindex="-3" href="javascript:;" title="Supprimer la ligne">X</a>' if i.etatbesoin.etat == 'N' else ''}</div></td>
                             <td><input class="form-control qty" placeholder="Qte" required type="number" value={i.qte}></td>
                             <td><input class="form-control price" placeholder="Prix" required type="number" value={i.prix}></td>
                             <td><span class="total">{i.qte*i.prix}</span></td>
                         </tr>
        """
    #rec = list(item)
    return JsonResponse(txt, safe=False)


@login_required
@permission_required('operation.validation',raise_exception=True)
def getvalidation(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin_id=request.GET.get('id'),etatbesoin__etat='A').order_by('-id')
    txt=""
    for i in item:
        txt+=f"""
        <tr class="item-row">
                             <td><div class="delete-btn"><input type="text" required class="form-control item text-uppercase" value="{i.item}" placeholder="Ecrivez le nom de l'article" type="text"><a class="delete" tabindex="-3" href="javascript:;" title="Supprimer la ligne">X</a></div></td>
                             <td><input class="form-control qty" placeholder="Qte" required type="number" value={i.qte}></td>
                             <td><input class="form-control price" placeholder="Prix" required type="number" value={i.prix}></td>
                             <td><span class="total">{i.qte*i.prix}</span></td>
                         </tr>
        """

    #rec = list(item)
    return JsonResponse(txt, safe=False)



@login_required
@permission_required('operation.validation',raise_exception=True)
def getvalidationTot(request):
    listsomme = []
    listdevise = ["USD", "CDF", "EURO", "CFA"]
    for i in range(4):
        c = DetailEtatBesoin.objects.filter(etatbesoin__devise=listdevise[i], etatbesoin__etat='A').aggregate(
            multitot=Sum(F("prix") * F("qte"))).get('multitot')
        if c is None:
            c = 0
        listsomme.append(c)
    return JsonResponse({'totusd': listsomme[0],'totcdf': listsomme[1],'toteuro': listsomme[2],'totcfa': listsomme[3]},safe=False)


@login_required
@require_POST
@permission_required('operation.superviseur',raise_exception=True)
def deleteetat(request):
    try:
        with transaction.atomic():
            DetailEtatBesoin.objects.filter(etatbesoin_id=request.POST.get('id')).delete()
            EtatBesoin.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

@login_required
@require_POST
@permission_required('operation.validation',raise_exception=True)
def deletevalidation(request):
    try:
        with transaction.atomic():
            s = Signature.objects.filter(user=request.user, etat=False)
            if s:
                aes = AESCipher(settings.SECRET_KEY[:16], 32)
                s = s.first()
                a = aes.decrypt(s.txt)
                dt = datetime.datetime.fromisoformat(str(a).split("_caisse_")[1])

                if s.delai.replace(tzinfo=None) > datetime.datetime.now() and dt > datetime.datetime.now():
                    #EtatBesoin.objects.filter(id=request.POST.get('id')).update(etat='C', userAdmi=request.user)
                    EtatBesoin.objects.filter(id=request.POST.get('id')).update(etat='R')
                    return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
                else:
                    s.etat = True
                    s.save()
                    return JsonResponse({"id": "0",
                                         'msg': "Le délai a expiré.Veuillez changer le délai dans l'onglet << Signature >> partie de l'administration"},
                                        safe=False)
            else:
                return JsonResponse({"id": "0", 'msg': "L'access Interdit!!!"}, safe=False)
            #
            #return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)

@login_required
@require_POST
@permission_required('operation.superviseur',raise_exception=True)
def sendetat(request):
    try:
        with transaction.atomic():
            EtatBesoin.objects.filter(id=request.POST.get('id')).update(etat='A')
            return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


@login_required
@require_POST
@permission_required('operation.validation',raise_exception=True)
def sendvalidationfull(request):
    try:
        with transaction.atomic():

            #####################################################
            #####################################################
            s = Signature.objects.filter(user=request.user, etat=False)
            if s:
                aes = AESCipher(settings.SECRET_KEY[:16], 32)
                s = s.first()
                a = aes.decrypt(s.txt)
                dt = datetime.datetime.fromisoformat(str(a).split("_caisse_")[1])

                #print(s.delai.replace(tzinfo=None),datetime.datetime.now(''),dt,datetime.datetime.now())
                if s.delai.replace(tzinfo=None) > datetime.datetime.now() and dt > datetime.datetime.now():

                    EtatBesoin.objects.filter(id=request.POST.get('id')).update(etat='A', userAdmi=request.user)
                    return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
                else:

                    s.etat = True
                    s.save()
                    return JsonResponse({"id": "0",
                                         'msg': "Le délai a expiré.Veuillez changer le délai dans l'onglet << Signature >> partie de l'administration"},
                                        safe=False)
            else:
                return JsonResponse({"id": "0", 'msg': "L'access Interdit!!!"}, safe=False)

    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


@login_required
@require_POST
@permission_required('operation.validation',raise_exception=True)
def sendvalidation(request):
    try:
        with transaction.atomic():

            #####################################################
            #####################################################
            s = Signature.objects.filter(user=request.user, etat=False)
            if s:
                aes = AESCipher(settings.SECRET_KEY[:16], 32)
                s = s.first()
                a = aes.decrypt(s.txt)
                dt = datetime.datetime.fromisoformat(str(a).split("_caisse_")[1])

                #print(s.delai.replace(tzinfo=None),datetime.datetime.now(''),dt,datetime.datetime.now())
                if s.delai.replace(tzinfo=None) > datetime.datetime.now() and dt > datetime.datetime.now():
                    EtatBesoin.objects.filter(id=request.POST.get('id')).update(etat='C', userAdmi=request.user)
                    return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
                else:

                    s.etat = True
                    s.save()
                    return JsonResponse({"id": "0",
                                         'msg': "Le délai a expiré.Veuillez changer le délai dans l'onglet << Signature >> partie de l'administration"},
                                        safe=False)
            else:
                return JsonResponse({"id": "0", 'msg': "L'access Interdit!!!"}, safe=False)

    except Exception as e:
        return JsonResponse({"msg": "Erreur !!!.Recommencez s.v.p " + str(e), "id": "0"}, safe=False)


@login_required
@permission_required('operation.superviseur',raise_exception=True)
def getbesoin(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin__superviseur__user=request.user).values("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__etat").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__etat")
    #item=DetailEtatBesoin.objects.filter(etatbesoin__superviseur__user=request.user,etatbesoin__etat__in=('N','R')).values("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__etat").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__etat")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)


@login_required
@permission_required('operation.validation',raise_exception=True)
def getbesoinvalidation(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin__etat='A').values("etatbesoin__superviseur__user__imageuser__imagebs","etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)

@login_required
@permission_required('operation.validation',raise_exception=True)
def getbesoinvalidationfull(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin__etat__in=('R','C')).values("etatbesoin__etat","etatbesoin__superviseur__user__imageuser__imagebs","etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)


@login_required
@permission_required('operation.sortie',raise_exception=True)
def getbesoincaisse(request):
    item=DetailEtatBesoin.objects.filter(etatbesoin__etat='C',etatbesoin__datemvt=datetime.date.today()).values("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle","etatbesoin__superviseur__departement__id").annotate(multitot=Sum(F("prix") * F("qte"))).order_by("etatbesoin__id","etatbesoin__datemvt","etatbesoin__demandeur","etatbesoin__motif","etatbesoin__devise","etatbesoin__superviseur__departement__libelle","etatbesoin__superviseur__departement__id")
    rec = list(item)
    return JsonResponse({"data":rec}, safe=False)

urlpatterns = [  
    path('admin/', admin.site.urls),
    path('', check, name="check"),
    path('etatbesoin/', etatbesoin,name='etatbesoin'),
    path('profil/', profil,name='profil'),
    path('superviseur/', superviseur,name='superviseur'),
    path('validation/', validation,name='validation'),
    path('validationfull/', validationfull,name='validationfull'),
    path('getbesoinvalidation/', getbesoinvalidation,name='getbesoinvalidation'),
    path('getbesoinvalidationfull/', getbesoinvalidationfull,name='getbesoinvalidationfull'),
    path('getbesoincaisse/', getbesoincaisse,name='getbesoincaisse'),
    path('getsuperviseur/', getsuperviseur,name='getsuperviseur'),
    path('getvalidation/', getvalidation,name='getvalidation'),
    path('getvalidationTot/', getvalidationTot,name='getvalidationTot'),
    path('getbesoin/', getbesoin,name='getbesoin'),
    path('sendetat/', sendetat,name='sendetat'),
    path('sendvalidation/', sendvalidation,name='sendvalidation'),
    path('sendvalidationfull/', sendvalidationfull,name='sendvalidationfull'),
    path('uncheck/', uncheck, name="uncheck"),
    path('deleteetat/', deleteetat, name='deleteetat'),
    path('deletevalidation/', deletevalidation, name='deletevalidation'),
    path('operation/', include('operation.urls'), name='operation'),
    path('licences/', include('licences.urls'), name='licences'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)