from django.urls import path

from .views import preparat_all, preparat_detail

urlpatterns = [
    path('', preparat_all, name='preparat_all'),
    path('<int:pk>/', preparat_detail, name='preparat_detail')
]