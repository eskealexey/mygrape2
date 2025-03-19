from django.shortcuts import render

from .models import Preparats
from sickpest.models import SickPest, SickPestImage

# Create your views here.
def preparat_all(request):
    data = Preparats.objects.all().order_by('name')
    context = {
        'title': 'Препараты',
        'data': data,
    }
    return render(request, 'preparats/preparat_list.html', context=context)

def preparat_detail(request, pk):
    data = Preparats.objects.get(pk=pk)
    context = {
        'title': data.name,
        'data': data,
    }


    return render(request, 'preparats/preparat_detail.html', context=context)