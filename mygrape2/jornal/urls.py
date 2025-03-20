from django.urls import path

from .views import index_jornal, add_place, edit_place, show_place, add_note, edit_note, show_note, delete_place
from .views import show_greenoper, add_greenoper, edit_greenoper, delete_greenoper
from .views import show_feeding, add_feeding, edit_feeding, delete_feeding, show_archiv, undo_archiv
from .views import show_processing, add_processing, edit_processing, delete_processing
from .views_mas import mas_greenoper, mas_feeding, mas_processing

urlpatterns = [
    path('', index_jornal, name='index_jornal'),
    path('<int:id>/', show_place, name='show_place'),
    path('add_place/', add_place, name='add_place'),
    path('edit/<int:id>/', edit_place, name='edit'),
    path('delete/<int:id>/', delete_place, name='delete'),
    path('archiv/', show_archiv, name='show_archiv'),
    path('archiv/undo/<int:id>/', undo_archiv, name='undo_archiv'),
    path('notes/add/<int:id>/', add_note, name='add_note'),
    path('notes/edit/<int:id>/', edit_note, name='edit_note'),
    path('notes/show/<int:id>/', show_note, name='show_note'),
    path('green/<int:id>/', show_greenoper, name='show_greenoper'),
    path('green/add/<int:id>/', add_greenoper, name='add_greenoper'),
    path('green/edit/<int:id>/', edit_greenoper, name='edit_greenoper'),
    path('green/delete/<int:id>/', delete_greenoper, name='delete_greenoper'),
    path('feeding/<int:id>/', show_feeding, name='show_feeding'),
    path('feeding/add/<int:id>/', add_feeding, name='add_feeding'),
    path('feeding/edit/<int:id>/', edit_feeding, name='edit_feeding'),
    path('feeding/delete/<int:id>/', delete_feeding, name='delete_feeding'),
    path('processing/<int:id>/', show_processing, name='show_processing'),
    path('processing/add/<int:id>/', add_processing, name='add_processing'),
    path('processing/edit/<int:id>/', edit_processing, name='edit_processing'),
    path('processing/delete/<int:id>/', delete_processing, name='delete_processing'),
    path('mas/greenoper/', mas_greenoper, name='mas_greenoper'),
    path('mas/feeding/', mas_feeding, name='mas_feeding'),
    path('mas/proces/', mas_processing, name='mas_proces'),
]