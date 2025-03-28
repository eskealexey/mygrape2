# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from accounts.models import CustomUser
from dung.models import JornalDung, Dung
from django.views.decorators.csrf import csrf_protect

from preparats.models import JornalPreparat, Preparats


# Create your views here.
@login_required
def jornal_dung_list(request, name):
    us = CustomUser.objects.get(username=name)
    jornal_dung = JornalDung.objects.all().filter(userid=us.id)
    if request.method == 'POST':
        ids = request.POST['jornal_id']
        quantity = JornalDung.objects.get(id=ids).quantity
        total = accounting_(request, quantity)
        JornalDung.objects.filter(id=ids).update(quantity=total)
    context = {
        "jornal_dung" : jornal_dung,
        "title" : "Учет удобрений",
    }
    return render(request, 'record/jornal_dung_list.html', context=context)


@login_required
def accounting_(request: HttpRequest, quantity: int = 0)-> type:
    """Учет удобрений"""
    amount = request.POST['amount']
    activ = request.POST['activ']
    if activ == '+':
        quantity += int(amount)
    else:
        quantity -= int(amount)
        if quantity < 0:
            quantity = 0
    return quantity


@login_required
@csrf_protect
def jornal_dung_add(request, name):
    """Добавление записи"""
    dungs = Dung.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        dung_spr = request.POST.get('dung_spr')
        dung = request.POST.get('dung')
        alias = request.POST.get('alias')
        quantity = int(request.POST.get('quantity'))
        user = CustomUser.objects.get(id=request.user.id)
        if dung_spr == '-':
            namedung = dung
        else:
            namedung = dung_spr
        JornalDung.objects.create(name=namedung, alias=alias, userid=user, quantity=quantity)
        return redirect("jornal_dung_list", name=username)

    context = {
        "title" : "Добавление записи",
        "dungs" : dungs,
    }
    return render(request, 'record/jornal_dung_add.html', context=context)


@login_required
@csrf_protect
def jornal_dung_edit(request, name, id):
    """Редактирование записи"""
    dungs = Dung.objects.all()
    jornal_dung = JornalDung.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        dung_spr = request.POST.get('dung_spr')
        dung = request.POST.get('dung')
        alias = request.POST.get('alias')
        quantity = int(request.POST.get('quantity'))
        if dung_spr == '-':
            namedung = dung
        else:
            namedung = dung_spr
        jornal_dung.name = namedung
        jornal_dung.alias = alias
        jornal_dung.quantity = quantity
        jornal_dung.save()
        return redirect("jornal_dung_list", name=username)
    context = {
        "title": "Редактирование записи",
        "dungs": dungs,
        "jornal_dung": jornal_dung,
    }
    return render(request, 'record/jornal_dung_edit.html', context=context)


@login_required
@csrf_protect
def jornal_dung_delete(request, name, id):
    """Удаление записи"""
    jornal_dung = JornalDung.objects.get(id=id)
    jornal_dung.delete()
    return redirect("jornal_dung_list", name=name)


def jornal_preparat_list(request, name):
    us = CustomUser.objects.get(username=name)
    jornal_preparat = JornalPreparat.objects.all().filter(userid=us.id)
    if request.method == 'POST':
        ids = request.POST['jornal_id']
        quantity = JornalPreparat.objects.get(id=ids).quantity
        total = accounting_(request, quantity)
        JornalPreparat.objects.filter(id=ids).update(quantity=total)
    context = {
        "jornal_preparat" : jornal_preparat,
        "title" : "Учет препаратов",
    }
    return render(request, 'record/jornal_preparat_list.html', context=context)


@csrf_protect
def jornal_peparat_add(request, name):
    """Добавление записи"""
    preparats = Preparats.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        preparat_spr = request.POST.get('preparat_spr')
        preparat = request.POST.get('preparat')
        alias = request.POST.get('alias')
        quantity = int(request.POST.get('quantity'))
        user = CustomUser.objects.get(id=request.user.id)
        if preparat_spr == '-':
            namepreparat = preparat
        else:
            namepreparat = preparat_spr
        JornalPreparat.objects.create(name=namepreparat, alias=alias, userid=user, quantity=quantity)
        return redirect("jornal_preparat_list", name=username)

    context = {
        "title" : "Добавление записи",
        "preparats" : preparats,
    }
    return render(request, 'record/jornal_preparat_add.html', context=context)


@csrf_protect
def jornal_preparat_delete(request, name, id):
    """Удаление записи"""
    jornal_preparat = JornalPreparat.objects.get(id=id)
    jornal_preparat.delete()
    return redirect("jornal_preparat_list", name=name)



@csrf_protect
def jornal_peparat_edit(request, name, id):
    """Добавление записи"""
    preparats = Preparats.objects.all()
    jornal_preparat = JornalPreparat.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        preparat_spr = request.POST.get('preparat_spr')
        preparat = request.POST.get('preparat')
        alias = request.POST.get('alias')
        quantity = int(request.POST.get('quantity'))
        user = User.objects.get(id=request.user.id)
        if preparat_spr == '-':
            namepreparat = preparat
        else:
            namepreparat = preparat_spr
        jornal_preparat.name = namepreparat
        jornal_preparat.alias = alias
        jornal_preparat.quantity = quantity
        jornal_preparat.save()

        return redirect("jornal_preparat_list", name=username)

    context = {
        "title" : "Добавление записи",
        "preparats" : preparats,
        "jornal_preparat" : jornal_preparat,
    }
    return render(request, 'record/jornal_preparat_edit.html', context=context)
