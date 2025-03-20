from django.shortcuts import render

from .models import Dung
# Create your views here.


def dung_all(request):
    data = Dung.objects.all().order_by('name')
    context = {
        'title': 'Удобрения',
        'data': data,
    }
    return render(request, 'dung/dung_list.html', context=context)

def dung_detail(request, pk):
    data = Dung.objects.get(pk=pk)
    context = {
        'title': data.name,
        'data': data,
    }
    return render(request, 'dung/dung_detail.html', context=context)