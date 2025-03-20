import datetime

from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FeedingAddForm, FeedingEditForm
from .forms import GreenOperAddForm, GreenOperEditForm
from .forms import ProcessingAddForm, ProcessingEditForm
from .forms import LocationAddForm, NoteAddForm, LocationEditForm, NoteEditForm, LocationDeleteForm
from .models import Location, Notes, GreenOper, Feeding, Processing


def get_age(date_start, date_end=None):
    """
    Get age from date_start to date_end
    :param date_start:
    :param date_end:
    :return: tuple (years, months, days)
    """
    if date_end is None:
        date_end = datetime.date.today()
    else:
        date_end = date_end
    age = date_end - date_start
    years = age.days // 365
    tmp = int(age.days) - years * 365
    months = tmp // 30
    days = tmp - months * 30
    return years, months,days


def format_date(date):
    """
    Форматирование даты
    """
    # return date.strftime("%d %b %Y")
    return date.strftime("%d.%m.%Y")


def index_jornal(request):
    """
    Вывод списка посадочных мест
    """
    data = Location.objects.all().filter(userid=request.user.pk, status=0)
    result= []
    num = 1
    for item in data:
        res = '<tr>'
        res += f'<td>{num} </td>'
        res += f'<td><a href="/jornal/{item.id}/"><span style="color:blue; font-size:24px; font-weight:bold; font-style:italic;">{item.name}</span></a>'
        res += f'<a href="edit/{item.id}/"><img src="/static/img/edit.png" width="20px" height="auto" title="Редактировать"></a><br>'
        sort = item.sort_id.all()
        res += f'<span style="color:red; font-size:12px;">Сорта: </span>'
        if sort:
            for i in sort:
                res += f'<a href="/sorts/{i.id}/"><span style="color:green; font-size:12px;">{i.name}; </span></a>'
        else:
            res += f'<span style="color:green; font-size:12px;">{item.sort} </span>'
        res += f'</td>'

        age = get_age(item.date_posadki)
        res += f'<td>{item.date_posadki.strftime("%d %b  %Y")} г.<br>'
        res += f'<span style="color:grey; font-size:10px;">Возраст: {age[0]} г. {age[1]} мес. {age[2]} дн.</span></td>'
        res += f'<td><img src="/files/{item.mesto_graf}" width="100px" height="auto" alt=" "></td>'
        res += f'<td>{item.mesto}</td>'
        res += f'<td><i><a href="/jornal/green/{item.id}">Зеленые операции</a><br>'
        res += f'<a href="/jornal/feeding/{item.id}">Подкормки</a><br>'
        res += f'<a href="/jornal/processing/{item.id}">Обработки</a></i></td>'
        res += f'</tr>'
        result.append(res)
        num += 1
    context = {
        'title': 'Журнал работы',
        'data': data,
        'result': result,
    }
    return render(request, 'jornal/index_jornal.html', context=context)


def add_place(request):
    """
    Добавление посадочного места
    """
    if request.method == 'POST':
        form = LocationAddForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            sorts= form.cleaned_data['sort_id']
            date_posadki = form.cleaned_data['date_posadki']
            mesto = form.cleaned_data['mesto']
            nameuser = form.cleaned_data['nameuser']
            mesto_graf = form.cleaned_data['mesto_graf']
            print(nameuser)
            form.save()
            Location.objects.filter(name=name).update(userid=request.user.pk)


            return redirect('index_jornal')
    else:
        form = LocationAddForm()

    context = {
        'title': 'Добавление посадочного места',
        'form': form,
    }
    return render(request, 'jornal/add_place.html', context=context)


def edit_place(request, id):
    """
    Редактирование посадочного места
    """
    place = get_object_or_404(Location, pk=id)
    if request.method == 'POST':
        form = LocationEditForm(request.POST or None, request.FILES or None, instance=place)
        if form.is_valid():
            name = form.cleaned_data['name']
            sorts= form.cleaned_data['sort_id']
            date_posadki = form.cleaned_data['date_posadki']
            mesto = form.cleaned_data['mesto']
            mesto_graf = form.cleaned_data['mesto_graf']
            form.save()
            context = {
                'form': form,
                'title': 'Посадочное место',
                'location': place,
            }
            return redirect('show_place', id)
    else:
        form = LocationEditForm(instance=place)
        context = {
            'location': place,
            'form': form,
            'title': 'Редактирование посадочного места',
        }
        return render(request, 'jornal/edit_place.html', context=context)


def show_place(request, id):
    """
    Просмотр посадочного места
    """
    place = Location.objects.get(id=id)
    sort_sprav = place.sort_id.all()
    sort_ = place.sort
    age = get_age(place.date_posadki)
    notes = Notes.objects.filter(locationid=id).order_by('-date_add')
    paginator = Paginator(notes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    greens = GreenOper.objects.all().filter(locationid=place.pk).order_by('-pk')[:10]
    if greens:
        last_oper = (greens[0].date_add, get_age(greens[0].date_add))
        text_oper = f'<span style="font-size: 13px;">{format_date(last_oper[0])} ({last_oper[1][0]} г. {last_oper[1][1]} мес. {last_oper[1][2]} д. назад)</span>',
    else:
        text_oper = f'<span style="font-size: 13px;">еще не проводились</span>',

    feeds = Feeding.objects.all().filter(locationid=place.pk).order_by('-pk')[:10]
    if feeds:
        last_feed = (feeds[0].date_add, get_age(feeds[0].date_add))
        text_feed = f'<span style="font-size: 13px;">{format_date(last_feed[0])} ({last_feed[1][0]} г. {last_feed[1][1]} мес. {last_feed[1][2]} д. назад)</span>',
    else:
        text_feed = f'<span style="font-size: 13px;">еще не проводились</span>',

    proces = Processing.objects.all().filter(locationid=place.pk).order_by('-pk')[:10]
    if proces:
        last_proc = (proces[0].date_add, get_age(proces[0].date_add))
        text_proc = f'<span style="font-size: 13px;">{format_date(last_proc[0])} ({last_proc[1][0]} г. {last_proc[1][1]} мес. {last_proc[1][2]} д. назад)</span>',
    else:
        text_proc = f'<span style="font-size: 13px;">еще не проводились</span>',

    context = {
        'title': 'Просмотр посадочного места',
        'place': place,
        'sort': sort_sprav,
        'sort_': sort_,
        'age': f'{age[0]} г. {age[1]} мес. {age[2]} дн.',
        'notes': notes,
        'page_obj': page_obj,
        'greens': greens,
        'last_oper': text_oper[0],
        'last_feed': text_feed[0],
        'last_proc': text_proc[0],
        'feeds': feeds,
        'proces': proces,
    }
    return render(request, 'jornal/show_place.html', context=context)


def delete_place(request, id):
    """
    Удаление посадочного места
    """
    place = Location.objects.get(id=id)
    if request.method == 'POST':
        form = LocationDeleteForm(request.POST)
        if form.is_valid():
            date_delete = form.cleaned_data['date_delete']
            prichina = form.cleaned_data['prichina']
            place.date_delete = date_delete
            place.prichina = prichina
            place.status = 1
            place.save()
            return redirect('index_jornal')
    else:
        form = LocationDeleteForm()
    context = {
        'form': form,
        'title': 'Удаление посадочного места',
        'place': place,
    }
    return render(request, 'jornal/delete_place.html', context=context)


def show_archiv(request):
    """
    Просмотр архива удаленных посадочных мест
    """
    places = Location.objects.all().filter(status=1, userid=request.user.pk).order_by('-date_delete')
    context = {
        'title': 'Архив',
        'places': places,
    }
    return render(request, 'jornal/show_archiv.html', context=context)


def undo_archiv(request, id):
    """
    Восстановление удаленного посадочного места
    """
    place = Location.objects.get(id=id)
    if request.method == 'GET':
        place.status = 0
        place.save()
        return redirect('index_jornal')
    else:
        return redirect('show_archiv')


# def add_note(request, id):
#     """
#     Добавление заметки
#     """
#     is_admin = request.user.is_staff  # Пример: проверка, является ли пользователь админом
#     place = Location.objects.filter(pk=id,)
#     if request.method == 'POST':
#         form = NoteAddForm(request.POST)
#         if form.is_valid():
#             title_note = form.cleaned_data['title_note']
#             date_add = form.cleaned_data['date_add']
#             description = form.cleaned_data['description']
#             form.save()
#             lpk = Notes.objects.latest('pk').pk
#             Notes.objects.filter(pk=lpk).update(locationid=id)
#             return redirect('show_place', id=id)
#     else:
#         form = NoteAddForm(is_admin=is_admin)
#     context = {
#         "title": "Новая запись",
#         "form": form,
#         "place": place[0].name,
#     }
#     return render(request, 'jornal/add_note.html', context=context)
def add_note(request, id):
    """
    Добавление заметки
    """
    is_admin = request.user.is_staff  # Пример: проверка, является ли пользователь админом
    place = Location.objects.filter(pk=id)
    if not place.exists():
        # Обработка ошибки, если место не найдено
        return HttpResponseNotFound("Место не найдено")

    if request.method == 'POST':
        form = NoteAddForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.locationid = place[0]  # Присваиваем объект Location, а не его id
            note.save()
            return redirect('show_place', id=id)
    else:
        form = NoteAddForm(is_admin=is_admin)
    context = {
        "title": "Новая запись",
        "form": form,
        "place": place[0].name,
    }
    return render(request, 'jornal/add_note.html', context=context)




def edit_note(request, id):
    """
    Редактирование заметки
    """
    note = get_object_or_404(Notes, pk=id)
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            title_note = form.cleaned_data['title_note']
            date_add = form.cleaned_data['date_add']
            description = form.cleaned_data['description']
            form.save()
            return redirect('show_note', id)
    else:
        form = NoteEditForm(instance=note)
        context ={
            "title": "Редактирование заметки",
            "form": form,
            "note": note,
        }
        return render(request, 'jornal/edit_note.html', context=context)


def show_note(request, id):
    """
    Просмотр заметки
    """
    note = Notes.objects.get(id=id)

    context = {
        "title": "Просмотр заметки",
        "note": note,
    }
    return render(request, 'jornal/show_note.html', context=context)


def show_greenoper(request, id):
    """
    Просмотр зеленых операций
    """
    SELECT_CHOUIS = ['5', '10', '15', '20', '25', ]
    green_oper = GreenOper.objects.all().filter(locationid=id).order_by('-pk')
    place = Location.objects.get(id=id)

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
    paginator = Paginator(green_oper, pag)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'title': 'Зеленые операции',
        'page_obj': page_obj,
        'place': place,
        'select_chouis': SELECT_CHOUIS,
        'pag': pag,
    }
    return render(request, 'jornal/greenoper.html', context=context)


def add_greenoper(request, id):
    """
    Добавление зеленых операций
    """
    if request.method == 'POST':
        form = GreenOperAddForm(request.POST)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            description = form.cleaned_data['description']
            form.save()
            lpk = GreenOper.objects.latest('pk').pk
            GreenOper.objects.filter(pk=lpk).update(locationid=id)
            return redirect('show_greenoper', id=id)
    else:
        form = GreenOperAddForm()
        location= Location.objects.get(id=id)
    context = {
        "title": "Новая запись",
        "form": form,
        'location': location,
    }
    return render(request, 'jornal/add_greenoper.html', context=context)


def edit_greenoper(request, id):
    """
    Редактирование зеленых операций
    """
    green_oper = get_object_or_404(GreenOper, pk=id)
    if request.method == 'POST':
        form = GreenOperEditForm(request.POST, instance=green_oper)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            description = form.cleaned_data['description']
            form.save()
            return redirect('show_greenoper', green_oper.locationid.id)
    else:
        form = GreenOperEditForm(instance=green_oper)
        location= Location.objects.get(id=green_oper.locationid.id)
        context ={
            "title": "Редактирование ",
            "form": form,
            "location": location,
        }
        return render(request, 'jornal/edit_greenoper.html', context=context)


def delete_greenoper(request, id):
    """
    Удаление зеленых операций
    """
    green_oper = get_object_or_404(GreenOper, pk=id)
    green_oper.delete()
    return redirect('show_greenoper', green_oper.locationid.id)


def show_feeding(request, id):
    """
    Просмотр журнала "Подкормки"
    """
    SELECT_CHOUIS = ['5', '10', '15', '20', '25', ]

    feeds = Feeding.objects.all().filter(locationid=id).order_by('-pk')
    place = Location.objects.get(id=id)

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
    paginator = Paginator(feeds, pag)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Подкормки',
        'page_obj': page_obj,
        'place': place,
        'select_chouis': SELECT_CHOUIS,
        # 'dung': dung,
        'pag': pag,
    }
    return render(request, 'jornal/feeding.html', context=context)


def add_feeding(request, id):
    """
        Добавление подкормок
        """
    if request.method == 'POST':
        form = FeedingAddForm(request.POST)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            dung_id = form.cleaned_data['dung_id']
            description = form.cleaned_data['description']
            form.save()
            lpk = Feeding.objects.latest('pk').pk
            Feeding.objects.filter(pk=lpk).update(locationid=id)
            return redirect('show_feeding', id=id)
    else:
        form = FeedingAddForm()
        location = Location.objects.get(id=id)
        context = {
            "title": "Новая запись",
            "form": form,
            'location': location,
        }
        return render(request, 'jornal/add_feeding.html', context=context)


def edit_feeding(request, id):
    """
        Редактирование подкормок
    """
    feeding = get_object_or_404(Feeding, pk=id)
    if request.method == 'POST':
        form = FeedingEditForm(request.POST, instance=feeding)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            dung_id = form.cleaned_data['dung_id']
            description = form.cleaned_data['description']
            form.save()

            return redirect('show_feeding', feeding.locationid.id)
    else:
        form = FeedingEditForm(instance=feeding)
        location = Location.objects.get(id=feeding.locationid.id)
    context = {
        "title": "Новая запись",
        "form": form,
        'location': location,
    }
    return render(request, 'jornal/edit_feeding.html', context=context)


def delete_feeding(request, id):
    """
    Удаление зеленых операций
    """
    feeds = get_object_or_404(Feeding, pk=id)
    feeds.delete()
    return redirect('show_feeding', feeds.locationid.id)


def show_processing(request, id):
    """
    Просмотр журнала "Обработки"
    """
    SELECT_CHOUIS = ['5', '10', '15', '20', '25', ]

    proces = Processing.objects.all().filter(locationid=id).order_by('-pk')
    place = Location.objects.get(id=id)

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
    paginator = Paginator(proces, pag)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Oбработки',
        'page_obj': page_obj,
        'place': place,
        'select_chouis': SELECT_CHOUIS,
        'pag': pag,
    }
    return render(request, 'jornal/processing.html', context=context)


def add_processing(request, id):
    """
    Добавление обработки
    """
    if request.method == 'POST':
        form = ProcessingAddForm(request.POST)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            preparat_id = form.cleaned_data['preparat_id']
            description = form.cleaned_data['description']
            form.save()
            lpk = Processing.objects.latest('pk').pk
            Processing.objects.filter(pk=lpk).update(locationid=id)
            return redirect('show_processing', id=id)
    else:
        form = ProcessingAddForm()
        location = Location.objects.get(id=id)
        context = {
            "title": "Новая запись",
            "form": form,
            'location': location,
        }
        return render(request, 'jornal/add_processing.html', context=context)


def edit_processing(request, id):
    """
    Редактирование обработки
    """
    proces = get_object_or_404(Processing, pk=id)
    if request.method == 'POST':
        form = ProcessingEditForm(request.POST, instance=proces)
        if form.is_valid():
            date_add = form.cleaned_data['date_add']
            preparat_id = form.cleaned_data['preparat_id']
            description = form.cleaned_data['description']
            form.save()
            return redirect('show_processing', id=proces.locationid.id)
    else:
        form = ProcessingEditForm(instance=proces)
        location = Location.objects.get(pk=proces.locationid.id)
        context = {
            "title": "Новая запись",
            "form": form,
            'location': location,
        }
        return render(request, 'jornal/edit_processing.html', context=context)


def delete_processing(request, id):
    """
    Удаление обработки
    """
    proces = get_object_or_404(Processing, pk=id)
    proces.delete()
    return redirect('show_processing', proces.locationid.id)