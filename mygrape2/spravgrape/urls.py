from django.urls import path
from .views import sort_all, sort_detail, info_detail, found

urlpatterns = [
    path('', sort_all, name='sort_all'),
    path('<int:sort_id>/', sort_detail, name='sort_id'),
    path('dop/<int:info_id>/', info_detail, name='info_detail'),
    path('found/', found, name='found'),
]