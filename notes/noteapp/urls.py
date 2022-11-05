from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_income_type/', views.income_type, name='add_income_type'),
    path('add_expenses_type/', views.expenses_type, name='add_expenses_type'),
    path('expenses/', views.expenses, name='expenses'),
    path('income/', views.income, name='income'),
    path('result_income/', views.result_income, name='result_income'),
    path('res_expenses/', views.res_expenses, name='res_expenses'),
]
