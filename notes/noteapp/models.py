from django.db import models


# Create your models here.


class ExpensesType(models.Model):
    type_ex = models.CharField(max_length=25, null=False)

    def __str__(self):
        return f"{self.type_ex}"


class Expenses(models.Model):
    money = models.FloatField(max_length=15, null=False)
    created = models.DateTimeField(auto_now_add=True)
    types = models.ManyToManyField(ExpensesType)
    comment = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"{self.money}   :   {self.created}   :   {self.types}   :   {self.comment}"


class IncomeType(models.Model):
    type_in = models.CharField(max_length=25, null=False)

    def __str__(self):
        return f"{self.type_in}"


class Income(models.Model):
    money = models.FloatField(max_length=15, null=False)
    created = models.DateTimeField(auto_now_add=True)
    types = models.ManyToManyField(IncomeType)
    comment = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"{self.money}    :   {self.created}    :   {self.types}   :    {self.comment}"