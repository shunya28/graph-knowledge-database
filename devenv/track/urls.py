from django.urls import path
from . import views

app_name = 'track'

urlpatterns = [
    path('', views.index, name='index'),
    path('addnode/', views.addnode, name='addnode'),
    path('delnode/', views.delnode, name='delnode')
]
