from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('show_person/', views.get_all_person),
    path('show_person_2/', views.get_all_person_2),
    path('show_company/', views.get_all_company),
    path('random-names/', views.get_random_names, name='random_names'),
    path('list_people_in_company/', views.list_people_in_company, name='list_people_in_company'),
    path('list_people_in_company_2/', views.list_people_in_company_2, name='list_people_in_company_2'),
    path('people_by_company_name/', views.get_people_by_company_name, name='people_by_company_name'),
    path('people_by_company_name_2/', views.get_people_by_company_name_2, name='people_by_company_name_2'),
    path('get_companies_by_first_name/', views.get_companies_by_name, name='get_companies_by_name'),
    path('get_companies_by_first_name_2/', views.get_companies_by_name_2, name='get_companies_by_name_2'),
    path('add_company_to_person/', views.add_company_to_person, name='add_company_to_person'),
    path('add_company_to_person_2/', views.add_company_to_person_2, name='add_company_to_person_2'),
]