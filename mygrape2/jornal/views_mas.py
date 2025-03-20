"""Views for mas"""
from django.shortcuts import render, redirect

from dung.models import Dung
from preparats.models import Preparats
from .models import Location, GreenOper, Feeding, Processing


def mas_greenoper(request):
    """
       Добавление зеленые операции массово
   """
    places = Location.objects.all().filter(userid=request.user.id)

    if request.method == 'POST':
        place_id = request.POST.getlist('locationid')
        date_add = request.POST['date_add']
        description = request.POST['description']
        for i in place_id:
            location = Location.objects.get(id=int(i))
            GreenOper.objects.create(description=description, date_add=date_add, locationid=location).save()
        return redirect('index_jornal')
    else:
        context = {
            "title": "Зеленные операции массово",
            "places": places,
        }
        return render(request, 'jornal/mas/green.html', context=context)


def mas_feeding(request,):
    """
       Добавление подкормок массово
   """
    places = Location.objects.all().filter(userid=request.user.id)
    dungs = Dung.objects.all()
    if request.method == 'POST':
        place_id= request.POST.getlist('locationid')
        dung_id = request.POST.getlist('dung_id')
        dung_ = request.POST['dung_']
        date_add = request.POST['date_add']
        description = request.POST['description']
        for i in place_id:
            location = Location.objects.get(id=i)
            feeding = Feeding.objects.create(locationid=location, description=description, date_add=date_add, dung=dung_)
            for j in dung_id:
                dung = Dung.objects.get(id=j)
                feeding.dung_id.add(dung)
        return redirect('index_jornal')
    context = {
        "title": "Подкормки массово",
        "places": places,
        "dungs": dungs,
    }
    return render(request, 'jornal/mas/feed.html', context=context)


def mas_processing(request,):
    """
       Добавление обработок массово
   """
    places = Location.objects.all().filter(userid=request.user.id)
    preparats = Preparats.objects.all()
    if request.method == 'POST':
        place_id= request.POST.getlist('locationid')
        preparat_id = request.POST.getlist('preparat_id')
        preparat_ = request.POST['preparat']
        date_add = request.POST['date_add']
        description = request.POST['description']
        for i in place_id:
            location = Location.objects.get(id=i)
            processing = Processing.objects.create(locationid=location, description=description, date_add=date_add, preparat=preparat_)
            for j in preparat_id:
                preparat = Preparats.objects.get(id=j)
                processing.preparat_id.add(preparat)
        return redirect('index_jornal')

    context = {
        "title": "Обработки массово",
        "places": places,
        "preparats": preparats,
    }
    return render(request, 'jornal/mas/proces.html', context=context)