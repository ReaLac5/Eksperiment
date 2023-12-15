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
]