from django.shortcuts import render

from .models import SickPest, SickPestImage

def sickpest_all(request):

    list_sickpest = SickPest.objects.all().order_by('name')
    context = {
        'title': 'Болезни и вредители',
        'data': list_sickpest,
    }
    return render(request, 'sickpest/pest_list.html', context=context)


def sickpest_detail(request, pk):

    sickpest = SickPest.objects.get(pk=pk)
    sickpest_image = SickPestImage.objects.filter(sickpest=sickpest)
    context = {
        'title': 'Болезни и вредители',
        'sickpest': sickpest,
        'sickpest_image': sickpest_image,
    }
    return render(request, 'sickpest/pest_detail.html', context=context)