from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import SortGrape, InfoGrape
from django.core.paginator import EmptyPage, PageNotAnInteger


def sort_all(request):
    """
    Список сортов
    """
    sorts = SortGrape.objects.all().order_by('name')
    paginator = Paginator(sorts, 15)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является целым числом, вернуть первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если страница выходит за пределы диапазона, вернуть последнюю страницу
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'title': 'Список сортов',
        'page_obj': page_obj,
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
        if not request.GET.get('find'):
            return redirect('sort_all')
        str_ = request.GET.get('find', '').strip()  # Получаем значение и убираем пробелы
        if str_:
            # Ищем по названию
            data = SortGrape.objects.filter(name__icontains=str_).all()
            if not data:
                # Если ничего не найдено, ищем по алиасу
                data = SortGrape.objects.filter(alias__icontains=str_).all()
            context['data'] = data  # Добавляем данные в контекст
        else:
            context['error'] = 'Введите текст для поиска.'  # Сообщение об ошибке, если строка пустая

    return render(request, 'spravgrape/found.html', context=context)
