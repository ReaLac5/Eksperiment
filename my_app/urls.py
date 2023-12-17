from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('show_person/', views.get_all_person),
    path('show_person_2/', views.get_all_person_2),
    path('show_person_3/', views.get_all_person_3),
    path('show_person_4/', views.get_all_person_4),
    path('show_company/', views.get_all_company),
    path('show_company_2/', views.get_all_company_2),
    path('get_companies_by_first_name/', views.get_companies_by_name, name='get_companies_by_name'),
    path('get_companies_by_first_name_2/', views.get_companies_by_name_2, name='get_companies_by_name_2'),
    path('people_by_company_name/', views.get_people_by_company_name, name='people_by_company_name'),
    path('people_by_company_name_2/', views.get_people_by_company_name_2, name='people_by_company_name_2'),
    path('add_company_to_person/', views.add_company_to_person, name='add_company_to_person'),
    path('add_company_to_person_2/', views.add_company_to_person_2, name='add_company_to_person_2'),
    path('update_companies/', views.update_companies, name='update_companies'),
    path('update_companies_2/', views.update_companies_2, name='update_companies_2'),
]