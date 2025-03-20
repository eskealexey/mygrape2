from django.urls import path

from .views import *

urlpatterns = [
    path('', dung_all, name='dung_all'),
    path('<int:pk>/', dung_detail, name='dung_detail')
]