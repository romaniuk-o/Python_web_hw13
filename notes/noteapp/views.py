from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import ExpensesType, IncomeType, Expenses, Income
from .forms import ExpensesTypeForm, IncomeTypeForm, ExpensesForm, IncomeForm


# Create your views here.


def main(request):
    notes = []
    total_income = 0
    total_expenses = 0
    list_income = get_list_or_404(Income)
    list_expenses = get_list_or_404(Expenses)
    for i in range(len(list_income)):
        total_income += list_income[i].money
    for i in range(len(list_expenses)):
        total_expenses += list_expenses[i].money
    balans = total_income - total_expenses
    return render(request, 'noteapp/index.html', {"total_income": total_income,
                                                  "total_expenses": total_expenses, "balans":balans})


@login_required
def income_type(request):
    if request.method == 'POST':
        try:
            form = IncomeTypeForm(request.POST)
            form.save()
            return redirect(to='main')
        except ValueError as err:
            print(err)
            return render(request, 'noteapp/add_income_type.html', {'form': IncomeTypeForm(), 'error': err})
        except IntegrityError as err:
            return render(request, 'noteapp/add_income_type.html', {'form': IncomeTypeForm(), 'error': 'Tag will be unique!'})
    return render(request, 'noteapp/add_income_type.html', {'form': IncomeTypeForm()})




def expenses_type(request):
    if request.method == 'POST':
        try:
            form = ExpensesTypeForm(request.POST)
            form.save()
            return redirect(to='main')
        except ValueError as err:
            print(err)
            return render(request, 'noteapp/add_expenses_type.html', {'form': ExpensesTypeForm(), 'error': err})
    return render(request, 'noteapp/add_expenses_type.html', {'form': ExpensesTypeForm()})


def expenses(request):
    expenses_type = ExpensesType.objects.all()
    if request.method == 'POST':
        try:
            expen = request.POST.getlist('expenses_type')
            form = ExpensesForm(request.POST)
            new_expense = form.save()
            choice_ex_type = ExpensesType.objects.filter(type_ex__in=expen)  # WHERE name in []
            for exp in choice_ex_type.iterator():
                new_expense.types.add(exp)
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'noteapp/expenses.html', {"expenses_type": expenses_type, 'form': ExpensesForm(), 'error': err})
    return render(request, 'noteapp/expenses.html', {"expenses_type": expenses_type, 'form': ExpensesForm()})


def income(request):
    in_come_type = IncomeType.objects.all()
    print(in_come_type)
    if request.method == 'POST':
        try:
            inc = request.POST.getlist('in_come_type')
            form = IncomeForm(request.POST)
            new_inc = form.save()
            choice_inc_type = IncomeType.objects.filter(type_in__in=inc)
            for income_ in choice_inc_type.iterator():
                print(income_)
                new_inc.types.add(income_)
                print(new_inc)
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'noteapp/income.html', {"in_come_type": in_come_type, 'form': IncomeForm(), 'error': err})

    return render(request, 'noteapp/income.html', {"in_come_type": in_come_type, 'form': IncomeForm()})


def result_income(request):
    if request.method == 'GET':
        expenses = Expenses.objects.all()
        income = Income.objects.all()
        return render(request, 'noteapp/result_income.html', {"expenses": expenses}, {"income": income})


def res_expenses(request):
    list_type_expenses = get_list_or_404(ExpensesType)
    expenses_data = get_list_or_404(Expenses)
    expenses_filter = []
    total = 0
    for i in range(len(expenses_data)):
        expenses_data[i].type_list = ', '.join([str(name) for name in expenses_data[i].types.all()])
        total += expenses_data[i].money
    if request.method == 'POST':
        total_filter = 0
        exp_type = request.POST.get('list_type_expenses')
        print(exp_type)
        choice_ex_type = ExpensesType.objects.filter(type_ex=exp_type)
        print(f'choice_ex_type{choice_ex_type}')
        if not choice_ex_type:
            expenses_filter = expenses_data
        else:
            some_type = ExpensesType.objects.get(id=choice_ex_type[0].id)
            expenses_filter = some_type.expenses_set.all()
            for i in range(len(expenses_filter)):
                expenses_filter[i].type_list = ', '.join([str(name) for name in expenses_filter[i].types.all()])
                total_filter += expenses_filter[i].money
            total = total_filter
        start_dat = request.POST['start_date']
        end_dat = request.POST['end_date']
        if start_dat and end_dat:
            try:
                start = datetime.strptime(start_dat, '%Y-%m-%d')
                end = datetime.strptime(end_dat, '%Y-%m-%d')
                print(type(start), end)
            except ValueError as err:
                return render(request, 'noteapp/res_expenses.html', {"expenses_data": expenses_filter,
                                                                    "list_type_expenses": list_type_expenses,
                                                                    "total": total, 'error': err})
        else:
            start = datetime.strptime('1990-01-01', '%Y-%m-%d')
            end = datetime.now()
        result = []
        sum = 0
        for i in expenses_filter:
            print(expenses_filter)
            if (i.created.date()>=start.date()) and (i.created.date()<=end.date()):
                result.append(i)
                sum += i.money
            total = sum
        return render(request, 'noteapp/res_expenses.html', {"expenses_data": result,
                                                            "list_type_expenses": list_type_expenses,
                                                            "total": total, })
    return render(request, 'noteapp/res_expenses.html', {"expenses_data": expenses_data, "list_type_expenses": list_type_expenses,
                                                        "total": total})


def result_income(request):
    list_type_income = get_list_or_404(IncomeType)
    income_data = get_list_or_404(Income)
    income_filter = []
    total = 0
    for i in range(len(income_data)):
        income_data[i].type_list = ', '.join([str(name) for name in income_data[i].types.all()])
        total += income_data[i].money
    if request.method == 'POST':
        total_filter = 0
        inc_type = request.POST.get('list_type_income')
        choice_inc_type = IncomeType.objects.filter(type_in=inc_type)
        print(choice_inc_type)
        if not choice_inc_type:
            income_filter = income_data
        else:
            some_type = IncomeType.objects.get(id=choice_inc_type[0].id)
            income_filter = some_type.income_set.all()
            for i in range(len(income_filter)):
                income_filter[i].type_list = ', '.join([str(name) for name in income_filter[i].types.all()])
                total_filter += income_filter[i].money
            total = total_filter
        start_dat = request.POST['start_date']
        end_dat = request.POST['end_date']
        if start_dat and end_dat:
            try:
                start = datetime.strptime(start_dat, '%Y-%m-%d')
                end = datetime.strptime(end_dat, '%Y-%m-%d')
            except ValueError as err:
                return render(request, 'noteapp/result_income.html', {"income_data": income_data,
                                                                    "list_type_income": list_type_income,
                                                                    "total": total, 'error': err})
        else:
            start = datetime.strptime('1990-01-01', '%Y-%m-%d')
            end = datetime.now()
        result = []
        sum = 0
        for i in income_filter:
            if (i.created.date()>=start.date()) and (i.created.date()<=end.date()):
                result.append(i)
                sum += i.money
            total = sum
        return render(request, 'noteapp/result_income.html', {"income_data": result,
                                                            "list_type_income": list_type_income,
                                                            "total": total, })
    return render(request, 'noteapp/result_income.html', {"income_data": income_data, "list_type_income": list_type_income,
                                                        "total": total})

