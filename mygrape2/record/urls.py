from django.urls import path

from .views import jornal_dung_list, jornal_dung_add, jornal_dung_edit, jornal_dung_delete, jornal_preparat_list
from .views import jornal_peparat_add, jornal_preparat_delete, jornal_peparat_edit

urlpatterns = [
    path('dung/<str:name>/', jornal_dung_list, name='jornal_dung_list'),
    path('dung/add/<str:name>/', jornal_dung_add, name='jornal_dung_add'),
    path('dung/edit/<str:name>/<int:id>/', jornal_dung_edit, name='jornal_dung_edit'),
    path('dung/delete/<str:name>/<int:id>/', jornal_dung_delete, name='jornal_dung_delete'),
    # path('dung/active/<int:id>/', accounting_dung, name='accounting_dung'),
    path('preparat/<str:name>/', jornal_preparat_list, name='jornal_preparat_list'),
    path('preparat/add/<str:name>/', jornal_peparat_add, name='jornal_preparat_add'),
    path('preparat/edit/<str:name>/<int:id>/', jornal_peparat_edit, name='jornal_preparat_edit'),
    path('preparat/delete/<str:name>/<int:id>/', jornal_preparat_delete, name='jornal_preparat_delete'),
    ]