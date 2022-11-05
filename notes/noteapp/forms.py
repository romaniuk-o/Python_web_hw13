from django.forms import ModelForm
from .models import ExpensesType, IncomeType, Expenses, Income





class IncomeTypeForm(ModelForm):
    class Meta:
        model = IncomeType
        fields = ['type_in']


class ExpensesTypeForm(ModelForm):
    class Meta:
        model = ExpensesType
        fields = ['type_ex']


class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ['money', 'comment']
        exclude = ['types']


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['money', 'comment']
        exclude = ['types']