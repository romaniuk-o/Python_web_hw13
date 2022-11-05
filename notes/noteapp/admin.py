from django.contrib import admin
from .models import  Income, IncomeType, Expenses, ExpensesType

# Register your models here.
admin.site.register(Income)
admin.site.register(IncomeType)
admin.site.register(Expenses)
admin.site.register(ExpensesType)