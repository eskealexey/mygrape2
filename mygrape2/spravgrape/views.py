from django.core.paginator import Paginator
from django.shortcuts import render

from .models import SortGrape, InfoGrape


def sort_all(request):
    SELECT_CHOUIS = ['5', '10', '15', '20', '25', ]
    sorts = SortGrape.objects.all().order_by('name')
    if request.GET.get('pag') is None:
        pag = 5
    else:
        pag = request.GET.get('pag')
    if request.method == 'POST':
        select = request.POST.get('select')
        if select is None:
            pag = 5
        else:
            pag = select
    paginator = Paginator(sorts, pag)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Список сортов',
        'page_obj': page_obj,
        'select_chouis': SELECT_CHOUIS,
        'pag': pag,
    }
    return render(request, 'spravgrape/grape_list.html', context=context)

def sort_detail(request, sort_id):
    sort = SortGrape.objects.get(id=sort_id)
    info = InfoGrape.objects.filter(id_sort=sort_id)
    context = {
        'info': info,
        'sort': sort,
        'title': sort.name,
    }
    return render(request, 'spravgrape/grape_detail.html', context=context)

def info_detail(request, info_id):
    info = InfoGrape.objects.get(id=info_id)
    context = {
        'title': info.title,
        'info': info,
    }
    return render(request, 'spravgrape/info_detail.html', context=context)

def found(request):
    context = {
        'title': 'Поиск по названию',
    }
    if request.method == "GET":
        str_ = request.GET.get('find')
        if str_ == '':
            return render(request, 'spravgrape/found.html',context=context)
        else:
            # data = SortGrape.objects.filter(name__contains=str_).all()
            data = SortGrape.objects.filter(name__icontains =str_).all()
            if not data:
                data = SortGrape.objects.filter(alias__icontains=str_).all()
            context = {
                'data': data,
            }
    return render(request, 'spravgrape/found.html',context=context)
