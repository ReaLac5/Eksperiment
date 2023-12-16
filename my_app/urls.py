from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add_person),
    path('show/', views.get_all_person),
    path('random-names/', views.get_random_names, name='random_names'),
    path('people_by_company/', views.get_people_by_company, name='people_by_company'),
    path('select-company/', views.select_company, name='select_company'),
    path('select-company-2/', views.select_company_2, name='select_company_2'),
    path('update-companies/', views.update_companies, name='update_companies'),
    path('update-companies-2/', views.update_companies_2, name='update_companies_2'),
    path('list_people_in_company/', views.list_people_in_company, name='list_people_in_company'),
    path('list_people_in_company_2/', views.list_people_in_company_2, name='list_people_in_company_2'),
    path('people_by_company_name/', views.get_people_by_company_name, name='people_by_company_name'),
    path('people_by_company_name_2/', views.get_people_by_company_name_2, name='people_by_company_name_2'),
    path('get_companies_by_first_name/', views.get_companies_by_name, name='get_companies_by_name'),
    path('get_companies_by_first_name_2/', views.get_companies_by_name_2, name='get_companies_by_name_2'),
    path('add_company_to_person/', views.add_company_to_person, name='add_company_to_person'),
    path('add_company_to_person_2/', views.add_company_to_person_2, name='add_company_to_person_2'),
]