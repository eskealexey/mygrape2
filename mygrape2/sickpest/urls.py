from django.urls import path

from .views import sickpest_all, sickpest_detail

urlpatterns = [
    path('', sickpest_all, name='sickpest_all'),
    path('<int:pk>/', sickpest_detail, name='sickpest_detail')
]