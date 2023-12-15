from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add_person),
    path('show/', views.get_all_person),
    path('random-names/', views.get_random_names, name='random_names'),
    path('people_by_company/', views.get_people_by_company, name='people_by_company'),
]