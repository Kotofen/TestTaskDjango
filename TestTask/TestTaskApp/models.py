from django.db import models
from datetime import date


# Статус Движения Денежных Средств (ДДС)
class TransactionStatus(models.Model):
    StatusName = models.CharField(max_length=100)  # Название

    def __str__(self):
        return self.StatusName


# Тип ДДС
class TransactionType(models.Model):
    TypeName = models.CharField(max_length=100)  # Название

    def __str__(self):
        return self.TypeName


# Категория ДДС
class TransactionCategory(models.Model):
    CatName = models.CharField(max_length=100)  # Название
    Type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)  # Тип к которому относится

    def __str__(self):
        return self.CatName


# Подкатегория ДДС
class Subcategory(models.Model):
    SubCatName = models.CharField(max_length=100)  # Название
    Category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)  # Категория к которой относится

    def __str__(self):
        return self.SubCatName


# ДДС
class Transaction(models.Model):
    TransactionDate = models.DateField(default=date.today)  # Дата ДДС
    Status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)  # Статус ДДС
    Type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)  # Тип ДДС
    Category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)  # Категория ДДС
    Subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)  # Подкатегория ДДС
    TransactionSumm = models.IntegerField()  # Сумма ДДС
    Commentary = models.CharField(max_length=1000, blank=True)  # Комментарий к ДДС


# Create your models here.
